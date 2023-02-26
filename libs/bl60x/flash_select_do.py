# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
# [GCC 9.4.0]
# Embedded file name: libs/bl60x/flash_select_do.py
import os, config as gol
from libs import bflb_utils
from libs.bflb_utils import app_path, conf_sign
from libs.bflb_configobj import BFConfigParser

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