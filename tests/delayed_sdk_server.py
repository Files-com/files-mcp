"""The server, started as usual, with one SDK service call replaced by a
stand-in whose cleanup takes a while after it is cancelled, as a transfer's
can. It records when it starts, sees the call's cancellation and finishes,
so tests can compare those moments with what the client receives.

    python delayed_sdk_server.py MARKERS [SOURCE_ROOT]

MARKERS is a directory for the records; SOURCE_ROOT, if given, is put on
sys.path to run the server from its source.
"""

import json
import sys
import time
from pathlib import Path

markers = Path(sys.argv[1])
if len(sys.argv) > 2:
    sys.path.insert(0, sys.argv[2])
sys.argv = [sys.argv[0]]

import files_sdk  # noqa: E402
import files_sdk.error  # noqa: E402
from files_com_mcp.__main__ import main  # noqa: E402

CLEANUP_SECONDS = 0.75


def mark(name):
    (markers / f"{name}.json").write_text(
        json.dumps({"monotonic": time.monotonic()})
    )


def find_user(id, params=None, options=None):
    mark("started")
    token = (options or {})["cancel_token"]
    deadline = time.monotonic() + 10
    while not token.cancelled:
        if time.monotonic() > deadline:
            raise RuntimeError("the call was not cancelled within 10 seconds")
        time.sleep(0.005)
    mark("cancel_seen")
    time.sleep(CLEANUP_SECONDS)
    mark("settled")
    raise files_sdk.error.OperationCancelledError("stopped")


files_sdk.user.find = find_user
main()
