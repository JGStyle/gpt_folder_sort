import sys
import os 
from os import listdir
from openai import OpenAI
import yaml
from termcolor import colored
import shutil

client = OpenAI()

def get_files(path):
    return listdir(path)

def get_sysprompt(name):
    with open('prompts.yaml', 'r') as file:
        data = yaml.safe_load(file)

    for prompt in data['prompts']:
        if prompt["name"] == name:
            return prompt["content"]


def gpt_prompt(input, sysprompt):
    gpt = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role" : "system", "content": sysprompt}, {"role": "user", "content": input}])
    return gpt.choices[0].message.content


def parse_fs(fs):
    folders = set()

    for line in fs.split("\n"):
        if "/" in line: 
            parts = line.split("/")  
            for i in range(1, len(parts)):
                folder_path = "/".join(parts[:i])
                folders.add(folder_path)  

    return sorted(list(folders))


def create_file_structure(fs, folders, base_path):
    # Create the folders first
    for folder in folders:
        full_path = os.path.join(base_path, folder)
        os.makedirs(full_path, exist_ok=True)
    
    # Process each line in the fs string
    for line in fs.strip().split('\n'):
        # Extract the target folder and filename from each line
        target_folder, filename = os.path.split(line)
        # Ensure the target folder is one of the folders we intend to create/move files into
        if target_folder in folders:
            # Construct the source path (file initially at the root of base_path)
            src_path = os.path.join(base_path, filename)
            # Construct the destination path
            dst_path = os.path.join(base_path, target_folder, filename)
            # Check if the source file exists before attempting to move
            if os.path.exists(src_path):
                # Move the file
                shutil.move(src_path, dst_path)
            else:
                print(f"File not found: {src_path}")

def sort_lines_alphabetically(input_string):
    lines = input_string.split('\n')
    sorted_lines = sorted(lines)
    sorted_string = '\n'.join(sorted_lines)
    return sorted_string



if __name__ == "__main__":

    folder_path = sys.argv[1]
    print(colored(f"selected folder: {folder_path}", 'blue'))

    folders = []
    folders_string = ""

    files = get_files(folder_path)
    files_string = "\n".join(files)

    if len(sys.argv) > 2:
        folders = sys.argv[2:len(sys.argv):1]
    else:
        req = gpt_prompt(files_string, get_sysprompt("asp-generate_foldernames-v1"))
        folders = f"{req}".split(",")
        for i in range(len(folders)): 
            folders[i] = folders[i].strip()

    folders_string = ",".join(folders)


    prompt = f"files: {files_string} \n folders: {folders_string}"
    new_file_structure = gpt_prompt(prompt, get_sysprompt("asp-sort_files_into_folders-v1"))

    print(colored("suggested file structure", 'blue'))
    print(sort_lines_alphabetically(new_file_structure))
    print("")

    print(colored("The following folders will be created", 'blue'))
    print(", ".join(folders))

    input(colored("[Hit enter to confirm]", 'green'))

    # print("\nsuccess")

    create_file_structure(new_file_structure, folders, folder_path)



