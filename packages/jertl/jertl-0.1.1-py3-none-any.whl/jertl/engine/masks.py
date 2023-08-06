import collections.abc
import copy
from   functools import singledispatch


class MaskedList(collections.abc.Sequence):
    def __init__(self, backing_sequence, offset=0, end=None):
        self.backing_sequence = backing_sequence
        self.offset = offset
        self.end = end if end is not None else len(backing_sequence)
        if not 0 <= self.end <= len(backing_sequence):
            raise IndexError(self.end)

    def __len__(self):
        return self.end - self.offset

    def __getitem__(self, index):
        offset_index = index + self.offset
        if offset_index < self.end:
            return self.backing_sequence[offset_index]
        else:
            raise IndexError(index)

    def __eq__(self, other):
        return other == self.backing_sequence[self.offset:self.end]

    def pop(self):
        value = self[0]
        self.offset += 1
        return value

    def widen(self):
        if self.end < len(self.backing_sequence):
            self.end += 1
        else:
            raise IndexError(len(self))

    def collapse(self):
        self.end = self.offset

    def snapshot(self):
        return MaskedList(self.backing_sequence, self.offset, self.end)

    def freeze(self):
        return [*self]

    def __repr__(self):
        return repr(self.backing_sequence[self.offset:self.end])


class MaskedDict(collections.abc.Mapping):
    def __init__(self, backing_mapping, masked_keys=None):
        self.backing_mapping = backing_mapping
        self.masked_keys = set() if masked_keys is None else masked_keys

    def __len__(self):
        return len(self.backing_mapping) - len(self.masked_keys)

    def __getitem__(self, key):
        if key in self.masked_keys:
            raise KeyError(key)
        else:
            return self.backing_mapping[key]

    def __delitem__(self, key):
        if key not in self.backing_mapping or key in self.masked_keys:
            raise KeyError(key)
        else:
            self.masked_keys |= {key}

    def pop(self, key):
        value = self[key]
        del self[key]
        return value

    def snapshot(self):
        return MaskedDict(self.backing_mapping, copy.copy(self.masked_keys))

    def freeze(self):
        return {**self}

    class Iterator:
        def __init__(self, masked_mapping):
            self.masked_keys    = masked_mapping.masked_keys
            self.inner_iterator = iter(masked_mapping.backing_mapping)

        def __next__(self):
            candidate_next = next(self.inner_iterator)
            if candidate_next in self.masked_keys:
                return self.__next__()
            else:
                return candidate_next
            
    def __iter__(self):
        return self.Iterator(self)

    def __repr__(self):
        return repr({k: v for k, v in self.backing_mapping.items() 
                          if k not in self.masked_keys})


@singledispatch
def freeze(value):
    return value

@freeze.register(MaskedList)
def _(masked_list):
    return masked_list.freeze()

@freeze.register(MaskedDict)
def _(masked_dict):
    return masked_dict.freeze()
