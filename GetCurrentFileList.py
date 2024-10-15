#!/usr/bin/env python3

from Functions import *

settings, files = get_settings(
    lambda error:
        print(error)
    , files_ret=True
)

for file in files:
    if file.endswith(".md"):
        print(file[:-3])