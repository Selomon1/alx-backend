#!/usr/bin/python3
"""
LRU caching module
"""

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """ LRUCache class """

    def __init__(self):
        """ initialize LRUCache """
        super().__init__()
        self.queue = []

    def put(self, key, item):
        """ Add an item in the cache """
        if key is not None and item is not None:
            if len(self.cache_data) >= self.MAX_ITEMS and key not in self.cache_data:
                discarded_key = self.queue.pop(0)
                del self.cache_data[discarded_key]
                print("DISCARD:", discarded_key)
            if key in self.cache_data:
                self.queue.remove(key)
            self.queue.append(key)
            self.cache_data[key] = item
        else:
            return

    def get(self, key):
        """ Get an item by key """
        if key is not None and key in self.cache_data:
            self.queue.remove(key)
            self.queue.append(key)
            return self.cache_data[key]
        return None
