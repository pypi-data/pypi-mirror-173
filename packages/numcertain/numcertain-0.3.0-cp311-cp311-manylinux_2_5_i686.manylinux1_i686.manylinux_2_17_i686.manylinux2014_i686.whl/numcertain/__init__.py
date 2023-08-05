from importlib.metadata import version

from ._numcertain import nominal, uncertain, uncertainty

__version__ = version("numcertain")

__all__ = ["__version__", "nominal", "uncertain", "uncertainty"]
