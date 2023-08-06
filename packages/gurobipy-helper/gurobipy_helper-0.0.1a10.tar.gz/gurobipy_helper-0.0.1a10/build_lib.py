import os
import platform
import site
from setuptools import Extension
from Cython.Build import cythonize


def build(setup_kwargs):
    """Called by poetry, the args are added to the kwargs for setup."""
    library_dirs = [
        os.path.join(r, 'gurobipy', '.libs') for r in site.getsitepackages()
    ]

    if platform.system() == 'Windows':
        library_dirs.append('D:\\a\\gurobipy_helper\\gurobipy_helper\\libs')

    extensions = [Extension(
        name='c_gurobipy_helper',
        sources=['src/c_gurobipy_helper.pyx'],
        libraries=['gurobi95'],
        library_dirs=library_dirs,
    ), Extension('gurobipy_helper', ['src/gurobipy_helper/__init__.py'])]

    setup_kwargs.update(dict(
        ext_modules=cythonize(extensions, language_level='3'),
        zip_safe=False,
    ))
