#!/usr/bin/env python
import sys

offset = int(sys.argv[1])
nprocesses = int(sys.argv[2])

limit = 5

for i in range(nprocesses):
    cmd = "python -m solution.tools.fill_db --limit %d --noparse --offset %d &" % (limit, offset)
    offset += limit
    print cmd
