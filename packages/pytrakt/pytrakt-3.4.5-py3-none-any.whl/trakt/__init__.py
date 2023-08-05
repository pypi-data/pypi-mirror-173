# -*- coding: utf-8 -*-
"""A wrapper for the Trakt.tv REST API"""
try:
    from trakt.core import *  # NOQA
except ImportError:
    pass

version_info = (3, 4, 5)
__author__ = 'Jon Nappi, Elan Ruusamäe'
__version__ = '.'.join([str(i) for i in version_info])
