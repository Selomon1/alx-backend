#!/usr/bin/python3
"""
MRU caching module
"""

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRUCache class """

    def __init__(self):
        """ Initialize MRUcache """
        super().__init__()
        self.mru_list = []

    def put(self, key, item):
        """ Add an item in the cache """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS and \
                    key not in self.cache_data:
                discarded_key = self.mru_list.pop()
                del self.cache_data[discarded_key]
                print("DISCARD:", discarded_key)
            self.cache_data[key] = item
            self.mru_list.append(key)
        else:
            return

    def get(self, key):
        """ Get an item by key """
        if key is not None and key in self.cache_data:
            self.mru_list.remove(key)
            self.mru_list.append(key)
            return self.cache_data[key]
        return None
