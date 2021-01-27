import sys

from pkg_resources import VersionConflict, require
from setuptools import setup, Extension

try:
    require('setuptools>=60.5')
except VersionConflict:
    print('Error: version of setuptools is too old (<60.5)!')
    sys.exit(1)

if __name__ == '__main__':
    ext_modules = [
        Extension(
            'fastapi_project_template.extmod',
            ['lib/extmod.c', ],
            include_dirs=['lib'],
            py_limited_api=True
        )
    ]

    setup(use_pyscaffold=True, ext_modules=ext_modules)
