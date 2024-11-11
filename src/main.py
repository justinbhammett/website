import os
import shutil

from htmlnode import *
from textnode import *

def remove_contents(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.unlink(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

def copy_contents(source_directory, destination_directory):
    for item in os.listdir(source_directory):
        source_path = os.path.join(source_directory, item)
        destination_path = os.path.join(destination_directory, item)
        if os.path.isdir(source_path):
            shutil.copytree(source_path,destination_path)
        else:
            shutil.copy2(source_path, destination_path)


def refresh_public_folder(static_folder="static", public_folder="public"):
    #remove all contents from public folder and replace with contents from static folder
    if not os.path.exists(public_folder):
        os.mkdir(public_folder)
    else:
        remove_contents(public_folder)
    copy_contents(static_folder, public_folder)

def extract_title(markdown):
    markdown_lines = markdown.split("\n")

    for markdown_line in markdown_lines:
        if markdown_line.startswith("# "):
            return markdown_line[2:].strip()
    raise Exception("No header found")

refresh_public_folder()

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # import markdown from from_path
    try:
        with open(from_path) as md_contents:
            markdown_contents = md_contents.read()
    except FileNotFoundError:
        return "Error: No file found."
    except Exception as e:
        return f"An error has occurred: {e}"
    
    # import template from template_path
    try:
        with open(template_path) as temp_contents:
            template_contents = temp_contents.read()
    except FileNotFoundError:
        return "Error: No file found."
    except Exception as e:
        return f"An error has occurred: {e}"

    md_to_html = markdown_to_html_node(markdown_contents).to_html()
    title = extract_title(markdown_contents)
    output_html = template_contents.replace("{{ Title }}", title).replace("{{ Content }}", md_to_html)
 
    try:
        with open(dest_path+"/index.html", 'w', encoding='utf-8') as file:
            file.write(output_html)
            print(f"Successfully wrote to the file: {dest_path+"/index.html"}")
    except Exception as e:
                print(f"An error occurred: {e}")
    
# generate_pages_recursively 
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    list_of_files = os.listdir(dir_path_content)
    for item in list_of_files:
        path_to = os.path.join(dir_path_content, item)
        if os.path.isfile(path_to):
            _, ext = os.path.splitext(path_to)
            if ext.lower() == ".md":
                generate_page(path_to, template_path, dest_dir_path)
        if os.path.isdir(path_to):
            new_dir_path_content = os.path.join(dir_path_content, item)
            new_dest_dir_path = os.path.join(dest_dir_path, item)
            if not os.path.exists(new_dest_dir_path):
                os.makedirs(new_dest_dir_path)
                print(f"directory created: {new_dest_dir_path}")
            generate_pages_recursive(new_dir_path_content, template_path, new_dest_dir_path)


def main():
    pass

# generate_page("content/index.md", "template.html", "public")
generate_pages_recursive("content", "/home/jhammett360/workspace/website/template.html", "public")





        