#!/usr/bin/env python3
import json

from Functions import *

def generate_error(error):
    return f"<b>error: </b><span color='red'>{error}</span>"


def print_data(text :str, tooltip :str):
    data = {
        "text" : text,
        "tooltip" : tooltip
    }
    print(json.dumps(data))

settings, file_content = open_taskFile(
    lambda error: 
        print_data(generate_error(error), "")
)

try:
    
    tasks, metadata = get_tasks(file_content)

    task_to_do = find_first_unchecked(tasks, metadata["offset"])

    text = ""
    if task_to_do == None:
        text = "<b>No more tasks to do</b>"
    else:
        text = convert_md_to_html(task_to_do["text"])

    tooltip = ""
    cnt = 0
    for task in tasks:
        if cnt == task_to_do["number"]:
            # arrow
            tooltip +=  "<span color='#a6e3a1'>&#x279C;</span>"
        else:
            # space
            tooltip += "<span>&#8195;</span>"
        tooltip += convert_md_to_html(task)
        cnt+=1

    # good print
    print_data(
        text,
        f"<span size='large' color='#a6e3a1'>&#8195;<b>{settings["currentFile"].replace("_", " ").title()}</b></span>\n\n" + #convert_md_to_html(content[metadata["end_char"]:].lstrip())
        tooltip
    )
except:
    print_data(generate_error("no tasks <b>(file empty)</b>"), "")
