import imp
from dogebuild.adapters.pip import PipAdapter


class Doge:
    def __init__(self):
        self.plugins = []
        self.contrib_name = 'dogebuild'
        self.pip = PipAdapter()

    def use_plugin(self, plugin_name, **kwargs):
        plugin_full_name = self.contrib_name + '-' + plugin_name
        plugin_package = self.contrib_name + '_' + plugin_name

        if not self._check_plugin_installed(plugin_package):
            self.pip.install(plugin_full_name)  # ???

        file, path, desc = self._find_dotted_module(plugin_package + '.loader')
        loader_file = imp.load_module('loader', file, path, desc)

        plugin = loader_file.get(**kwargs)
        self.plugins.append(plugin)
        return plugin

    def build(self):
        tasks = []
        for p in self.plugins:
            tasks.extend(p.get_active_tasks())

        for t in tasks:
            t.run()

    def _find_dotted_module(self, module_name, path=None):
        for x in module_name.split('.'):
            if path is not None:
                path = [path]
            file, path, description = imp.find_module(x, path)
        return file, path, description

    def _check_plugin_installed(self, plugin_full_name):
        try:
            self._find_dotted_module(plugin_full_name)
            return True
        except ImportError:
            return False





