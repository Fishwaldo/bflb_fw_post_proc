# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
# [GCC 9.4.0]
# Embedded file name: libs/bflb_ecdh.py
import binascii
from ecdsa import ECDH, NIST256p
from libs import bflb_utils

class BflbEcdh(object):

    def __init__(self, curve=NIST256p):
        self.ecdh = ECDH(curve)
        self.local_public_key = None
        self.sharedsecret = ''

    def create_public_key(self):
        self.ecdh.generate_private_key()
        self.local_public_key = self.ecdh.get_public_key()
        ret = binascii.hexlify(self.local_public_key.to_string()).decode('utf-8')
        bflb_utils.printf('local public key:')
        bflb_utils.printf(ret)
        return ret

    def create_shared_key(self, peer_pk):
        self.ecdh.load_received_public_key_bytes(binascii.unhexlify(peer_pk))
        self.sharedsecret = self.ecdh.generate_sharedsecret_bytes()
        ret = binascii.hexlify(self.sharedsecret).decode('utf-8')
        bflb_utils.printf('secret key:')
        bflb_utils.printf(ret)
        return ret