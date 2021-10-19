# -*- coding: utf-8 -*-

"""
elastic_panel
~~~~~~~~~~~~~~

:copyright: (c) 2014 by Benoit Chabord
:license: See LICENSE for more details.

"""

import importlib.metadata as ilm

try:
    __version__ = ilm.version('django-elasticsearch-debug-toolbar')
except ilm.PackageNotFoundError:
    __version__ = "unknown"

__title__ = "elastic_panel"
__author__ = "Benoit Chabord"
__copyright__ = "Copyright 2014 Benoit Chabord"

VERSION = __version__
