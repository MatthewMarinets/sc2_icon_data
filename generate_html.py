
from typing import *
import json
import io
import inspect

def write_start(fp: io.FileIO) -> None:
    fp.write(inspect.cleandoc("""
    <!doctype html>
    <html>
    <head>
        <title>Starcraft 2 Icon Repository</title>
        <meta name="description" content="A repository of Starcraft 2 icons used in Archipelago">
        <meta name="keywords" content="Archipelago Starcraft 2">
        <link rel="stylesheet" href="styles/common.css"/>
    </head>
    <body style="background-color: black; color: #ebb">
        <div id="main-content">
    """))

def brief_name(item_name: str) -> str:
    return item_name.strip().replace('/', '-').replace('(', '').replace(')', '').replace(' ', '-')

def write_table_of_contents(fp: io.FileIO, item_names: Iterable[str]) -> None:
    fp.write("""
    <div id="toc">
    <h2>Table of Contents</h2>
        <ol>
    """)
    for item_name in item_names:
        fp.write(f'<li><a href="#{brief_name(item_name)}">{item_name}</a></li>\n')
    fp.write('</ol></div>\n')

def write_item(fp: io.FileIO, item_name: str, item_info: str, icon_location: str|None) -> None:
    fp.write(inspect.cleandoc(f"""
    <div id="{item_name}">
        <h2><a id="{brief_name(item_name)}"></a>{item_name}</h2>
        {f'<img src="{icon_location}"/>' if icon_location else '<p class="error">Icon currently unavailable</p>'}
        <ul>
        <li>Faction: {item_info["race"]}</li>
        <li>Classification: {item_info["classification"]}</li>
        {f'<li>Description: {item_info["description"]}</li>' if item_info["description"] else ''}
        {f'<li>Parent: {item_info["parent_item"]}</li>' if item_info["parent_item"] else ''}
        {f'<li>Icon path: <code>{icon_location}</code></li>' if icon_location else ''}
        </ul>
    </div>
    """))

def write_end(fp: io.FileIO) -> None:
    fp.write(inspect.cleandoc("""
        </div>
    </body>
    </html>
    """))

if __name__ == '__main__':
    with open('data/item_data.json', 'r') as fp:
        item_data = json.load(fp)
    with open('data/icon_manifest.json', 'r') as fp:
        icon_manifest = json.load(fp)
    with open('index.html', 'w') as fp:
        write_start(fp)
        write_table_of_contents(fp, item_data)
        for item in item_data:
            write_item(fp, item, item_data[item], icon_manifest.get(item))
        write_end(fp)