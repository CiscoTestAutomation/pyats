Makefile
  - Removed fresh cloning of cisco-distutils during 'make develop' step, instead
    installing package from pyats-pypi. If already cloned, simply git pull and
    re-make. Similar functionality for 'make undevelop'