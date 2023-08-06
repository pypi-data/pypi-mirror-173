from collections.abc import Mapping as MappingABC, MutableMapping as MutableMappingABC
from typing import Callable, MutableMapping, Optional, Tuple


class KeyValueMapping(MutableMappingABC):

    def __init__(self, wrapped: MutableMapping,
                 key_fn: Optional[Tuple[Callable, Callable]] = None,
                 val_fn: Optional[Tuple[Callable, Callable]] = None):
        self._wrapped = wrapped
        self._dump_key, self._load_key = key_fn if key_fn else (lambda v: v, lambda v: v)
        self._dump_val, self._load_val = val_fn if val_fn else (lambda v: v, lambda v: v)

    def __getitem__(self, key):
        if isinstance(key, (tuple, list)):
            # handle list of keys
            key = [self._dump_key(k) for k in key]
            return [self._load_val(v) for v in self._wrapped[key]]

        elif isinstance(key, (slice, range)):
            # handle slice of keys
            key = slice(
                self._dump_key(key.start) if key.start is not None else None,
                self._dump_key(key.stop) if key.stop is not None else None, key.step)
            return [self._load_val(v) for v in self._wrapped[key]]

        else:
            # handle rest (i.e. key only)
            return self._load_val(self._wrapped[self._dump_key(key)])

    def __contains__(self, key):
        return self._dump_key(key) in self._wrapped

    def keys(self):
        return (self._load_key(k) for k in self._wrapped.keys())

    def items(self):
        return ((self._load_key(k), self._load_val(v)) for k, v in self._wrapped.items())

    def values(self):
        return (self._load_val(v) for v in self._wrapped.values())

    def __iter__(self):
        return self.keys()

    def __setitem__(self, key, value):
        self._wrapped[self._dump_key(key)] = self._dump_val(value)

    def __delitem__(self, key):
        del self._wrapped[self._dump_key(key)]

    def update(self, other=()):
        if isinstance(other, MappingABC):
            items = other.items()
        elif hasattr(other, "keys"):
            items = ((k, other[k]) for k in other.keys())
        else:
            items = other
        return self._wrapped.update((self._dump_key(k), self._dump_val(v)) for k, v in items)

    def __len__(self):
        return len(self._wrapped)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        if hasattr(self._wrapped, 'close'):
            self._wrapped.close()  # type: ignore
