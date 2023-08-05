# Build Instructions

Increment the version number in `pyproject.toml`

run the command:
```python3 -m build --sdist shieldpython/```

or
```python3 -m build --wheel```

build files will be in `dist` directory

To install the resulting files on the local system, use:

```python3 -m pip install dist/<filename>.whl```
