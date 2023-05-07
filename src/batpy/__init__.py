# -*- coding: UTF-8 -*-
"""Package to interact with BatPaC
"""
import logging
from importlib.metadata import version
from logging import NullHandler

__version__ = version("batpy")

logging.getLogger(__name__).addHandler(NullHandler())
