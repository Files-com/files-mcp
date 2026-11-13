"""Formats, checks, tests, packages and locks the Files.com MCP server.

    python scripts/tasks.py format    # rewrite the sources with pinned Black
    python scripts/tasks.py check     # formatting, lint, types, then test
    python scripts/tasks.py test [--artifact WHEEL_OR_SDIST]
    python scripts/tasks.py build     # build and inspect the sdist and wheel
    python scripts/tasks.py package   # build, inspect and test the artifacts
    python scripts/tasks.py lock      # resolve requirements/*.txt again
    python scripts/tasks.py twine ... # run the pinned twine

Only format and lock change files. Every environment is built with the
interpreter that runs this script, so "python3.11 scripts/tasks.py test"
tests the oldest supported Python. Environments are installed from the
hash-pinned files in requirements/ into .tools/ (or $FILES_MCP_TOOLS_DIR)
and reused until those files change. Type checking needs Node.js and npm on
PATH.

The server depends on the Files.com SDK generated with it, which is not
published: check, test and package install the files-com wheel that
FILES_COM_SDK names, or else build one from the Python SDK generated next to
this package (../python). Build does not need the SDK, so a release can
build and check its artifacts without it.
"""

import argparse
import datetime
import email.parser
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import venv
import zipfile
from pathlib import Path

if sys.version_info < (3, 11):
    sys.exit(f"tasks.py needs Python 3.11 or newer, not {sys.version}")

import tomllib  # noqa: E402 (needs the version check above)

PACKAGE = Path(__file__).resolve().parent.parent
REQUIREMENTS = PACKAGE / "requirements"
TOOLS = Path(
    os.environ.get("FILES_MCP_TOOLS_DIR", PACKAGE / ".tools")
).absolute()
SOURCES = ("files_com_mcp", "tests", "scripts")
# The files the sdist holds besides files_com_mcp/.
BUILD_INPUTS = ("pyproject.toml", "MANIFEST.in", "README.md", "LICENSE")
PYTHON_TAG = f"py{sys.version_info.major}{sys.version_info.minor}"
RUN_TESTS = PACKAGE / "scripts" / "run_tests.py"
PIP_INSTALL = ("-m", "pip", "--disable-pip-version-check", "--no-input")
LOCKED = ("install", "--quiet", "--require-hashes", "--only-binary", ":all:")
# Releases published more recently than this are not locked.
MINIMUM_RELEASE_AGE = datetime.timedelta(days=5)


class TaskFailed(Exception):
    pass


def run(*command, **options):
    command = [str(part) for part in command]
    print("+", " ".join(command), flush=True)
    status = subprocess.run(command, **options).returncode
    if status != 0:
        raise TaskFailed(
            f"{Path(command[0]).name} exited with status {status}"
        )


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def python_in(environment):
    if os.name == "nt":
        return environment / "Scripts" / "python.exe"
    return environment / "bin" / "python"


def fresh_environment(path, *locks, requirements=()):
    """A new virtual environment holding exactly the locked packages and
    the hash-pinned requirements files given."""
    venv.EnvBuilder(clear=True, with_pip=True).create(path)
    python = python_in(path)
    run(python, *PIP_INSTALL, *LOCKED, "-r", REQUIREMENTS / "pip.txt")
    if sys.version_info < (3, 12):
        # Python 3.11's venv also installs setuptools, which nothing here uses.
        run(
            python, *PIP_INSTALL, "uninstall", "--yes", "--quiet", "setuptools"
        )
    files = [REQUIREMENTS / lock for lock in locks] + list(requirements)
    if files:
        arguments = [arg for file in files for arg in ("-r", file)]
        run(python, *PIP_INSTALL, *LOCKED, *arguments)
    run(python, *PIP_INSTALL, "check")
    run(python, *PIP_INSTALL, "list", "--format=freeze")
    return python


def environment(name, *locks, requirements=()):
    """The environment called name, rebuilt when its locks, requirements or
    this interpreter change."""
    path = TOOLS / f"{name}-{PYTHON_TAG}"
    stamp = {
        "python": sys.version,
        "executable": sys.executable,
        "locks": {
            str(lock): sha256(REQUIREMENTS / lock)
            for lock in ("pip.txt", *locks)
        },
        "requirements": [Path(file).read_text() for file in requirements],
    }
    stamp_file = path / "files-mcp-locks.json"
    if stamp_file.exists() and json.loads(stamp_file.read_text()) == stamp:
        return python_in(path)
    python = fresh_environment(path, *locks, requirements=requirements)
    stamp_file.write_text(json.dumps(stamp, indent=2))
    return python


def pinned_requirement(name, artifact, directory):
    """A requirements file installing artifact, checked against its hash."""
    requirement = Path(directory) / f"{name}.txt"
    requirement.write_text(
        f"{name} @ {artifact.as_uri()} --hash=sha256:{sha256(artifact)}\n"
    )
    return requirement


def pyright():
    """The command that runs the Pyright version tools/pyright locks."""
    node, npm = shutil.which("node"), shutil.which("npm")
    if not node or not npm:
        raise TaskFailed("Type checking needs Node.js and npm on PATH.")
    node_version = subprocess.run(
        [node, "--version"], capture_output=True, text=True, check=True
    ).stdout.strip()
    print(f"Node.js {node_version}")

    lock_dir = PACKAGE / "tools" / "pyright"
    path = TOOLS / "pyright"
    stamp = json.dumps(
        {"lock": sha256(lock_dir / "package-lock.json"), "node": node_version}
    )
    stamp_file = path / "files-mcp-lock.json"
    if not stamp_file.exists() or stamp_file.read_text() != stamp:
        shutil.rmtree(path, ignore_errors=True)
        path.mkdir(parents=True)
        for name in ("package.json", "package-lock.json"):
            shutil.copy(lock_dir / name, path)
        # fsevents is optional and only watches files; skip it and its
        # install script. Refuse packages published in the last 5 days.
        run(
            npm,
            "ci",
            "--omit=optional",
            "--ignore-scripts",
            "--no-audit",
            "--no-fund",
            "--min-release-age=5",
            cwd=path,
            env={**os.environ, "npm_config_cache": str(TOOLS / "npm-cache")},
        )
        stamp_file.write_text(stamp)
    return [node, path / "node_modules" / "pyright" / "index.js"]


def project():
    return tomllib.loads((PACKAGE / "pyproject.toml").read_text())["project"]


def supported_python():
    """Fail unless this interpreter meets the package's requires-python."""
    requires_python = project()["requires-python"]
    floor = re.fullmatch(r">=\s*(\d+)\.(\d+)", requires_python)
    if not floor:
        raise TaskFailed(f"Cannot read requires-python {requires_python!r}")
    if sys.version_info[:2] < tuple(map(int, floor.groups())):
        raise TaskFailed(
            f"Python {sys.version.split()[0]} is older than this package's "
            f"requires-python {requires_python}"
        )


# The Files.com SDK


def wheel_metadata(wheel):
    with zipfile.ZipFile(wheel) as archive:
        [name] = [
            name
            for name in archive.namelist()
            if re.fullmatch(r"[^/]+\.dist-info/METADATA", name)
        ]
        return email.parser.HeaderParser().parsestr(
            archive.read(name).decode()
        )


def sdk_wheel():
    """The files-com wheel to test with, checked against the version this
    package requires."""
    named = os.environ.get("FILES_COM_SDK")
    if named:
        wheel = Path(named).resolve()
        if wheel.suffix != ".whl" or not wheel.is_file():
            raise TaskFailed(f"FILES_COM_SDK must name a wheel, not {named}")
    else:
        tasks = PACKAGE.parent / "python" / "scripts" / "tasks.py"
        if not tasks.is_file():
            raise TaskFailed(
                "Set FILES_COM_SDK to the files-com wheel built from the "
                "Python SDK generated with this server, or generate the "
                "python target next to this one"
            )
        outdir = TOOLS / "sdk-dist"
        run(sys.executable, tasks, "build", "--outdir", outdir)
        wheel = only(outdir.glob("*.whl"), "SDK wheel")

    metadata = wheel_metadata(wheel)
    [requirement] = [
        dependency
        for dependency in project()["dependencies"]
        if re.match(r"files[-_]com\b", dependency)
    ]
    required = re.fullmatch(r"files[-_]com==(\S+)", requirement)
    if not required:
        raise TaskFailed(f"Tests need an exact files-com, not {requirement}")
    if (metadata["Name"], metadata["Version"]) != ("files_com", required[1]):
        raise TaskFailed(
            f"{wheel.name} is {metadata['Name']} {metadata['Version']}, "
            f"but this package requires {requirement}"
        )
    print(f"files-com SDK: {wheel} sha256 {sha256(wheel)}")
    return wheel


def test_environment(sdk):
    TOOLS.mkdir(parents=True, exist_ok=True)
    requirement = pinned_requirement("files_com", sdk, TOOLS)
    return environment("test", "runtime.txt", requirements=[requirement])


# Checks


def black(*arguments):
    # Keep Black's cache with the other tool state, not in the user's cache.
    run(
        environment("check", "check.txt"),
        "-m",
        "black",
        *arguments,
        *SOURCES,
        cwd=PACKAGE,
        env={**os.environ, "BLACK_CACHE_DIR": str(TOOLS / "black-cache")},
    )


def format_sources():
    black("--quiet")


def check():
    black("--check", "--diff")
    run(
        environment("check", "check.txt"),
        "-m",
        "flake8",
        *SOURCES,
        cwd=PACKAGE,
    )
    sdk = sdk_wheel()
    python = test_environment(sdk)
    verify_framework_requirements(python)
    run(*pyright(), "--pythonpath", python, cwd=PACKAGE)
    test(sdk=sdk)


# The requirements pyproject.toml declares differently from fastmcp-slim's
# "server" extra, each explained there: requirement name -> (upstream, ours).
FRAMEWORK_DEVIATIONS = {
    "py-key-value-aio": (
        "py-key-value-aio[filetree,keyring,memory]<0.5.0,>=0.4.4",
        "py-key-value-aio[filetree,memory]<0.5.0,>=0.4.4",
    ),
    "mcp": ("mcp<2.0,>=1.24.0", "mcp==1.30.0"),
}


def verify_framework_requirements(python):
    """Fail unless the dependencies pyproject.toml declares for FastMCP are
    the requirements of the installed fastmcp-slim's "server" extra, apart
    from FRAMEWORK_DEVIATIONS."""
    requires = json.loads(
        subprocess.run(
            [
                python,
                "-I",
                "-c",
                "import importlib.metadata as m, json; "
                "print(json.dumps(m.requires('fastmcp-slim')))",
            ],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    )
    server = {}
    for requirement in requires:
        spec, _, marker = requirement.partition(";")
        if re.fullmatch(r"""\s*extra\s*==\s*(["'])server\1\s*""", marker):
            server[requirement_key(spec)[0]] = spec.strip()
    expected = dict(server)
    for name, (upstream, ours) in FRAMEWORK_DEVIATIONS.items():
        if name not in expected or requirement_key(
            expected[name]
        ) != requirement_key(upstream):
            raise TaskFailed(
                f"fastmcp-slim now requires {expected.get(name)!r}, not "
                f"{upstream!r}; reconcile pyproject.toml and "
                "FRAMEWORK_DEVIATIONS"
            )
        expected[name] = ours
    declared = {
        requirement_key(d)[0]: d
        for d in project()["dependencies"]
        if requirement_key(d)[0] not in ("fastmcp-slim", "files-com")
    }
    if sorted(map(requirement_key, declared.values())) != sorted(
        map(requirement_key, expected.values())
    ):
        raise TaskFailed(
            "pyproject.toml's FastMCP dependencies differ from fastmcp-slim's "
            f"server extra: declared {sorted(declared.values())}, expected "
            f"{sorted(expected.values())}"
        )
    print(f"FastMCP server requirements reconciled ({len(declared)})")


def test(artifact=None, report=None, sdk=None):
    supported_python()
    sdk = sdk or sdk_wheel()
    if artifact:
        test_installed(Path(artifact).resolve(), sdk, report)
    else:
        python = test_environment(sdk)
        run(
            python,
            "-X",
            "dev",
            RUN_TESTS,
            *report_arguments(report),
            cwd=PACKAGE,
        )


def report_arguments(report):
    return ("--report", Path(report).resolve()) if report else ()


# Packaging


def copy_tree_files(source, destination, pattern):
    for path in sorted(source.rglob(pattern)):
        if "__pycache__" in path.parts or not path.is_file():
            continue
        target = destination / path.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def stage_build_inputs(staging):
    """Copy only the files the build reads, so nothing else in this
    directory can reach an artifact."""
    for name in BUILD_INPUTS:
        shutil.copy2(PACKAGE / name, staging / name)
    copy_tree_files(
        PACKAGE / "files_com_mcp", staging / "files_com_mcp", "*.py"
    )


def build_environment():
    """Isolated builds install exactly the verified setuptools."""
    return {
        **os.environ,
        "PIP_CONSTRAINT": str(REQUIREMENTS / "build-backend.txt"),
        "PIP_ONLY_BINARY": ":all:",
    }


def only(paths, description):
    paths = list(paths)
    if len(paths) != 1:
        raise TaskFailed(f"Expected one {description}, found {paths}")
    return paths[0]


def wheel_contents(wheel):
    with zipfile.ZipFile(wheel) as archive:
        return {name: archive.read(name) for name in archive.namelist()}


def sdist_contents(sdist):
    contents = {}
    with tarfile.open(sdist) as archive:
        for member in archive.getmembers():
            file = archive.extractfile(member) if member.isfile() else None
            if file is not None:
                contents[member.name] = file.read()
    return contents


def payload_files(staging):
    return {
        path.relative_to(staging).as_posix(): path.read_bytes()
        for path in sorted((staging / "files_com_mcp").rglob("*"))
        if path.is_file()
    }


def verify_names(artifact, names):
    for name in names:
        if not name.isascii():
            raise TaskFailed(
                f"{artifact.name} contains a non-ASCII path: {name!r}"
            )


def verify_contents(artifact, contents, expected, payload, prefix=""):
    verify_names(artifact, contents)
    if set(contents) != expected:
        raise TaskFailed(
            f"{artifact.name} contents differ from the build inputs: "
            f"unexpected {sorted(set(contents) - expected)}, "
            f"missing {sorted(expected - set(contents))}"
        )
    changed = [
        name for name in payload if contents[prefix + name] != payload[name]
    ]
    if changed:
        raise TaskFailed(
            f"{artifact.name} changed these build inputs: {changed}"
        )


def verify_wheel(wheel, payload, dist_info):
    contents = wheel_contents(wheel)
    expected = set(payload) | {
        f"{dist_info}/{name}"
        for name in (
            "METADATA",
            "WHEEL",
            "RECORD",
            "top_level.txt",
            "entry_points.txt",
            "licenses/LICENSE",
        )
    }
    verify_contents(wheel, contents, expected, payload)
    return contents


def verify_sdist(sdist, payload, root):
    egg_info = (
        "PKG-INFO",
        "SOURCES.txt",
        "dependency_links.txt",
        "entry_points.txt",
        "requires.txt",
        "top_level.txt",
    )
    expected = (
        {f"{root}/{name}" for name in (*BUILD_INPUTS, "PKG-INFO", "setup.cfg")}
        | {f"{root}/files_com_mcp.egg-info/{name}" for name in egg_info}
        | {f"{root}/{name}" for name in payload}
    )
    verify_contents(
        sdist, sdist_contents(sdist), expected, payload, prefix=f"{root}/"
    )


def requirement_key(requirement):
    """A requirement's normalized name, extras and specifiers, which
    setuptools may write in another order ("files-com<3,>=2.0.0" for
    "files-com>=2.0.0,<3")."""
    match = re.fullmatch(
        r"\s*([A-Za-z0-9._-]+)\s*(\[[^\]]*\])?\s*(.*?)\s*", requirement
    )
    if not match:
        raise TaskFailed(f"Cannot read the requirement {requirement!r}")
    name, extras, specifiers = match.groups()
    return (
        re.sub(r"[-_.]+", "-", name).lower(),
        sorted(
            e.strip() for e in (extras or "[]")[1:-1].split(",") if e.strip()
        ),
        sorted(s.replace(" ", "") for s in specifiers.split(",") if s.strip()),
    )


def verify_metadata(contents, dist_info):
    """The published metadata matches pyproject.toml, and the console
    script starts the server."""
    metadata = contents[f"{dist_info}/METADATA"].decode()
    headers = email.parser.HeaderParser().parsestr(metadata)
    requires_python = headers.get_all("Requires-Python", [])
    if requires_python != [project()["requires-python"]]:
        raise TaskFailed(f"Requires-Python is {requires_python}")
    requires = sorted(
        map(requirement_key, headers.get_all("Requires-Dist", []))
    )
    declared = sorted(map(requirement_key, project()["dependencies"]))
    if requires != declared:
        raise TaskFailed(f"Requires-Dist is {requires}, not {declared}")
    entry_points = contents[f"{dist_info}/entry_points.txt"].decode()
    if "files-com-mcp = files_com_mcp.__main__:main" not in entry_points:
        raise TaskFailed(f"The console script is missing: {entry_points}")


def build_and_check(tools, outdir):
    TOOLS.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=TOOLS) as scratch:
        scratch = Path(scratch)
        staging = scratch / "staging"
        staging.mkdir()
        stage_build_inputs(staging)
        payload = payload_files(staging)

        run(
            tools,
            "-m",
            "build",
            "--sdist",
            "--wheel",
            "--outdir",
            outdir,
            staging,
            env=build_environment(),
        )
        sdist = only(outdir.glob("*.tar.gz"), "sdist")
        wheel = only(outdir.glob("*.whl"), "wheel")
        root = sdist.name.removesuffix(".tar.gz")
        dist_info = root + ".dist-info"
        verify_sdist(sdist, payload, root)
        contents = verify_wheel(wheel, payload, dist_info)
        verify_metadata(contents, dist_info)

        # Rebuild the wheel from the sdist alone, as pip does for sdist users.
        with tarfile.open(sdist) as archive:
            archive.extractall(scratch / "sdist", filter="data")
        rebuilt_dir = outdir / "from-sdist"
        run(
            tools,
            "-m",
            "build",
            "--wheel",
            "--outdir",
            rebuilt_dir,
            scratch / "sdist" / root,
            env=build_environment(),
        )
        rebuilt = only(rebuilt_dir.glob("*.whl"), "wheel built from the sdist")
        rebuilt_contents = verify_wheel(rebuilt, payload, dist_info)
        if (
            rebuilt_contents[f"{dist_info}/METADATA"]
            != contents[f"{dist_info}/METADATA"]
        ):
            raise TaskFailed(
                "The wheel built from the sdist has different metadata"
            )

        run(tools, "-m", "twine", "check", "--strict", sdist, wheel, rebuilt)
    return sdist, wheel, rebuilt


def build(outdir):
    """Build the sdist and wheel from the build inputs alone, rebuild the
    wheel from the sdist, and check all three. Returns (sdist, wheel). A
    failed check removes outdir, so nothing unchecked is left to upload."""
    supported_python()
    tools = environment("package", "package.txt")
    outdir = Path(outdir).resolve()
    shutil.rmtree(outdir, ignore_errors=True)
    try:
        sdist, wheel, rebuilt = build_and_check(tools, outdir)
    except BaseException:  # Whatever stopped the checks, drop the output.
        shutil.rmtree(outdir, ignore_errors=True)
        raise

    manifest = {
        artifact.relative_to(outdir).as_posix(): sha256(artifact)
        for artifact in (sdist, wheel, rebuilt)
    }
    (outdir / "SHA256SUMS.json").write_text(
        json.dumps(manifest, indent=2) + "\n"
    )
    print(json.dumps(manifest, indent=2))
    return sdist, wheel


def artifact_payload(artifact, package):
    """The files of package in a wheel or sdist, by path in the package."""
    if artifact.suffix == ".whl":
        contents = wheel_contents(artifact)
    else:
        root = artifact.name.removesuffix(".tar.gz") + "/"
        contents = {
            name.removeprefix(root): data
            for name, data in sdist_contents(artifact).items()
        }
    return {
        name: data
        for name, data in contents.items()
        if name.startswith(f"{package}/")
    }


def installed_payload(environment, package):
    """The files of package installed in environment. The import runs in
    isolated mode (-I) from the environment's own directory, so neither
    PYTHONPATH, the user site-packages nor a source tree in the working
    directory can stand in for the installed package."""
    imported = subprocess.run(
        [
            python_in(environment),
            "-I",
            "-c",
            f"import {package}; print({package}.__path__[0])",
        ],
        cwd=environment,
        capture_output=True,
        text=True,
    )
    if imported.returncode != 0:
        raise TaskFailed(f"Cannot import {package}: {imported.stderr.strip()}")
    location = Path(imported.stdout.strip()).resolve()
    if not location.is_relative_to(environment.resolve()):
        raise TaskFailed(f"{package} was imported from {location}")
    return {
        path.relative_to(location.parent).as_posix(): path.read_bytes()
        for path in sorted(location.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    }


def verify_installed(environment, package, artifact):
    """Fail unless environment holds exactly the files of package that
    artifact has."""
    if installed_payload(environment, package) != artifact_payload(
        artifact, package
    ):
        raise TaskFailed(
            f"The installed {package} differs from {artifact.name}"
        )


def test_installed(artifact, sdk, report=None):
    """Install artifact and the SDK with the locked runtime graph into a
    new environment, confirm what was installed, and run the tests against
    it from outside the source tree."""
    TOOLS.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=TOOLS) as scratch:
        scratch = Path(scratch)
        environment = scratch / "environment"
        requirements = [
            pinned_requirement("files_com", sdk, scratch),
            pinned_requirement("files_com_mcp", artifact, scratch),
        ]
        formats = (
            ()
            if artifact.suffix == ".whl"
            else ("--no-binary", "files-com-mcp")
        )
        venv.EnvBuilder(clear=True, with_pip=True).create(environment)
        python = python_in(environment)
        run(python, *PIP_INSTALL, *LOCKED, "-r", REQUIREMENTS / "pip.txt")
        if sys.version_info < (3, 12):
            run(
                python,
                *PIP_INSTALL,
                "uninstall",
                "--yes",
                "--quiet",
                "setuptools",
            )
        run(
            python,
            *PIP_INSTALL,
            *LOCKED,
            *formats,
            "-r",
            REQUIREMENTS / "runtime.txt",
            *(arg for file in requirements for arg in ("-r", file)),
            env=build_environment(),
        )
        run(python, *PIP_INSTALL, "check")
        run(python, *PIP_INSTALL, "list", "--format=freeze")
        verify_installed(environment, "files_com_mcp", artifact)
        verify_installed(environment, "files_sdk", sdk)

        tests = scratch / "tests"
        copy_tree_files(PACKAGE / "tests", tests / "tests", "*.py")
        copy_tree_files(PACKAGE / "tests", tests / "tests", "*.json")
        run(
            python,
            "-X",
            "dev",
            RUN_TESTS,
            "--installed",
            *report_arguments(report),
            cwd=tests,
        )


def package(outdir):
    sdk = sdk_wheel()
    sdist, wheel = build(outdir)
    test_installed(wheel, sdk)
    test_installed(sdist, sdk)


def twine(arguments):
    """Run the twine that requirements/package.txt pins, for example to upload
    what build checked."""
    run(environment("package", "package.txt"), "-m", "twine", *arguments)


# Locking


def lock(names, cutoff, allow_newer):
    """Resolve requirements/*.in (or just those named) for every platform
    and supported Python (uv --universal), from releases published before
    cutoff: by default, 5 days ago. An allow_newer entry, NAME=TIME, admits
    NAME releases up to TIME when a requirement leaves no older choice; the
    lock header records it, and such a lock does not meet the release-age
    rule. runtime.txt resolves the package's own dependencies from
    pyproject.toml and those of the SDK wheel, but locks neither files-com
    nor this package."""
    uv = environment("lock", "lock.txt").parent / "uv"
    version = subprocess.run(
        [uv, "--version"], capture_output=True, text=True, check=True
    ).stdout.strip()
    cutoff = cutoff or (
        datetime.datetime.now(datetime.timezone.utc) - MINIMUM_RELEASE_AGE
    ).strftime("%Y-%m-%dT%H:%M:%SZ")
    options = ["--exclude-newer", cutoff]
    for entry in allow_newer:
        options += ["--exclude-newer-package", entry]
    sdk = sdk_wheel()
    with tempfile.TemporaryDirectory(dir=TOOLS) as scratch:
        sources = sorted(REQUIREMENTS.glob("*.in"))
        if names:
            sources = [REQUIREMENTS / f"{name}.in" for name in names]
        for source in sources:
            inputs = [source]
            if source.name == "runtime.in":
                dependencies = [
                    d
                    for d in project()["dependencies"]
                    if requirement_key(d)[0] != "files-com"
                ]
                inputs.append(Path(scratch) / "runtime-dependencies.in")
                inputs[-1].write_text(
                    "\n".join([*dependencies, f"files-com @ {sdk.as_uri()}"])
                    + "\n"
                )
            resolved = Path(scratch) / f"{source.stem}.txt"
            run(
                uv,
                "pip",
                "compile",
                "--no-config",
                "--quiet",
                "--universal",
                "--python-version",
                "3.11",
                *options,
                "--only-binary",
                ":all:",
                "--generate-hashes",
                "--no-header",
                "--no-annotate",
                *inputs,
                "-o",
                resolved,
                env={
                    **os.environ,
                    "UV_CACHE_DIR": str(TOOLS / "uv-cache"),
                    "UV_PYTHON_DOWNLOADS": "never",
                },
            )
            entries = re.split(r"\n(?=\S)", resolved.read_text().strip())
            entries = [e for e in entries if not e.startswith("files-com @")]
            header = (
                f"# Generated by scripts/tasks.py lock from {source.name}. "
                "Do not edit; see that script.\n"
                f"# Resolved with {version} for Python >=3.11 on every "
                f"platform, from releases published before {cutoff}"
                + "".join(f"; {entry} allowed" for entry in allow_newer)
                + ".\n"
            )
            if allow_newer:
                header += (
                    "# Provisional: it admits releases newer than the cutoff, "
                    "so it does not meet\n# the release-age rule. Resolve it "
                    "again without --allow-newer before release.\n"
                )
            output = source.with_suffix(".txt")
            output.write_text(header + "\n".join(entries) + "\n")
            print(f"wrote {output} ({len(entries)} packages)")


def main():
    parser = argparse.ArgumentParser(
        description="Formats, checks, tests, packages and locks the server."
    )
    tasks = parser.add_subparsers(dest="task", required=True)
    tasks.add_parser("format", help="rewrite the sources with pinned Black")
    tasks.add_parser("check", help="run every check without changing files")
    test_parser = tasks.add_parser("test", help="run the tests")
    test_parser.add_argument(
        "--artifact",
        help="test this installed wheel or sdist instead of the source",
    )
    test_parser.add_argument("--report", help="write the counts as JSON here")
    for name, description in (
        ("build", "build and check the sdist and wheel"),
        ("package", "build, check and test the sdist and wheel"),
    ):
        tasks.add_parser(name, help=description).add_argument(
            "--outdir", default=TOOLS / "dist"
        )
    lock_parser = tasks.add_parser("lock", help="resolve requirements/*.txt")
    lock_parser.add_argument(
        "names", nargs="*", help="the requirements/*.in to resolve (all)"
    )
    lock_parser.add_argument(
        "--cutoff", help="consider releases published before this UTC time"
    )
    lock_parser.add_argument(
        "--allow-newer",
        action="append",
        default=[],
        metavar="NAME=TIME",
        help="admit releases of NAME published up to TIME",
    )
    twine_parser = tasks.add_parser("twine", help="run the pinned twine")
    twine_parser.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    try:
        if args.task == "format":
            format_sources()
        elif args.task == "check":
            check()
        elif args.task == "test":
            test(args.artifact, args.report)
        elif args.task == "build":
            build(args.outdir)
        elif args.task == "package":
            package(args.outdir)
        elif args.task == "lock":
            lock(args.names, args.cutoff, args.allow_newer)
        else:
            twine(args.arguments)
    except TaskFailed as failure:
        sys.exit(f"{args.task} failed: {failure}")


if __name__ == "__main__":
    main()
