__author__ = 'kir'

import site
import pip
import imp


class Doge:
    def __init__(self):
        self.plugins = []
        self.plugin_root_name = "dogebuild"

    def use_plugin(self, plugin_name):
        key = self.plugin_root_name + "." + plugin_name
        key_dir = key.replace(".", "/")

        file, path, description = imp.find_module(key_dir)
        imp.load_package(key, path)
        plugin = imp.load_source(key, path + "/Plugin.py").get()
        self.plugins.append(plugin)
        return plugin

    def build(self):
        for p in self.plugins:
            p.build()
