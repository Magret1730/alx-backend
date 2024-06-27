#!/usr/bin/python3
""" Task 3: Least Recently Used """
BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """ Least Recently Used cache """
    def __init__(self):
        """
        Child class initialization
        """
        super().__init__()
        self.accessed_order = []

    def put(self, key, item):
        """ Add an item to the cache """
        if key is None or item is None:
            return

        # Check if the cache is full
        if len(self.cache_data) >= self.MAX_ITEMS:
            # Find the least recently used key
            lru_key = self.accessed_order.pop(0)
            del self.cache_data[lru_key]
            print(f"DISCARD: {lru_key}")

        # Add or update the item
        self.cache_data[key] = item
        # Update access order
        if key in self.accessed_order:
            self.accessed_order.remove(key)
        self.accessed_order.append(key)

    def get(self, key):
        """ Get an item from the cache """
        if key is None or key not in self.cache_data:
            return None

        # Update access order
        self.accessed_order.remove(key)
        self.accessed_order.append(key)

        return self.cache_data[key]
