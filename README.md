# dogebuild
Dogebuild main program

This version (0.1) is pre^10 alpha. You can use it, but everything can change. 


## Create plugin
To create plugin you should create class with method build 

```
class MyPlugin:
    def build():
        print("hi!")
```

To give dogebuild access to your class you should create file "Plugin.py" 
with function "get" returning instance of your plugin class:

```
def get():
    return MyPlugin()
```
