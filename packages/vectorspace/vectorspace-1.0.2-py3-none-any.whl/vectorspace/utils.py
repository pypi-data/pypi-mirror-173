import itertools
import json
import os
from random import shuffle
from typing import Iterable, List, TypeVar


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


def readlines(path, binary=False, skip_rows=0):
    path = expand_path(path)
    with open(path, 'rb' if binary else 'r', encoding=None if binary else 'utf-8') as f:
        for i, line in enumerate(f):
            if i >= skip_rows:
                yield line.rstrip()


def writelines(lines, path, binary=False):
    path = expand_path(path)
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, 'wb' if binary else 'w', encoding=None if binary else 'utf-8') as f:
        for i, line in enumerate(lines):
            if (i > 0):
                f.write(b'\n' if binary else '\n')
            f.write(line)


T = TypeVar('T')


def take(n: int, iterable: Iterable[T]) -> List[T]:
    "Return first n items of the iterable as a list"
    return list(itertools.islice(iterable, n))


def chunked(iterable: Iterable[T], n: int) -> Iterable[List[T]]:
    "Break iterable into chunks of length n"
    it = iter(iterable)
    chunk = take(n, it)
    while chunk != []:
        yield chunk
        chunk = take(n, it)


def randomize(iterable: Iterable[T], bufsize: int = 1000) -> Iterable[T]:
    "Naïve shuffle algorithm"
    for chunk in chunked(iterable, bufsize):
        shuffle(chunk)
        yield from chunk
