#!/bin/env python
import os
import sys

print(sys.argv[1:])

os.system("gnome-terminal -- bash -c \"/home/dev/src/rmrf/themes/hugo-for-photographers/scripts/photo-post.py %s;read -p DONE\"" % " ".join(sys.argv[1:]))
