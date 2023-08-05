#!/usr/bin/env python3

import os, sys
import json
from pathlib import Path
from xdg import BaseDirectory
import subprocess as sp
from typing import Union
from re import search
import requests
import urllib.parse
import bs4
from bs4 import BeautifulSoup, NavigableString, Tag

class Config:
    DOMAIN: Union[str, None] = None
    USERNAME: Union[str, None] = None
    PASSWORD: Union[str, None] = None

def die(m):
    print(m + '\nAborting...', file=sys.stderr)
    exit(1)

# Basically useless. Only here for lookup.
def assert_config_init():
    if not (isinstance(Config.DOMAIN, str) and isinstance(Config.USERNAME, str) and isinstance(Config.PASSWORD, str)):
        die("Config not initialized!")

def count_path(p: Path) -> Path:
    counting_p: Path = p
    i = 0
    while counting_p.exists():
        counting_p = Path(str(p) + str(i))
        i += 1
    return counting_p

def search_update(session: requests.Session, search_object: str, success_command: str, cache_dir: Union[str, None] = None):
    if not (isinstance(Config.DOMAIN, str) and isinstance(Config.USERNAME, str) and isinstance(Config.PASSWORD, str)):
        die("Config not initialized!")
    if not search_object.endswith(".html"):
        search_object += ".html"
    cat_request = session.get(Config.DOMAIN + '/' + search_object)
    if cat_request.status_code not in [200, 302]:
        die("Could not find " + search_object)
    soup = BeautifulSoup(cat_request.text, 'html.parser')
    items = soup.find_all("div", class_="il_ContainerListItem")

    if not cache_dir:
        cache_dir = BaseDirectory.save_cache_path('ilias-course-watcher')
    cache_dir_path = Path(cache_dir).expanduser()
    cache_dir_path.mkdir(parents=True, exist_ok=True)

    if not cache_dir_path.is_dir():
        die("Failed to create cache directory: " + str(cache_dir_path))

    object_cache_path = cache_dir_path / (search_object.split('.')[0] + '.icw')

    items_list = []
    top_text = soup.find('div', class_="ilc_Paragraph")
    if isinstance(top_text, Tag):
        items_list.append(top_text.text)

    for item in items:
        item_list = []
        item_list.append(item.find('a', class_="il_ContainerItemTitle").text)
        item_list.append(item.find('a', class_="il_ContainerItemTitle").href)
        item_list.append(item.find('div', class_="il_Description").text)
        item_properties = item.find_all('span', class_="il_ItemProperty")
        property_list = []
        for item_property in item_properties:
            property_list.append(item_property.text)
        item_list.append(property_list)
        items_list.append(item_list)

    compare_str = str(items_list)

    if object_cache_path.exists():
        with open(object_cache_path, "r") as object_cache_file:
            object_cache_contents = object_cache_file.read()
        if object_cache_contents != compare_str:
            object_cache_path.rename(count_path(Path(str(object_cache_path) + '.old')))
            with open(str(object_cache_path), "w") as object_cache_file:
                object_cache_file.write(compare_str)
            sp.run(success_command, shell=True)
    else:
        with open(str(object_cache_path), "w") as object_cache_file:
            object_cache_file.write(compare_str)

def search_entry(session: requests.Session, search_object: str, search_string: str, success_command: str):
    if not (isinstance(Config.DOMAIN, str) and isinstance(Config.USERNAME, str) and isinstance(Config.PASSWORD, str)):
        die("Config not initialized!")
    if not search_object.endswith(".html"):
        search_object += ".html"
    cat_request = session.get(Config.DOMAIN + '/' + search_object)
    if cat_request.status_code not in [200, 302]:
        die("Could not find " + search_object)
    soup = BeautifulSoup(cat_request.text, 'html.parser')
    items_container = soup.find("div", class_="ilContainerItemsContainer")
    if items_container is None:
        die("Failed to find container for " + search_object)
    elif isinstance(items_container, NavigableString):
        die("Uhm, I do not know what a NavigableString is and I did not expect one.")
    else:
        titles = map(lambda l: l.text, items_container.find_all("a", class_="il_ContainerItemTitle"))
        for title in titles:
            if search_string.lower() in title.lower():
                sp.run(success_command, shell=True)
                return (True, title)
        return (False, None)

def login(session: requests.Session):
    if not (isinstance(Config.DOMAIN, str) and isinstance(Config.USERNAME, str) and isinstance(Config.PASSWORD, str)):
        die("Config not initialized!")

    headers = {'Content-type': 'application/x-www-form-urlencoded'}

    login_response = session.post(url=Config.DOMAIN + '/studon/ilias.php?lang=de'
           '&client_id=StudOn&cmd=post'
           '&cmdClass=ilstartupgui&cmdNode=15j'
           '&baseClass=ilStartUpGUI&rtoken=',
           data='username=' + urllib.parse.quote_plus(Config.USERNAME) +
           '&password=' + urllib.parse.quote_plus(Config.PASSWORD) +
           '&cmd%5BdoStandardAuthentication%5D=Anmelden',
           headers=headers)

    if login_response.status_code not in [200, 302]:
        die('Expected statuscode 200 or 302 on login. Received: ' + str(login_response.status_code))
    return session

def watch_courses(json_cfg_path: str):

    with sys.stdin if json_cfg_path == '-' else open(json_cfg_path, 'r') as json_file:
        json_cfg = json.load(json_file)

    Config.DOMAIN = json_cfg["Domain"]
    Config.USERNAME = json_cfg["Username"]
    Config.PASSWORD = json_cfg["Password"]

    watch_tasks = json_cfg["Tasks"]

    with requests.Session() as s:
        login(s)

        for watch_task in watch_tasks:
            wtt = watch_task.pop("type")
            watch_task_type = wtt.lower()
            if watch_task_type == "search_entry":
                task_fn = search_entry
            elif watch_task_type == "search_update":
                task_fn = search_update
            elif watch_task_type == "queue":
                die("Queues are not yet implemented.")
            else:
                die("Unknown type: " + wtt)
            task_fn(session=s, **watch_task)

if __name__ == "__main__":
    if os.getuid() == 0:
        die("Nope, I'm not doing anything as root. Come back when you've acquired a brain!")

    if len(sys.argv) != 2:
        die("A config file has to be specified as a parameter!")
    watch_courses(sys.argv[1])
