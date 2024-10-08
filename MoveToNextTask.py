#!/usr/bin/env python3
import json
import os
import yaml

from Functions import *

settings, file_content = open_taskFile(
    lambda error:
        print("error")
)

try:
    tasks, metadata = get_tasks(file_content)
except:
    print("file empty")