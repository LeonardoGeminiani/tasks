import json
import os
import yaml


def find_first_unchecked(elements, offset: int):
    cnt = 0
    for element in elements:
        tmp = element.replace(" ", "")

        if tmp.startswith('[]'):
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

def generate_error(error):
    return f"<b>error: </b><span color='red'>{error}</span>"

def print_data(text :str, tooltip :str):
    data = {
        "text" : text,
        "tooltip" : tooltip
    }
    print(json.dumps(data))

def get_metadata(file: str, metadata_tag: str):
    if file.lstrip().startswith(metadata_tag):
        # Find the first occurrence of the tag and move to the end of it
        tag_len = len(metadata_tag)
        start_index = file.find(metadata_tag) + tag_len
        # Find the second occurrence of the tag, starting after the first one
        end_index = file.find(metadata_tag, start_index)
        
        if start_index != -1 and end_index != -1:
            return {
                "content": file[start_index:end_index].strip(),
                "end_char": (end_index + tag_len)
            }
        return None
    return None



def open_task():
    try:
        dir = f"{os.getenv('HOME')}/tasks"
        files = os.listdir(dir)

        if ".config" not in files:
            os.makedirs(f"{dir}/.config", exist_ok=True)

        with open(f"{dir}/.config/settings.json", "r+") as file:
            try:
                settings = json.load(file)
            except:
                #default settings
                settings = {
                    "currentFile": ""
                }
                json.dump(settings, file, indent=4)
    except:
        print_data(generate_error(f"{dir} does not exist"), "")
        exit()


    currentFile = settings["currentFile"]

    try:
        with open(f"{dir}/{currentFile}.md", 'r') as file:
            content = file.read()
    except:
        print_data(generate_error(f"not valid currentFile Selected"), "")
        exit()
    
    return [
        settings,
        content
    ]