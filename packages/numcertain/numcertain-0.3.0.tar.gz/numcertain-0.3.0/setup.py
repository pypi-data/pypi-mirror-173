from sysconfig import get_paths

from numpy import get_include
from numpy.distutils.core import Extension, setup

INCLUDE_DIRS = [get_paths()["include"], get_include()]

EXT_MODULES = [
    Extension(
        name="numcertain._numcertain",
        sources=[
            "src/numcertain/numcertain.c",
            "src/numcertain/numpy.c",
            "src/numcertain/pytype.c",
            "src/numcertain/ctype.c",
        ],
        include_dirs=INCLUDE_DIRS,
    ),
]

setup(ext_modules=EXT_MODULES)
