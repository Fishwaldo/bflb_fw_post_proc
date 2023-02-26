# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
# [GCC 9.4.0]
# Embedded file name: libs/bl602/img_create_do.py
import hashlib, binascii, ecdsa
from libs import bflb_utils
from libs.bflb_utils import open_file, img_create_sha256_data, img_create_encrypt_data
from libs.bflb_configobj import BFConfigParser
from libs.bl602.bootheader_cfg_keys import bootheader_len as header_len
keyslot0 = 28
keyslot1 = keyslot0 + 16
keyslot2 = keyslot1 + 16
keyslot3 = keyslot2 + 16
keyslot4 = keyslot3 + 16
keyslot5 = keyslot4 + 16
keyslot6 = keyslot5 + 16
wr_lock_key_slot_4_l = 13
wr_lock_key_slot_5_l = 14
wr_lock_boot_mode = 15
wr_lock_dbg_pwd = 16
wr_lock_sw_usage_0 = 17
wr_lock_wifi_mac = 18
wr_lock_key_slot_0 = 19
wr_lock_key_slot_1 = 20
wr_lock_key_slot_2 = 21
wr_lock_key_slot_3 = 22
wr_lock_key_slot_4_h = 23
wr_lock_key_slot_5_h = 24
rd_lock_dbg_pwd = 25
rd_lock_key_slot_0 = 26
rd_lock_key_slot_1 = 27
rd_lock_key_slot_2 = 28
rd_lock_key_slot_3 = 29
rd_lock_key_slot_4 = 30
rd_lock_key_slot_5 = 31

def img_update_efuse(cfg, sign, pk_hash, flash_encryp_type, flash_key, sec_eng_key_sel, sec_eng_key, security=False):
    efuse_data = bytearray(128)
    efuse_mask_data = bytearray(128)
    if cfg != None:
        fp = open(cfg.get('Img_Cfg', 'efuse_file'), 'rb')
        efuse_data = bytearray(fp.read()) + bytearray(0)
        fp.close()
        fp = open(cfg.get('Img_Cfg', 'efuse_mask_file'), 'rb')
        efuse_mask_data = bytearray(fp.read()) + bytearray(0)
        fp.close()
    mask_4bytes = bytearray.fromhex('FFFFFFFF')
    efuse_data[0] |= flash_encryp_type
    efuse_data[0] |= sign << 2
    if flash_encryp_type > 0:
        efuse_data[0] |= 128
        efuse_data[0] |= 48
    efuse_mask_data[0] |= 255
    rw_lock = 0
    if pk_hash is not None:
        efuse_data[keyslot0:keyslot2] = pk_hash
        efuse_mask_data[keyslot0:keyslot2] = mask_4bytes * 8
        rw_lock |= 1 << wr_lock_key_slot_0
        rw_lock |= 1 << wr_lock_key_slot_1
    if flash_key is not None:
        if flash_encryp_type == 1:
            efuse_data[keyslot2:keyslot3] = flash_key[0:16]
            efuse_mask_data[keyslot2:keyslot3] = mask_4bytes * 4
        else:
            if flash_encryp_type == 2:
                efuse_data[keyslot2:keyslot4] = flash_key
                efuse_mask_data[keyslot2:keyslot4] = mask_4bytes * 8
                rw_lock |= 1 << wr_lock_key_slot_3
                rw_lock |= 1 << rd_lock_key_slot_3
            else:
                if flash_encryp_type == 3:
                    efuse_data[keyslot2:keyslot4] = flash_key
                    efuse_mask_data[keyslot2:keyslot4] = mask_4bytes * 8
                    rw_lock |= 1 << wr_lock_key_slot_3
                    rw_lock |= 1 << rd_lock_key_slot_3
                rw_lock |= 1 << wr_lock_key_slot_2
                rw_lock |= 1 << rd_lock_key_slot_2
    if sec_eng_key is not None:
        if flash_encryp_type == 0:
            if sec_eng_key_sel == 0:
                efuse_data[keyslot3:keyslot4] = sec_eng_key[0:16]
                efuse_mask_data[keyslot3:keyslot4] = mask_4bytes * 4
                rw_lock |= 1 << wr_lock_key_slot_3
                rw_lock |= 1 << rd_lock_key_slot_3
            if sec_eng_key_sel == 1:
                efuse_data[keyslot2:keyslot3] = sec_eng_key[0:16]
                efuse_mask_data[keyslot2:keyslot3] = mask_4bytes * 4
                rw_lock |= 1 << wr_lock_key_slot_2
                rw_lock |= 1 << rd_lock_key_slot_2
        if flash_encryp_type == 1:
            if sec_eng_key_sel == 0:
                efuse_data[keyslot4:keyslot5] = sec_eng_key[0:16]
                efuse_mask_data[keyslot4:keyslot5] = mask_4bytes * 4
                rw_lock |= 1 << wr_lock_key_slot_4_l
                rw_lock |= 1 << wr_lock_key_slot_4_h
                rw_lock |= 1 << rd_lock_key_slot_4
            if sec_eng_key_sel == 1:
                efuse_data[keyslot4:keyslot5] = sec_eng_key[0:16]
                efuse_mask_data[keyslot4:keyslot5] = mask_4bytes * 4
                rw_lock |= 1 << wr_lock_key_slot_4_l
                rw_lock |= 1 << wr_lock_key_slot_4_h
                rw_lock |= 1 << rd_lock_key_slot_4
    efuse_data[124:128] = bflb_utils.int_to_4bytearray_l(rw_lock)
    efuse_mask_data[124:128] = bflb_utils.int_to_4bytearray_l(rw_lock)
    if cfg != None:
        if security is True:
            bflb_utils.printf('Encrypt efuse data')
            security_key, security_iv = bflb_utils.get_security_key()
            efuse_data = img_create_encrypt_data(efuse_data, security_key, security_iv, 0)
            efuse_data = bytearray(4096) + efuse_data
        fp = open(cfg.get('Img_Cfg', 'efuse_file'), 'wb+')
        fp.write(efuse_data)
        fp.close()
        fp = open(cfg.get('Img_Cfg', 'efuse_mask_file'), 'wb+')
        fp.write(efuse_mask_data)
        fp.close()
    return efuse_data


def img_create_get_sign_encrypt_info(bootheader_data):
    sign = bootheader_data[116] & 3
    encrypt = bootheader_data[116] >> 2 & 3
    key_sel = bootheader_data[116] >> 4 & 3
    return (sign, encrypt, key_sel)


def img_create_get_hash_ignore(bootheader_data):
    return bootheader_data[118] >> 1 & 1


def img_create_get_crc_ignore(bootheader_data):
    return bootheader_data[118] & 1


def img_create_update_bootheader_if(bootheader_data, hash, seg_cnt):
    bootheader_data[120:124] = bflb_utils.int_to_4bytearray_l(seg_cnt)
    sign = bootheader_data[116] & 3
    encrypt = bootheader_data[116] >> 2 & 3
    key_sel = bootheader_data[116] >> 4 & 3
    if bootheader_data[118] >> 1 & 1 == 1 and sign == 0:
        bflb_utils.printf('Hash ignored')
    else:
        bootheader_data[132:164] = hash
    if bootheader_data[118] & 1 == 1:
        bflb_utils.printf('Header crc ignored')
    else:
        hd_crcarray = bflb_utils.get_crc32_bytearray(bootheader_data[0:header_len - 4])
        bootheader_data[header_len - 4:header_len] = hd_crcarray
        bflb_utils.printf('Header crc: ', binascii.hexlify(hd_crcarray))
    return bootheader_data


def img_create_update_bootheader(bootheader_data, hash, seg_cnt):
    bootheader_data[120:124] = bflb_utils.int_to_4bytearray_l(seg_cnt)
    sign, encrypt, key_sel = img_create_get_sign_encrypt_info(bootheader_data)
    if img_create_get_hash_ignore(bootheader_data) == 1 and sign == 0:
        bflb_utils.printf('Hash ignored')
    else:
        bootheader_data[132:164] = hash
    if img_create_get_crc_ignore(bootheader_data) == 1:
        bflb_utils.printf('Header crc ignored')
    else:
        hd_crcarray = bflb_utils.get_crc32_bytearray(bootheader_data[0:header_len - 4])
        bootheader_data[header_len - 4:header_len] = hd_crcarray
        bflb_utils.printf('Header crc: ', binascii.hexlify(hd_crcarray))
    return bootheader_data[0:header_len]


def img_create_update_segheader(segheader, segdatalen, segdatacrc):
    segheader[4:8] = segdatalen
    segheader[8:12] = segdatacrc
    return segheader


def img_create_sign_data(data_bytearray, privatekey_file_uecc, publickey_file):
    sk = ecdsa.SigningKey.from_pem(open(privatekey_file_uecc).read())
    vk = ecdsa.VerifyingKey.from_pem(open(publickey_file).read())
    pk_data = vk.to_string()
    bflb_utils.printf('Private key: ', binascii.hexlify(sk.to_string()))
    bflb_utils.printf('Public key: ', binascii.hexlify(pk_data))
    pk_hash = img_create_sha256_data(pk_data)
    bflb_utils.printf('Public key hash=', binascii.hexlify(pk_hash))
    signature = sk.sign(data_bytearray, hashfunc=(hashlib.sha256),
      sigencode=(ecdsa.util.sigencode_string))
    bflb_utils.printf('Signature=', binascii.hexlify(signature))
    len_array = bflb_utils.int_to_4bytearray_l(len(signature))
    sig_field = len_array + signature
    crcarray = bflb_utils.get_crc32_bytearray(sig_field)
    return (pk_data, pk_hash, sig_field + crcarray)


def img_create_read_file_append_crc(file, crc):
    fp = open(file, 'rb')
    read_data = bytearray(fp.read())
    crcarray = bytearray(0)
    if crc:
        crcarray = bflb_utils.get_crc32_bytearray(read_data)
    fp.close()
    return read_data + crcarray


def encrypt_loader_bin_do(file, sign, encrypt, createcfg):
    if encrypt != 0 or sign != 0:
        encrypt_key = bytearray(0)
        encrypt_iv = bytearray(0)
        load_helper_bin_header = bytearray(0)
        load_helper_bin_body = bytearray(0)
        offset = 116
        sign_pos = 0
        encrypt_type_pos = 2
        key_sel_pos = 4
        pk_data = bytearray(0)
        signature = bytearray(0)
        aesiv_data = bytearray(0)
        data_tohash = bytearray(0)
        cfg = BFConfigParser()
        cfg.read(createcfg)
        with open(file, 'rb') as (fp):
            load_helper_bin = fp.read()
            load_helper_bin_header = load_helper_bin[0:header_len]
            load_helper_bin_body = load_helper_bin[header_len:]
        if load_helper_bin_header != bytearray(0):
            if load_helper_bin_body != bytearray(0):
                load_helper_bin_body = bflb_utils.add_to_16(load_helper_bin_body)
                if encrypt != 0:
                    encrypt_key = bflb_utils.hexstr_to_bytearray(cfg.get('Img_Cfg', 'aes_key_org'))
                    encrypt_iv = bflb_utils.hexstr_to_bytearray(cfg.get('Img_Cfg', 'aes_iv'))
                    iv_crcarray = bflb_utils.get_crc32_bytearray(encrypt_iv)
                    aesiv_data = encrypt_iv + iv_crcarray
                    data_tohash = data_tohash + aesiv_data
                    load_helper_bin_body_encrypt = bflb_utils.img_create_encrypt_data(load_helper_bin_body, encrypt_key, encrypt_iv, 0)
                else:
                    load_helper_bin_body_encrypt = load_helper_bin_body
                data = bytearray(load_helper_bin_header)
                oldval = bflb_utils.bytearray_to_int(bflb_utils.bytearray_reverse(data[offset:offset + 4]))
                newval = oldval
                if encrypt != 0:
                    newval = newval | 1 << encrypt_type_pos
                    newval = newval | 0 << key_sel_pos
                if sign != 0:
                    newval = newval | 1 << sign_pos
                    data_tohash += load_helper_bin_body_encrypt
                    publickey_file = cfg.get('Img_Cfg', 'publickey_file')
                    privatekey_file_uecc = cfg.get('Img_Cfg', 'privatekey_file_uecc')
                    pk_data, pk_hash, signature = img_create_sign_data(data_tohash, privatekey_file_uecc, publickey_file)
                    pk_data = pk_data + bflb_utils.get_crc32_bytearray(pk_data)
                data[offset:offset + 4] = bflb_utils.int_to_4bytearray_l(newval)
                load_helper_bin_header = data
                load_helper_bin_encrypt = load_helper_bin_header + pk_data + signature + aesiv_data + load_helper_bin_body_encrypt
                hash = img_create_sha256_data(data_tohash)
                bflb_utils.printf('Image hash is ', binascii.hexlify(hash))
                load_helper_bin_data = bytearray(load_helper_bin_encrypt)
                load_helper_bin_encrypt = img_create_update_bootheader_if(load_helper_bin_data, hash, 1)
        return (
         True, load_helper_bin_encrypt)
    return (False, None)


def create_encryptandsign_flash_data(data, offset, key, iv, publickey, privatekey):
    encrypt = 0
    encrypt_type = 0
    sign = 0
    data_len = len(data)
    aesiv_data = bytearray(0)
    pk_data = bytearray(0)
    data_tohash = bytearray(0)
    efuse_data = bytearray(128)
    bootheader_data = data[0:176]
    img_len = bflb_utils.bytearray_to_int(data[120:121]) + (bflb_utils.bytearray_to_int(data[121:122]) << 8) + (bflb_utils.bytearray_to_int(data[122:123]) << 16) + (bflb_utils.bytearray_to_int(data[123:124]) << 24)
    img_data = data[offset:offset + img_len]
    if key:
        if iv:
            encrypt = 1
            if len(key) == 32:
                encrypt_type = 1
            else:
                if len(key) == 64:
                    encrypt_type = 2
                else:
                    if len(key) == 48:
                        encrypt_type = 3
            bootheader_data[116] |= encrypt_type
    if publickey:
        if privatekey:
            sign = 1
            bootheader_data[116] |= 4
    if encrypt:
        encrypt_key = bflb_utils.hexstr_to_bytearray(key)
        encrypt_iv = bflb_utils.hexstr_to_bytearray(iv)
        iv_crcarray = bflb_utils.get_crc32_bytearray(encrypt_iv)
        aesiv_data = encrypt_iv + iv_crcarray
        data_tohash = data_tohash + aesiv_data
    else:
        mfgBin = False
        if img_data[img_len - 16:img_len - 12] == bytearray('0mfg'.encode('utf-8')):
            bflb_utils.printf('mfg bin')
            mfgBin = True
        data_toencrypt = bytearray(0)
        if mfgBin:
            data_toencrypt += img_data[:img_len - 16]
        else:
            data_toencrypt += img_data
    if encrypt:
        data_toencrypt = img_create_encrypt_data(data_toencrypt, encrypt_key, encrypt_iv, 1)
    if mfgBin:
        data_toencrypt += img_data[img_len - 16:img_len]
    fw_data = bytearray(0)
    data_tohash += data_toencrypt
    fw_data = data_toencrypt
    seg_cnt = len(data_toencrypt)
    hash = img_create_sha256_data(data_tohash)
    bflb_utils.printf('Image hash is ', binascii.hexlify(hash))
    bootheader_data = img_create_update_bootheader(bootheader_data, hash, seg_cnt)
    signature = bytearray(0)
    pk_hash = None
    if sign:
        pk_data, pk_hash, signature = img_create_sign_data(data_tohash, privatekey, publickey)
        pk_data = pk_data + bflb_utils.get_crc32_bytearray(pk_data)
    bflb_utils.printf('Write flash img')
    bootinfo = bootheader_data + pk_data + signature + aesiv_data
    output_data = bytearray(data_len)
    for i in range(data_len):
        output_data[i] = 255

    output_data[0:len(bootinfo)] = bootinfo
    output_data[offset:offset + seg_cnt] = fw_data
    if encrypt != 0:
        if encrypt_type == 1:
            efuse_data = img_update_efuse(None, sign, pk_hash, 1, encrypt_key + bytearray(32 - len(encrypt_key)), 0, encrypt_key + bytearray(32 - len(encrypt_key)))
        if encrypt_type == 2:
            efuse_data = img_update_efuse(None, sign, pk_hash, 3, encrypt_key + bytearray(32 - len(encrypt_key)), 0, encrypt_key + bytearray(32 - len(encrypt_key)))
        if encrypt_type == 3:
            efuse_data = img_update_efuse(None, sign, pk_hash, 2, encrypt_key + bytearray(32 - len(encrypt_key)), 0, encrypt_key + bytearray(32 - len(encrypt_key)))
    return (
     output_data, efuse_data, seg_cnt)


def img_creat_process(flash_img, cfg, security=False):
    encrypt_blk_size = 16
    padding = bytearray(encrypt_blk_size)
    data_tohash = bytearray(0)
    cfg_section = 'Img_Cfg'
    segheader_file = []
    if flash_img == 0:
        for files in cfg.get(cfg_section, 'segheader_file').split(' '):
            segheader_file.append(str(files))

    segdata_file = []
    for files in cfg.get(cfg_section, 'segdata_file').split('|'):
        segdata_file.append(str(files))
        if flash_img == 1:
            break

    boot_header_file = cfg.get(cfg_section, 'boot_header_file')
    bootheader_data = img_create_read_file_append_crc(boot_header_file, 0)
    encrypt = 0
    sign, encrypt, key_sel = img_create_get_sign_encrypt_info(bootheader_data)
    aesiv_data = bytearray(0)
    pk_data = bytearray(0)
    if sign != 0:
        bflb_utils.printf('Image need sign')
        publickey_file = cfg.get(cfg_section, 'publickey_file')
        privatekey_file_uecc = cfg.get(cfg_section, 'privatekey_file_uecc')
    if encrypt != 0:
        bflb_utils.printf('Image need encrypt ', encrypt)
        encrypt_key_org = bflb_utils.hexstr_to_bytearray(cfg.get(cfg_section, 'aes_key_org'))
        if encrypt == 1:
            encrypt_key = encrypt_key_org[0:16]
        else:
            if encrypt == 2:
                encrypt_key = encrypt_key_org[0:32]
            else:
                if encrypt == 3:
                    encrypt_key = encrypt_key_org[0:24]
                bflb_utils.printf('Key= ', binascii.hexlify(encrypt_key))
        encrypt_iv = bflb_utils.hexstr_to_bytearray(cfg.get(cfg_section, 'aes_iv'))
        iv_crcarray = bflb_utils.get_crc32_bytearray(encrypt_iv)
        aesiv_data = encrypt_iv + iv_crcarray
        data_tohash = data_tohash + aesiv_data
    else:
        seg_cnt = len(segheader_file)
        if flash_img == 0:
            if seg_cnt != len(segdata_file):
                bflb_utils.printf('Segheader count and segdata count not match')
                return ('FAIL', data_tohash)
            mfgBin = False
            data_toencrypt = bytearray(0)
            if flash_img == 0:
                i = 0
                seg_header_list = []
                seg_data_list = []
                while i < seg_cnt:
                    seg_data = img_create_read_file_append_crc(segdata_file[i], 0)
                    padding_size = 0
                    if len(seg_data) % encrypt_blk_size != 0:
                        padding_size = encrypt_blk_size - len(seg_data) % encrypt_blk_size
                        seg_data += padding[0:padding_size]
                    segdata_crcarray = bflb_utils.get_crc32_bytearray(seg_data)
                    seg_data_list.append(seg_data)
                    seg_header = img_create_read_file_append_crc(segheader_file[i], 0)
                    seg_header = img_create_update_segheader(seg_header, bflb_utils.int_to_4bytearray_l(len(seg_data)), segdata_crcarray)
                    segheader_crcarray = bflb_utils.get_crc32_bytearray(seg_header)
                    seg_header = seg_header + segheader_crcarray
                    seg_header_list.append(seg_header)
                    i = i + 1

                i = 0
                while i < seg_cnt:
                    data_toencrypt += seg_header_list[i]
                    data_toencrypt += seg_data_list[i]
                    i += 1

        else:
            seg_data = img_create_read_file_append_crc(segdata_file[0], 0)
            padding_size = 0
            if len(seg_data) % encrypt_blk_size != 0:
                padding_size = encrypt_blk_size - len(seg_data) % encrypt_blk_size
                seg_data += padding[0:padding_size]
            else:
                if seg_data[len(seg_data) - 16:len(seg_data) - 12] == bytearray('0mfg'.encode('utf-8')):
                    mfgBin = True
                if mfgBin:
                    data_toencrypt += seg_data[:len(seg_data) - 16]
                else:
                    data_toencrypt += seg_data
            seg_cnt = len(data_toencrypt)
            if mfgBin:
                seg_cnt += 16
        if encrypt != 0:
            data_toencrypt = img_create_encrypt_data(data_toencrypt, encrypt_key, encrypt_iv, flash_img)
        elif mfgBin:
            data_toencrypt += seg_data[len(seg_data) - 16:len(seg_data)]
        else:
            fw_data = bytearray(0)
            data_tohash += data_toencrypt
            fw_data = data_toencrypt
            hash = img_create_sha256_data(data_tohash)
            bflb_utils.printf('Image hash is ', binascii.hexlify(hash))
            bootheader_data = img_create_update_bootheader(bootheader_data, hash, seg_cnt)
            signature = bytearray(0)
            pk_hash = None
            if sign == 1:
                pk_data, pk_hash, signature = img_create_sign_data(data_tohash, privatekey_file_uecc, publickey_file)
                pk_data = pk_data + bflb_utils.get_crc32_bytearray(pk_data)
            if flash_img == 1:
                bflb_utils.printf('Write flash img')
                bootinfo_file_name = cfg.get(cfg_section, 'bootinfo_file')
                fp = open(bootinfo_file_name, 'wb+')
                bootinfo = bootheader_data + pk_data + signature + aesiv_data
                fp.write(bootinfo)
                fp.close()
                fw_file_name = cfg.get(cfg_section, 'img_file')
                fp = open(fw_file_name, 'wb+')
                fp.write(fw_data)
                fp.close()
                fw_data_hash = img_create_sha256_data(fw_data)
                fp = open(fw_file_name.replace('.bin', '_withhash.bin'), 'wb+')
                fp.write(fw_data + fw_data_hash)
                fp.close()
                if encrypt != 0:
                    if encrypt == 1:
                        img_update_efuse(cfg, sign, pk_hash, 1, encrypt_key + bytearray(32 - len(encrypt_key)), key_sel, encrypt_key + bytearray(32 - len(encrypt_key)), security)
                    if encrypt == 2:
                        img_update_efuse(cfg, sign, pk_hash, 3, encrypt_key + bytearray(32 - len(encrypt_key)), key_sel, encrypt_key + bytearray(32 - len(encrypt_key)), security)
                    if encrypt == 3:
                        img_update_efuse(cfg, sign, pk_hash, 2, encrypt_key + bytearray(32 - len(encrypt_key)), key_sel, encrypt_key + bytearray(32 - len(encrypt_key)), security)
                else:
                    img_update_efuse(cfg, sign, pk_hash, encrypt, None, key_sel, None, security)
            else:
                bflb_utils.printf('Write if img')
                whole_img_file_name = cfg.get(cfg_section, 'whole_img_file')
                fp = open(whole_img_file_name, 'wb+')
                img_data = bootheader_data + pk_data + signature + aesiv_data + fw_data
                fp.write(img_data)
                fp.close()
                if encrypt != 0:
                    if encrypt == 1:
                        img_update_efuse(cfg, sign, pk_hash, 1, None, key_sel, encrypt_key + bytearray(32 - len(encrypt_key)), security)
                    if encrypt == 2:
                        img_update_efuse(cfg, sign, pk_hash, 3, None, key_sel, encrypt_key + bytearray(32 - len(encrypt_key)), security)
                    if encrypt == 3:
                        img_update_efuse(cfg, sign, pk_hash, 2, None, key_sel, encrypt_key + bytearray(32 - len(encrypt_key)), security)
                else:
                    img_update_efuse(cfg, sign, pk_hash, 0, None, key_sel, bytearray(32), security)
    return (
     'OK', data_tohash)


def img_create_do(args, img_dir_path=None, config_file=None):
    bflb_utils.printf('Image create path: ', img_dir_path)
    if config_file is None:
        config_file = img_dir_path + '/img_create_cfg.ini'
    else:
        bflb_utils.printf('Config file: ', config_file)
        cfg = BFConfigParser()
        cfg.read(config_file)
        img_type = 'media'
        signer = 'none'
        security = False
        data_tohash = bytearray(0)
        try:
            if args.image:
                img_type = args.image
            if args.signer:
                signer = args.signer
            if args.security:
                security = args.security == 'efuse'
        except Exception as e:
            try:
                bflb_utils.printf(e)
            finally:
                e = None
                del e

        if img_type == 'media':
            flash_img = 1
        else:
            flash_img = 0
    ret, data_tohash = img_creat_process(flash_img, cfg, security)
    if ret != 'OK':
        bflb_utils.printf('Fail to create images!')
        return False
    return True


def create_sp_media_image(config, cpu_type=None, security=False):
    bflb_utils.printf('========= sp image create =========')
    cfg = BFConfigParser()
    cfg.read(config)
    img_creat_process(1, cfg, security)