# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
# [GCC 9.4.0]
# Embedded file name: libs/bl702l/chiptype_patch.py


def img_load_create_predata_before_run_img():
    pre_data = bytearray(12)
    pre_data[0] = 80
    pre_data[1] = 0
    pre_data[2] = 8
    pre_data[3] = 0
    pre_data[4] = 0
    pre_data[5] = 241
    pre_data[6] = 0
    pre_data[7] = 64
    pre_data[8] = 69
    pre_data[9] = 72
    pre_data[10] = 66
    pre_data[11] = 78
    pre_data2 = bytearray(12)
    pre_data2[0] = 80
    pre_data2[1] = 0
    pre_data2[2] = 8
    pre_data2[3] = 0
    pre_data2[4] = 4
    pre_data2[5] = 241
    pre_data2[6] = 0
    pre_data2[7] = 64
    pre_data2[8] = 0
    pre_data2[9] = 0
    pre_data2[10] = 1
    pre_data2[11] = 34
    pre_data3 = bytearray(12)
    pre_data3[0] = 80
    pre_data3[1] = 0
    pre_data3[2] = 8
    pre_data3[3] = 0
    pre_data3[4] = 24
    pre_data3[5] = 0
    pre_data3[6] = 0
    pre_data3[7] = 64
    pre_data3[8] = 0
    pre_data3[9] = 0
    pre_data3[10] = 0
    pre_data3[11] = 0
    pre_data4 = bytearray(12)
    pre_data4[0] = 80
    pre_data4[1] = 0
    pre_data4[2] = 8
    pre_data4[3] = 0
    pre_data4[4] = 24
    pre_data4[5] = 0
    pre_data4[6] = 0
    pre_data4[7] = 64
    pre_data4[8] = 2
    pre_data4[9] = 0
    pre_data4[10] = 0
    pre_data4[11] = 0
    return pre_data + pre_data2 + pre_data3 + pre_data4