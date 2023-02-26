# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
# [GCC 9.4.0]
# Embedded file name: cklink/errors.py


class CKLinkException(Exception):
    __doc__ = 'Generic CK-Link exception.'

    def __init__(self, message):
        super(CKLinkException, self).__init__(message)
        self.message = message