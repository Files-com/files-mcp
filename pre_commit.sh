#!/usr/bin/env sh
# The release process (push_release.rb) runs this in the files-mcp
# repository before it commits and publishes a release. Development builds
# depend on the unreleased SDK generated with them, files-com==1.0, which no
# published release satisfies. This replaces that requirement with the
# published SDK releases the server supports, and stops the release until
# the oldest of them is on PyPI, so no published server depends on an SDK
# that cannot be installed.
set -eu

development='"files-com==1.0"'
release='"files-com>=2.0.0,<3"'
minimum='2.0.0'
index="${FILES_COM_SDK_INDEX:-https://pypi.org/pypi}"

if ! grep -qF "$development" pyproject.toml; then
  echo "pre_commit.sh: pyproject.toml does not require $development" >&2
  exit 1
fi

if ! python3 - "$index/files-com/$minimum/json" <<'EOF'
import sys
import urllib.request

try:
    urllib.request.urlopen(sys.argv[1], timeout=30).close()
except Exception as error:
    sys.exit(f"pre_commit.sh: {sys.argv[1]}: {error}")
EOF
then
  echo "pre_commit.sh: files-com $minimum is not published at $index; release the SDK first" >&2
  exit 1
fi

sed "s|$development|$release|" pyproject.toml > pyproject.toml.release
mv pyproject.toml.release pyproject.toml

if grep -qF "$development" pyproject.toml || ! grep -qF "$release" pyproject.toml; then
  echo "pre_commit.sh: could not write $release to pyproject.toml" >&2
  exit 1
fi
