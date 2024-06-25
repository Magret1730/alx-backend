#!/usr/bin/python3
""" TAsk 2 """
BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """ Child class of BaseCaching using LIFO algorithm of caching"""

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
            return

        # Check if the cache is full
        if len(self.cache_data) >= self.MAX_ITEMS:
            # Get the last item (LIFO eviction)
            last_key = list(self.cache_data.keys())[-1]
            del self.cache_data[last_key]
            print(f"DISCARD: {last_key}")

        # Add the new item
        self.cache_data[key] = item

    def get(self, key):
        """
        Must return the value in self.cache_data linked to key.

        If key is None or if the key doesn’t exist in self.cache_data,
        return None
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
