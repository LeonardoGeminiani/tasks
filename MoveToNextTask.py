#!/usr/bin/env python3
import json
import os
import yaml

from Functions import *

settings, file_content = open_taskFile(
    lambda error:
        print(error)
)

try:
    tasks, metadata = get_tasks(file_content)
    unchecked_tasks = count_unchecked(tasks)

    offset = metadata["offset"]

    newoffset = (offset +1)%unchecked_tasks
    metadata["offset"] = newoffset

    print(newoffset)
except:
    print("file empty")