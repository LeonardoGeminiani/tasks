#!/usr/bin/env python3

import subprocess

from Functions import *

settings, file_content = open_taskFile(
    lambda error:
        print(error)
)

subprocess.run(["code", f"{os.getenv('HOME')}/tasks/{settings["currentFile"]}.md"])