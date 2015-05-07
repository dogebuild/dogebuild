import imp
from dogebuild.adapters.pip import PipAdapter
from dogebuild.loaders.plugin_loader import PluginLoader
from dogebuild.plugin.interfaces import *


class Doge:
    def __init__(self):
        self.plugins = []
        self.contrib_name = 'dogebuildcontrib'
        self.pip = PipAdapter()

    def use_plugin(self, plugin_name):
        plugin_full_name = self.contrib_name + '.' + plugin_name

        if not self.check_plugin_installed(plugin_full_name):
            self.pip.install(plugin_full_name)  # ???

        file, path, desc = self.find_dotted_module(plugin_full_name + '.loader')
        loader_file = imp.load_module('loader', file, path, desc)

        plugin = loader_file.get()
        self.plugins.append(plugin)
        return plugin

    def build(self):
        tasks = []
        for p in self.plugins:
            tasks.extend(p.get_active_tasks())

        for t in tasks:
            t.run()

    def find_dotted_module(self, module_name, path=None):
        for x in module_name.split('.'):
            print('1', path, x)
            if path is not None:
                path = [path]
            file, path, description = imp.find_module(x, path)
            print('2', file, path, description)
        return file, path, description

    def check_plugin_installed(self, plugin_full_name):
        try:
            self.find_dotted_module(plugin_full_name)
            return True
        except ImportError:
            return False





