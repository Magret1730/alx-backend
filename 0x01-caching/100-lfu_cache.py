#!/usr/bin/python3
"""
LFU Cache implementation inheriting from BaseCaching
"""
BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """
    LFUCache class that inherits from BaseCaching
    """
    def __init__(self):
        """
        Initialize the LFU Cache instance
        """
        super().__init__()
        self.frequency = {}  # To track the frequency of each item
        self.access_order = {}  # To track the order of access

    def put(self, key, item):
        """
        Add an item to the cache using LFU algorithm
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.frequency[key] += 1
            self.access_order[key] = len(self.access_order)
        else:
            if len(self.cache_data) >= self.MAX_ITEMS:
                lfu_key = self._get_lfu_key()
                print(f"DISCARD: {lfu_key}")
                del self.cache_data[lfu_key]
                del self.frequency[lfu_key]
                del self.access_order[lfu_key]

            self.cache_data[key] = item
            self.frequency[key] = 1
            self.access_order[key] = len(self.access_order)

    def get(self, key):
        """
        Retrieve an item from the cache
        """
        if key is None or key not in self.cache_data:
            return None

        self.frequency[key] += 1
        self.access_order[key] = len(self.access_order)

        return self.cache_data[key]

    def _get_lfu_key(self):
        """
        Get the key of the least frequently used item.
        If multiple keys have the same frequency, return the least recently
        used one.
        """
        lfu_key = min(self.frequency,
                      key=lambda k: (self.frequency[k], self.access_order[k]))
        return lfu_key
