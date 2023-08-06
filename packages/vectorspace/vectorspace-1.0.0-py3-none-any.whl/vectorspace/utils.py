import json
import os


def expand_path(path: str):
    return os.path.expandvars(os.path.expanduser(path))


def json_load(path):
    path = expand_path(path)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def json_dump(obj, path, **kwargs):
    path = expand_path(path)
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        return json.dump(obj, f, **kwargs)
