import os
import shutil
import sys

from block_markdown import markdown_to_html_node
from copy_static import copy_files_recursive
from gen_content import generate_page, generate_pages_recursive
from htmlnode import HTMLNode

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    base_path = sys.argv[1] if sys.argv else "/"
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating content...")
    generate_pages_recursive(
        dir_path_content, template_path, dir_path_public, base_path
    )


main()
