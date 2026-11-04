"""Records a server child in a ledger, then becomes that child.

    python -I child_ledger.py LEDGER COMMAND [ARGUMENT...]

A qualification run sets FILES_MCP_CHILD_LEDGER so that every server the
tests start, each in a session of its own, is recorded before it runs;
afterwards the run checks that each has exited. The recorded process is the
server itself: exec keeps its process ID and gives it COMMAND's argv.
"""

import json
import os
import sys

ledger, command = sys.argv[1], sys.argv[2:]
with open(ledger, "a") as records:
    records.write(
        json.dumps(
            {
                "pid": os.getpid(),
                "pgid": os.getpgid(0),
                "sid": os.getsid(0),
                "argv": command,
            }
        )
        + "\n"
    )
os.execv(command[0], command)
