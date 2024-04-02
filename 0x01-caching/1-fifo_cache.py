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
            if len(self.cache_data) >= self.MAX_ITEMS:
                discarded_key = self.queue.pop(0)
                del self.cache_data[discarded_key]
                print("DISCARD:", discarded_key)
            self.cache_data[key] = item
            self.queue.append(key)

    def get(self, key):
        """ Get an item by key """
        if key is not None:
            return self.cache-data.get(key)
        return None
