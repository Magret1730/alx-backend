#!/usr/bin/python3
""" Task 1 """
BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """ Child class of BaseCaching using FIFO algorithm"""
    def __init__(self):
        """
        Initialization of child class
        """
        super().__init__()

    def put(self, key, item):
        """
        assign to the dictionary self.cache_data the item value for the key
        Implement the FIFO algorithm

        If key or item is None, this method should not do anything.
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            first_key = next(iter(self.cache_data))
            self.cache_data.pop(first_key)
            print(f"DISCARD: {first_key}")

    def get(self, key):
        """
        Must return the value in self.cache_data linked to key.

        If key is None or if the key doesn’t exist in self.cache_data,
        return None
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
