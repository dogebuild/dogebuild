How to create dogebuild plugin
=====

## Naming conventions

`dogebuild-{{plugin_name}}` as name for pip ("-" is better than "_" in name)

`dogebuild_{{plugin_name}}` as package name


## Plugin class

Inherit your class from `dogebuild.plugin.interfaces.Plugin` class and override all methods.

Method `get_active_tasks()` should return array of tasks selected as active.
 
Task object `dogebuild.plugin.interfaces.Task` has method `run()` in which 



## Entry point

You should create entry point so dogebuild can load your plugin. 

define method `get()` with no arguments in `dogebuild_{{plugin_name}}.loader` module which returns instance of class.    


