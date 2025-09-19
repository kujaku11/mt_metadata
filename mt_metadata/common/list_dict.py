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
    """
    Hack together an object that acts like a dictionary and list such that a
    user can get an item by index or key.

    This is the first attempt, seems to work, might think about inheriting
    an OrderedDict and overloading.

    """

    def __init__(self, values={}):
        self._home = OrderedDict(values)

    def __str__(self):
        lines = ["Contents:", "-" * 12]
        for k, v in self._home.items():
            lines.append(f"\t{k} = {v}")

        return "\n".join(lines)

    def __repr__(self):
        """
        Return a string representation that is consistent across Python versions.
        """
        if not self._home:
            return "ListDict({})"

        # Create a consistent representation using standard dict format
        items = []
        for key, value in self._home.items():
            # Use repr() for both key and value to handle proper quoting
            items.append(f"{repr(key)}: {repr(value)}")

        items_str = "{" + ", ".join(items) + "}"
        return f"ListDict({items_str})"

    def __eq__(self, other):
        return self._home.__eq__(other._home)

    def __len__(self):
        return self._home.__len__()

    def _get_key_from_index(self, index):
        try:
            return next(key for ii, key in enumerate(self._home) if ii == index)

        except StopIteration:
            raise KeyError(f"Could not find {index}")

    def _get_index_from_key(self, key):
        try:
            return next(index for index, k in enumerate(self._home) if k == key)

        except StopIteration:
            raise KeyError(f"Could not find {key}")

    def _get_key_from_object(self, obj):
        """
        Get the key from the metadata object

        :param obj: DESCRIPTION
        :type obj: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        if hasattr(obj, "id"):
            return obj.id
        elif hasattr(obj, "component"):
            return obj.component
        else:
            raise TypeError("could not identify an appropriate key from object")

    def __deepcopy__(self, memodict={}):
        """
        Need to skip copying the logger
        need to copy properties as well.

        :return: DESCRIPTION
        :rtype: TYPE

        """
        copied = type(self)()
        for key, value in self.items():
            if hasattr(value, "copy"):
                value = value.copy()
            copied[key] = value

        return copied

    def copy(self):
        """
        Copy object

        """

        return self.__deepcopy__()

    def _get_index_slice_from_slice(self, items, key_slice):
        """
        Get the slice index values from either an integer or key value

        :param items: DESCRIPTION
        :type items: TYPE
        :param key_slice: DESCRIPTION
        :type key_slice: TYPE
        :raises TypeError: DESCRIPTION
        :return: DESCRIPTION
        :rtype: TYPE

        """
        if key_slice.start is None or isinstance(key_slice.start, int):
            start = key_slice.start
        elif isinstance(key_slice.start, str):
            start = self._get_index_from_key(key_slice.start)
        else:
            raise TypeError("Slice start must be type int or str")

        if key_slice.stop is None or isinstance(key_slice.stop, int):
            stop = key_slice.stop
        elif isinstance(key_slice.stop, str):
            stop = self._get_index_from_key(key_slice.stop)
        else:
            raise TypeError("Slice stop must be type int or str")

        return slice(start, stop, key_slice.step)

    def __getitem__(self, value):
        if isinstance(value, str):
            try:
                return self._home[value]
            except KeyError:
                raise KeyError(f"Could not find {value}")

        elif isinstance(value, int):
            key = self._get_key_from_index(value)
            return self._home[key]

        elif isinstance(value, slice):
            return ListDict(
                list(self.items())[
                    self._get_index_slice_from_slice(self.items(), value)
                ]
            )

        else:
            raise TypeError("Index must be a string or integer value.")

    def __setitem__(self, index, value):
        if isinstance(index, str):
            self._home[index] = value

        elif isinstance(index, int):
            try:
                key = self._get_key_from_index(index)
            except KeyError:
                try:
                    key = self._get_key_from_object(value)
                except TypeError:
                    key = str(index)

            self._home[key] = value

        elif isinstance(index, slice):
            raise NotImplementedError(
                "Setting values from slice is not implemented yet"
            )

    def __iter__(self):
        return iter(self.values())

    def keys(self):
        return list(self._home.keys())

    def values(self):
        return list(self._home.values())

    def items(self):
        return self._home.items()

    def append(self, obj):
        """
        Append an object

        :param obj: DESCRIPTION
        :type obj: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        try:
            key = self._get_key_from_object(obj)
        except TypeError:
            key = str(len(self.keys()))

        self._home[key] = obj

    def remove(self, key):
        """
        remove an item based on key or index

        :param key: DESCRIPTION
        :type key: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        if isinstance(key, str):
            self._home.__delitem__(key)

        elif isinstance(key, int):
            key = self._get_key_from_index(key)
            self._home.__delitem__(key)
        elif key is None:
            try:
                self._home.__delitem__(key)
            except KeyError:
                raise (KeyError("Could not find None in keys."))

        else:
            raise TypeError("could not identify an appropriate key from object")

    def extend(self, other, skip_keys=[]):
        """
        extend the dictionary from another ListDict object

        :param other: DESCRIPTION
        :type other: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """
        if isinstance(skip_keys, str):
            skip_keys = [skip_keys]

        if isinstance(other, (ListDict, dict, OrderedDict)):
            for key, value in other.items():
                if key in skip_keys:
                    continue
                self._home[key] = value

        else:
            raise TypeError(f"Cannot extend from {type(other)}")

    def sort(self, inplace=True):
        """
        sort the dictionary keys into alphabetical order
        """

        od = OrderedDict()
        for key in sorted(self._home.keys()):
            od[key] = self._home[key]

        if inplace:
            self._home = od
        else:
            return od

    def update(self, other):
        """
        Update from another ListDict
        """

        if not isinstance(other, (ListDict, dict, OrderedDict)):
            raise TypeError(
                f"Cannot update from {type(other)}, must be a "
                "ListDict, dict, OrderedDict"
            )

        self._home.update(other)

    def pop(self, key):
        """
        pop item off of dictionary.  The key must be verbatim

        :param key: key of item to be popped off of dictionary
        :type key: string
        :return: item popped

        """

        if key in self.keys():
            return dict([self._home.popitem(key)])
        else:
            raise KeyError(f"{key} is not in ListDict keys.")

    def to_dict(self, single=False, nested=False, required=False) -> None:
        """ """
        return None
