#!/usr/bin/env python3
""" Task 0: Basic Caching"""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """
    A class imherited from BaseCaching class
    """
    def __init__(self):
        """
        Initialization of child class
        """
        super().__init__()

    def put(self, key, item):
        """
        assign to the dictionary self.cache_data the item value for the key

        If key or item is None, this method should not do anything.
        """
        if key is None or item is None:
            pass
        else:
            self.cache_data[key] = item

    def get(self, key):
        """
        Must return the value in self.cache_data linked to key.

        If key is None or if the key doesn’t exist in self.cache_data,
        return None
        """
        if key is None or key not in self.cache_data:
            return None
        else:
            return self.cache_data.get(key)
