# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
# [GCC 9.4.0]
# Embedded file name: libs/bl702l/flash_select_do.py
import os, csv, config as gol
from libs import bflb_utils
from libs.bflb_utils import app_path, conf_sign
from libs.bflb_configobj import BFConfigParser
from libs.bl702l.bootheader_cfg_keys import bootheader_cfg_keys as flash_cfg_keys

def get_suitable_file_name(cfg_dir, flash_id):
    conf_files = []
    for home, dirs, files in os.walk(cfg_dir):
        for filename in files:
            if filename.split('_')[-1] == flash_id + '.conf':
                conf_files.append(filename)

    if len(conf_files) > 1:
        bflb_utils.printf('Flash id duplicate and alternative is:')
        for i in range(len(conf_files)):
            tmp = conf_files[i].split('.')[0]
            bflb_utils.printf('%d:%s' % (i + 1, tmp))

        return conf_files[i]
    if len(conf_files) == 1:
        return conf_files[0]
    return ''


def update_flash_cfg_do(chipname, chiptype, flash_id, file=None, create=False, section=None):
    if conf_sign:
        cfg_dir = app_path + '/utils/flash/' + chipname + '/'
    else:
        cfg_dir = app_path + '/utils/flash/' + gol.flash_dict[chipname] + '/'
    conf_name = get_suitable_file_name(cfg_dir, flash_id)
    value_key = []
    if os.path.isfile(cfg_dir + conf_name) is False:
        return False
    fp = open(cfg_dir + conf_name, 'r')
    for line in fp.readlines():
        value = line.split('=')[0].strip()
        if value == '[FLASH_CFG]':
            continue
        value_key.append(value)

    cfg1 = BFConfigParser()
    cfg1.read(cfg_dir + conf_name)
    cfg2 = BFConfigParser()
    cfg2.read(file)
    for i in range(len(value_key)):
        if cfg1.has_option('FLASH_CFG', value_key[i]) and cfg2.has_option(section, value_key[i]):
            tmp_value = cfg1.get('FLASH_CFG', value_key[i])
            bflb_utils.update_cfg(cfg2, section, value_key[i], tmp_value)

    cfg2.write(file, 'w+')
    bflb_utils.printf('Update flash cfg finished')


def get_supported_flash_do():
    flash_type = []
    return flash_type


def get_int_mask(pos, length):
    ones = '11111111111111111111111111111111'
    zeros = '00000000000000000000000000000000'
    mask = ones[0:32 - pos - length] + zeros[0:length] + ones[0:pos]
    return int(mask, 2)


def create_flashcfg_data_from_cfg(cfg_len, cfgfile):
    section = 'FLASH_CFG'
    cfg = BFConfigParser()
    cfg.read(cfgfile)
    data = bytearray(cfg_len)
    minOffset = int(flash_cfg_keys.get('io_mode')['offset'], 10)
    for key in cfg.options(section):
        if flash_cfg_keys.get(key) == None:
            bflb_utils.printf(key + ' not exist')
            continue
        else:
            val = cfg.get(section, key)
            if val.startswith('0x'):
                val = int(val, 16)
            else:
                val = int(val, 10)
        offset = int(flash_cfg_keys.get(key)['offset'], 10) - minOffset
        pos = int(flash_cfg_keys.get(key)['pos'], 10)
        bitlen = int(flash_cfg_keys.get(key)['bitlen'], 10)
        oldval = bflb_utils.bytearray_to_int(bflb_utils.bytearray_reverse(data[offset:offset + 4]))
        newval = (oldval & get_int_mask(pos, bitlen)) + (val << pos)
        data[offset:offset + 4] = bflb_utils.int_to_4bytearray_l(newval)

    crcarray = bflb_utils.get_crc32_bytearray(data)
    data = bflb_utils.int_to_4bytearray_l(1195787078) + data + crcarray
    return data


def create_flashcfg_table(start_addr):
    single_flashcfg_len = 92
    flash_table_list = bytearray(0)
    flash_table_data = bytearray(0)
    if conf_sign:
        table_file = os.path.join(app_path, 'utils', 'flash', 'bl702l', 'flashcfg_list.csv')
    else:
        table_file = os.path.join(app_path, 'utils', 'flash', 'bl702l', 'flashcfg_list.csv')
    with open(table_file, 'r', encoding='utf-8-sig') as (csvfile):
        table_list = []
        cfgfile_list = []
        reader = csv.DictReader(csvfile)
        cnt = 0
        for row in reader:
            row_dict = {}
            row_dict['jid'] = row.get('flashJedecID', '')
            row_dict['cfgfile'] = row.get('configFile', '')
            if row_dict['cfgfile'] not in cfgfile_list:
                cfgfile_list.append(row_dict['cfgfile'])
            table_list.append(row_dict)
            cnt += 1

        table_list_len = 4 + cnt * 8 + 4
        for cfgfile in cfgfile_list:
            if conf_sign:
                cfgfile = os.path.join(app_path, 'utils', 'flash', 'bl702l', cfgfile)
            else:
                cfgfile = os.path.join(app_path, 'utils', 'flash', 'bl702l', cfgfile)
            data = create_flashcfg_data_from_cfg(single_flashcfg_len - 8, cfgfile)
            flash_table_data += data

        for dict in table_list:
            flash_table_list += bflb_utils.int_to_4bytearray_b(int(dict['jid'] + '00', 16))
            i = 0
            offset = 0
            for cfgfile in cfgfile_list:
                if cfgfile == dict['cfgfile']:
                    offset = start_addr + table_list_len + single_flashcfg_len * i
                    break
                i += 1

            flash_table_list += bflb_utils.int_to_4bytearray_l(offset)

    crcarray = bflb_utils.get_crc32_bytearray(flash_table_list)
    flash_table_list = bflb_utils.int_to_4bytearray_l(1196704582) + flash_table_list + crcarray
    return (
     flash_table_list, flash_table_data, len(flash_table_list))