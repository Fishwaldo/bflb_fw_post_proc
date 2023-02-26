# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
# [GCC 9.4.0]
# Embedded file name: libs/bl602/firmware_post_process_do.py
import os, sys, hashlib, binascii, codecs, ecdsa
from CryptoPlus.Cipher import AES as AES_XTS
from libs import bflb_utils
from libs.bflb_utils import img_create_sha256_data, img_create_encrypt_data
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

def img_update_efuse_data(cfg, sign, pk_hash, flash_encryp_type, flash_key, sec_eng_key_sel, sec_eng_key, security=False):
    efuse_data = bytearray(128)
    efuse_mask_data = bytearray(128)
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
    if security is True:
        fp = open(os.path.join(cfg, 'efusedata_raw.bin'), 'wb+')
        fp.write(efuse_data)
        fp.close()
        bflb_utils.printf('Encrypt efuse data')
        security_key, security_iv = bflb_utils.get_security_key()
        efuse_data = img_create_encrypt_data(efuse_data, security_key, security_iv, 0)
        efuse_data = bytearray(4096) + efuse_data
    fp = open(os.path.join(cfg, 'efusedata.bin'), 'wb+')
    fp.write(efuse_data)
    fp.close()
    fp = open(os.path.join(cfg, 'efusedata_mask.bin'), 'wb+')
    fp.write(efuse_mask_data)
    fp.close()


def img_create_sign_data(data_bytearray, privatekey_file, publickey_file):
    sk = ecdsa.SigningKey.from_pem(open(privatekey_file).read())
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


def firmware_post_get_flash_encrypt_type(encrypt, xts_mode):
    flash_encrypt_type = 0
    if encrypt != 0:
        if encrypt == 1:
            flash_encrypt_type = 1
        if encrypt == 2:
            flash_encrypt_type = 3
        if encrypt == 3:
            flash_encrypt_type = 2
        if xts_mode == 1:
            flash_encrypt_type += 3
    return flash_encrypt_type


def firmware_post_proc_do_encrypt(data_bytearray, aeskey_hexstr, aesiv_hexstr, xts_mode, privatekey_file, publickey_file, imgfile):
    flash_img = 1
    bootcfg_start = 116
    if flash_img:
        image_offset = firmware_post_proc_get_image_offset(data_bytearray)
        bflb_utils.printf('Image Offset:' + hex(image_offset))
        image_data = data_bytearray[image_offset:len(data_bytearray)]
        boot_data = data_bytearray[0:image_offset]
    if aeskey_hexstr != None:
        bflb_utils.printf('Image need encryption')
        if aesiv_hexstr == None:
            bflb_utils.printf('[Error] AES IV not given, skip encryption')
            return (data_bytearray, None)
        elif xts_mode != None:
            xts_mode = int(xts_mode)
        else:
            xts_mode = 0
        if xts_mode == 1:
            bflb_utils.printf('[Error] XTS mode not support!!!!')
            return (data_bytearray, None)
            data_tohash = bytearray(0)
            aesiv_data = bytearray(0)
            encrypt = 0
            if aeskey_hexstr != None:
                data_toencrypt = bytearray(0)
                aeskey_bytearray = bflb_utils.hexstr_to_bytearray(aeskey_hexstr)
                if len(aeskey_bytearray) != 32:
                    if len(aeskey_bytearray) != 24:
                        if len(aeskey_bytearray) != 16:
                            bflb_utils.printf('Key length error')
                            return (data_bytearray, None)
                if len(aeskey_bytearray) == 16:
                    encrypt = 1
        elif len(aeskey_bytearray) == 32:
            if xts_mode == 1:
                encrypt = 1
        else:
            encrypt = 2
    else:
        if len(aeskey_bytearray) == 24:
            encrypt = 3
        else:
            encrypt_key = aeskey_bytearray
            bflb_utils.printf('Key= ', binascii.hexlify(encrypt_key))
            boot_data[bootcfg_start] |= (encrypt << 2) + (xts_mode << 6)
            iv_value = aesiv_hexstr
            if xts_mode == 1:
                iv_value = iv_value[24:32] + iv_value[:24]
            encrypt_iv = bflb_utils.hexstr_to_bytearray(iv_value)
            iv_crcarray = bflb_utils.get_crc32_bytearray(encrypt_iv)
            aesiv_data = encrypt_iv + iv_crcarray
            data_tohash += aesiv_data
            data_toencrypt += image_data
            unencrypt_mfg_data = bytearray(0)
            if len(data_toencrypt) >= 8192:
                if data_toencrypt[4096:4100] == bytearray('0mfg'.encode('utf-8')):
                    unencrypt_mfg_data = data_toencrypt[4096:8192]
                elif xts_mode != 0:
                    image_data = img_create_encrypt_data_xts(data_toencrypt, encrypt_key, encrypt_iv, encrypt)
                else:
                    image_data = img_create_encrypt_data(data_toencrypt, encrypt_key, encrypt_iv, flash_img)
                if unencrypt_mfg_data != bytearray(0):
                    image_data = image_data[0:4096] + unencrypt_mfg_data + image_data[8192:]
                data_tohash += image_data
            else:
                data_tohash += image_data
            hash = img_create_sha256_data(data_tohash)
            bflb_utils.printf('Image hash is ', binascii.hexlify(hash))
            pk_data = bytearray(0)
            signature = bytearray(0)
            sign = 0
            pk_hash = None
            if privatekey_file != None:
                if publickey_file != None:
                    pk_data, pk_hash, signature = img_create_sign_data(data_tohash, privatekey_file, publickey_file)
                    pk_data = pk_data + bflb_utils.get_crc32_bytearray(pk_data)
                    boot_data[bootcfg_start] |= 1
                    sign = 1
                boot_data[176:176 + len(pk_data + signature)] = pk_data + signature
                boot_data[176 + len(pk_data + signature):176 + len(pk_data + signature) + len(aesiv_data)] = aesiv_data
                filedir, ext = os.path.split(imgfile)
                flash_encrypt_type = firmware_post_get_flash_encrypt_type(encrypt, xts_mode)
                key_sel = 0
                security = True
                if encrypt != 0:
                    img_update_efuse_data(filedir, sign, pk_hash, flash_encrypt_type, encrypt_key + bytearray(32 - len(encrypt_key)), key_sel, encrypt_key + bytearray(32 - len(encrypt_key)), security)
            else:
                img_update_efuse_data(filedir, sign, pk_hash, flash_encrypt_type, None, key_sel, None, security)
        return (
         boot_data + image_data, hash)


def firmware_post_proc_update_flash_crc(image_data):
    flash_cfg_start = 8
    crcarray = bflb_utils.get_crc32_bytearray(image_data[flash_cfg_start + 4:flash_cfg_start + 4 + 84])
    image_data[flash_cfg_start + 4 + 84:flash_cfg_start + 4 + 84 + 4] = crcarray
    bflb_utils.printf('Flash config crc: ', binascii.hexlify(crcarray))
    return image_data


def firmware_post_proc_update_clock_crc(image_data):
    clockcfg_start = 100
    crcarray = bflb_utils.get_crc32_bytearray(image_data[clockcfg_start + 4:clockcfg_start + 12])
    image_data[clockcfg_start + 12:clockcfg_start + 12 + 4] = crcarray
    bflb_utils.printf('Clock config crc: ', binascii.hexlify(crcarray))
    return image_data


def firmware_post_proc_update_bootheader_crc(image_data):
    crcarray = bflb_utils.get_crc32_bytearray(image_data[0:172])
    image_data[172:176] = crcarray
    bflb_utils.printf('Bootheader config crc: ', binascii.hexlify(crcarray))
    return image_data


def firmware_post_proc_get_hash_ignore(image_data):
    bootcfg_start = 116
    return image_data[bootcfg_start + 2] >> 1 & 1


def firmware_post_proc_enable_hash_cfg(image_data):
    bootcfg_start = 116
    image_data[bootcfg_start + 2] &= -3
    return image_data


def firmware_post_proc_get_image_offset(image_data):
    cpucfg_start = 128
    return image_data[cpucfg_start + 0] + (image_data[cpucfg_start + 1] << 8) + (image_data[cpucfg_start + 2] << 16) + (image_data[cpucfg_start + 3] << 24)


def firmware_post_proc_update_hash(image_data, force_update, args, hash):
    image_offset = firmware_post_proc_get_image_offset(image_data)
    bflb_utils.printf('Image Offset:' + hex(image_offset))
    bootcfg_start = 116
    image_data[bootcfg_start + 4:bootcfg_start + 4 + 4] = bflb_utils.int_to_4bytearray_l(len(image_data) - image_offset)
    if args.hd_append != None:
        bflb_utils.printf('Append bootheader data')
        bh_append_data = firmware_get_file_data(args.hd_append)
        if len(bh_append_data) <= image_offset - 512:
            image_data[image_offset - len(bh_append_data):image_offset] = bh_append_data
        else:
            bflb_utils.printf('Append data is too long,not append!!!!!!', len(bh_append_data))
    if firmware_post_proc_get_hash_ignore(image_data) == 1:
        if force_update == False:
            bflb_utils.printf('Image hash ignore,not calculate')
            return image_data
    image_data = firmware_post_proc_enable_hash_cfg(image_data)
    if hash == None:
        hash = img_create_sha256_data(image_data[image_offset:len(image_data)])
        bflb_utils.printf('Image hash:', binascii.hexlify(hash))
    image_data[bootcfg_start + 16:bootcfg_start + 16 + 32] = hash
    return image_data


def firmware_get_file_data(file):
    with open(file, 'rb') as (fp):
        data = fp.read()
    return bytearray(data)


def firmware_save_file_data(file, data):
    datas = []
    with open(file, 'wb+') as (fp):
        fp.write(data)
        fp.close()


def firmware_post_proc(args):
    bflb_utils.printf('========= sp image create =========')
    image_data = firmware_get_file_data(args.imgfile)
    if len(image_data) % 16 != 0:
        image_data = image_data + bytearray(16 - len(image_data) % 16)
    else:
        img_hash = None
        image_data = firmware_post_proc_update_flash_crc(image_data)
        image_data = firmware_post_proc_update_clock_crc(image_data)
        image_data, img_hash = firmware_post_proc_do_encrypt(image_data, args.aeskey, args.aesiv, args.xtsmode, args.privatekey, args.publickey, args.imgfile)
        if args.publickey != None:
            image_data = firmware_post_proc_update_hash(image_data, True, args, img_hash)
        else:
            image_data = firmware_post_proc_update_hash(image_data, False, args, img_hash)
    image_data = firmware_post_proc_update_bootheader_crc(image_data)
    firmware_save_file_data(args.imgfile, image_data)


if __name__ == '__main__':
    data_bytearray = codecs.decode('42464E500100000046434647040101036699FF039F00B7E904EF0001C72052D8060232000B010B013B01BB006B01EB02EB02025000010001010002010101AB01053500000131000038FF20FF77030240770302F02C01B004B0040500FFFF030036C3DD9E5043464704040001010105000101050000010101A612AC86000144650020000000000000503100007A6345494BCABEC7307FD8F8396729EB67DDC8C63B7AD69B797B08564E982A8701000000000000000000000000000000000000D80000000000010000000000000000000000200100000001D80000000000010000000000000000000000200200000002580000000000010000000000000000000000200300000003580000000000010000D0C57503C09E750300200400000004580000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000935F92BB', 'hex')
    key_bytearray = codecs.decode('fffefdfcfbfaf9f8f7f6f5f4f3f2f1f0000102030405060708090a0b0c0d0e0f', 'hex')
    need_reverse_iv_bytearray = codecs.decode('01000000000000000000000000000000', 'hex')
    iv_bytearray = codecs.decode(reverse_iv(need_reverse_iv_bytearray), 'hex')
    img_create_encrypt_data_xts(data_bytearray, key_bytearray, iv_bytearray, 0)