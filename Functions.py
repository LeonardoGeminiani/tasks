import json
import os
import yaml

DIR = f"{os.getenv('HOME')}/tasks"

def task_is_uncheked(task):
    tmp = task.replace(" ", "")
    return tmp.startswith('[]')

def find_first_unchecked(elements, offset: int):
    cnt = 0
    for element in elements:

        if task_is_uncheked(element):
            tmp = element.replace('[', "", 1).replace(']', "", 1).strip()
            if tmp[-2:] == '\\n':
                tmp = tmp[:-2]
            if offset == 0:
                return {
                    "text": tmp,
                    "number": cnt
                }
            else:
                offset-=1
        cnt+=1
    return None

def count_unchecked(tasks):
    c = 0
    for task in tasks:
        if task_is_uncheked(task):
            c+=1
    return c

def convert_md_to_html(markdown_text):
    markdown_text = markdown_text.replace('\\**', '')
    markdown_text = markdown_text.replace('\\*', '')
    markdown_text = markdown_text.replace('\\==', '')
    
    # Convert bold text
    while '**' in markdown_text:
        markdown_text = markdown_text.replace('**', '<b>', 1).replace('**', '</b>', 1)
    
    # Convert italic text
    while '*' in markdown_text:
        markdown_text = markdown_text.replace('*', "<i>", 1).replace('*', '</i>', 1)
    
    # Convert highlight
    while '==' in markdown_text:
        markdown_text = markdown_text.replace('==', "<span bgcolor='#27611b'>", 1).replace('==', '</span>', 1)

    markdown_text = markdown_text.replace('-', "&#x2022;")
    # ck box ☐☑
    for char in ['[ ]', '[]']:
        markdown_text = markdown_text.replace(char, "☐")
    markdown_text = markdown_text.replace('[x]', "✔")

    return markdown_text

def get_metadata(file: str, metadata_tag: str):
    if file.lstrip().startswith(metadata_tag):
        # Find the first occurrence of the tag and move to the end of it
        tag_len = len(metadata_tag)
        start_index = file.find(metadata_tag) + tag_len
        # Find the second occurrence of the tag, starting after the first one
        end_index = file.find(metadata_tag, start_index)
        
        if end_index != -1:
            return {
                "content": file[start_index:end_index].strip(),
                "end_char": (end_index + tag_len)
            }
        return None
    return None

def set_settings(settings, on_error):
    try:
        files = os.listdir(DIR)

        if ".config" not in files:
            on_error(f"{DIR}/.config does not exsist")
            exit()
            
        files = os.listdir(f"{DIR}/.config")
        
        if "settings.json" not in files:
            on_error("settings.json does not exist")

    except:
        on_error(f"{DIR} does not exist")
        exit()
    
    with open(f"{DIR}/.config/settings.json", "w") as file:
        json.dump(settings, file, indent=4)
        print("ra")


def get_settings(on_error, files_ret=False):
    try:
        files = os.listdir(DIR)

        if ".config" not in files:
            os.makedirs(f"{DIR}/.config", exist_ok=True)

        with open(f"{DIR}/.config/settings.json", "r+") as file:
            try:
                settings = json.load(file)
            except:
                #default settings
                settings = {
                    "currentFile": ""
                }
                
                json.dump(settings, file, indent=4)
    except:
        on_error(f"{DIR} does not exist")
        exit()
    if files_ret:
        return settings, files
    return settings


def open_taskFile(on_error):
    settings = get_settings(on_error)

    currentFile = settings["currentFile"]

    try:
        with open(f"{DIR}/{currentFile}.md", 'r') as file:
            file_content = file.read()
    except:
        on_error(f"not valid currentFile Selected")
        exit()
    
    return settings, file_content

def write_taskFile(content: str, settings: object, on_error):
    try:
        files = os.listdir(DIR)

        if ".config" not in files:
            on_error(f"{DIR}/.config does not exsist")
            exit()

    except:
        on_error(f"{DIR} does not exist")
        exit()

    currentFile = settings["currentFile"]

    try:
        with open(f"{DIR}/{currentFile}.md", 'w') as file:
            file.write(content)
    except:
        on_error(f"not valid currentFile Selected")


def get_tasks(file_content: str, raw_metadata=False):
    metadata = get_metadata(file_content, "---")
    metadata_yaml = yaml.safe_load(metadata["content"])

    tasks = file_content[metadata["end_char"]:].lstrip().split("-", 1)[1].split("-")

    if raw_metadata:
        return tasks, metadata_yaml, metadata
    return tasks, metadata_yaml

def set_metadata(metadata: object, metadata_tag: str, file: str):
    start_index = 0
    if file.lstrip().startswith(metadata_tag):
        # Find the first occurrence of the tag and move to the end of it
        tag_len = len(metadata_tag)
        start_index = file.find(metadata_tag) 
        end_index = file.find(metadata_tag, start_index + tag_len) + tag_len
        
        if end_index != -1:
            file = file[:start_index] + file[end_index + 1:]
    file = file[:start_index] + "---\n" + yaml.dump(metadata, default_flow_style=False) + "---\n" + file[start_index:]
    return file
    