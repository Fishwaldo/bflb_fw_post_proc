# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
# [GCC 9.4.0]
# Embedded file name: cklink/__init__.py
__version__ = '0.0.1'
__title__ = 'pycklink'
__author__ = 'tanjiaxi'
__author_email__ = 'jxtan@bouffalolab.com'
__copyright__ = 'Copyright 2021 Bouffalo Lab'
__license__ = 'MIT'
__url__ = 'http://pypi.org/project/pycklink/'
__description__ = 'Python interface for CKLink.'
__long_description__ = "This module provides a Python implementation of the\nCKLink SDK by leveraging the SDK's DLL.\n"
from .cklink import *
from .structs import *
from .errors import *