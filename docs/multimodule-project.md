# Multimodule project

Each module must be in his own directory.

For example. Project with two library `library-A` and `library-B` and `main` module will have following structure:

```
project/
  library-A/
    dogefile.py
    ... library A files ...
  library-B/
    dogefile.py
    ... library B files ...
  main/
    dogefile.py
    ... main module files ...
  dogefile.py
```

A project dogefile must contain function `modules` with all module directories as arguments:

```python
from dogebuild import modules

modules(
    'library-A',
    'library-B',
    'main',
)
```
