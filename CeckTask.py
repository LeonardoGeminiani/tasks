#!/usr/bin/env python3

from Functions import *

settings, file_content = open_taskFile(
    lambda error:
        print(error)
)


try:
    tasks, metadata, raw_metadata = get_tasks(file_content, raw_metadata=True)
    #    unchecked_tasks = count_unchecked(tasks)

    task_to_do = find_first_unchecked(tasks, metadata["offset"])

    #print(task_to_do["text"])

    c = ""
    if tasks[task_to_do["number"]][-1] == "\n":
        c = "\n"

    tasks[task_to_do["number"]] = " [x] " + task_to_do["text"] + c

    #try:
    start_index = file_content[raw_metadata["end_char"]:].index("-") + raw_metadata["end_char"]
    new_file_content = file_content[:start_index]

    for task in tasks:
        new_file_content += "-" + task

    #print(tasks)
    metadata["offset"] = 0
    write_taskFile(set_metadata(metadata, "---", new_file_content), settings, lambda error:
        print(error)
    )

    #except:
    print("not valid file")

except:
    print("file empty")