# first-python-package

This package is awesome.

## Installation

```shell
python -m pip install first-python-package
```

## Notes
1. Use `pyproject-build` for building your project
   - use newer `pyproject.toml` for specification
   - you can also use `setup.py` if other options not availble
   - `pyproject-build` creates source distribution pkg and binary distirbution pkg
   - add info about required build system
2. Package Metadata
   - use `setup.cfg` to specify that
      - name
      - version
      - url
      - author
      - author_email
      - description
      - license
      - long_description (this is best based on README.md)
3. Split directory structure into `src` and `test` - such separation is important for packaging. You want to run your tests against packaged code, not raw source code.
4. In `MANIFEST.in` specify non-Python files that should be included.

### Adding Cython to your project
1. Find code for optimization and port it to Cython (.pyx)
2. Add Cython as a build requirement in `pyproject.toml` -> if you want to work with Cython you need a package
3. Create `setup.py` where you specify Cython files.
