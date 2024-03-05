import json
import pathlib
import sys
from tkinter import messagebox

import requests
import os
import re

UUID_PATTERN = re.compile(r'[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}', re.IGNORECASE)

def getCollection():
    file_dir = os.path.dirname(sys.argv[1])
    collection_io = {}

    if file_dir:
        for file in os.listdir(file_dir):
            if file == 'collection.io':
                f = os.path.join(file_dir, file)
                with open(f, 'r') as col:
                    collection_io = json.load(col)
    return collection_io

def getContent(collection: {}, contentType: str, key: str):
    if contentType in collection:
        return True

def getFileContent(file):
    f = open(file, 'r', encoding='utf-8')

    if pathlib.Path(file).suffix == '.json':
        file_content = json.load(f)
        if type(file_content) is list:
            out = json.dumps(flatten_json(file_content)[''], ensure_ascii=False)
        else:
            out = json.dumps(flatten_json(file_content), ensure_ascii=False)
    else:
        out = ''.join(f.readlines())

    return out

def flatten_json(nested_json):
   flattened_json = {}
   def flatten(x, name=''):
      if type(x) is dict:
         for a in x:
            flatten(x[a], name + a + '_')
      else:
         flattened_json[name[:-1]] = x

   flatten(nested_json)
   return flattened_json


def AvraeRest(type: str, endpoint: str, payload = None):
    if payload is None:
        payload = ""

    token = os.environ.get('AVRAE_TOKEN')
    header = {
        "Authorization": token
    }
    url = '/'.join(['https://api.avrae.io', endpoint]).strip('/')

    try:
        request: requests.Response = requests.request(type.upper(), url, headers=header, json=payload)
    except:
        return

    if request.status_code in [200, 201]:
        print(f"Succesfully {type.upper()} to {endpoint}")
    else:
        print(f"Unsuccessful {type.upper()} to {endpoint}. Error code {request.status_code} - {request.text}")
        messagebox.showerror(title=f"Error {request.status_code}", message=f"{json.loads(request.text)['error']}")
    return request


def isJSON(str):
    try:
        json.loads(str)
    except:
        return False
    return True