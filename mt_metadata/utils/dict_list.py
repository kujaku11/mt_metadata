# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 11:08:25 2022

@author: jpeacock
"""
# =============================================================================
# Imports
# =============================================================================
from collections import OrderedDict

# =============================================================================


class ListDict:
    def __init__(self):

        self._home = OrderedDict()

    def __str__(self):
        return "Keys In Order: " + ", ".join(list(self._home.keys()))

    def __repr__(self):
        return self._home.__repr__()

    def _get_key_from_index(self, index):
        try:
            return next(
                key for ii, key in enumerate(self._home) if ii == index
            )

        except StopIteration:
            raise KeyError(f"Could not find {index}")

    def __getitem__(self, value):

        if isinstance(value, str):
            try:
                return self._home[value]
            except KeyError:
                raise KeyError(f"Could not find {value}")

        elif isinstance(value, int):
            key = self._get_key_from_index(value)
            return self._home[key]

        else:
            raise TypeError("Index must be a string or integer value.")

    def __setitem__(self, index, value):

        if isinstance(index, str):
            self._home[index] = value

        elif isinstance(index, int):
            try:
                key = self._get_key_from_index(index)
            except KeyError:

                if hasattr(value, "id"):
                    key = value.id
                elif hasattr(value, "component"):
                    key = value.component
                else:
                    key = str(index)

            self._home[key] = value

    def __iter__(self):
        return self._home.__iter__()

    def keys(self):
        return list(self._home.keys())

    def values(self):
        return list(self._home.values())

    def items(self):
        return self._home.items()
