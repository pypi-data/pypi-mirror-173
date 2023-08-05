from ast import Import
import re
import os
from setuptools import setup, find_packages

try:
    from pypandoc import convert_file
    def read_md(fname):
        return convert_file(os.path.join(os.path.dirname(__file__), fname), 'rst')
except ModuleNotFoundError:
    def read_md(fname):
        return open(os.path.join(os.path.dirname(__file__), fname)).read()

VERSIONFILE = "version/__init__.py"
ver_file = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, ver_file, re.M)

if mo:
    version = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setup(name="dinkum",
      version=version,
      description="Some functions for interacting with [destmn]bd files in Python. Intent is to return a usable data object.",
      author="pye, Sean",
      author_email="",
      url="https://ceotr.ocean.dal.ca/",
      packages=find_packages(exclude=['tests']),
      python_requires='>=3.8',
      long_description=read_md('README.md'),
      license = "GNU General Public License v3 (GPLv3)",
      install_requires=[
          "bitstring",
          "numpy",
          "pandas",
          "dbdreader"
      ],
      zip_safe=True
      )
