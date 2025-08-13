import os
import shutil

from block import markdown_to_html_node
from extract_markdown import extract_title
from htmlnode import HTMLNode


def generate_page_r(dir_path_content, template_path, dest_dir_path):
    os.makedirs(dest_dir_path, exist_ok=True)
    with open(template_path, "r", encoding="utf-8") as template_file:
        template_content = template_file.read()

    for name in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, name)
        dst_path = os.path.join(dest_dir_path, name)

        if os.path.isdir(src_path):
            generate_page_r(src_path, template_path, dst_path)
        elif name.lower().endswith(".md"):
            with open(src_path, "r", encoding="utf-8") as md_file:
                md_content = md_file.read()
            html_content = markdown_to_html_node(md_content).to_html()
            html_title = extract_title(md_content)
            page = (
                template_content.replace("{{ Title }}", html_title)
                .replace("{{ Content }}", html_content)
                .replace('href="/', f'href="{dir_path_content}')
                .replace('src="/', f'src="{dir_path_content}')
            )

            out_path = os.path.splitext(dst_path)[0] + ".html"
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as output_file:
                output_file.write(page)


def generate_page(from_path, template_path, to_path):
    print(
        f"Generating page from {from_path} using template {template_path} to {to_path}"
    )

    with open(from_path, "r", encoding="utf-8") as md_file:
        md_content = md_file.read()

    with open(template_path, "r", encoding="utf-8") as template_file:
        template_content = template_file.read()

    html_content = markdown_to_html_node(md_content).to_html()
    html_title = extract_title(md_content)

    template_content = template_content.replace("{{ Title }}", html_title)
    template_content = template_content.replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(to_path), exist_ok=True)

    with open(to_path, "w", encoding="utf-8") as output_file:
        output_file.write(template_content)
