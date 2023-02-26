# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
# [GCC 9.4.0]
# Embedded file name: libs/wb03/efuse_create_do.py
import os, binascii, hashlib, ecdsa
from libs import bflb_utils
from libs import bflb_efuse_boothd_create
from libs.bflb_utils import verify_hex_num, str_endian_switch
ef_sf_aes_mode_list = [
 'None', 'AES128', 'AES192', 'AES256']

def img_create_sha256_data(data_bytearray):
    hashfun = hashlib.sha256()
    hashfun.update(data_bytearray)
    return bflb_utils.hexstr_to_bytearray(hashfun.hexdigest())


def create_key_data_do(values, chip_name, chip_type, cfg_file, efuse_data):
    tips = ''
    bflb_utils.printf('Create_key_data')
    fp = open(cfg_file, 'w+')
    fp.write('[EFUSE_CFG]\n')
    aes_mode = ef_sf_aes_mode_list.index(values['ef_sf_aes_mode'])
    tips += 'AES Mode:' + values['ef_sf_aes_mode'] + '\r\n'
    bflb_utils.printf(ef_sf_aes_mode_list[aes_mode])
    fp.write('ef_cpu_enc_en = 1\n')
    if values['cpu0_pk_simple'] != '':
        if os.path.exists(values['cpu0_pk_simple']) is False:
            bflb_utils.printf('Error: public key file not found')
            return 'Error: public key file not found'
        vk = ecdsa.VerifyingKey.from_pem(open(values['cpu0_pk_simple']).read())
        pk_data = vk.to_string()
        bflb_utils.printf('Public key: ', binascii.hexlify(pk_data))
        pk_hash = img_create_sha256_data(pk_data)
        bflb_utils.printf('Public key hash=', binascii.hexlify(pk_hash))
        fp.write('ef_sboot_sign_mode = 1\n')
        fp.write('ef_key_slot_0_w0 = 0x' + str_endian_switch(str(pk_hash.hex())[0:8]) + '\n')
        fp.write('ef_key_slot_0_w1 = 0x' + str_endian_switch(str(pk_hash.hex())[8:16]) + '\n')
        fp.write('ef_key_slot_0_w2 = 0x' + str_endian_switch(str(pk_hash.hex())[16:24]) + '\n')
        fp.write('ef_key_slot_0_w3 = 0x' + str_endian_switch(str(pk_hash.hex())[24:32]) + '\n')
        fp.write('ef_key_slot_1_w0 = 0x' + str_endian_switch(str(pk_hash.hex())[32:40]) + '\n')
        fp.write('ef_key_slot_1_w1 = 0x' + str_endian_switch(str(pk_hash.hex())[40:48]) + '\n')
        fp.write('ef_key_slot_1_w2 = 0x' + str_endian_switch(str(pk_hash.hex())[48:56]) + '\n')
        fp.write('ef_key_slot_1_w3 = 0x' + str_endian_switch(str(pk_hash.hex())[56:64]) + '\n')
        if values['cpu0_pk_wp_enable'] is True:
            fp.write('wr_lock_key_slot_0 = 1\n')
            fp.write('wr_lock_key_slot_1 = 1\n')
        else:
            fp.write('wr_lock_key_slot_0 = 0\n')
            fp.write('wr_lock_key_slot_1 = 0\n')
        tips += 'public key hash\r\n'
    if aes_mode != 0:
        if len(values['cpu0_aes_key_simple']) >= 32:
            if verify_hex_num(values['cpu0_aes_key_simple']) is True:
                fp.write('ef_sf_aes_mode = ' + str(ef_sf_aes_mode_list.index(values['ef_sf_aes_mode'])) + '\n')
                fp.write('ef_key_slot_2_w0 = 0x' + str_endian_switch(values['cpu0_aes_key_simple'][0:8]) + '\n')
                fp.write('ef_key_slot_2_w1 = 0x' + str_endian_switch(values['cpu0_aes_key_simple'][8:16]) + '\n')
                fp.write('ef_key_slot_2_w2 = 0x' + str_endian_switch(values['cpu0_aes_key_simple'][16:24]) + '\n')
                fp.write('ef_key_slot_2_w3 = 0x' + str_endian_switch(values['cpu0_aes_key_simple'][24:32]) + '\n')
                if values['cpu0_aes_key_wp_enable'] is True:
                    fp.write('wr_lock_key_slot_2 = 1\n')
                else:
                    fp.write('wr_lock_key_slot_2 = 0\n')
                if values['cpu0_aes_key_rp_enable'] is True:
                    fp.write('rd_lock_key_slot_2 = 1\n')
                else:
                    fp.write('rd_lock_key_slot_2 = 0\n')
                tips += 'AES key\r\n'
            else:
                bflb_utils.printf('Error: Please check AES key data and len')
                return 'Error: Please check AES key data and len'
        else:
            pass
    if values['cpu0_aes_key_simple'] != '':
        bflb_utils.printf('Error: AES mode is None, no need to fill in CPU0 AES key')
        return 'Error: AES mode is None, no need to fill in CPU0 AES key'
    if aes_mode == 1:
        if len(values['cpu0_aes_key_simple']) != 32:
            bflb_utils.printf('Error: Please check AES key len')
            return 'Error: Please check AES key len'
        else:
            if aes_mode == 2:
                if len(values['cpu0_aes_key_simple']) == 48:
                    fp.write('ef_key_slot_3_w0 = 0x' + str_endian_switch(values['cpu0_aes_key_simple'][32:40]) + '\n')
                    fp.write('ef_key_slot_3_w1 = 0x' + str_endian_switch(values['cpu0_aes_key_simple'][40:48]) + '\n')
                    if values['cpu0_aes_key_wp_enable'] is True:
                        fp.write('wr_lock_key_slot_3 = 1\n')
                    else:
                        fp.write('wr_lock_key_slot_3 = 0\n')
                elif values['cpu0_aes_key_rp_enable'] is True:
                    fp.write('rd_lock_key_slot_3 = 1\n')
                else:
                    fp.write('rd_lock_key_slot_3 = 0\n')
            else:
                bflb_utils.printf('Error: Please check AES key len')
                return 'Error: Please check AES key len'
    else:
        if aes_mode == 3:
            if len(values['cpu0_aes_key_simple']) == 64:
                fp.write('ef_key_slot_3_w0 = 0x' + str_endian_switch(values['cpu0_aes_key_simple'][32:40]) + '\n')
                fp.write('ef_key_slot_3_w1 = 0x' + str_endian_switch(values['cpu0_aes_key_simple'][40:48]) + '\n')
                fp.write('ef_key_slot_3_w2 = 0x' + str_endian_switch(values['cpu0_aes_key_simple'][48:56]) + '\n')
                fp.write('ef_key_slot_3_w3 = 0x' + str_endian_switch(values['cpu0_aes_key_simple'][56:64]) + '\n')
                if values['cpu0_aes_key_wp_enable'] is True:
                    fp.write('wr_lock_key_slot_3 = 1\n')
                else:
                    fp.write('wr_lock_key_slot_3 = 0\n')
                if values['cpu0_aes_key_rp_enable'] is True:
                    fp.write('rd_lock_key_slot_3 = 1\n')
                else:
                    fp.write('rd_lock_key_slot_3 = 0\n')
            else:
                bflb_utils.printf('Error: Please check AES key len')
                return 'Error: Please check AES key len'
        bflb_utils.printf('Following will be burned:\r\n' + tips)
        fp.close()
        bflb_efuse_boothd_create.efuse_create_process(chip_name, chip_type, cfg_file, efuse_data)