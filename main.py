import pyautogui
import sys
import inspect
import math
import json
import os
from tkinter import filedialog
from threading import Thread


def editable_input(text: str) -> str:
    Thread(target=pyautogui.write, args=(text,)).start()
    modified_input = input()
    return modified_input

def print_help():
    raise NotImplementedError
    function_name = inspect.currentframe().f_back.f_code.co_name
    if function_name == ...:
        ...

def print_cursor(keys_path: list[str]) -> None:
    print("[", "/".join(keys_path), "]")

def _get_an_integer(mini: int = 0, maxi: int = math.inf) -> int:
    lever = True
    while lever:
        raw_string: str = input(">>> ").strip()
        if not raw_string.lstrip("-+").isnumeric():
            print(f"Expected output: [{mini}:{maxi}]")
            continue
        raw_int: int = int(raw_string)
        if raw_int < mini and raw_int > maxi:
            print(f"Expected output: [{mini}:{maxi}]")
            continue
        lever = False
    return raw_int


def quit_program():
    sys.exit(0)

def add_entry(global_dict: dict, keys_path: list[str]) -> None:
    new_key = input("Add entry:\n>>> ")
    cursor = global_dict
    for key in keys_path:
        cursor = cursor[key]
    if new_key not in cursor:
        cursor[new_key]={}
        print("Node successfully added:", new_key)
    else:
        print("Node already in map")

def remove_entry(global_dict: dict, keys_path: list[str]) -> None:
    cursor = global_dict
    cursor_keys = cursor.keys()
    for key in keys_path:
        cursor = cursor[key]
    for i, key in enumerate(cursor_keys):
        index = i + 1
        print(index, key)
    print("0 Cancel")
    res = _get_an_integer(0, len(cursor_keys))
    if res:
        _ = cursor.pop(cursor_keys[res - 1])
        print("Node successfully removed:", _)
    else:
        print("Delete operation cancelled")

def edit_entry(global_dict: dict, keys_path: list[str]) -> None:
    cursor = global_dict
    for key in keys_path[:-1]:
        cursor = cursor[key]
    cursor_keys = list(cursor.keys())
    for i, key in enumerate(cursor_keys):
        index = i + 1
        print(index, key)
    print("0 Cancel")
    res = _get_an_integer(0, len(cursor_keys))
    if res:
        old_key = cursor_keys[res - 1]
        new_key = editable_input(old_key)
        cursor[new_key] = cursor[old_key]
        cursor.pop(old_key)
        if old_key == keys_path[-1]:
            keys_path.pop()
            keys_path.append(new_key)
        print(f"Node successfully edited: {old_key} -> {new_key}")
    else:
        print("Edit operation cancelled")

def view_map(global_dict: dict) -> None:
    def view_map_rec(a_dict: dict, indents: int) -> None:
        tabs = "    " * indents
        for key in a_dict:
            print(tabs + key)
            if len(a_dict[key]):
                view_map_rec(a_dict[key], indents + 1)      
    
    view_map_rec(global_dict, 0)

def navigate_map(global_dict: dict, keys_path: list[str]) -> None:
    def navigate_map_internal(global_dict: dict, keys_path: list[str]) -> bool:
        cursor = global_dict
        parent_of_cursor = global_dict
        if keys_path:
            for key in keys_path[:-1]:
                cursor = cursor[key]
                parent_of_cursor = parent_of_cursor[key]
            cursor = cursor[keys_path[-1]]
        cursor_keys = list(cursor.keys())
        if cursor_keys:
            for i, key in enumerate(cursor_keys):
                index = i + 1
                print(index, key)
        else:
            print("...")
        print("0 Go up")
        print("-1 Quit mode")
        print_cursor(keys_path)
        res = _get_an_integer(-1 , len(cursor_keys))
        if res == -1:
            return False
        elif res == 0:
            if len(keys_path) == 1:
                print(f"Cannot go up anymore")
            else:
                keys_path.pop()
        else:
            keys_path.append(cursor_keys[res - 1])
        return True

    lever = True
    while lever:
        lever = navigate_map_internal(global_dict, keys_path)
        
def save_map(global_dict: dict) -> None:
    map_name = input("Enter save name:\n>>> ")
    file_name = f'{map_name}.map.json'
    with open(file_name, 'w') as f:
        json.dump(global_dict, f, indent=4)
    print(f"{file_name} saved")

def load_map(file_name: str = "test.map.json") -> dict:
    if not file_name:
        file_name = filedialog.askopenfilename(
            title='Open a map',
            initialdir=os.getcwd(),
            filetypes=(
                ('Map files', '*.map.json'),
                ('All files', '*.*')
            )
        )
    with open(file_name, 'r') as f:
        return json.load(f)

def select_mode(list_of_actions: list[str], global_dict: dict, keys_path: list[str]) -> None:
    for index, action in enumerate(list_of_actions):
        print(index, action)
    print_cursor(keys_path)
    res = _get_an_integer(0, len(list_of_actions) - 1)
    if res == 0:
        quit_program()
    elif res == 1:
        add_entry(global_dict, keys_path)
    elif res == 2:
        edit_entry(global_dict, keys_path)
    elif res == 3:
        navigate_map(global_dict, keys_path)
    elif res == 4:
        view_map(global_dict)
    elif res == 5:
        remove_entry(global_dict, keys_path)
    elif res == 6:
        save_map(global_dict)
    elif res == 7:
        global_dict = load_map()
        keys_path = list(global_dict.keys())


def main() -> None:
    list_of_actions = [
        "Quit program",
        "Add entry",
        "Edit entry",
        "Navigate",
        "View map",
        "Remove entry",
        "Save map",
        "Load map",
    ]
    d = load_map()
    k = list(d.keys())
    while True:
        select_mode(list_of_actions, d, k)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        quit_program()
