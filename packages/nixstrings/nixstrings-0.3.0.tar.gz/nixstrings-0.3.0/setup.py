import os
from setuptools import Extension, setup

try:
    from Cython.Build import cythonize
except ImportError:
    cythonize = None

extensions = [
    Extension(
        name="nixstrings",
        sources=[
            "nixstrings.pyx",
        ],
    )
]
if cythonize:
    extensions = cythonize(extensions, compiler_directives={'language_level' : "3"},)

setup(ext_modules=extensions)
