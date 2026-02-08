import sys
from importlib.metadata import PackageNotFoundError, version

from setuptools import Extension, setup
from setuptools_rust import Binding, RustExtension

try:
    if int(version('setuptools').split('.')[0]) < 78:
        raise ValueError
except (PackageNotFoundError, ValueError):
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
