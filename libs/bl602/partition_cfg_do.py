# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
# [GCC 9.4.0]
# Embedded file name: libs/bl602/partition_cfg_do.py
import binascii
from libs import bflb_utils
partition1_addr = 'E000'
partition2_addr = 'F000'
fireware_name = 'FW'
mfg_name = 'mfg'
partition_magic_code = 1111904340
bootheader_magic_code = 1111903824

def check_pt_data(data):
    """
    partition data 0~15 is partition table config
    parrition data 12~15 is partition table config crc32
    partition data 16~16+36 is partition entry 1, 16+36~16+72 is partition entry 2 ...
    partition data last 4 byte is partition entry data crc32
    """
    if partition_magic_code != bflb_utils.bytearray_to_int(data[0:4]):
        bflb_utils.printf('partition bin magic check fail ', binascii.hexlify(data[0:4]))
        return (False, 0, 0)
    table_count = bflb_utils.bytearray_to_int(data[6:7]) + (bflb_utils.bytearray_to_int(data[7:8]) << 8)
    if table_count > 16:
        bflb_utils.printf('error, pt enter size > 16')
        return (False, 0, 0)
    crcarray = bflb_utils.get_crc32_bytearray(data[:12])
    if data[12:16] != crcarray:
        bflb_utils.printf('pt table crc fail ', binascii.hexlify(crcarray))
        return (False, 0, 0)
    crcarray = bflb_utils.get_crc32_bytearray(data[16:16 + 36 * table_count])
    if data[16 + 36 * table_count:16 + 36 * table_count + 4] != crcarray:
        bflb_utils.printf('pt entries crc fail ', binascii.hexlify(crcarray))
        return (False, 0, 0)
    age = bflb_utils.bytearray_to_int(data[8:9]) + (bflb_utils.bytearray_to_int(data[9:10]) << 8) + (bflb_utils.bytearray_to_int(data[10:11]) << 16) + (bflb_utils.bytearray_to_int(data[11:12]) << 24)
    return (True, table_count, age)


def parse_pt_data(data):
    entry_type = []
    entry_addr = []
    entry_len = []
    if partition_magic_code != bflb_utils.bytearray_to_int(data[0:4]):
        bflb_utils.printf('partition bin magic check fail ', binascii.hexlify(data[0:4]))
        return (False, 0, 0)
    table_count = bflb_utils.bytearray_to_int(data[6:7]) + (bflb_utils.bytearray_to_int(data[7:8]) << 8)
    if table_count > 16:
        bflb_utils.printf('error, pt enter size > 16')
        return (False, 0, 0)
    crcarray = bflb_utils.get_crc32_bytearray(data[:12])
    if data[12:16] != crcarray:
        bflb_utils.printf('pt table crc fail ', binascii.hexlify(crcarray))
        return (False, 0, 0)
    crcarray = bflb_utils.get_crc32_bytearray(data[16:16 + 36 * table_count])
    if data[16 + 36 * table_count:16 + 36 * table_count + 4] != crcarray:
        bflb_utils.printf('pt entries crc fail ', binascii.hexlify(crcarray))
        return (False, 0, 0)
    ptdata = data[16:]
    for i in range(table_count):
        if fireware_name == ptdata[i * 36 + 3:i * 36 + 3 + len(fireware_name)].decode(encoding='utf-8'):
            addr_start = 0
            if bflb_utils.bytearray_to_int(ptdata[i * 36 + 2:i * 36 + 3]) != 0:
                addr_start = i * 36 + 16
            else:
                addr_start = i * 36 + 12
            fwaddr = bflb_utils.bytearray_to_int(ptdata[addr_start + 0:addr_start + 1]) + (bflb_utils.bytearray_to_int(ptdata[addr_start + 1:addr_start + 2]) << 8) + (bflb_utils.bytearray_to_int(ptdata[addr_start + 2:addr_start + 3]) << 16) + (bflb_utils.bytearray_to_int(ptdata[addr_start + 3:addr_start + 4]) << 24)
            maxlen = bflb_utils.bytearray_to_int(ptdata[addr_start + 0 + 8:addr_start + 1 + 8]) + (bflb_utils.bytearray_to_int(ptdata[addr_start + 1 + 8:addr_start + 2 + 8]) << 8) + (bflb_utils.bytearray_to_int(ptdata[addr_start + 2 + 8:addr_start + 3 + 8]) << 16) + (bflb_utils.bytearray_to_int(ptdata[addr_start + 3 + 8:addr_start + 4 + 8]) << 24)
            entry_type.append(fireware_name)
            entry_addr.append(fwaddr)
            entry_len.append(maxlen)
        if mfg_name == ptdata[i * 36 + 3:i * 36 + 3 + len(mfg_name)].decode(encoding='utf-8'):
            addr_start = 0
            if bflb_utils.bytearray_to_int(ptdata[i * 36 + 2:i * 36 + 3]) != 0:
                addr_start = i * 36 + 16
            else:
                addr_start = i * 36 + 12
            fwaddr = bflb_utils.bytearray_to_int(ptdata[addr_start + 0:addr_start + 1]) + (bflb_utils.bytearray_to_int(ptdata[addr_start + 1:addr_start + 2]) << 8) + (bflb_utils.bytearray_to_int(ptdata[addr_start + 2:addr_start + 3]) << 16) + (bflb_utils.bytearray_to_int(ptdata[addr_start + 3:addr_start + 4]) << 24)
            maxlen = bflb_utils.bytearray_to_int(ptdata[addr_start + 0 + 8:addr_start + 1 + 8]) + (bflb_utils.bytearray_to_int(ptdata[addr_start + 1 + 8:addr_start + 2 + 8]) << 8) + (bflb_utils.bytearray_to_int(ptdata[addr_start + 2 + 8:addr_start + 3 + 8]) << 16) + (bflb_utils.bytearray_to_int(ptdata[addr_start + 3 + 8:addr_start + 4 + 8]) << 24)
            entry_type.append(mfg_name)
            entry_addr.append(fwaddr)
            entry_len.append(maxlen)

    return (
     entry_type, entry_addr, entry_len)