#!/usr/bin/python3
"""
LFUCache module
"""

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFUCache class that inherits from BaseCaching """

    def __init__(self):
        """ Initializes the LFUCache instance """
        super().__init__()
        self.usage = []
        self.ref_count = {}

    def put(self, key, item):
        """ Add an item in the cache """
        if key is None or item is None:
            return


        if len(self.cache_data) >= BaseCaching.MAX_ITEMS and \
                key not in self.cache_data:
            lfu_keys = [k for k, v in self.ref_count.items() if v == min(self.ref_count.values())]
            if len(lfu_keys) > 1:
                lfu_key = {k: self.usage.index(k) for k in lfu_keys}
                discard = min(lfu_key, key=lfu_key.get)
            else:
                discard = lfu_keys[0]

            print(f"DISCARD: {discard}")
            del self.cache_data[discard]
            del self.usage[self.usage.index(discard)]
            del self.ref_count[discard]

        if key in self.ref_count:
            self.ref_count[key] += 1
        else:
            self.ref_count[key] = 1

        if key in self.usage:
            del self.usage[self.usage.index(key)]
        self.usage.append(key)
        self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key """
        if key in self.cache_data:
            self.usage.remove(key)
            self.usage.append(key)
            self.ref_count[key] = self.ref_count.get(key, 0) + 1
            return self.cache_data[key]
        return None
