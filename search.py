"""
Author:         Cody Hawkins
Date:           12/1/2020
Class:          5130
File:           search.py
Desc:           search for chromedriver.exe in provided drive
                and return the file path
"""
import os
import sys


def file_search(filename, directory):
    print(f"searching for {filename}, this may take a few minutes")
    result = []
    for root, dirs, files in os.walk(directory):
        if filename in files:
            result.append(os.path.join(root, filename))
    if len(result) == 0:
        print("Could not find image! Please try a new image!")
        sys.exit(1)
    else:
        print(f"{filename} found at {result[0]}")

    return result[0]