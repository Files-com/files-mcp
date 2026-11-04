"""Runs the MCP server's tests. Fails if any test fails, if a test module
cannot be imported, or if no tests are found.

Run it from a directory containing tests/, with the interpreter and
dependencies under test:

    python scripts/run_tests.py                 # every test, on the source
    python scripts/run_tests.py tests.test_stdio
    python scripts/run_tests.py --installed     # the installed package
"""

import argparse
import json
import sys
import unittest
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Runs the MCP server's tests."
    )
    parser.add_argument("names", nargs="*", help="test modules to run")
    parser.add_argument(
        "--installed",
        action="store_true",
        help="fail unless files_com_mcp is imported from outside this directory",
    )
    parser.add_argument("--report", help="write the counts as JSON here")
    args = parser.parse_args()

    here = Path.cwd().resolve()
    sys.path.insert(0, str(here))
    import files_com_mcp
    import files_sdk

    location = Path(files_com_mcp.__file__).resolve().parent
    if args.installed == location.is_relative_to(here):
        sys.exit(
            f"files_com_mcp was imported from {location}, which is "
            f"{'' if args.installed else 'not '}in {here}"
        )

    loader = unittest.TestLoader()
    if args.names:
        suite = loader.loadTestsFromNames(args.names)
    else:
        suite = loader.discover("tests", top_level_dir=str(here))
    if loader.errors:
        for error in loader.errors:
            print(error, file=sys.stderr)
        sys.exit("Some test modules could not be loaded")
    if suite.countTestCases() == 0:
        sys.exit("No tests were found")

    result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = {
        "python": sys.version,
        "executable": sys.executable,
        "files_com_mcp": str(location),
        "files_sdk": str(Path(files_sdk.__file__).resolve().parent),
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": [
            {"test": test.id(), "reason": reason}
            for test, reason in result.skipped
        ],
        "successful": result.wasSuccessful(),
    }
    print(json.dumps(report, indent=2))
    if args.report:
        Path(args.report).write_text(json.dumps(report, indent=2) + "\n")
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
