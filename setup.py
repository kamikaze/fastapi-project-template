import sys

from pkg_resources import VersionConflict, require
from setuptools import setup, Extension
from setuptools_rust import Binding, RustExtension

try:
    require('setuptools>=78.0')
except VersionConflict:
    print('Error: version of setuptools is too old (<78.0)!')
    sys.exit(1)

if __name__ == '__main__':
    setup(
        # packages=find_packages(where='src'),
        # package_dir={'': 'src'},
        ext_modules=[
            Extension(
                'fastapi_project_template._cmod',
                ['clib/lib.c'],
                include_dirs=['clib'],
                py_limited_api=True
            ),
        ],
        rust_extensions=[
            RustExtension(
                'fastapi_project_template._rustmod',
                'rustlib/Cargo.toml',
                binding=Binding.PyO3
            ),
        ],
    )
