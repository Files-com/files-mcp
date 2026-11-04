#!/usr/bin/env bash
# Checks this package without changing it: formatting, lint, types and the
# tests (see scripts/tasks.py). PYTHON chooses the interpreter, which must
# be Python 3.11 or newer. FILES_COM_SDK names the files-com wheel to test
# with; without it, the Python SDK generated next to this package is built.
set -euo pipefail
cd "$(dirname "$0")"
exec "${PYTHON:-python3}" scripts/tasks.py check
