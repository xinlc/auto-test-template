""" local storage 工具

Usage example:
    # get the local storage
    storage = LocalStorage(driver)

    # set an item
    storage["mykey"] = 1234
    storage.set("mykey2", 5678)

    # get an item
    print(storage["mykey"])      # raises a KeyError if the key is missing
    print(storage.get("mykey"))  # returns None if the key is missing

    # delete an item
    storage.remove("mykey")

    # iterate items
    for key, value in storage.items():
      print("%s: %s" % (key, value))

    # delete items
    storage.clear()
"""

__author__ = 'Richard'
__version__ = '2021-07-10'


class LocalStorage:

    def __init__(self, driver):
        self.driver = driver

    def __len__(self):
        return self.driver.execute_script("return window.localStorage.length;")

    def items(self):
        return self.driver.execute_script( \
            "var ls = window.localStorage, items = {}; " \
            "for (var i = 0, k; i < ls.length; ++i) " \
            "  items[k = ls.key(i)] = ls.getItem(k); " \
            "return items; ")

    def keys(self):
        return self.driver.execute_script( \
            "var ls = window.localStorage, keys = []; " \
            "for (var i = 0; i < ls.length; ++i) " \
            "  keys[i] = ls.key(i); " \
            "return keys; ")

    def get(self, key):
        return self.driver.execute_script("return window.localStorage.getItem(arguments[0]);", key)

    def set(self, key, value):
        self.driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", key, value)

    def has(self, key):
        return key in self.keys()

    def remove(self, key):
        self.driver.execute_script("window.localStorage.removeItem(arguments[0]);", key)

    def clear(self):
        self.driver.execute_script("window.localStorage.clear();")

    def __getitem__(self, key):
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, key):
        return key in self.keys()

    def __iter__(self):
        return self.items().__iter__()

    def __repr__(self):
        return self.items().__str__()
