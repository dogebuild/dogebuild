# Dogefile.py format

## Module dogefile

```python
# import part
from pathlib import Path

from dogebuild import make_mode, task, lifecycle
from dogebuild_demo_plugin import DemoPlugin

# Lifecycle
lifecycle({})
# Or make_mode()

# Variables part

sources = Path().glog('**/*.cpp')

# Plugin initializing part
DemoPlugin(sources)

# File task part 

@task(phase='build')
def make_build_dir():
    artifacts = do_some_stuff_(sources)
    return 0, {'artifacts': artifacts}
```

There is no strict order in parts except that `lifecycle` or `make_mode` must be called before any tasks or plugins
because they are part of initialization of dogefile.  
