# AzzieL3MTools
# utils.py
# Hillman
# June 2025

import json


## file handling functions  follow (housekeeping)
keep_alive = "30m"

def loadjson(fname):
    with open(fname, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def loadtext (fname):
    with open(fname,"r") as file:
        return file.read()
