import functools as _functools

from . import compat as _compat


_functools.cached_property = _compat.functools.cached_property
_functools.singledispatchmethod = _compat.functools.singledispatchmethod


import importlib as _importlib

from .namespace import *


__all__ = _importlib.import_module('.namespace', __name__).__all__
__doc__ = Server.__doc__
__license__ = 'GPL-3.0-only'
__version__ = Server.__version__
