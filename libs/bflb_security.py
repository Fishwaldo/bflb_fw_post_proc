# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
# [GCC 9.4.0]
# Embedded file name: libs/bflb_security.py
import os, sys, binascii
from libs import bflb_utils
from libs.bflb_configobj import BFConfigParser

def load_sec_eng_key_slot(cmd, cfgfile, write_callback, ack_callback):
    cfg = BFConfigParser()
    cfg.read(cfgfile)
    aeskey = bflb_utils.hexstr_to_bytearray(cfg.get('Img_Cfg', 'aes_key_org'))
    aeslen = len(aeskey)
    bflb_utils.printf('load sec eng key: ')
    tmp = bflb_utils.int_to_2bytearray_l(aeslen * 2)
    cmd_id = bflb_utils.hexstr_to_bytearray(cmd)
    data = cmd_id + bytearray(1) + tmp
    i = 0
    while i < aeslen:
        start_addr = bflb_utils.int_to_4bytearray_l(1073770672 + i)
        write_data = aeskey[i:i + 4]
        data += start_addr + write_data
        i += 4

    write_callback(data)
    res = ack_callback(dmy_data=False)
    if res.startswith('OK') is False:
        bflb_utils.printf('load sec eng key fail!')
        return False
    tmp = bflb_utils.int_to_2bytearray_l(8)
    start_addr = bflb_utils.int_to_4bytearray_l(1074200800)
    write_data = bflb_utils.int_to_4bytearray_l(805318656)
    data = cmd_id + bytearray(1) + tmp + start_addr + write_data
    write_callback(data)
    res = ack_callback(dmy_data=False)
    if res.startswith('OK') is False:
        bflb_utils.printf('load rd/wr lock key slot fail!')
        return False
    return True