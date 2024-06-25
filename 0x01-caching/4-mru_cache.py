#!/usr/bin/python3
"""
MRU Cache implementation inheriting from BaseCaching
"""
BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    """
    MRUCache class that inherits from BaseCaching
    """
    def __init__(self):
        """
        Initialize the MRU Cache instance
        """
        super().__init__()
        self.mru_list = []  # To track MRU order

    def put(self, key, item):
        """
        Add an item to the cache using MRU algorithm
        """
        if key is None or item is None:
            return

        # If cache is full, remove the most recently used item (MRU)
        if len(self.cache_data) >= self.MAX_ITEMS:
            mru_key = self.mru_list.pop()  # Remove from MRU list
            print(f"DISCARD: {mru_key}")
            del self.cache_data[mru_key]

        # Add the new item
        self.cache_data[key] = item
        self.mru_list.append(key)  # Add to MRU list

    def get(self, key):
        """
        Retrieve an item from the cache
        """
        if key is None or key not in self.cache_data:
            return None

        # Move the accessed item to the end of the MRU list
        self.mru_list.remove(key)
        self.mru_list.append(key)

        return self.cache_data[key]
