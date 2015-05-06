import imp
from dogebuild.adapters.pip import PipAdapter
from dogebuild.loaders.plugin_loader import PluginLoader


class Doge:
    def __init__(self):
        self.plugins = []
        self.contrib_name = 'dogebuildcontrib'
        self.pip = PipAdapter()

    def use_plugin(self, plugin_name):
        plugin_full_name = self.contrib_name + '.' + plugin_name

        if not self.check_plugin_installed(plugin_full_name):
            self.pip.install(plugin_full_name)  # ???

        file, path, description = imp.find_module(self.contrib_name)
        imp.load_module(self.contrib_name, file, path, description)

        file, path, description = imp.find_module(plugin_full_name)
        plugin_module = imp.load_module(plugin_full_name, file, path, description)

        plugin = plugin_module





        self.plugins.append(plugin)
        return plugin

    def build(self):
        for p in self.plugins:
            p.build()

    def check_plugin_installed(self, plugin_name):
        try:
            plugin_info = imp.find_module(plugin_name)
            return True
        except ImportError:
            return False

if __name__ == 'main':
    Doge().use_plugin('pip')

