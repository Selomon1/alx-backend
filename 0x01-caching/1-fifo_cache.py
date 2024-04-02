#!/usr/bin/python3
"""
FIFO caching module
"""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFOCache class """

    def __init__(self):
        """ Initialize FIFOCache """
        super().__init__()
        self.queue = []

    def put(self, key, item):
        """ Add an item in the cache """
        if key is not None and item is not None:
            self.cache_data[key] = item
            self.queue.append(key)
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                first_key = self.queue.pop(0)
                del self.cache_data[first_key]
                print("DISCARD:", first_key)

    def get(self, key):
        """ Get an item by key """
        if key is not None or key in self.cache_data:
            return self.cache_data[key]
        return None
