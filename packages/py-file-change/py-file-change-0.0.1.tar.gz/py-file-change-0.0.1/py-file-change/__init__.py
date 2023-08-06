"""
py-file-change
==============

py-file-change is a tool that execute specific command when any file changes in the directory.
"""

import os
import sys
import time
import subprocess

def get_last_modified_dict(path:str) -> dict:
    """
    returns the dict object containing filename and last modified time

    args:
        path <str> : directory path to use
    """
    data = os.walk(path)
    return_data = dict()
    for root, _, files in data:
        for file in files:
            file = os.path.join(root,file)
            return_data[file] = os.stat(file).st_mtime
    return return_data


def get_unique_data(old_dict:dict, new_dict:dict) -> dict:
    """
    returns the dict object that contains new files , changed files, deleted files by comparing
    two arguments that contains last modified time

    args:
        old_dict <dict> : dict value returned by `get_last_modified_dict` method(before)
        new_dict <dict> : dict value returned by `get_last_modified_dict` method(after)
    """
    return_data = {
        "changed" : [],
        "new" : [],
        "deleted" : [],
        "count" : 0
    }
    if old_dict != new_dict:
        return_data["changed"] = [
            file for file in set(old_dict.keys()).intersection(set(new_dict.keys()))
            if old_dict[file] != new_dict[file]
        ]
        return_data["new"] = list(set(new_dict.keys()).difference(set(old_dict.keys())))
        return_data["deleted"] = list(set(old_dict.keys()).difference(set(new_dict.keys())))
        return_data["count"] = len(return_data["new"])+len(return_data["changed"])+len(return_data["deleted"])

    return return_data


def is_exclude(unique_collection:dict, exclude_ends:list) -> bool:
    """
    return file in collection or not

    args:
        unique_collection <dict> : dict value returned by `get_unique_data` method
        exclude_ends <list> : list of ending string
    """
    unique_files = unique_collection["new"]+unique_collection["deleted"]+unique_collection["changed"]

    value = False

    for file in unique_files:
        for end in exclude_ends:
            if file.endswith(end):
                value = True
                break
        if value == True:
            break
    
    return value


def main(command:str, watchdir:str=".", exclude_ends:list = [], do_print:bool = False, use_kill:bool = False):
    """
    the main method

    args:
        command <str> : command to execute
        watchdir <str> : the directory to watch
        exclude_ends <list> : exclude ending files (won't restart when changed)
        do_print <bool> : print created, changed and deleted file if True
        use_kill <bool> : uses kill method of process instead terminate if True
    """
    print("File change monitor watching \"%s\""%(os.path.abspath(watchdir)))
    print("\nexecuting \"%s\"\n" %(command))
    try:
        process = subprocess.Popen(command.split())
    except PermissionError:
        print("\t*Cannot create process, check for permissions")
        sys.exit(1)
    current_data = get_last_modified_dict(watchdir)

    while True:
        try:
            new_data = get_last_modified_dict(watchdir)
            if new_data != current_data:
                unique_data = get_unique_data(current_data, new_data)
                if is_exclude(unique_data, exclude_ends) == False:
                    if use_kill == True:
                        print("\nKilling last process...")
                        process.kill()
                    else:
                        print("\nTerminate last process...")
                        process.terminate()

                    if do_print == True:
                        print("Total files affected : %d"%(unique_data["count"]))
                        if unique_data["changed"]:
                            print("changed files :",",".join(unique_data["changed"]))
                        if unique_data["new"]:
                            print("new files :",",".join(unique_data["new"]))
                        if unique_data["deleted"]:
                            print("deleted files :",",".join(unique_data["deleted"]))
                    else:
                        print("Files changed[%d]"%(unique_data["count"]))

                    print("\nexecuting : \"%s\"\n"%(command))
                    try:
                        process = subprocess.Popen(command.split())
                    except PermissionError:
                        print("\t*Cannot create process, check for permissions")
                        sys.exit(1)
                current_data = new_data
            time.sleep(0.05)

        except KeyboardInterrupt:
            print("Keyboard interrupt received...")
            if use_kill == True:
                print("\nKilling last process...")
                process.kill()
            else:
                print("\nTerminate last process...")
                process.terminate()
            sys.exit(0)