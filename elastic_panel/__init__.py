# -*- coding: utf-8 -*-

"""
elastic_panel
~~~~~~~~~~~~~~

:copyright: (c) 2014 by Benoit Chabord
:license: See LICENSE for more details.

"""

import pkg_resources

try:
    __version__ = pkg_resources.get_distribution("django-elasticsearch-debug-toolbar").version
except Exception:
    __version__ = "unknown"


__title__ = "elastic_panel"
__author__ = "Benoit Chabord"
__copyright__ = "Copyright 2014 Benoit Chabord"

VERSION = __version__
