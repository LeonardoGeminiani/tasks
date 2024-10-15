#!/usr/bin/env python3

import sys
from Functions import *

settings = get_settings(
    lambda error:
        print(error)
)

if sys.argv[1] == "":
    exit()

settings["currentFile"] = sys.argv[1]

set_settings(settings, lambda error:
    print(error)
)