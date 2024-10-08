#!/usr/bin/env python3
import json
import os
import yaml

from Functions import *

[settings, content] = open_task()

#try:

metadata = get_metadata(content, "---")
metadata_yaml = yaml.safe_load(metadata["content"])

tasks = content[metadata["end_char"]:].lstrip().split("-", 1)[1].split("-")

task_to_do = find_first_unchecked(tasks, metadata_yaml["offset"])

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
#except:
#print_data(generate_error("no tasks <b>(file empty)</b>"), "")
