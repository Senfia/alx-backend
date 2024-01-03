#!/usr/bin/env python3
'''Basic caching.
'''
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    '''Allow for storage and ritrival of items from a dictionary.
    '''
    def put(self, key, item):
        '''Adds an item in the cache.
        '''
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        '''Fetches an item based on a specific key.
        '''
        return self.cache_data.get(key, None)
