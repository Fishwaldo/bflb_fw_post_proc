# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
# [GCC 9.4.0]
# Embedded file name: libs/bflb_eflash_loader.py
import os, sys, re, time, hashlib, binascii, subprocess, traceback, shutil, lzma, csv, zipfile
from importlib import reload
import portalocker, ecdsa
from Crypto.Cipher import AES
try:
    import bflb_path
except ImportError:
    from libs import bflb_path

import config as gol
from libs import bflb_version
from libs import bflb_interface_uart
from libs import bflb_interface_sdio
from libs import bflb_interface_jlink
from libs import bflb_interface_cklink
from libs import bflb_interface_openocd
from libs import bflb_efuse_boothd_create
from libs import bflb_img_loader
from libs import bflb_flash_select
from libs import bflb_utils
from libs import bflb_ecdh
from libs.bflb_utils import app_path, chip_path, open_file, eflash_loader_parser_init, convert_path
from libs.bflb_configobj import BFConfigParser
try:
    import changeconf as cgc
    conf_sign = True
except ImportError:
    conf_sign = False

try:
    from config import mutex
    th_sign = True
except ImportError:
    th_sign = False

try:
    from PySide2 import QtCore
    qt_sign = True
except ImportError:
    qt_sign = False

FLASH_LOAD_SHAKE_HAND = 'Flash load shake hand'
FLASH_ERASE_SHAKE_HAND = 'Flash erase shake hand'
try:
    from config import NUM_ERR
except ImportError:
    NUM_ERR = 5

class BflbEflashLoader(object):

    def __init__(self, chipname='bl60x', chiptype='bl60x'):
        self._bflb_auto_download = False
        self._bflb_com_img_loader = None
        self._bflb_com_if = None
        self._bflb_com_device = ''
        self._bflb_boot_speed = 0
        self._bflb_com_speed = 0
        self._bflb_com_tx_size = 0
        self._erase_time_out = 10000
        self._default_time_out = 2.0
        self._need_shake_hand = True
        self._checksum_err_retry_limit = 2
        self._csv_burn_en = False
        self._task_num = None
        self._cpu_reset = False
        self._retry_delay_after_cpu_reset = 0
        self._input_macaddr = ''
        self._macaddr_check = bytearray(0)
        self._decompress_write = False
        self._chip_type = chiptype
        self._chip_name = chipname
        self._mass_opt = False
        self._efuse_bootheader_file = ''
        self._img_create_file = ''
        self._csv_data = ''
        self._csv_file = ''
        self._skip_addr = 0
        self._skip_len = 0
        self._loader_checksum_err_str = 'FL0103'
        self._bootinfo = None
        self._isp_shakehand_timeout = 0
        self._isp_en = False
        self._macaddr_check_status = False
        self._efuse_data = bytearray(0)
        self._efuse_mask_data = bytearray(0)
        self._ecdh_shared_key = None
        self._ecdh_public_key = None
        self._ecdh_private_key = None
        self._flash2_en = False
        self._flash1_size = 0
        self._flash2_size = 0
        self._flash2_select = False
        self._com_cmds = {'change_rate':{'cmd_id':'20', 
          'data_len':'0008', 
          'callback':None}, 
         'reset':{'cmd_id':'21', 
          'data_len':'0000', 
          'callback':None}, 
         'clk_set':{'cmd_id':'22', 
          'data_len':'0000', 
          'callback':None}, 
         'opt_finish':{'cmd_id':'23', 
          'data_len':'0000', 
          'callback':None}, 
         'flash_erase':{'cmd_id':'30', 
          'data_len':'0000', 
          'callback':None}, 
         'flash_write':{'cmd_id':'31', 
          'data_len':'0100', 
          'callback':None}, 
         'flash_read':{'cmd_id':'32', 
          'data_len':'0100', 
          'callback':None}, 
         'flash_boot':{'cmd_id':'33', 
          'data_len':'0000', 
          'callback':None}, 
         'flash_xip_read':{'cmd_id':'34', 
          'data_len':'0100', 
          'callback':None}, 
         'flash_switch_bank':{'cmd_id':'35', 
          'data_len':'0100', 
          'callback':None}, 
         'flash_read_jid':{'cmd_id':'36', 
          'data_len':'0000', 
          'callback':None}, 
         'flash_read_status_reg':{'cmd_id':'37', 
          'data_len':'0000', 
          'callback':None}, 
         'flash_write_status_reg':{'cmd_id':'38', 
          'data_len':'0000', 
          'callback':None}, 
         'flash_write_check':{'cmd_id':'3a', 
          'data_len':'0000', 
          'callback':None}, 
         'flash_set_para':{'cmd_id':'3b', 
          'data_len':'0000', 
          'callback':None}, 
         'flash_chiperase':{'cmd_id':'3c', 
          'data_len':'0000', 
          'callback':None}, 
         'flash_readSha':{'cmd_id':'3d', 
          'data_len':'0100', 
          'callback':None}, 
         'flash_xip_readSha':{'cmd_id':'3e', 
          'data_len':'0100', 
          'callback':None}, 
         'flash_decompress_write':{'cmd_id':'3f', 
          'data_len':'0100', 
          'callback':None}, 
         'efuse_write':{'cmd_id':'40', 
          'data_len':'0080', 
          'callback':None}, 
         'efuse_read':{'cmd_id':'41', 
          'data_len':'0000', 
          'callback':None}, 
         'efuse_read_mac':{'cmd_id':'42', 
          'data_len':'0000', 
          'callback':None}, 
         'efuse_write_mac':{'cmd_id':'43', 
          'data_len':'0006', 
          'callback':None}, 
         'flash_xip_read_start':{'cmd_id':'60', 
          'data_len':'0080', 
          'callback':None}, 
         'flash_xip_read_finish':{'cmd_id':'61', 
          'data_len':'0000', 
          'callback':None}, 
         'log_read':{'cmd_id':'71', 
          'data_len':'0000', 
          'callback':None}, 
         'efuse_security_write':{'cmd_id':'80', 
          'data_len':'0080', 
          'callback':None}, 
         'efuse_security_read':{'cmd_id':'81', 
          'data_len':'0000', 
          'callback':None}, 
         'ecdh_get_pk':{'cmd_id':'90', 
          'data_len':'0000', 
          'callback':None}, 
         'ecdh_chanllenge':{'cmd_id':'91', 
          'data_len':'0000', 
          'callback':None}}
        self._resp_cmds = [
         "'flash_read'", "'flash_xip_read'", "'efuse_read'", 
         "'efuse_read_mac'", "'flash_readSha'", 
         "'flash_xip_readSha'", 
         "'flash_read_jid'", "'flash_read_status_reg'", "'log_read'", 
         "'ecdh_get_pk'", 
         "'ecdh_chanllenge'", "'efuse_security_read'"]

    def object_status_clear(self):
        self._bootinfo = None
        self._macaddr_check = bytearray(0)
        self._macaddr_check_status = False

    def set_config_file(self, bootheaderFile, imgCreateFile):
        self._efuse_bootheader_file = bootheaderFile
        self._img_create_file = imgCreateFile

    def set_mass_opt_flag(self, flag):
        self._mass_opt = flag

    def com_process_one_cmd(self, section, cmd_id, data_send):
        data_read = bytearray(0)
        data_len = bflb_utils.int_to_2bytearray_l(len(data_send))
        checksum = 0
        checksum += bflb_utils.bytearray_to_int(data_len[0:1]) + bflb_utils.bytearray_to_int(data_len[1:2])
        for char in data_send:
            checksum += char

        data = cmd_id + bflb_utils.int_to_2bytearray_l(checksum & 255)[0:1] + data_len + data_send
        self._bflb_com_if.if_write(data)
        if section in self._resp_cmds:
            res, data_read = self._bflb_com_if.if_deal_response()
        else:
            res = self._bflb_com_if.if_deal_ack()
        return (
         res, data_read)

    def com_inf_change_rate(self, section, newrate):
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get(section)['cmd_id'])
        cmd_len = bflb_utils.hexstr_to_bytearray(self._com_cmds.get(section)['data_len'])
        bflb_utils.printf('Process ', section, ', cmd=', binascii.hexlify(cmd_id).decode('utf-8'), ',data len=', binascii.hexlify(cmd_len).decode('utf-8'))
        baudrate = self._bflb_com_if.if_get_rate()
        oldv = bflb_utils.int_to_4bytearray_l(baudrate)
        newv = bflb_utils.int_to_4bytearray_l(newrate)
        tmp = bytearray(3)
        tmp[1] = cmd_len[1]
        tmp[2] = cmd_len[0]
        data = cmd_id + tmp + oldv + newv
        self._bflb_com_if.if_write(data)
        stime = 110 / float(baudrate) * 2
        if stime < 0.003:
            stime = 0.003
        time.sleep(stime)
        self._bflb_com_speed = newrate
        self._bflb_com_if.if_init(self._bflb_com_device, self._bflb_com_speed, self._chip_type, self._chip_name)
        return self._bflb_com_if.if_deal_ack()

    def load_helper_bin(self, interface, helper_file, do_reset=False, reset_hold_time=100, shake_hand_delay=100, reset_revert=True, cutoff_time=0, shake_hand_retry=2, isp_timeout=0):
        bflb_utils.printf('========= load eflash_loader.bin =========')
        bootinfo = None
        if interface == 'jlink':
            bflb_utils.printf('Load eflash_loader.bin via jlink')
            self._bflb_com_if.if_init(self._bflb_com_device, self._bflb_com_speed, self._chip_type, self._chip_name)
            self._bflb_com_if.reset_cpu()
            imge_fp = open_file(helper_file, 'rb')
            fw_data = bytearray(imge_fp.read())[192:] + bytearray(0)
            imge_fp.close()
            sub_module = __import__(('libs.' + self._chip_type), fromlist=[self._chip_type])
            load_addr = sub_module.jlink_load_cfg.jlink_load_addr
            self._bflb_com_if.if_raw_write(load_addr, fw_data)
            pc = fw_data[4:8]
            pc = bytes([pc[3], pc[2], pc[1], pc[0]])
            msp = fw_data[0:4]
            msp = bytes([msp[3], msp[2], msp[1], msp[0]])
            self._bflb_com_if.set_pc_msp(binascii.hexlify(pc), binascii.hexlify(msp).decode('utf-8'))
            time.sleep(0.01)
            self._bflb_com_if.if_close()
            return (True, bootinfo, '')
        if interface == 'openocd':
            bflb_utils.printf('Load eflash_loader.bin via openocd')
            self._bflb_com_if.if_init(self._bflb_com_device, self._bflb_sn_device, self._bflb_com_speed, self._chip_type, self._chip_name)
            self._bflb_com_if.halt_cpu()
            imge_fp = open_file(helper_file, 'rb')
            fw_data = bytearray(imge_fp.read())[192:] + bytearray(0)
            imge_fp.close()
            sub_module = __import__(('libs.' + self._chip_type), fromlist=[self._chip_type])
            load_addr = sub_module.openocd_load_cfg.openocd_load_addr
            self._bflb_com_if.if_raw_write(load_addr, fw_data)
            pc = fw_data[4:8]
            pc = bytes([pc[3], pc[2], pc[1], pc[0]])
            msp = fw_data[0:4]
            msp = bytes([msp[3], msp[2], msp[1], msp[0]])
            self._bflb_com_if.set_pc_msp(binascii.hexlify(pc), binascii.hexlify(msp).decode('utf-8'))
            return (True, bootinfo, '')
        if interface == 'cklink':
            bflb_utils.printf('Load eflash_loader.bin via cklink')
            self._bflb_com_if.if_init(self._bflb_com_device, self._bflb_sn_device, self._bflb_com_speed, self._chip_type, self._chip_name)
            self._bflb_com_if.halt_cpu()
            imge_fp = open_file(helper_file, 'rb')
            fw_data = bytearray(imge_fp.read())[192:] + bytearray(0)
            imge_fp.close()
            sub_module = __import__(('libs.' + self._chip_type), fromlist=[self._chip_type])
            load_addr = sub_module.openocd_load_cfg.openocd_load_addr
            self._bflb_com_if.if_raw_write(load_addr, fw_data)
            pc = fw_data[4:8]
            pc = bytes([pc[3], pc[2], pc[1], pc[0]])
            msp = fw_data[0:4]
            msp = bytes([msp[3], msp[2], msp[1], msp[0]])
            self._bflb_com_if.set_pc_msp(binascii.hexlify(pc), binascii.hexlify(msp).decode('utf-8'))
            self._bflb_com_if.resume_cpu()
            return (True, bootinfo, '')
        if interface == 'uart' or interface == 'sdio':
            ret = True
            bflb_utils.printf('Load eflash_loader.bin via %s' % interface)
            start_time = time.time() * 1000
            ret, bootinfo, res = self._bflb_com_img_loader.img_load_process(self._bflb_com_device, self._bflb_boot_speed, self._bflb_boot_speed, helper_file, '', None, do_reset, reset_hold_time, shake_hand_delay, reset_revert, cutoff_time, shake_hand_retry, isp_timeout, True, self._bootinfo)
            bflb_utils.printf('Load helper bin time cost(ms): ', time.time() * 1000 - start_time)
            return (ret, bootinfo, res)

    def load_shake_hand(self, interface, do_reset=False, reset_hold_time=100, shake_hand_delay=100, reset_revert=True, cutoff_time=0, shake_hand_retry=2, isp_timeout=0):
        bflb_utils.printf('========= shakehand with bootrom =========')
        if interface == 'jlink':
            bflb_utils.printf('shakehand via jlink')
            self._bflb_com_if.if_init(self._bflb_com_device, self._bflb_com_speed, self._chip_type, self._chip_name)
            return ('OK', None)
        if interface == 'openocd':
            bflb_utils.printf('shakehand via openocd')
            self._bflb_com_if.if_init(self._bflb_com_device, self._bflb_sn_device, self._bflb_com_speed, self._chip_type, self._chip_name)
            return ('OK', None)
        if interface == 'cklink':
            bflb_utils.printf('shakehand via cklink')
            self._bflb_com_if.if_init(self._bflb_com_device, self._bflb_sn_device, self._bflb_com_speed, self._chip_type, self._chip_name)
            return ('OK', None)
        if interface == 'uart':
            ret = True
            bflb_utils.printf('shakehand via uart')
            ret = self._bflb_com_img_loader.img_load_shake_hand(self._bflb_com_device, self._bflb_boot_speed, self._bflb_boot_speed, do_reset, reset_hold_time, shake_hand_delay, reset_revert, cutoff_time, shake_hand_retry, isp_timeout)
            return (ret, None)

    def get_boot_info(self, interface, helper_file, do_reset=False, reset_hold_time=100, shake_hand_delay=100, reset_revert=True, cutoff_time=0, shake_hand_retry=2, isp_timeout=0):
        bflb_utils.printf('========= get_boot_info =========')
        bootinfo = ''
        if interface == 'uart':
            ret = True
            start_time = time.time() * 1000
            ret, bootinfo = self._bflb_com_img_loader.img_get_bootinfo(self._bflb_com_device, self._bflb_boot_speed, self._bflb_boot_speed, helper_file, '', None, do_reset, reset_hold_time, shake_hand_delay, reset_revert, cutoff_time, shake_hand_retry, isp_timeout)
            chipid = None
            if ret is True:
                bootinfo = bootinfo.decode('utf-8')
                if self._chip_type == 'bl702' or self._chip_type == 'bl702l':
                    chipid = bootinfo[32:34] + bootinfo[34:36] + bootinfo[36:38] + bootinfo[38:40] + bootinfo[40:42] + bootinfo[42:44] + bootinfo[44:46] + bootinfo[46:48]
                else:
                    chipid = bootinfo[34:36] + bootinfo[32:34] + bootinfo[30:32] + bootinfo[28:30] + bootinfo[26:28] + bootinfo[24:26]
                bflb_utils.printf('========= ChipID: ', chipid, ' =========')
                bflb_utils.printf('Get bootinfo time cost(ms): ', time.time() * 1000 - start_time)
            if qt_sign:
                if th_sign:
                    if QtCore.QThread.currentThread().objectName():
                        with mutex:
                            num = str(QtCore.QThread.currentThread().objectName())
                            gol.list_chipid[int(num) - 1] = chipid
                            if chipid is not None:
                                gol.list_chipid_check[int(num) - 1] = chipid
                            for i, j in gol.list_download_check_last:
                                if chipid is not None and chipid == i and j is True:
                                    return (
                                     True, bootinfo, 'repeat_burn')

                            if chipid is not None:
                                return (
                                 True, bootinfo, 'OK')
                            return (False, bootinfo, 'chipid_is_none')
            return (
             ret, bootinfo, 'OK')
        bflb_utils.printf('interface not fit')
        return (False, bootinfo, '')

    def error_code_print(self, code):
        bflb_utils.set_error_code(code, self._task_num)
        bflb_utils.printf('ErrorCode: ' + code + ', ErrorMsg: ' + bflb_utils.eflash_loader_error_code[code])

    def img_load_shake_hand(self):
        isp_sh_time = 0
        if self._chip_type == 'bl702' or self._chip_type == 'bl702l':
            isp_sh_time = self._isp_shakehand_timeout
        self._bflb_com_if.if_init(self._bflb_com_device, self._bflb_com_speed, self._chip_type, self._chip_name)
        if self._bflb_com_if.if_shakehand(do_reset=False, reset_hold_time=100,
          shake_hand_delay=100,
          reset_revert=True,
          cutoff_time=0,
          shake_hand_retry=2,
          isp_timeout=isp_sh_time,
          boot_load=False) != 'OK':
            self.error_code_print('0001')
            return False
        self._need_shake_hand = False
        return True

    def operate_finish(self, shakehand=0):
        bflb_utils.printf('Boot from flash')
        if shakehand != 0:
            bflb_utils.printf(FLASH_ERASE_SHAKE_HAND)
            if self.img_load_shake_hand() is False:
                return False
        else:
            if self._bflb_com_if is not None:
                self._bflb_com_if.if_close()
            self._bflb_com_if.if_init(self._bflb_com_device, self._bflb_com_speed, self._chip_type, self._chip_name)
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get('opt_finish')['cmd_id'])
        ret, dmy = self.com_process_one_cmd('opt_finish', cmd_id, bytearray(0))
        if ret.startswith('OK'):
            return True
        self.error_code_print('000D')
        return False

    def boot_from_flash(self, shakehand=0):
        bflb_utils.printf('Boot from flash')
        if shakehand != 0:
            bflb_utils.printf(FLASH_ERASE_SHAKE_HAND)
            if self.img_load_shake_hand() is False:
                return False
        else:
            if self._bflb_com_if is not None:
                self._bflb_com_if.if_close()
            self._bflb_com_if.if_init(self._bflb_com_device, self._bflb_com_speed, self._chip_type, self._chip_name)
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get('flash_boot')['cmd_id'])
        ret, dmy = self.com_process_one_cmd('flash_boot', cmd_id, bytearray(0))
        if ret.startswith('OK'):
            return True
        self.error_code_print('003F')
        return False

    def clear_boot_status(self, shakehand=0):
        bflb_utils.printf('Clear boot status at hbn rsvd register')
        if shakehand != 0:
            bflb_utils.printf(FLASH_ERASE_SHAKE_HAND)
            if self.img_load_shake_hand() is False:
                return False
        data = bytearray(12)
        data[0] = 80
        data[1] = 0
        data[2] = 8
        data[3] = 0
        data[4] = 8
        data[5] = 241
        data[6] = 0
        data[7] = 32
        data[8] = 0
        data[9] = 0
        data[10] = 0
        data[11] = 0
        self._bflb_com_if.if_write(data)
        self._bflb_com_if.if_deal_ack(dmy_data=False)
        return True

    def reset_cpu(self, shakehand=0):
        bflb_utils.printf('CPU Reset')
        if shakehand != 0:
            bflb_utils.printf(FLASH_ERASE_SHAKE_HAND)
            if self.img_load_shake_hand() is False:
                return False
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get('reset')['cmd_id'])
        ret, dmy = self.com_process_one_cmd('reset', cmd_id, bytearray(0))
        if ret.startswith('OK'):
            return True
        self.error_code_print('0004')
        return False

    def clock_pll_set(self, shakehand, irq_en, speed, clk_para):
        bflb_utils.printf('Clock PLL set')
        if shakehand != 0:
            bflb_utils.printf('clock set shake hand')
            if self.img_load_shake_hand() is False:
                return False
        start_time = time.time() * 1000
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get('clk_set')['cmd_id'])
        irq_enable = bytearray(4)
        load_speed = bytearray(4)
        if irq_en:
            irq_enable = b'\x01\x00\x00\x00'
        load_speed = bflb_utils.int_to_4bytearray_l(int(speed))
        data_send = irq_enable + load_speed + clk_para
        if len(clk_para) > 0:
            bflb_utils.printf('clock para:')
            bflb_utils.printf(binascii.hexlify(clk_para).decode('utf-8'))
        try_cnt = 0
        while True:
            ret, dmy = self.com_process_one_cmd('clk_set', cmd_id, data_send)
            if ret.startswith('OK'):
                break
            if try_cnt < self._checksum_err_retry_limit:
                bflb_utils.printf('Retry')
                try_cnt += 1
            else:
                self.error_code_print('000C')
                return False

        bflb_utils.printf('Set clock time cost(ms): ', time.time() * 1000 - start_time)
        self._bflb_com_if.if_init(self._bflb_com_device, speed, self._chip_type, self._chip_name)
        self._bflb_com_if.if_clear_buf()
        time.sleep(0.01)
        return True

    def close_port(self, shakehand=0):
        if self._bflb_com_if is not None:
            self._bflb_com_if.if_close()

    def efuse_compare(self, read_data, maskdata, write_data):
        i = 0
        for i in range(len(read_data)):
            compare_data = read_data[i] & maskdata[i]
            if compare_data & write_data[i] != write_data[i]:
                bflb_utils.printf('compare fail: ', i)
                bflb_utils.printf(read_data[i], write_data[i])
                return False

        return True

    def get_ecdh_shared_key(self, shakehand=0):
        bflb_utils.printf('========= get ecdh shared key =========')
        publickey_file = 'utils/pem/publickey_uecc.pem'
        if shakehand != 0:
            bflb_utils.printf('Shake hand')
            ret = self.img_load_shake_hand()
            if ret is False:
                return
        else:
            tmp_ecdh = bflb_ecdh.BflbEcdh()
            self._ecdh_public_key = tmp_ecdh.create_public_key()
            self._ecdh_private_key = binascii.hexlify(tmp_ecdh.ecdh.private_key.to_string()).decode('utf-8')
            bflb_utils.printf('ecdh public key')
            bflb_utils.printf(self._ecdh_public_key)
            bflb_utils.printf('ecdh private key')
            bflb_utils.printf(self._ecdh_private_key)
            cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get('ecdh_get_pk')['cmd_id'])
            data_send = bytearray.fromhex(self._ecdh_public_key)
            ret, data_read = self.com_process_one_cmd('ecdh_get_pk', cmd_id, data_send)
            if ret.startswith('OK') is True:
                self._ecdh_peer_public_key = binascii.hexlify(data_read).decode('utf-8')
                bflb_utils.printf('ecdh peer key')
                bflb_utils.printf(self._ecdh_peer_public_key)
                self._ecdh_shared_key = tmp_ecdh.create_shared_key(self._ecdh_peer_public_key[0:128])
                bflb_utils.printf('ecdh shared key')
                bflb_utils.printf(self._ecdh_shared_key)
                cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get('ecdh_chanllenge')['cmd_id'])
                data_send = bytearray(0)
                ret, data_read = self.com_process_one_cmd('ecdh_chanllenge', cmd_id, data_send)
                if ret.startswith('OK') is True:
                    bflb_utils.printf('challenge data')
                    bflb_utils.printf(binascii.hexlify(data_read).decode('utf-8'))
                    encrypted_data = data_read[0:32]
                    signature = data_read[32:96]
                    signature_r = data_read[32:64]
                    signature_s = data_read[64:96]
                    vk = ecdsa.VerifyingKey.from_pem(open_file('utils\\pem\\room_root_publickey_ecc.pem').read())
                    try:
                        ret = vk.verify(signature, (self.ecdh_decrypt_data(encrypted_data)),
                          hashfunc=(hashlib.sha256),
                          sigdecode=(ecdsa.util.sigdecode_string))
                    except Exception as err:
                        try:
                            bflb_utils.printf(err)
                        finally:
                            err = None
                            del err

                    if ret is True:
                        return True
                    bflb_utils.printf('Challenge verify fail')
                    return False
                else:
                    bflb_utils.printf('Challenge ack fail')
                    return False
            else:
                bflb_utils.printf('Get shared key fail')
                return False

    def ecdh_encrypt_data(self, data):
        cryptor = AES.new(bytearray.fromhex(self._ecdh_shared_key[0:32]), AES.MODE_CBC, bytearray(16))
        ciphertext = cryptor.encrypt(data)
        return ciphertext

    def ecdh_decrypt_data(self, data):
        cryptor = AES.new(bytearray.fromhex(self._ecdh_shared_key[0:32]), AES.MODE_CBC, bytearray(16))
        plaintext = cryptor.decrypt(data)
        return plaintext

    def efuse_read_mac_addr_process(self, shakehand=1, callback=None):
        readdata = bytearray(0)
        macLen = 6
        if self._chip_type == 'bl702' or self._chip_type == 'bl702l':
            macLen = 8
        if shakehand != 0:
            bflb_utils.printf(FLASH_LOAD_SHAKE_HAND)
            if self.img_load_shake_hand() is False:
                return (False, None)
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get('efuse_read_mac')['cmd_id'])
        bflb_utils.printf('Read mac addr ')
        ret, data_read = self.com_process_one_cmd('efuse_read_mac', cmd_id, bytearray(0))
        if ret.startswith('OK') is False:
            self.error_code_print('0023')
            return (False, None)
        readdata += data_read
        crcarray = bflb_utils.get_crc32_bytearray(readdata[:macLen])
        if crcarray != readdata[macLen:macLen + 4]:
            bflb_utils.printf(binascii.hexlify(crcarray))
            bflb_utils.printf(binascii.hexlify(readdata[macLen:macLen + 4]))
            self.error_code_print('0025')
            return (False, None)
        return (
         True, readdata[:macLen])

    def efuse_write_mac_addr_process(self, macaddr, shakehand=1, callback=None):
        if shakehand != 0:
            bflb_utils.printf(FLASH_LOAD_SHAKE_HAND)
            if self.img_load_shake_hand() is False:
                return (False, None)
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get('efuse_write_mac')['cmd_id'])
        ret, data_read = self.com_process_one_cmd('efuse_write_mac', cmd_id, macaddr)
        bflb_utils.printf('Write mac addr ')
        if ret.startswith('OK') is False:
            self.error_code_print('0024')
            return (False, None)
        return (True, None)

    def efuse_read_main_process(self, start_addr, data_len, shakehand=0, file=None, security_read=False):
        readdata = bytearray(0)
        if shakehand != 0:
            bflb_utils.printf(FLASH_LOAD_SHAKE_HAND)
            if self.img_load_shake_hand() is False:
                return (False, None)
        elif security_read:
            cmd_name = 'efuse_security_read'
        else:
            cmd_name = 'efuse_read'
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get(cmd_name)['cmd_id'])
        data_send = bflb_utils.int_to_4bytearray_l(start_addr) + bflb_utils.int_to_4bytearray_l(data_len)
        ret, data_read = self.com_process_one_cmd(cmd_name, cmd_id, data_send)
        bflb_utils.printf('Read efuse ')
        if ret.startswith('OK') is False:
            self.error_code_print('0020')
            return (False, None)
        readdata += data_read
        if security_read:
            readdata = self.ecdh_decrypt_data(readdata)
        bflb_utils.printf('Finished')
        if file is not None:
            fp = open_file(file, 'wb+')
            fp.write(readdata)
            fp.close()
        return (
         True, readdata)

    def efuse_load_main_process(self, file, maskfile, efusedata, efusedatamask, verify=0, security_write=False):
        if efusedata != bytearray(0):
            bflb_utils.printf('Load data')
            efuse_data = efusedata
            mask_data = efusedatamask
        else:
            if file is not None:
                bflb_utils.printf('Load file: ', file)
                fp = open_file(file, 'rb')
                efuse_data = bytearray(fp.read()) + bytearray(0)
                fp.close()
                fp = open_file(maskfile, 'rb')
                mask_data = bytearray(fp.read()) + bytearray(0)
                fp.close()
                if len(efuse_data) > 4096:
                    bflb_utils.printf('Decrypt efuse data')
                    efuse_data = efuse_data[4096:]
                    security_key, security_iv = bflb_utils.get_security_key()
                    efuse_data = bflb_utils.aes_decrypt_data(efuse_data, security_key, security_iv, 0)
                else:
                    efuse_data = self._efuse_data
                    mask_data = self._efuse_mask_data
            elif security_write:
                if self.get_ecdh_shared_key() is not True:
                    return False
                else:
                    bflb_utils.printf('Load efuse 0')
                    if security_write:
                        cmd_name = 'efuse_security_write'
                    else:
                        cmd_name = 'efuse_write'
                    cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get(cmd_name)['cmd_id'])
                    data_send = efuse_data[0:124] + bytearray(4)
                    if security_write:
                        data_send = self.ecdh_encrypt_data(data_send)
                    data_send = bflb_utils.int_to_4bytearray_l(0) + data_send
                    ret, dmy = self.com_process_one_cmd(cmd_name, cmd_id, data_send)
                    if ret.startswith('OK') is False:
                        bflb_utils.printf('Write Fail')
                        self.error_code_print('0021')
                        return False
                    if verify >= 1:
                        ret, read_data = self.efuse_read_main_process(0, 128,
                          shakehand=0,
                          file=None,
                          security_read=security_write)
                        if ret is True and self.efuse_compare(read_data, mask_data[0:124] + bytearray(4), efuse_data[0:124] + bytearray(4)):
                            bflb_utils.printf('Verify success')
                        else:
                            bflb_utils.printf('Read: ')
                            bflb_utils.printf(binascii.hexlify(read_data[0:124]).decode('utf-8'))
                            bflb_utils.printf('Expected: ')
                            bflb_utils.printf(binascii.hexlify(efuse_data[0:124]).decode('utf-8'))
                            bflb_utils.printf('Verify fail')
                            self.error_code_print('0022')
                            return False
                    data_send = bytearray(12) + efuse_data[124:128]
                    if security_write:
                        data_send = self.ecdh_encrypt_data(data_send)
                    data_send = bflb_utils.int_to_4bytearray_l(112) + data_send
                    ret, dmy = self.com_process_one_cmd(cmd_name, cmd_id, data_send)
                    if ret.startswith('OK') is False:
                        bflb_utils.printf('Write Fail')
                        self.error_code_print('0021')
                        return False
                    if verify >= 1:
                        ret, read_data = self.efuse_read_main_process(112, 16,
                          shakehand=0,
                          file=None,
                          security_read=security_write)
                        if ret is True and self.efuse_compare(read_data, bytearray(12) + mask_data[124:128], bytearray(12) + efuse_data[124:128]):
                            bflb_utils.printf('Verify success')
                        else:
                            bflb_utils.printf('Read: ')
                            bflb_utils.printf(binascii.hexlify(read_data[12:16]))
                            bflb_utils.printf('Expected: ')
                            bflb_utils.printf(binascii.hexlify(efuse_data[124:128]))
                            bflb_utils.printf('Verify fail')
                            self.error_code_print('0022')
                            return False
                if len(efuse_data) > 128:
                    bflb_utils.printf('Load efuse 1')
                    if security_write:
                        cmd_name = 'efuse_security_write'
                    else:
                        cmd_name = 'efuse_write'
                    cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get(cmd_name)['cmd_id'])
                    data_send = efuse_data[128:252] + bytearray(4)
                    if security_write:
                        data_send = self.ecdh_encrypt_data(data_send)
                    data_send = bflb_utils.int_to_4bytearray_l(128) + data_send
                    ret, dmy = self.com_process_one_cmd(cmd_name, cmd_id, data_send)
                    if ret.startswith('OK') is False:
                        bflb_utils.printf('Write Fail')
                        self.error_code_print('0021')
                        return False
                    if verify >= 1:
                        ret, read_data = self.efuse_read_main_process(128, 128,
                          shakehand=0,
                          file=None,
                          security_read=security_write)
                        if ret is True and self.efuse_compare(read_data, mask_data[128:252] + bytearray(4), efuse_data[128:252] + bytearray(4)):
                            bflb_utils.printf('Verify success')
                        else:
                            bflb_utils.printf('Verify fail')
                            self.error_code_print('0022')
                            return False
                    data_send = bytearray(12) + efuse_data[252:256]
                    if security_write:
                        data_send = self.ecdh_encrypt_data(data_send)
                    data_send = bflb_utils.int_to_4bytearray_l(240) + data_send
                    ret, dmy = self.com_process_one_cmd(cmd_name, cmd_id, data_send)
                    if ret.startswith('OK') is False:
                        bflb_utils.printf('Write Fail')
                        self.error_code_print('0021')
                        return False
                    if verify >= 1:
                        ret, read_data = self.efuse_read_main_process(240, 16,
                          shakehand=0,
                          file=None,
                          security_read=security_write)
                        if ret is True and self.efuse_compare(read_data, bytearray(12) + mask_data[252:256], bytearray(12) + efuse_data[252:256]):
                            bflb_utils.printf('Verify success')
            else:
                bflb_utils.printf('Verify fail')
                self.error_code_print('0022')
            bflb_utils.printf('Finished')
            return True

    def efuse_load_specified(self, file, maskfile, efusedata, efusedatamask, verify=0, shakehand=0, security_write=False):
        bflb_utils.printf('========= efuse load =========')
        if shakehand != 0:
            bflb_utils.printf('Efuse load shake hand')
            ret = self.img_load_shake_hand()
            if ret is False:
                return False
        ret = self.efuse_load_main_process(file, maskfile, efusedata, efusedatamask, verify, security_write)
        return ret

    def efuse_load_macaddr(self, macaddr, verify=0, shakehand=0, security_write=False):
        bflb_utils.printf('========= efuse macaddr load =========')
        cnt = 0
        mac = macaddr[:12]
        if security_write:
            if self.get_ecdh_shared_key() is not True:
                return False
        else:
            for i in range(0, 12):
                temp = int(mac[i:i + 1], 16)
                for j in range(0, 4):
                    if temp & 1 << j == 0:
                        cnt += 1

            bflb_utils.printf('mac check cnt: 0x%02X' % cnt)
            data_efuse = mac[10:12] + mac[8:10] + mac[6:8] + mac[4:6] + mac[2:4] + mac[0:2] + '%02X' % cnt
            efusedatastr = data_efuse
            efusemaskdata = bytearray(128)
            zeromac = bytearray(6)
            ret, efusedata = self.efuse_read_main_process(0, 128,
              shakehand,
              file=None,
              security_read=security_write)
            if ret is False:
                return False
                efusedata = bytearray(efusedata)
                sub_module = __import__(('libs.' + self._chip_type), fromlist=[self._chip_type])
                slot0_addr = sub_module.efuse_cfg_keys.efuse_mac_slot_offset['slot0']
                slot1_addr = sub_module.efuse_cfg_keys.efuse_mac_slot_offset['slot1']
                slot2_addr = sub_module.efuse_cfg_keys.efuse_mac_slot_offset['slot2']
                if efusedata[int(slot0_addr, 10):int(slot0_addr, 10) + 6] == zeromac:
                    bflb_utils.printf('Efuse load mac slot 0')
                    efuseaddrstr = slot0_addr
            elif efusedata[int(slot1_addr, 10):int(slot1_addr, 10) + 6] == zeromac:
                bflb_utils.printf('Efuse load mac slot 1')
                efuseaddrstr = slot1_addr
            else:
                if efusedata[int(slot2_addr, 10):int(slot2_addr, 10) + 6] == zeromac:
                    bflb_utils.printf('Efuse load mac slot 2')
                    efuseaddrstr = slot2_addr
                else:
                    bflb_utils.printf('Efuse mac slot 0/1/2 all not empty')
                    return False
        for num in range(int(efuseaddrstr), int(efuseaddrstr) + int(len(efusedatastr) / 2)):
            efusedata[num] |= bytearray.fromhex(efusedatastr)[num - int(efuseaddrstr)]
            efusemaskdata[num] |= 255

        for num in range(0, 128):
            if efusedata[num] != 0:
                efusemaskdata[num] |= 255

        ret = self.efuse_load_specified(None, None, efusedata, efusemaskdata, verify, 0, security_write)
        if ret is False:
            return False
        return ret

    def efuse_load_702_macaddr(self, macaddr, verify=0, shakehand=0, security_write=False):
        bflb_utils.printf('========= efuse 702 macaddr load =========')
        cnt = 0
        mac = macaddr[:16]
        if security_write:
            if self.get_ecdh_shared_key() is not True:
                return False
        else:
            for i in range(0, 16):
                temp = int(mac[i:i + 1], 16)
                for j in range(0, 4):
                    if temp & 1 << j == 0:
                        cnt += 1

            bflb_utils.printf('mac check cnt: 0x%02X' % cnt)
            efusedatastr = mac
            efusemaskdata = bytearray(128)
            zeromac = bytearray(8)
            ret, efusedata = self.efuse_read_main_process(0, 128,
              shakehand,
              file=None,
              security_read=security_write)
            if ret is False:
                return False
                efusedata = bytearray(efusedata)
                sub_module = __import__(('libs.' + self._chip_type), fromlist=[self._chip_type])
                slot0_addr = sub_module.efuse_cfg_keys.efuse_mac_slot_offset['slot0']
                slot1_addr = sub_module.efuse_cfg_keys.efuse_mac_slot_offset['slot1']
                slot2_addr = sub_module.efuse_cfg_keys.efuse_mac_slot_offset['slot2']
                if efusedata[int(slot0_addr, 10):int(slot0_addr, 10) + 8] == zeromac:
                    bflb_utils.printf('Efuse load mac slot 0')
                    efuseaddrstr = slot0_addr
                    data_cnt = cnt
            elif efusedata[int(slot1_addr, 10):int(slot1_addr, 10) + 8] == zeromac:
                bflb_utils.printf('Efuse load mac slot 1')
                efuseaddrstr = slot1_addr
                data_cnt = cnt << 6
            else:
                if efusedata[int(slot2_addr, 10):int(slot2_addr, 10) + 8] == zeromac:
                    bflb_utils.printf('Efuse load mac slot 2')
                    efuseaddrstr = slot2_addr
                    data_cnt = cnt << 12
                else:
                    bflb_utils.printf('Efuse mac slot 0/1/2 all not empty')
                    return False
        efusedata[116:120] = bflb_utils.int_to_4bytearray_l(data_cnt)
        for num in range(int(efuseaddrstr), int(efuseaddrstr) + int(len(efusedatastr) / 2)):
            efusedata[num] |= bytearray.fromhex(efusedatastr)[num - int(efuseaddrstr)]
            efusemaskdata[num] |= 255

        for num in range(0, 128):
            if efusedata[num] != 0:
                efusemaskdata[num] |= 255

        ret = self.efuse_load_specified(None, None, efusedata, efusemaskdata, verify, 0, security_write)
        if ret is False:
            return False
        return ret

    def efuse_load_aes_key(self, type, value, verify=0, shakehand=0, security_write=False):
        bflb_utils.printf('========= efuse key load =========')
        sub_module = __import__(('libs.' + self._chip_type), fromlist=[self._chip_type])
        efusedata, efusemaskdata = sub_module.efuse_data_create.efuse_data_create(type, value)
        if shakehand != 0:
            bflb_utils.printf('Efuse load shake hand')
            ret = self.img_load_shake_hand()
            if ret is False:
                return False
        ret = self.efuse_load_main_process(None, None, efusedata, efusemaskdata, verify, security_write)
        return ret

    def efuse_load_data_process(self, data, addr, func=0, verify=0, shakehand=0, security_write=False):
        bflb_utils.printf('========= efuse data load =========')
        if shakehand is not False:
            bflb_utils.printf(FLASH_LOAD_SHAKE_HAND)
            if self.img_load_shake_hand() is False:
                return (False, None)
        if security_write:
            if self.get_ecdh_shared_key() is not True:
                return False
        bflb_utils.printf('Load efuse data')
        try:
            if security_write:
                cmd_name = 'efuse_security_write'
            else:
                cmd_name = 'efuse_write'
            cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get(cmd_name)['cmd_id'])
            start_addr = int(addr) - int(addr) % 16
            efuse_data = bytearray(int(addr) % 16) + bytearray.fromhex(data) + bytearray(16 - (int(addr) + int(len(data) / 2)) % 16)
            bflb_utils.printf('efuse_data: ', start_addr)
            bflb_utils.printf(binascii.hexlify(efuse_data))
            mask_data = bytearray(len(efuse_data))
            if func > 0:
                bflb_utils.printf('Read and check efuse data')
                ret, read_data = self.efuse_read_main_process(start_addr, (len(efuse_data)),
                  0,
                  file=None,
                  security_read=security_write)
                i = int(addr) - start_addr
                for i in range(int(addr) - start_addr, int(addr) - start_addr + int(len(data) / 2)):
                    compare_data = read_data[i] & efuse_data[i]
                    if compare_data != read_data[i]:
                        bflb_utils.printf("The efuse data to be written can't overwrite the efuse area at ", i + start_addr)
                        bflb_utils.printf(read_data[i])
                        bflb_utils.printf(efuse_data[i])
                        return False

            if security_write:
                efuse_data = self.ecdh_encrypt_data(efuse_data)
            data_send = bflb_utils.int_to_4bytearray_l(start_addr) + efuse_data
            ret, dmy = self.com_process_one_cmd(cmd_name, cmd_id, data_send)
            if ret.startswith('OK') is False:
                bflb_utils.printf('Write Fail')
                self.error_code_print('0021')
                return False
            for num in range(0, len(efuse_data)):
                if efuse_data[num] != 0:
                    mask_data[num] |= 255

        except Exception as e:
            try:
                bflb_utils.printf(e)
                return False
            finally:
                e = None
                del e

        if verify >= 1:
            ret, read_data = self.efuse_read_main_process(start_addr, (len(efuse_data)),
              0,
              file=None,
              security_read=security_write)
            if ret is True and self.efuse_compare(read_data, mask_data, efuse_data):
                bflb_utils.printf('Verify success')
            else:
                bflb_utils.printf('Read: ')
                bflb_utils.printf(binascii.hexlify(read_data))
                bflb_utils.printf('Expected: ')
                bflb_utils.printf(binascii.hexlify(efuse_data))
                bflb_utils.printf('Verify fail')
                bflb_utils.printf(binascii.hexlify(mask_data))
                self.error_code_print('0022')
                return False

    def flash_read_jedec_id_process(self, callback=None):
        bflb_utils.printf('========= flash read jedec ID =========')
        readdata = bytearray(0)
        if self._need_shake_hand is not False:
            bflb_utils.printf(FLASH_LOAD_SHAKE_HAND)
            if self.img_load_shake_hand() is False:
                return (False, None)
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get('flash_read_jid')['cmd_id'])
        ret, data_read = self.com_process_one_cmd('flash_read_jid', cmd_id, bytearray(0))
        bflb_utils.printf('Read flash jedec ID ')
        if ret.startswith('OK') is False:
            self.error_code_print('0030')
            return (False, None)
        readdata += data_read
        bflb_utils.printf('readdata: ')
        bflb_utils.printf(binascii.hexlify(readdata))
        bflb_utils.printf('Finished')
        return (True, readdata[:4])

    def flash_read_status_reg_process(self, cmd, len, callback=None):
        bflb_utils.printf('========= flash read status register =========')
        readdata = bytearray(0)
        if self._need_shake_hand is not False:
            bflb_utils.printf(FLASH_LOAD_SHAKE_HAND)
            if self.img_load_shake_hand() is False:
                return (False, None)
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get('flash_read_status_reg')['cmd_id'])
        data_send = bflb_utils.int_to_4bytearray_l(int(cmd, 16)) + bflb_utils.int_to_4bytearray_l(len)
        ret, data_read = self.com_process_one_cmd('flash_read_status_reg', cmd_id, data_send)
        bflb_utils.printf('Read flash status register ')
        if ret.startswith('OK') is False:
            self.error_code_print('0031')
            return (False, None)
        readdata += data_read
        bflb_utils.printf('readdata: ')
        bflb_utils.printf(binascii.hexlify(readdata))
        bflb_utils.printf('Finished')
        return (True, readdata)

    def flash_write_status_reg_process(self, cmd, len, write_data, callback=None):
        bflb_utils.printf('========= flash write status register =========')
        if self._need_shake_hand is not False:
            bflb_utils.printf(FLASH_LOAD_SHAKE_HAND)
            if self.img_load_shake_hand() is False:
                return (False, 'Flash load shake hand fail')
        bflb_utils.printf('write_data ', write_data)
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get('flash_write_status_reg')['cmd_id'])
        data_send = bflb_utils.int_to_4bytearray_l(int(cmd, 16)) + bflb_utils.int_to_4bytearray_l(len) + bflb_utils.int_to_4bytearray_l(int(write_data, 16))
        ret, data_read = self.com_process_one_cmd('flash_write_status_reg', cmd_id, data_send)
        bflb_utils.printf('Write flash status register ')
        if ret.startswith('OK') is False:
            self.error_code_print('0032')
            return (False, 'Write fail')
        bflb_utils.printf('Finished')
        return (True, None)

    def flash_erase_main_process(self, start_addr, end_addr, shakehand=0):
        bflb_utils.printf('========= flash erase =========')
        bflb_utils.printf('Erase flash from ', hex(start_addr), ' to ', hex(end_addr))
        if shakehand != 0:
            bflb_utils.printf(FLASH_ERASE_SHAKE_HAND)
            if self.img_load_shake_hand() is False:
                bflb_utils.printf('Shake hand fail')
                return False
        start_time = time.time() * 1000
        if not self._chip_type == 'bl602':
            if self._chip_type == 'bl702' or self._chip_type == 'bl702l':
                self._bflb_com_if.if_set_rx_timeout(self._default_time_out)
        else:
            self._bflb_com_if.if_set_rx_timeout(self._erase_time_out / 1000)
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get('flash_erase')['cmd_id'])
        data_send = bflb_utils.int_to_4bytearray_l(start_addr) + bflb_utils.int_to_4bytearray_l(end_addr)
        try_cnt = 0
        while True:
            ret, dmy = self.com_process_one_cmd('flash_erase', cmd_id, data_send)
            if ret.startswith('OK'):
                break
            else:
                if ret.startswith('PD'):
                    bflb_utils.printf('erase pending')
                    while True:
                        ret = self._bflb_com_if.if_deal_ack()
                        if ret.startswith('PD'):
                            bflb_utils.printf('erase pending')
                        else:
                            self._bflb_com_if.if_set_rx_timeout(0.02)
                            self._bflb_com_if.if_read(1000)
                            break
                        if time.time() * 1000 - start_time > self._erase_time_out:
                            bflb_utils.printf('erase timeout')
                            break

                if ret.startswith('OK'):
                    break
            if try_cnt < self._checksum_err_retry_limit:
                bflb_utils.printf('Retry')
                try_cnt += 1
            else:
                bflb_utils.printf('Erase Fail')
                self._bflb_com_if.if_set_rx_timeout(self._default_time_out)
                self.error_code_print('0034')
                return False

        bflb_utils.printf('Erase time cost(ms): ', time.time() * 1000 - start_time)
        self._bflb_com_if.if_set_rx_timeout(self._default_time_out)
        return True

    def flash_chiperase_main_process(self, shakehand=0):
        bflb_utils.printf('Flash Chip Erase All')
        if shakehand != 0:
            bflb_utils.printf(FLASH_ERASE_SHAKE_HAND)
            if self.img_load_shake_hand() is False:
                bflb_utils.printf('Shake hand fail')
                return False
        start_time = time.time() * 1000
        if not self._chip_type == 'bl602':
            if self._chip_type == 'bl702' or self._chip_type == 'bl702l':
                self._bflb_com_if.if_set_rx_timeout(self._default_time_out)
        else:
            self._bflb_com_if.if_set_rx_timeout(self._erase_time_out / 1000)
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get('flash_chiperase')['cmd_id'])
        try_cnt = 0
        while True:
            ret, dmy = self.com_process_one_cmd('flash_chiperase', cmd_id, bytearray(0))
            if ret.startswith('OK'):
                break
            else:
                if ret.startswith('PD'):
                    bflb_utils.printf('erase pending')
                    while True:
                        ret = self._bflb_com_if.if_deal_ack()
                        if ret.startswith('PD'):
                            bflb_utils.printf('erase pending')
                        else:
                            self._bflb_com_if.if_set_rx_timeout(0.02)
                            self._bflb_com_if.if_read(1000)
                            break
                        if time.time() * 1000 - start_time > self._erase_time_out:
                            bflb_utils.printf('erase timeout')
                            break

                if ret.startswith('OK'):
                    break
            if try_cnt < self._checksum_err_retry_limit:
                bflb_utils.printf('Retry')
                try_cnt += 1
            else:
                bflb_utils.printf('Erase Fail')
                self._bflb_com_if.if_set_rx_timeout(self._default_time_out)
                self.error_code_print('0033')
                return False

        bflb_utils.printf('Chip erase time cost(ms): ', time.time() * 1000 - start_time)
        self._bflb_com_if.if_set_rx_timeout(self._default_time_out)
        return True

    def flash_loader_cut_flash_bin(self, file, addr, flash1_size):
        flash1_bin = 'flash1.bin'
        flash2_bin = 'flash2.bin'
        fp = open_file(file, 'rb')
        flash_data = bytearray(fp.read())
        fp.close()
        flash_data_len = len(flash_data)
        if flash1_size < addr + flash_data_len:
            if flash1_size > addr:
                flash1_data = flash_data[0:flash1_size - addr]
                flash2_data = flash_data[flash1_size - addr:flash_data_len]
                fp = open_file(flash1_bin, 'wb+')
                fp.write(flash1_data)
                fp.close()
                fp = open_file(flash2_bin, 'wb+')
                fp.write(flash2_data)
                fp.close()
                return (flash1_bin, len(flash1_data), flash2_bin, len(flash2_data))
        return ('', 0, '', 0)

    def flash_switch_bank_process(self, bank, shakehand=0):
        bflb_utils.printf('Flash Switch Bank')
        if shakehand != 0:
            bflb_utils.printf('Flash switch bank shake hand')
            if self.img_load_shake_hand() is False:
                bflb_utils.printf('Shake hand fail')
                return False
        else:
            start_time = time.time() * 1000
            self._bflb_com_if.if_set_rx_timeout(self._erase_time_out / 1000)
            cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get('flash_switch_bank')['cmd_id'])
            data_send = bflb_utils.int_to_4bytearray_l(bank)
            ret, dmy = self.com_process_one_cmd('flash_switch_bank', cmd_id, data_send)
            if ret.startswith('OK') is False:
                bflb_utils.printf('Switch Fail')
                self._bflb_com_if.if_set_rx_timeout(self._default_time_out)
                self.error_code_print('0042')
                return False
                bflb_utils.printf('Switch bank time cost(ms): ', time.time() * 1000 - start_time)
                self._bflb_com_if.if_set_rx_timeout(self._default_time_out)
                if bank == 0:
                    self._flash2_select = False
            else:
                self._flash2_select = True
        return True

    def flash_set_para_main_process(self, flash_pin, flash_para, shakehand=0):
        bflb_utils.printf('Set flash config ')
        if flash_para != bytearray(0):
            if flash_para[13:14] == b'\xff':
                bflb_utils.printf('Skip set flash para due to flash id is 0xFF')
                return True
        if shakehand != 0:
            bflb_utils.printf('Flash set para shake hand')
            if self.img_load_shake_hand() is False:
                return False
        start_time = time.time() * 1000
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get('flash_set_para')['cmd_id'])
        data_send = bflb_utils.int_to_4bytearray_l(flash_pin) + flash_para
        try_cnt = 0
        while True:
            ret, dmy = self.com_process_one_cmd('flash_set_para', cmd_id, data_send)
            if ret.startswith('OK'):
                break
            if try_cnt < self._checksum_err_retry_limit:
                bflb_utils.printf('Retry')
                try_cnt += 1
            else:
                self.error_code_print('003B')
                return False

        bflb_utils.printf('Set para time cost(ms): ', time.time() * 1000 - start_time)
        return True

    def flash_read_main_process(self, start_addr, flash_data_len, shakehand=0, file=None, callback=None):
        bflb_utils.printf('========= flash read =========')
        i = 0
        cur_len = 0
        readdata = bytearray(0)
        if shakehand != 0:
            bflb_utils.printf(FLASH_LOAD_SHAKE_HAND)
            if self.img_load_shake_hand() is False:
                return (False, None)
        start_time = time.time() * 1000
        log = ''
        while i < flash_data_len:
            cur_len = flash_data_len - i
            if cur_len > self._bflb_com_tx_size - 8:
                cur_len = self._bflb_com_tx_size - 8
            else:
                cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get('flash_read')['cmd_id'])
                data_send = bflb_utils.int_to_4bytearray_l(i + start_addr) + bflb_utils.int_to_4bytearray_l(cur_len)
                try_cnt = 0
                while True:
                    ret, data_read = self.com_process_one_cmd('flash_read', cmd_id, data_send)
                    if ret.startswith('OK'):
                        break
                    if try_cnt < self._checksum_err_retry_limit:
                        bflb_utils.printf('Retry')
                        try_cnt += 1
                    else:
                        self.error_code_print('0035')
                        return (False, None)

                i += cur_len
                log += 'Read ' + str(i) + '/' + str(flash_data_len)
                if len(log) > 50:
                    bflb_utils.printf(log)
                    log = ''
                else:
                    log += '\n'
            if callback is not None:
                callback(i, flash_data_len, 'APP_VR')
            readdata += data_read

        bflb_utils.printf(log)
        bflb_utils.printf('Flash read time cost(ms): ', time.time() * 1000 - start_time)
        bflb_utils.printf('Finished')
        if file is not None:
            fp = open_file(file, 'wb+')
            fp.write(readdata)
            fp.close()
        return (
         True, readdata)

    def flash_xip_read_main_process(self, start_addr, flash_data_len, shakehand=0, file=None, callback=None):
        bflb_utils.printf('========= flash read =========')
        i = 0
        cur_len = 0
        readdata = bytearray(0)
        if shakehand != 0:
            bflb_utils.printf(FLASH_LOAD_SHAKE_HAND)
            if self.img_load_shake_hand() is False:
                return (False, None)
        start_time = time.time() * 1000
        log = ''
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get('flash_xip_read_start')['cmd_id'])
        ret, dmy = self.com_process_one_cmd('flash_xip_read_start', cmd_id, bytearray(0))
        if ret.startswith('OK') is False:
            self.error_code_print('0039')
            return (False, None)
        while i < flash_data_len:
            cur_len = flash_data_len - i
            if cur_len > self._bflb_com_tx_size - 8:
                cur_len = self._bflb_com_tx_size - 8
            else:
                cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get('flash_xip_read')['cmd_id'])
                data_send = bflb_utils.int_to_4bytearray_l(i + start_addr) + bflb_utils.int_to_4bytearray_l(cur_len)
                try_cnt = 0
                while True:
                    ret, data_read = self.com_process_one_cmd('flash_xip_read', cmd_id, data_send)
                    if ret.startswith('OK'):
                        break
                    if try_cnt < self._checksum_err_retry_limit:
                        bflb_utils.printf('Retry')
                        try_cnt += 1
                    else:
                        self.error_code_print('0035')
                        return (False, None)

                i += cur_len
                log += 'Read ' + str(i) + '/' + str(flash_data_len)
                if len(log) > 50:
                    bflb_utils.printf(log)
                    log = ''
                else:
                    log += '\n'
            if callback is not None:
                callback(i, flash_data_len, 'APP_VR')
            readdata += data_read

        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get('flash_xip_read_finish')['cmd_id'])
        ret, dmy = self.com_process_one_cmd('flash_xip_read_finish', cmd_id, bytearray(0))
        if ret.startswith('OK') is False:
            self.error_code_print('0039')
            return (False, None)
        bflb_utils.printf(log)
        bflb_utils.printf('Flash read time cost(ms): ', time.time() * 1000 - start_time)
        bflb_utils.printf('Finished')
        if file is not None:
            fp = open_file(file, 'wb+')
            fp.write(readdata)
            fp.close()
        return (
         True, readdata)

    def flash_read_sha_main_process(self, start_addr, flash_data_len, shakehand=0, file=None, callback=None):
        readdata = bytearray(0)
        if shakehand != 0:
            bflb_utils.printf(FLASH_LOAD_SHAKE_HAND)
            if self.img_load_shake_hand() is False:
                return (False, None)
        start_time = time.time() * 1000
        log = ''
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get('flash_readSha')['cmd_id'])
        data_send = bflb_utils.int_to_4bytearray_l(start_addr) + bflb_utils.int_to_4bytearray_l(flash_data_len)
        try_cnt = 0
        while True:
            ret, data_read = self.com_process_one_cmd('flash_readSha', cmd_id, data_send)
            if ret.startswith('OK'):
                break
            if try_cnt < self._checksum_err_retry_limit:
                bflb_utils.printf('Retry')
                try_cnt += 1
            else:
                self.error_code_print('0038')
                return (False, None)

        log += 'Read Sha256/' + str(flash_data_len)
        if callback is not None:
            callback(flash_data_len, flash_data_len, 'APP_VR')
        readdata += data_read
        bflb_utils.printf(log)
        bflb_utils.printf('Flash readsha time cost(ms): ', time.time() * 1000 - start_time)
        bflb_utils.printf('Finished')
        if file is not None:
            fp = open_file(file, 'wb+')
            fp.write(readdata)
            fp.close()
        return (
         True, readdata)

    def flash_xip_read_sha_main_process(self, start_addr, flash_data_len, shakehand=0, file=None, callback=None):
        readdata = bytearray(0)
        if shakehand != 0:
            bflb_utils.printf(FLASH_LOAD_SHAKE_HAND)
            if self.img_load_shake_hand() is False:
                return (False, None)
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get('flash_xip_read_start')['cmd_id'])
        ret, dmy = self.com_process_one_cmd('flash_xip_read_start', cmd_id, bytearray(0))
        if ret.startswith('OK') is False:
            self.error_code_print('0039')
            return (False, None)
        start_time = time.time() * 1000
        log = ''
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get('flash_xip_readSha')['cmd_id'])
        data_send = bflb_utils.int_to_4bytearray_l(start_addr) + bflb_utils.int_to_4bytearray_l(flash_data_len)
        try_cnt = 0
        while True:
            ret, data_read = self.com_process_one_cmd('flash_xip_readSha', cmd_id, data_send)
            if ret.startswith('OK'):
                break
            if try_cnt < self._checksum_err_retry_limit:
                bflb_utils.printf('Retry')
                try_cnt += 1
            else:
                bflb_utils.printf('Read Fail')
                cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get('flash_xip_read_finish')['cmd_id'])
                ret, dmy = self.com_process_one_cmd('flash_xip_read_finish', cmd_id, bytearray(0))
                if ret.startswith('OK') is False:
                    self.error_code_print('0039')
                    return (False, None)
                return (False, None)

        log += 'Read Sha256/' + str(flash_data_len)
        if callback is not None:
            callback(flash_data_len, flash_data_len, 'APP_VR')
        readdata += data_read
        bflb_utils.printf(log)
        bflb_utils.printf('Flash xip readsha time cost(ms): ', time.time() * 1000 - start_time)
        bflb_utils.printf('Finished')
        if file is not None:
            fp = open_file(file, 'wb+')
            fp.write(readdata)
            fp.close()
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get('flash_xip_read_finish')['cmd_id'])
        ret, dmy = self.com_process_one_cmd('flash_xip_read_finish', cmd_id, bytearray(0))
        if ret.startswith('OK') is False:
            self.error_code_print('0039')
            return (False, None)
        return (
         True, readdata)

    def flash_write_check_main_process(self, shakehand=0):
        bflb_utils.printf('Write check')
        if shakehand != 0:
            bflb_utils.printf(FLASH_LOAD_SHAKE_HAND)
            if self.img_load_shake_hand() is False:
                return False
        cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get('flash_write_check')['cmd_id'])
        try_cnt = 0
        while True:
            retry = 0
            if self._decompress_write:
                retry = 10
            ret, dmy = self.com_process_one_cmd('flash_write_check', cmd_id, bytearray(0))
            if ret.startswith('OK'):
                break
            if try_cnt < self._checksum_err_retry_limit + retry:
                bflb_utils.printf('Retry')
                try_cnt += 1
            else:
                self.error_code_print('0037')
                return False

        return True

    def flash_load_xz_compress(self, file):
        try:
            xz_filters = [
             {'id':lzma.FILTER_LZMA2, 
              'dict_size':32768}]
            fp = open_file(file, 'rb')
            data = bytearray(fp.read())
            fp.close()
            flash_data = lzma.compress(data, check=(lzma.CHECK_CRC32), filters=xz_filters)
            flash_data_len = len(flash_data)
        except Exception as e:
            try:
                bflb_utils.printf(e)
                return (False, None, None)
            finally:
                e = None
                del e

        return (
         True, flash_data, flash_data_len)

    def flash_load_main_process(self, file, start_addr, erase=1, callback=None):
        fp = open_file(file, 'rb')
        flash_data = bytearray(fp.read())
        fp.close()
        flash_data_len = len(flash_data)
        i = 0
        cur_len = 0
        if erase == 1:
            ret = self.flash_erase_main_process(start_addr, start_addr + flash_data_len - 1)
            if ret is False:
                return False
        else:
            start_time = time.time() * 1000
            log = ''
            if self._decompress_write:
                if flash_data_len > 4096:
                    self._bflb_com_if.if_set_rx_timeout(30.0)
                    start_addr |= 2147483648
                    cmd_name = 'flash_decompress_write'
                    ret, flash_data, flash_data_len = self.flash_load_xz_compress(file)
                    if ret is False:
                        bflb_utils.printf('Flash write data xz fail')
                        self._bflb_com_if.if_set_rx_timeout(self._default_time_out)
                        return False
                    if time.time() * 1000 - start_time > 2200:
                        bflb_utils.printf(FLASH_LOAD_SHAKE_HAND)
                        if self.img_load_shake_hand() is False:
                            return False
                    elif time.time() * 1000 - start_time > 1800:
                        time.sleep(0.5)
                        bflb_utils.printf(FLASH_LOAD_SHAKE_HAND)
                        if self.img_load_shake_hand() is False:
                            return False
                        bflb_utils.printf('decompress flash load ', flash_data_len)
                    else:
                        pass
            cmd_name = 'flash_write'
        while i < flash_data_len:
            cur_len = flash_data_len - i
            if cur_len > self._bflb_com_tx_size - 8:
                cur_len = self._bflb_com_tx_size - 8
            cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get(cmd_name)['cmd_id'])
            data_send = bflb_utils.int_to_4bytearray_l(i + start_addr) + flash_data[i:i + cur_len]
            start_addr &= 2147483647
            try_cnt = 0
            while True:
                ret, dmy = self.com_process_one_cmd(cmd_name, cmd_id, data_send)
                if ret.startswith('OK'):
                    break
                if try_cnt < self._checksum_err_retry_limit:
                    bflb_utils.printf('Retry')
                    try_cnt += 1
                else:
                    self.error_code_print('0036')
                    self._bflb_com_if.if_set_rx_timeout(self._default_time_out)
                    return False

            i += cur_len
            log = 'Load ' + str(i) + '/' + str(flash_data_len) + ' {"progress":' + str(i * 100 // flash_data_len) + '}'
            bflb_utils.printf(log)
            if callback is not None and flash_data_len > 200:
                callback(i, flash_data_len, 'APP_WR')

        bflb_utils.printf(log)
        if self.flash_write_check_main_process() is False:
            bflb_utils.printf('Flash write check fail')
            self._bflb_com_if.if_set_rx_timeout(self._default_time_out)
            return False
        self._bflb_com_if.if_set_rx_timeout(self._default_time_out)
        bflb_utils.printf('Flash load time cost(ms): ', time.time() * 1000 - start_time)
        bflb_utils.printf('Finished')
        return True

    def get_flash_pin_from_bootinfo(self, chiptype, bootinfo):
        if chiptype == 'bl808':
            sw_usage_data = bootinfo[22:24] + bootinfo[20:22] + bootinfo[18:20] + bootinfo[16:18]
            sw_usage_data = int(sw_usage_data, 16)
            return sw_usage_data >> 14 & 31
        if chiptype == 'bl616' or chiptype == 'wb03':
            sw_usage_data = bootinfo[22:24] + bootinfo[20:22] + bootinfo[18:20] + bootinfo[16:18]
            sw_usage_data = int(sw_usage_data, 16)
            return sw_usage_data >> 14 & 63
        if chiptype == 'bl702l':
            dev_info_data = bootinfo[30:32] + bootinfo[28:30] + bootinfo[26:28] + bootinfo[24:26]
            dev_info_data = int(dev_info_data, 16)
            flash_cfg = dev_info_data >> 26 & 7
            sf_reverse = dev_info_data >> 29 & 1
            sf_swap_cfg = dev_info_data >> 22 & 3
            if flash_cfg == 0:
                return 0
            if sf_reverse == 0:
                return sf_swap_cfg + 1
            return sf_swap_cfg + 5
        return 128

    def setOpenFile_zip(self, packet_file):
        bflb_utils.printf('Unpack file')
        filename = packet_file
        try:
            if filename:
                efuse_burn = 'false'
                eflash_loader_file = ''
                zip_file = zipfile.ZipFile(filename)
                zip_list = zip_file.namelist()
                for f in zip_list:
                    if f.find('efusedata.bin') != -1:
                        efuse_burn = 'true'
                    if f.find('eflash_loader_cfg') != -1:
                        eflash_loader_file = os.path.join(app_path, 'chips', f)
                    zip_file.extract(f, os.path.join(app_path, 'chips'))

                zip_file.close()
                cfg = BFConfigParser()
                cfg.read(eflash_loader_file)
                if cfg.has_option('EFUSE_CFG', 'burn_en'):
                    cfg.set('EFUSE_CFG', 'burn_en', efuse_burn)
                    cfg.write(eflash_loader_file, 'w')
                bflb_utils.printf('Unpack Success')
        except Exception as err:
            try:
                error = str(err)
                bflb_utils.printf('Unpack fail: ' + error)
                self.error_code_print('000E')
            finally:
                err = None
                del err

    def flash_cfg_option(self, read_flash_id, flash_para_file, flash_set, id_valid_flag, binfile, cfgfile, cfg, create_img_callback=None, create_simple_callback=None):
        ret = bflb_flash_select.flash_bootheader_config_check(self._chip_name, self._chip_type, read_flash_id, convert_path(binfile), flash_para_file)
        if ret is False:
            bflb_utils.printf('flashcfg not match first')
            if self.is_conf_exist(read_flash_id) is True:
                bflb_utils.update_cfg(cfg, 'FLASH_CFG', 'flash_id', read_flash_id)
                if isinstance(cfgfile, BFConfigParser) == False:
                    cfg.write(cfgfile, 'w+')
                if create_img_callback is not None:
                    create_img_callback()
                elif create_simple_callback is not None:
                    create_simple_callback()
            else:
                self.error_code_print('003D')
                return False
            ret = bflb_flash_select.flash_bootheader_config_check(self._chip_name, self._chip_type, read_flash_id, convert_path(binfile), flash_para_file)
            if ret is False:
                bflb_utils.printf('flashcfg not match again')
                self.error_code_print('0040')
                return False
        if flash_para_file:
            if id_valid_flag != '80':
                bflb_utils.printf('flash para file: ', flash_para_file)
                fp = open_file(flash_para_file, 'rb')
                flash_para = bytearray(fp.read())
                fp.close()
                ret = self.flash_set_para_main_process(flash_set, flash_para, self._need_shake_hand)
                self._need_shake_hand = False
                if ret is False:
                    return False

    def flash_load_tips(self):
        bflb_utils.printf('########################################################################')
        bflb_utils.printf('请按照以下描述排查问题：')
        bflb_utils.printf('是否降低烧录波特率到500K测试过')
        bflb_utils.printf('烧写文件的大小是否超过Flash所能存储的最大空间')
        bflb_utils.printf('Flash是否被写保护')
        bflb_utils.printf('########################################################################')

    def flash_load_opt(self, file, start_addr, erase=1, verify=0, shakehand=0, callback=None):
        bflb_utils.printf('========= flash load =========')
        if shakehand != 0:
            bflb_utils.printf(FLASH_LOAD_SHAKE_HAND)
            if self.img_load_shake_hand() is False:
                return False
        if self._flash2_select is True:
            start_addr -= self._flash1_size
        if self._chip_type == 'bl808':
            if self._mass_opt is False:
                fp = open_file(file, 'rb')
                flash_data = bytearray(fp.read())
                fp.close()
                flash_data_len = len(flash_data)
                end_addr = start_addr + flash_data_len - 1
                if start_addr <= 4096:
                    if end_addr > 4096:
                        ret, flash_read_data = self.flash_read_main_process(4096, 4096, 0, None, callback)
                        if flash_read_data[0:4] == bflb_utils.int_to_4bytearray_b(1112298054):
                            bflb_utils.printf('RF para already write at flash 0x1000 addr, replace it.')
                            flash_data[4096:8192] = flash_read_data[0:4096]
                            fp = open_file(file, 'wb')
                            fp.write(flash_data)
                            fp.close()
        ret = self.flash_load_main_process(file, start_addr, erase, callback)
        if ret is False:
            bflb_utils.printf('Flash load fail')
            return ret
        fw_sha256 = ''
        fp = open_file(file, 'rb')
        flash_data = fp.read()
        fp.close()
        flash_data_len = len(flash_data)
        if flash_data_len > 2097152:
            self._bflb_com_if.if_set_rx_timeout(2.0 * (flash_data_len / 2097152 + 1))
        sh = hashlib.sha256()
        sh.update(flash_data)
        fw_sha256 = sh.hexdigest()
        fw_sha256 = bflb_utils.hexstr_to_bytearray(fw_sha256)
        bflb_utils.printf('Sha caled by host: ', binascii.hexlify(fw_sha256).decode('utf-8'))
        del sh
        bflb_utils.printf('xip mode Verify')
        ret, read_data = self.flash_xip_read_sha_main_process(start_addr, flash_data_len, 0, None, callback)
        bflb_utils.printf('Sha caled by dev: ', binascii.hexlify(read_data).decode('utf-8'))
        if ret is True and read_data == fw_sha256:
            bflb_utils.printf('Verify success')
        else:
            bflb_utils.printf('Verify fail')
            self.flash_load_tips()
            self.error_code_print('003E')
            ret = False
        if verify > 0:
            fp = open_file(file, 'rb')
            flash_data = bytearray(fp.read())
            fp.close()
            flash_data_len = len(flash_data)
            ret, read_data = self.flash_read_main_process(start_addr, flash_data_len, 0, None, callback)
            if ret is True and read_data == flash_data:
                bflb_utils.printf('Verify success')
            else:
                bflb_utils.printf('Verify fail')
                self.flash_load_tips()
                self.error_code_print('003E')
                ret = False
            bflb_utils.printf('sbus mode Verify')
            ret, read_data = self.flash_read_sha_main_process(start_addr, flash_data_len, 0, None, callback)
            bflb_utils.printf('Sha caled by dev: ', binascii.hexlify(read_data).decode('utf-8'))
            if ret is True and read_data == fw_sha256:
                bflb_utils.printf('Verify success')
        else:
            bflb_utils.printf('Verify fail')
            self.flash_load_tips()
            self.error_code_print('003E')
            ret = False
        self._bflb_com_if.if_set_rx_timeout(self._default_time_out)
        return ret

    def flash_load_specified(self, file, start_addr, erase=1, verify=0, shakehand=0, callback=None):
        ret = False
        if self._skip_len > 0:
            bflb_utils.printf('skip flash file, skip addr 0x%08X, skip len 0x%08X' % (
             self._skip_addr, self._skip_len))
            fp = open_file(file, 'rb')
            flash_data = fp.read()
            fp.close()
            flash_data_len = len(flash_data)
            if self._skip_addr <= start_addr:
                if self._skip_addr + self._skip_len > start_addr and self._skip_addr + self._skip_len < start_addr + flash_data_len:
                    addr = self._skip_addr + self._skip_len
                    data = flash_data[self._skip_addr + self._skip_len - start_addr:]
                    filename, ext = os.path.splitext(file)
                    file_temp = os.path.join(app_path, filename + '_skip' + ext)
                    fp = open(file_temp, 'wb')
                    fp.write(data)
                    fp.close()
                    ret = self.flash_load_opt(file_temp, addr, erase, verify, shakehand, callback)
                elif self._skip_addr > start_addr and self._skip_addr + self._skip_len < start_addr + flash_data_len:
                    addr = start_addr
                    data = flash_data[:self._skip_addr - start_addr]
                    filename, ext = os.path.splitext(file)
                    file_temp = os.path.join(app_path, filename + '_skip1' + ext)
                    fp = open(file_temp, 'wb')
                    fp.write(data)
                    fp.close()
                    ret = self.flash_load_opt(file_temp, addr, erase, verify, shakehand, callback)
                    addr = self._skip_addr + self._skip_len
                    data = flash_data[self._skip_addr + self._skip_len - start_addr:]
                    filename, ext = os.path.splitext(file)
                    file_temp = os.path.join(app_path, filename + '_skip2' + ext)
                    fp = open(file_temp, 'wb')
                    fp.write(data)
                    fp.close()
                    ret = self.flash_load_opt(file_temp, addr, erase, verify, shakehand, callback)
            elif self._skip_addr > start_addr and self._skip_addr < start_addr + flash_data_len and self._skip_addr + self._skip_len >= start_addr + flash_data_len:
                addr = start_addr
                data = flash_data[:self._skip_addr - start_addr]
                filename, ext = os.path.splitext(file)
                file_temp = os.path.join(app_path, filename + '_skip' + ext)
                fp = open(file_temp, 'wb')
                fp.write(data)
                fp.close()
                ret = self.flash_load_opt(file_temp, addr, erase, verify, shakehand, callback)
            else:
                if self._skip_addr <= start_addr:
                    if self._skip_addr + self._skip_len >= start_addr + flash_data_len:
                        return True
                ret = self.flash_load_opt(file, start_addr, erase, verify, shakehand, callback)
        else:
            ret = self.flash_load_opt(file, start_addr, erase, verify, shakehand, callback)
        return ret

    def log_read_process(self, shakehand=1, callback=None):
        readdata = bytearray(0)
        try:
            if shakehand != 0:
                bflb_utils.printf(FLASH_LOAD_SHAKE_HAND)
                if self.img_load_shake_hand() is False:
                    bflb_utils.printf('Shake hand redo')
            cmd_id = bflb_utils.hexstr_to_bytearray(self._com_cmds.get('log_read')['cmd_id'])
            ret, data_read = self.com_process_one_cmd('log_read', cmd_id, bytearray(0))
            bflb_utils.printf('Read log ')
            if ret.startswith('OK') is False:
                bflb_utils.printf('Read Fail')
                return (False, None)
            readdata += data_read
            bflb_utils.printf('log: ')
            bflb_utils.printf('========================================================')
            bflb_utils.printf(readdata.decode('utf-8'))
            bflb_utils.printf('========================================================')
            bflb_utils.printf('Finished')
        except Exception as e:
            try:
                bflb_utils.printf(e)
                self.error_code_print('0006')
                traceback.print_exc(limit=NUM_ERR, file=(sys.stdout))
                return (False, None)
            finally:
                e = None
                del e

        return (
         True, readdata)

    def get_active_fwbin_addr(self, ptaddr1, ptaddr2, entry_name, shakehand=1, callback=None):
        fwaddr = 0
        maxlen = 0
        ptdata = bytearray(0)
        table_count = 0
        try:
            if shakehand != 0:
                bflb_utils.printf(FLASH_LOAD_SHAKE_HAND)
                if self.img_load_shake_hand() is False:
                    return (False, 0)
            else:
                bflb_utils.printf('read partition 1 0x', ptaddr1)
                ret, ptdata1 = self.flash_read_main_process(int(ptaddr1, 16), 768, 0, None, callback)
                if ret is False:
                    bflb_utils.printf('read pt 1 data fail')
                bflb_utils.printf('read partition 2 0x', ptaddr2)
                ret, ptdata2 = self.flash_read_main_process(int(ptaddr2, 16), 768, 0, None, callback)
                if ret is False:
                    bflb_utils.printf('read pt 2 data fail')
                sub_module = __import__(('libs.' + self._chip_type), fromlist=[self._chip_type])
                ret1, table_count1, age1 = sub_module.partition_cfg_do.check_pt_data(ptdata1)
                if ret1 is False:
                    bflb_utils.printf('pt table 1 check fail')
                ret2, table_count2, age2 = sub_module.partition_cfg_do.check_pt_data(ptdata2)
                if ret2 is False:
                    bflb_utils.printf('pt table 2 check fail')
                if ret1 is not False and ret2 is not False:
                    if age1 >= age2:
                        ptdata = ptdata1[16:]
                        table_count = table_count1
                    else:
                        ptdata = ptdata2[16:]
                        table_count = table_count2
                else:
                    if ret1 is not False:
                        ptdata = ptdata1[16:]
                        table_count = table_count1
                    else:
                        if ret2 is not False:
                            ptdata = ptdata2[16:]
                            table_count = table_count2
                        else:
                            bflb_utils.printf('pt table all check fail')
                            return (False, 0, 0)
            for i in range(table_count):
                if entry_name == ptdata[i * 36 + 3:i * 36 + 3 + len(entry_name)].decode(encoding='utf-8'):
                    addr_start = 0
                    if bflb_utils.bytearray_to_int(ptdata[i * 36 + 2:i * 36 + 3]) != 0:
                        addr_start = i * 36 + 16
                    else:
                        addr_start = i * 36 + 12
                    fwaddr = bflb_utils.bytearray_to_int(ptdata[addr_start + 0:addr_start + 1]) + (bflb_utils.bytearray_to_int(ptdata[addr_start + 1:addr_start + 2]) << 8) + (bflb_utils.bytearray_to_int(ptdata[addr_start + 2:addr_start + 3]) << 16) + (bflb_utils.bytearray_to_int(ptdata[addr_start + 3:addr_start + 4]) << 24)
                    maxlen = bflb_utils.bytearray_to_int(ptdata[addr_start + 0 + 8:addr_start + 1 + 8]) + (bflb_utils.bytearray_to_int(ptdata[addr_start + 1 + 8:addr_start + 2 + 8]) << 8) + (bflb_utils.bytearray_to_int(ptdata[addr_start + 2 + 8:addr_start + 3 + 8]) << 16) + (bflb_utils.bytearray_to_int(ptdata[addr_start + 3 + 8:addr_start + 4 + 8]) << 24)

        except Exception as e:
            try:
                bflb_utils.printf(e)
                traceback.print_exc(limit=NUM_ERR, file=(sys.stdout))
                return (False, 0, 0)
            finally:
                e = None
                del e

        return (
         True, fwaddr, maxlen)

    def load_romfs_data(self, data, addr, verify, shakehand=1, callback=None):
        romfs_path = os.path.join(chip_path, self._chip_name, 'romfs')
        dst_img_name = os.path.join(chip_path, self._chip_name, 'img_create_iot/media.bin')
        if not os.path.exists(romfs_path):
            os.makedirs(romfs_path)
        private_key_file = os.path.join(romfs_path, 'private_key')
        f = open(private_key_file, 'w+')
        f.write(data)
        f.close()
        exe = None
        if os.name == 'nt':
            exe = os.path.join(app_path, 'utils/genromfs', 'genromfs.exe')
        else:
            if os.name == 'posix':
                machine = os.uname().machine
                if machine == 'x86_64':
                    exe = os.path.join(app_path, 'utils/genromfs', 'genromfs_amd64')
                else:
                    if machine == 'armv7l':
                        exe = os.path.join(app_path, 'utils/genromfs', 'genromfs_armel')
        if exe is None:
            bflb_utils.printf('NO supported genromfs exe for your platform!')
            return -1
        dir = os.path.abspath(romfs_path)
        dst = os.path.abspath(dst_img_name)
        CREATE_NO_WINDOW = 134217728
        subprocess.call(['exe', "'-d'", 'dir', "'-f'", 'dst'], creationflags=CREATE_NO_WINDOW)
        bflb_utils.printf('========= programming romfs ', dst_img_name, ' to ', hex(addr))
        ret = self.flash_load_specified(dst_img_name, addr, 1, verify, 0, callback)
        return ret

    def load_firmware_bin(self, file, verify, shakehand=1, callback=None):
        entry_name = ''
        sub_module = __import__(('libs.' + self._chip_type), fromlist=[self._chip_type])
        pt_addr1 = sub_module.partition_cfg_do.partition1_addr
        pt_addr2 = sub_module.partition_cfg_do.partition2_addr
        entry_name = sub_module.partition_cfg_do.fireware_name
        ret, fwaddr, max_len = self.get_active_fwbin_addr(pt_addr1, pt_addr2, entry_name, shakehand, callback)
        if ret is False:
            bflb_utils.printf('get active fwbin addr fail')
            return False
        if os.path.getsize(file) > max_len:
            bflb_utils.printf('fwbin size > max len ', os.path.getsize(file))
            return False
        bflb_utils.printf('========= programming firmare ', file, ' to ', hex(fwaddr))
        ret = self.flash_load_specified(file, fwaddr, 1, verify, 0, callback)
        return ret

    def get_suitable_conf_name(self, cfg_dir, flash_id):
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

    def get_factory_config_info(self, file, output_file):
        version = 'ver0.0.1'
        csv_mac = ''
        info_dict = {
         'ProductKey': "''", 
         'DeviceName': "''", 
         'DeviceSecret': "''", 
         'ProductSecret': "''", 
         'ProductID': "''"}
        lock_file = open('lock.txt', 'w+')
        portalocker.lock(lock_file, portalocker.LOCK_EX)
        try:
            with open(file, 'r') as (csvfile):
                reader = csv.DictReader(csvfile)
                list_csv = []
                list_product_secret = []
                list_product_id = []
                for row in reader:
                    list_product_secret.append(info_dict['ProductSecret'])
                    list_product_id.append(info_dict['ProductID'])
                    if 'Burned' not in row:
                        if csv_mac == '':
                            burnkey = {'Burned': 'P'}
                            row.update(burnkey)
                        list_csv.append(row)
                    else:
                        if row.get('Burned', '') != 'Y' and row.get('Burned', '') != 'P':
                            if csv_mac == '':
                                row['Burned'] = 'P'
                            list_csv.append(row)
                        else:
                            list_csv.append(row)
                            continue
                    if csv_mac == '':
                        info_dict['ProductKey'] = row.get('ProductKey', '')
                        csv_mac = info_dict['DeviceName'] = row.get('DeviceName', '')
                        info_dict['DeviceSecret'] = row.get('DeviceSecret', '')
                        info_dict['ProductSecret'] = row.get('ProductSecret', '')
                        info_dict['ProductID'] = row.get('ProductID', '')
                        if len(set(list_product_secret)) > 1:
                            print('Error: ProductSecret is not same')
                            return (False, csv_mac)
                        if len(set(list_product_id)) > 1:
                            print('Error: ProductID is not same')
                            return (False, csv_mac)
                        if re.match('^([0-9a-fA-F]{2,2}){6,6}$', csv_mac) is None:
                            print('Error: ' + csv_mac + ' is not a valid MAC address')
                            return (False, csv_mac)
                        self._csv_data = csv_mac
                        self._csv_file = file

                if csv_mac == '':
                    bflb_utils.printf('All facotry info used up!')
                    lock_file.close()
                    os.remove('lock.txt')
                    return (False, csv_mac)
                ret, efusedata = self.efuse_read_main_process(0, 128,
                  (self._need_shake_hand),
                  file=None,
                  security_read=False)
                if ret is False:
                    return (
                     False, csv_mac)
                efusedata = bytearray(efusedata)
                data_efuse = csv_mac[10:12] + csv_mac[8:10] + csv_mac[6:8] + csv_mac[4:6] + csv_mac[2:4] + csv_mac[0:2]
                mac_bytearray = bflb_utils.hexstr_to_bytearray(data_efuse)
                sub_module = __import__(('libs.' + self._chip_type), fromlist=[self._chip_type])
                slot0_addr = sub_module.efuse_cfg_keys.efuse_mac_slot_offset['slot0']
                slot1_addr = sub_module.efuse_cfg_keys.efuse_mac_slot_offset['slot1']
                slot2_addr = sub_module.efuse_cfg_keys.efuse_mac_slot_offset['slot2']
                bflb_utils.printf(mac_bytearray)
                bflb_utils.printf(efusedata[int(slot0_addr, 10):int(slot0_addr, 10) + 6])
                bflb_utils.printf(efusedata[int(slot1_addr, 10):int(slot1_addr, 10) + 6])
                bflb_utils.printf(efusedata[int(slot2_addr, 10):int(slot2_addr, 10) + 6])
                if efusedata[int(slot2_addr, 10):int(slot2_addr, 10) + 6] == mac_bytearray:
                    bflb_utils.printf('DeviceName was already write at efuse mac slot 2')
                    return (False, csv_mac)
                if efusedata[int(slot1_addr, 10):int(slot1_addr, 10) + 6] == mac_bytearray:
                    bflb_utils.printf('DeviceName was already write at efuse mac slot 1')
                    return (False, csv_mac)
                if efusedata[int(slot0_addr, 10):int(slot0_addr, 10) + 6] == mac_bytearray:
                    bflb_utils.printf('DeviceName was already write at efuse mac slot 0')
                    return (False, csv_mac)
            with open(file, 'w', newline='') as (f):
                headers = ["'ProductKey'", "'DeviceName'", "'DeviceSecret'", 
                 "'ProductSecret'", 
                 "'ProductID'", "'Burned'"]
                f_csv = csv.DictWriter(f, headers)
                f_csv.writeheader()
                f_csv.writerows(list_csv)
            lock_file.close()
            os.remove('lock.txt')
        except Exception as e:
            try:
                bflb_utils.printf(e)
                lock_file.close()
                os.remove('lock.txt')
                return (False, csv_mac)
            finally:
                e = None
                del e

        try:
            data_value = bytearray()
            data_len = 0
            temp = bflb_utils.int_to_4bytearray_l(1)
            for b in temp:
                data_value.append(b)

            temp = bflb_utils.int_to_4bytearray_l(len(version) + 1)
            for b in temp:
                data_value.append(b)

            ver = bflb_utils.string_to_bytearray(version)
            for b in ver:
                data_value.append(b)

            data_value.append(0)
            data_len += 8 + len(version) + 1
            for key, value in info_dict.items():
                if value != '':
                    temp = bflb_utils.int_to_4bytearray_l(257)
                    for b in temp:
                        data_value.append(b)

                    temp = bflb_utils.int_to_4bytearray_l(len(key) + 1)
                    for b in temp:
                        data_value.append(b)

                    temp = bflb_utils.string_to_bytearray(key)
                    for b in temp:
                        data_value.append(b)

                    data_value.append(0)
                    data_len += 8 + len(key) + 1
                    temp = bflb_utils.int_to_4bytearray_l(258)
                    for b in temp:
                        data_value.append(b)

                    temp = bflb_utils.int_to_4bytearray_l(len(value) + 1)
                    for b in temp:
                        data_value.append(b)

                    temp = bflb_utils.string_to_bytearray(value)
                    for b in temp:
                        data_value.append(b)

                    data_value.append(0)
                    data_len += 8 + len(value) + 1

            info = bytearray()
            info.append(165)
            info.append(165)
            info.append(165)
            info.append(165)
            temp = bflb_utils.int_to_4bytearray_l(data_len)
            for b in temp:
                info.append(b)

            for _ in range(40):
                info.append(255)

            sh = hashlib.sha256()
            sh.update(data_value)
            data_sha256 = sh.hexdigest()
            data_sha256 = bflb_utils.hexstr_to_bytearray(data_sha256)
            temp = data_sha256[-16:]
            for b in temp:
                info.append(b)

            for b in data_value:
                info.append(b)

            with open(output_file, mode='wb') as (f):
                f.write(info)
        except Exception as e:
            try:
                bflb_utils.printf(e)
                return (False, csv_mac)
            finally:
                e = None
                del e

        return (
         True, csv_mac)

    def is_conf_exist(self, flash_id):
        if conf_sign:
            cfg_dir = app_path + '/utils/flash/' + cgc.lower_name + '/'
        else:
            cfg_dir = app_path + '/utils/flash/' + self._chip_type + '/'
        conf_name = self.get_suitable_conf_name(cfg_dir, flash_id)
        if os.path.isfile(cfg_dir + conf_name) is False:
            return False
        return True

    def clock_para_update(self, file):
        if os.path.isfile(file) is False:
            efuse_bootheader_path = os.path.join(chip_path, self._chip_name, 'efuse_bootheader')
            efuse_bh_cfg = efuse_bootheader_path + '/efuse_bootheader_cfg.conf'
            sub_module = __import__(('libs.' + self._chip_type), fromlist=[self._chip_type])
            section = 'BOOTHEADER_GROUP0_CFG'
            fp = open(efuse_bh_cfg, 'r')
            data = fp.read()
            fp.close()
            if 'BOOTHEADER_CFG' in data:
                section = 'BOOTHEADER_CFG'
            else:
                if 'BOOTHEADER_CPU0_CFG' in data:
                    section = 'BOOTHEADER_CPU0_CFG'
                else:
                    if 'BOOTHEADER_GROUP0_CFG' in data:
                        section = 'BOOTHEADER_GROUP0_CFG'
            bh_data, tmp = bflb_efuse_boothd_create.update_data_from_cfg(sub_module.bootheader_cfg_keys.bootheader_cfg_keys, efuse_bh_cfg, section)
            bh_data = bflb_efuse_boothd_create.bootheader_update_flash_pll_crc(bh_data, self._chip_type)
            fp = open(file, 'wb+')
            if self._chip_type == 'bl808':
                if section == 'BOOTHEADER_GROUP0_CFG':
                    fp.write(bh_data[100:128])
            else:
                if self._chip_type == 'bl628':
                    if section == 'BOOTHEADER_GROUP0_CFG':
                        fp.write(bh_data[100:124])
                elif self._chip_type == 'bl616':
                    if section == 'BOOTHEADER_GROUP0_CFG':
                        fp.write(bh_data[100:120])
                elif self._chip_type == 'wb03':
                    if section == 'BOOTHEADER_GROUP0_CFG':
                        fp.write(bh_data[308:328])
                elif self._chip_type == 'bl702l':
                    if section == 'BOOTHEADER_CFG':
                        fp.write(bh_data[100:116])
                fp.close()
        fp = open_file(file, 'rb')
        clock_para = bytearray(fp.read())
        fp.close()
        return clock_para

    def flash_para_update(self, file, jedec_id):
        flash_para = bytearray(0)
        if self.is_conf_exist(jedec_id) is True:
            sub_module = __import__(('libs.' + self._chip_type), fromlist=[self._chip_type])
            if conf_sign:
                cfg_dir = app_path + '/utils/flash/' + self._chip_name + '/'
            else:
                cfg_dir = app_path + '/utils/flash/' + self._chip_type + '/'
            conf_name = sub_module.flash_select_do.get_suitable_file_name(cfg_dir, jedec_id)
            offset, flashCfgLen, flash_para, flashCrcOffset, crcOffset = bflb_flash_select.update_flash_para_from_cfg(sub_module.bootheader_cfg_keys.bootheader_cfg_keys, cfg_dir + conf_name)
            fp = open(os.path.join(app_path, file), 'wb+')
            fp.write(flash_para)
            fp.close()
        return flash_para

    def efuse_flash_loader(self, args, eflash_loader_cfg, eflash_loader_bin, callback=None, create_simple_callback=None, create_img_callback=None, macaddr_callback=None, task_num=None):
        ret = None
        if task_num == None:
            bflb_utils.local_log_enable(True)
        bflb_utils.printf('Version: ', bflb_version.eflash_loader_version_text)
        start_time = time.time() * 1000
        try:
            retry = -1
            update_cutoff_time = True
            if task_num != None:
                if task_num > 256:
                    self._csv_burn_en = False
                    self._task_num = task_num - 256
                else:
                    self._csv_burn_en = True
                    self._task_num = task_num
            else:
                self._csv_burn_en = False
                self._task_num = None
            while 1:
                if self._bflb_com_if is not None:
                    self._bflb_com_if.if_close()
                bflb_utils.printf('Program Start')
                ret, flash_burn_retry = self.efuse_flash_loader_do(args, eflash_loader_cfg, eflash_loader_bin, callback, update_cutoff_time, create_simple_callback, create_img_callback, macaddr_callback, task_num)
                self._skip_len = 0
                if ret == 'repeat_burn':
                    if self._bflb_com_if is not None:
                        self._bflb_com_if.if_close()
                    return 'repeat_burn'
                if self._cpu_reset is True:
                    bflb_utils.printf('Reset cpu')
                    self.reset_cpu()
                if self._retry_delay_after_cpu_reset > 0:
                    bflb_utils.printf('delay for uart timeout: ', self._retry_delay_after_cpu_reset)
                    time.sleep(self._retry_delay_after_cpu_reset)
                if retry == -1:
                    retry = flash_burn_retry
                if ret is True:
                    if not args.none:
                        bflb_utils.printf('All time cost(ms): ', time.time() * 1000 - start_time)
                        time.sleep(0.1)
                        if self._bflb_com_if is not None:
                            self._bflb_com_if.if_close()
                            bflb_utils.printf('close interface')
                        if self._csv_data:
                            if self._csv_file:
                                lock_file = open('lock.txt', 'w+')
                                portalocker.lock(lock_file, portalocker.LOCK_EX)
                                with open(self._csv_file, 'r') as (csvf):
                                    reader = csv.DictReader(csvf)
                                    list_csv = []
                                    for row in reader:
                                        if row.get('DeviceName', '') == self._csv_data:
                                            if row.get('Burned', '') == 'P':
                                                row['Burned'] = 'Y'
                                            else:
                                                bflb_utils.printf(self._csv_data + ' status not programing')
                                        list_csv.append(row)

                                    with open((self._csv_file), 'w', newline='') as (f):
                                        headers = ["'ProductKey'", "'DeviceName'", "'DeviceSecret'", 
                                         "'ProductSecret'", 
                                         "'ProductID'", 
                                         "'Burned'"]
                                        f_csv = csv.DictWriter(f, headers)
                                        f_csv.writeheader()
                                        f_csv.writerows(list_csv)
                                lock_file.close()
                                os.remove('lock.txt')
                        bflb_utils.printf('[All Success]')
                        bflb_utils.local_log_save('log', self._input_macaddr)
                    return True
                retry -= 1
                bflb_utils.printf('Burn Retry')
                bflb_utils.printf(retry)
                if retry <= 0:
                    break

            bflb_utils.printf('Burn return with retry fail')
            if self._csv_data:
                if self._csv_file:
                    lock_file = open('lock.txt', 'w+')
                    portalocker.lock(lock_file, portalocker.LOCK_EX)
                    with open(self._csv_file, 'r') as (csvf):
                        reader = csv.DictReader(csvf)
                        list_csv = []
                        for row in reader:
                            if row.get('DeviceName', '') == self._csv_data:
                                if row.get('Burned', '') == 'P':
                                    row['Burned'] = ''
                                else:
                                    bflb_utils.printf(self._csv_data + ' status not programing')
                            list_csv.append(row)

                        with open((self._csv_file), 'w', newline='') as (f):
                            headers = ["'ProductKey'", "'DeviceName'", "'DeviceSecret'", 
                             "'ProductSecret'", 
                             "'ProductID'", "'Burned'"]
                            f_csv = csv.DictWriter(f, headers)
                            f_csv.writeheader()
                            f_csv.writerows(list_csv)
                    lock_file.close()
                    os.remove('lock.txt')
            bflb_utils.local_log_save('log', self._input_macaddr)
            if self._bflb_com_if is not None:
                self._bflb_com_if.if_close()
            return bflb_utils.errorcode_msg(self._task_num)
        except Exception as e:
            try:
                bflb_utils.printf('efuse_flash_loader fail')
                if self._csv_data:
                    if self._csv_file:
                        lock_file = open('lock.txt', 'w+')
                        portalocker.lock(lock_file, portalocker.LOCK_EX)
                        with open(self._csv_file, 'r') as (csvf):
                            reader = csv.DictReader(csvf)
                            list_csv = []
                            for row in reader:
                                if row.get('DeviceName', '') == self._csv_data:
                                    if row.get('Burned', '') == 'P':
                                        row['Burned'] = ''
                                    else:
                                        bflb_utils.printf(self._csv_data + ' status not programing')
                                list_csv.append(row)

                            with open((self._csv_file), 'w', newline='') as (f):
                                headers = ["'ProductKey'", "'DeviceName'", "'DeviceSecret'", 
                                 "'ProductSecret'", 
                                 "'ProductID'", 
                                 "'Burned'"]
                                f_csv = csv.DictWriter(f, headers)
                                f_csv.writeheader()
                                f_csv.writerows(list_csv)
                        lock_file.close()
                        os.remove('lock.txt')
                bflb_utils.local_log_save('log', self._input_macaddr)
                if self._bflb_com_if is not None:
                    self._bflb_com_if.if_close()
                return bflb_utils.errorcode_msg(self._task_num)
            finally:
                e = None
                del e

    def efuse_flash_loader2(self, options, eflash_loader_cfg, eflash_loader_bin, callback=None, port=''):
        if port is not None and port:
            import socket
            bflb_utils.printf('Listen on Port: ', port)
            ip_port = ('127.0.0.1', int(port))
            server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server.bind(ip_port)
            while True:
                data, client_addr = server.recvfrom(1024)

            server.close()
        else:
            self.efuse_flash_loader(options, eflash_loader_cfg, eflash_loader_bin, callback)

    def efuse_flash_loader_do--- This code section failed: ---

 L.2612         0  LOAD_GLOBAL              bflb_utils
                2  LOAD_METHOD              printf
                4  LOAD_STR                 '========= eflash loader cmd arguments ========='
                6  CALL_METHOD_1         1  '1 positional argument'
                8  POP_TOP          

 L.2613        10  LOAD_GLOBAL              bflb_utils
               12  LOAD_METHOD              printf
               14  LOAD_FAST                'eflash_loader_cfg'
               16  CALL_METHOD_1         1  '1 positional argument'
               18  POP_TOP          

 L.2614        20  LOAD_CONST               None
               22  STORE_FAST               'config_file'

 L.2615        24  LOAD_CONST               None
               26  STORE_FAST               'eflash_loader_file'

 L.2616        28  LOAD_CONST               None
               30  STORE_FAST               'bootinfo'

 L.2617     32_34  SETUP_EXCEPT        740  'to 740'

 L.2618        36  LOAD_STR                 ''
               38  STORE_FAST               'start'

 L.2619        40  LOAD_STR                 ''
               42  STORE_FAST               'end'

 L.2620        44  LOAD_STR                 ''
               46  STORE_FAST               'packet_file'

 L.2621        48  LOAD_STR                 ''
               50  STORE_FAST               'file'

 L.2622        52  LOAD_STR                 ''
               54  STORE_FAST               'efusefile'

 L.2623        56  LOAD_STR                 ''
               58  STORE_FAST               'massbin'

 L.2624        60  LOAD_STR                 ''
               62  STORE_FAST               'fwbin'

 L.2625        64  LOAD_STR                 ''
               66  STORE_FAST               'address'

 L.2626        68  LOAD_STR                 ''
               70  STORE_FAST               'load_str'

 L.2627        72  LOAD_STR                 ''
               74  STORE_FAST               'load_data'

 L.2628        76  LOAD_STR                 ''
               78  STORE_FAST               'interface'

 L.2629        80  LOAD_STR                 ''
               82  STORE_FAST               'port'

 L.2630        84  LOAD_STR                 ''
               86  STORE_FAST               'load_speed'

 L.2631        88  LOAD_STR                 ''
               90  STORE_FAST               'aeskey'

 L.2632        92  LOAD_STR                 ''
               94  STORE_FAST               'chip_type'

 L.2633        96  LOAD_STR                 ''
               98  STORE_FAST               'xtal_type'

 L.2634       100  LOAD_STR                 ''
              102  STORE_FAST               'load_file'

 L.2635       104  LOAD_STR                 ''
              106  STORE_FAST               'macaddr'

 L.2636       108  LOAD_STR                 ''
              110  STORE_FAST               'romfs_data'

 L.2637       112  LOAD_STR                 ''
              114  STORE_FAST               'csvfile'

 L.2638       116  LOAD_STR                 ''
              118  STORE_FAST               'csvaddr'

 L.2639       120  LOAD_STR                 ''
              122  STORE_FAST               'efuse_para'

 L.2640       124  LOAD_STR                 ''
              126  STORE_FAST               'create_cfg'

 L.2641       128  LOAD_CONST               0
              130  STORE_FAST               'flash_set'

 L.2642       132  LOAD_CONST               0
              134  STORE_FAST               'read_flash_id'

 L.2643       136  LOAD_STR                 '80'
              138  STORE_FAST               'id_valid_flag'

 L.2644       140  LOAD_CONST               0
              142  STORE_FAST               'read_flash2_id'

 L.2645       144  LOAD_STR                 '80'
              146  STORE_FAST               'id2_valid_flag'

 L.2646       148  LOAD_CONST               0
              150  STORE_FAST               'efuse_load_func'

 L.2647       152  LOAD_FAST                'args'
              154  LOAD_ATTR                config
              156  POP_JUMP_IF_FALSE   172  'to 172'
              158  LOAD_FAST                'config_file'
              160  LOAD_CONST               None
              162  COMPARE_OP               is
              164  POP_JUMP_IF_FALSE   172  'to 172'

 L.2648       166  LOAD_FAST                'args'
              168  LOAD_ATTR                config
              170  STORE_FAST               'config_file'
            172_0  COME_FROM           164  '164'
            172_1  COME_FROM           156  '156'

 L.2649       172  LOAD_FAST                'args'
              174  LOAD_ATTR                interface
              176  POP_JUMP_IF_FALSE   184  'to 184'

 L.2650       178  LOAD_FAST                'args'
              180  LOAD_ATTR                interface
              182  STORE_FAST               'interface'
            184_0  COME_FROM           176  '176'

 L.2651       184  LOAD_FAST                'args'
              186  LOAD_ATTR                port
              188  POP_JUMP_IF_FALSE   196  'to 196'

 L.2652       190  LOAD_FAST                'args'
              192  LOAD_ATTR                port
              194  STORE_FAST               'port'
            196_0  COME_FROM           188  '188'

 L.2653       196  LOAD_FAST                'args'
              198  LOAD_ATTR                baudrate
              200  POP_JUMP_IF_FALSE   208  'to 208'

 L.2654       202  LOAD_FAST                'args'
              204  LOAD_ATTR                baudrate
              206  STORE_FAST               'load_speed'
            208_0  COME_FROM           200  '200'

 L.2655       208  LOAD_FAST                'args'
              210  LOAD_ATTR                mass
              212  POP_JUMP_IF_FALSE   220  'to 220'

 L.2656       214  LOAD_FAST                'args'
              216  LOAD_ATTR                mass
              218  STORE_FAST               'massbin'
            220_0  COME_FROM           212  '212'

 L.2657       220  LOAD_FAST                'args'
              222  LOAD_ATTR                userarea
              224  POP_JUMP_IF_FALSE   232  'to 232'

 L.2658       226  LOAD_FAST                'args'
              228  LOAD_ATTR                userarea
              230  STORE_FAST               'fwbin'
            232_0  COME_FROM           224  '224'

 L.2659       232  LOAD_FAST                'args'
              234  LOAD_ATTR                start
              236  POP_JUMP_IF_FALSE   244  'to 244'

 L.2660       238  LOAD_FAST                'args'
              240  LOAD_ATTR                start
              242  STORE_FAST               'start'
            244_0  COME_FROM           236  '236'

 L.2661       244  LOAD_FAST                'args'
              246  LOAD_ATTR                end
          248_250  POP_JUMP_IF_FALSE   258  'to 258'

 L.2662       252  LOAD_FAST                'args'
              254  LOAD_ATTR                end
              256  STORE_FAST               'end'
            258_0  COME_FROM           248  '248'

 L.2663       258  LOAD_FAST                'args'
              260  LOAD_ATTR                packet
          262_264  POP_JUMP_IF_FALSE   272  'to 272'

 L.2664       266  LOAD_FAST                'args'
              268  LOAD_ATTR                packet
              270  STORE_FAST               'packet_file'
            272_0  COME_FROM           262  '262'

 L.2665       272  LOAD_FAST                'args'
              274  LOAD_ATTR                file
          276_278  POP_JUMP_IF_FALSE   286  'to 286'

 L.2666       280  LOAD_FAST                'args'
              282  LOAD_ATTR                file
              284  STORE_FAST               'file'
            286_0  COME_FROM           276  '276'

 L.2667       286  LOAD_FAST                'args'
              288  LOAD_ATTR                efusefile
          290_292  POP_JUMP_IF_FALSE   300  'to 300'

 L.2668       294  LOAD_FAST                'args'
              296  LOAD_ATTR                efusefile
              298  STORE_FAST               'efusefile'
            300_0  COME_FROM           290  '290'

 L.2669       300  LOAD_FAST                'args'
              302  LOAD_ATTR                efusecheck
          304_306  POP_JUMP_IF_FALSE   314  'to 314'

 L.2670       308  LOAD_CONST               1
              310  STORE_FAST               'efuse_load_func'
              312  JUMP_FORWARD        318  'to 318'
            314_0  COME_FROM           304  '304'

 L.2672       314  LOAD_CONST               0
              316  STORE_FAST               'efuse_load_func'
            318_0  COME_FROM           312  '312'

 L.2673       318  LOAD_FAST                'args'
              320  LOAD_ATTR                data
          322_324  POP_JUMP_IF_FALSE   332  'to 332'

 L.2674       326  LOAD_FAST                'args'
              328  LOAD_ATTR                data
              330  STORE_FAST               'load_data'
            332_0  COME_FROM           322  '322'

 L.2675       332  LOAD_FAST                'args'
              334  LOAD_ATTR                addr
          336_338  POP_JUMP_IF_FALSE   346  'to 346'

 L.2676       340  LOAD_FAST                'args'
              342  LOAD_ATTR                addr
              344  STORE_FAST               'address'
            346_0  COME_FROM           336  '336'

 L.2677       346  LOAD_FAST                'args'
              348  LOAD_ATTR                skip
          350_352  POP_JUMP_IF_FALSE   498  'to 498'

 L.2678       354  LOAD_FAST                'args'
              356  LOAD_ATTR                skip
              358  STORE_FAST               'skip_str'

 L.2679       360  LOAD_FAST                'skip_str'
              362  LOAD_METHOD              split
              364  LOAD_STR                 ','
              366  CALL_METHOD_1         1  '1 positional argument'
              368  STORE_FAST               'skip_para'

 L.2680       370  LOAD_FAST                'skip_para'
              372  LOAD_CONST               0
              374  BINARY_SUBSCR    
              376  LOAD_CONST               0
              378  LOAD_CONST               2
              380  BUILD_SLICE_2         2 
              382  BINARY_SUBSCR    
              384  LOAD_STR                 '0x'
              386  COMPARE_OP               ==
          388_390  POP_JUMP_IF_FALSE   418  'to 418'

 L.2681       392  LOAD_GLOBAL              int
              394  LOAD_FAST                'skip_para'
              396  LOAD_CONST               0
              398  BINARY_SUBSCR    
              400  LOAD_CONST               2
              402  LOAD_CONST               None
              404  BUILD_SLICE_2         2 
              406  BINARY_SUBSCR    
              408  LOAD_CONST               16
              410  CALL_FUNCTION_2       2  '2 positional arguments'
              412  LOAD_FAST                'self'
              414  STORE_ATTR               _skip_addr
              416  JUMP_FORWARD        434  'to 434'
            418_0  COME_FROM           388  '388'

 L.2683       418  LOAD_GLOBAL              int
              420  LOAD_FAST                'skip_para'
              422  LOAD_CONST               0
              424  BINARY_SUBSCR    
              426  LOAD_CONST               10
              428  CALL_FUNCTION_2       2  '2 positional arguments'
              430  LOAD_FAST                'self'
              432  STORE_ATTR               _skip_addr
            434_0  COME_FROM           416  '416'

 L.2684       434  LOAD_FAST                'skip_para'
              436  LOAD_CONST               1
              438  BINARY_SUBSCR    
              440  LOAD_CONST               0
              442  LOAD_CONST               2
              444  BUILD_SLICE_2         2 
              446  BINARY_SUBSCR    
              448  LOAD_STR                 '0x'
              450  COMPARE_OP               ==
          452_454  POP_JUMP_IF_FALSE   482  'to 482'

 L.2685       456  LOAD_GLOBAL              int
              458  LOAD_FAST                'skip_para'
              460  LOAD_CONST               1
              462  BINARY_SUBSCR    
              464  LOAD_CONST               2
              466  LOAD_CONST               None
              468  BUILD_SLICE_2         2 
              470  BINARY_SUBSCR    
              472  LOAD_CONST               16
              474  CALL_FUNCTION_2       2  '2 positional arguments'
              476  LOAD_FAST                'self'
              478  STORE_ATTR               _skip_len
              480  JUMP_FORWARD        498  'to 498'
            482_0  COME_FROM           452  '452'

 L.2687       482  LOAD_GLOBAL              int
              484  LOAD_FAST                'skip_para'
              486  LOAD_CONST               1
              488  BINARY_SUBSCR    
              490  LOAD_CONST               10
              492  CALL_FUNCTION_2       2  '2 positional arguments'
              494  LOAD_FAST                'self'
              496  STORE_ATTR               _skip_len
            498_0  COME_FROM           480  '480'
            498_1  COME_FROM           350  '350'

 L.2688       498  LOAD_FAST                'args'
              500  LOAD_ATTR                key
          502_504  POP_JUMP_IF_FALSE   512  'to 512'

 L.2689       506  LOAD_FAST                'args'
              508  LOAD_ATTR                key
              510  STORE_FAST               'aeskey'
            512_0  COME_FROM           502  '502'

 L.2690       512  LOAD_FAST                'args'
              514  LOAD_ATTR                createcfg
          516_518  POP_JUMP_IF_FALSE   526  'to 526'

 L.2691       520  LOAD_FAST                'args'
              522  LOAD_ATTR                createcfg
              524  STORE_FAST               'create_cfg'
            526_0  COME_FROM           516  '516'

 L.2692       526  LOAD_FAST                'args'
              528  LOAD_ATTR                chipname
          530_532  POP_JUMP_IF_FALSE   546  'to 546'

 L.2693       534  LOAD_GLOBAL              gol
              536  LOAD_ATTR                dict_chip_cmd
              538  LOAD_FAST                'args'
              540  LOAD_ATTR                chipname
              542  BINARY_SUBSCR    
              544  STORE_FAST               'chip_type'
            546_0  COME_FROM           530  '530'

 L.2694       546  LOAD_FAST                'args'
              548  LOAD_ATTR                xtal
          550_552  POP_JUMP_IF_FALSE   584  'to 584'

 L.2695       554  LOAD_FAST                'args'
              556  LOAD_ATTR                xtal
              558  LOAD_METHOD              replace
              560  LOAD_STR                 'm'
              562  LOAD_STR                 'M'
              564  CALL_METHOD_2         2  '2 positional arguments'
              566  LOAD_METHOD              replace
              568  LOAD_STR                 'rc'
              570  LOAD_STR                 'RC'
              572  CALL_METHOD_2         2  '2 positional arguments'
              574  LOAD_METHOD              replace
              576  LOAD_STR                 'none'
              578  LOAD_STR                 'None'
              580  CALL_METHOD_2         2  '2 positional arguments'
              582  STORE_FAST               'xtal_type'
            584_0  COME_FROM           550  '550'

 L.2696       584  LOAD_FAST                'args'
              586  LOAD_ATTR                loadstr
          588_590  POP_JUMP_IF_FALSE   598  'to 598'

 L.2697       592  LOAD_FAST                'args'
              594  LOAD_ATTR                loadstr
              596  STORE_FAST               'load_str'
            598_0  COME_FROM           588  '588'

 L.2698       598  LOAD_FAST                'args'
              600  LOAD_ATTR                loadfile
          602_604  POP_JUMP_IF_FALSE   612  'to 612'

 L.2699       606  LOAD_FAST                'args'
              608  LOAD_ATTR                loadfile
              610  STORE_FAST               'load_file'
            612_0  COME_FROM           602  '602'

 L.2700       612  LOAD_FAST                'args'
              614  LOAD_ATTR                mac
          616_618  POP_JUMP_IF_FALSE   626  'to 626'

 L.2701       620  LOAD_FAST                'args'
              622  LOAD_ATTR                mac
              624  STORE_FAST               'macaddr'
            626_0  COME_FROM           616  '616'

 L.2702       626  LOAD_FAST                'args'
              628  LOAD_ATTR                isp
          630_632  POP_JUMP_IF_FALSE   642  'to 642'

 L.2703       634  LOAD_CONST               True
              636  LOAD_FAST                'self'
              638  STORE_ATTR               _isp_en
              640  JUMP_FORWARD        648  'to 648'
            642_0  COME_FROM           630  '630'

 L.2705       642  LOAD_CONST               False
              644  LOAD_FAST                'self'
              646  STORE_ATTR               _isp_en
            648_0  COME_FROM           640  '640'

 L.2706       648  LOAD_FAST                'args'
              650  LOAD_ATTR                romfs
          652_654  POP_JUMP_IF_FALSE   662  'to 662'

 L.2707       656  LOAD_FAST                'args'
              658  LOAD_ATTR                romfs
              660  STORE_FAST               'romfs_data'
            662_0  COME_FROM           652  '652'

 L.2708       662  LOAD_FAST                'args'
              664  LOAD_ATTR                csvfile
          666_668  POP_JUMP_IF_FALSE   676  'to 676'

 L.2709       670  LOAD_FAST                'args'
              672  LOAD_ATTR                csvfile
              674  STORE_FAST               'csvfile'
            676_0  COME_FROM           666  '666'

 L.2710       676  LOAD_FAST                'args'
              678  LOAD_ATTR                csvaddr
          680_682  POP_JUMP_IF_FALSE   690  'to 690'

 L.2711       684  LOAD_FAST                'args'
              686  LOAD_ATTR                csvaddr
              688  STORE_FAST               'csvaddr'
            690_0  COME_FROM           680  '680'

 L.2712       690  LOAD_FAST                'args'
              692  LOAD_ATTR                auto
          694_696  POP_JUMP_IF_FALSE   716  'to 716'

 L.2713       698  LOAD_GLOBAL              bflb_utils
              700  LOAD_METHOD              printf
              702  LOAD_STR                 'auto burn'
              704  CALL_METHOD_1         1  '1 positional argument'
              706  POP_TOP          

 L.2714       708  LOAD_CONST               True
              710  LOAD_FAST                'self'
              712  STORE_ATTR               _bflb_auto_download
              714  JUMP_FORWARD        722  'to 722'
            716_0  COME_FROM           694  '694'

 L.2716       716  LOAD_CONST               False
              718  LOAD_FAST                'self'
              720  STORE_ATTR               _bflb_auto_download
            722_0  COME_FROM           714  '714'

 L.2717       722  LOAD_FAST                'args'
              724  LOAD_ATTR                para
          726_728  POP_JUMP_IF_FALSE   736  'to 736'

 L.2718       730  LOAD_FAST                'args'
              732  LOAD_ATTR                para
              734  STORE_FAST               'efuse_para'
            736_0  COME_FROM           726  '726'
              736  POP_BLOCK        
              738  JUMP_FORWARD        796  'to 796'
            740_0  COME_FROM_EXCEPT     32  '32'

 L.2719       740  DUP_TOP          
              742  LOAD_GLOBAL              Exception
              744  COMPARE_OP               exception-match
          746_748  POP_JUMP_IF_FALSE   794  'to 794'
              750  POP_TOP          
              752  STORE_FAST               'e'
              754  POP_TOP          
              756  SETUP_FINALLY       782  'to 782'

 L.2720       758  LOAD_GLOBAL              bflb_utils
              760  LOAD_METHOD              printf
              762  LOAD_FAST                'e'
              764  CALL_METHOD_1         1  '1 positional argument'
              766  POP_TOP          

 L.2721       768  LOAD_FAST                'self'
              770  LOAD_METHOD              error_code_print
              772  LOAD_STR                 '0002'
              774  CALL_METHOD_1         1  '1 positional argument'
              776  POP_TOP          

 L.2722       778  LOAD_CONST               (False, 0)
              780  RETURN_VALUE     
            782_0  COME_FROM_FINALLY   756  '756'
              782  LOAD_CONST               None
              784  STORE_FAST               'e'
              786  DELETE_FAST              'e'
              788  END_FINALLY      
              790  POP_EXCEPT       
              792  JUMP_FORWARD        796  'to 796'
            794_0  COME_FROM           746  '746'
              794  END_FINALLY      
            796_0  COME_FROM           792  '792'
            796_1  COME_FROM           738  '738'

 L.2724       796  LOAD_FAST                'packet_file'
              798  LOAD_STR                 ''
              800  COMPARE_OP               !=
          802_804  POP_JUMP_IF_FALSE   820  'to 820'

 L.2725       806  LOAD_FAST                'self'
              808  LOAD_METHOD              setOpenFile_zip
              810  LOAD_FAST                'packet_file'
              812  CALL_METHOD_1         1  '1 positional argument'
              814  POP_TOP          

 L.2726       816  LOAD_CONST               (True, 0)
              818  RETURN_VALUE     
            820_0  COME_FROM           802  '802'

 L.2727       820  LOAD_FAST                'chip_type'
          822_824  POP_JUMP_IF_FALSE   832  'to 832'

 L.2728       826  LOAD_FAST                'chip_type'
              828  LOAD_FAST                'self'
              830  STORE_ATTR               _chip_type
            832_0  COME_FROM           822  '822'

 L.2729       832  LOAD_FAST                'config_file'
              834  LOAD_CONST               None
              836  COMPARE_OP               is
          838_840  POP_JUMP_IF_FALSE   882  'to 882'

 L.2730       842  LOAD_FAST                'self'
              844  LOAD_ATTR                _chip_name
          846_848  POP_JUMP_IF_FALSE   878  'to 878'

 L.2731       850  LOAD_GLOBAL              os
              852  LOAD_ATTR                path
              854  LOAD_METHOD              join
              856  LOAD_GLOBAL              app_path
              858  LOAD_STR                 'chips'
              860  LOAD_FAST                'self'
              862  LOAD_ATTR                _chip_name
              864  LOAD_METHOD              lower
              866  CALL_METHOD_0         0  '0 positional arguments'

 L.2732       868  LOAD_STR                 'eflash_loader'
              870  LOAD_STR                 'eflash_loader_cfg.ini'
              872  CALL_METHOD_5         5  '5 positional arguments'
              874  STORE_FAST               'config_file'
              876  JUMP_FORWARD        882  'to 882'
            878_0  COME_FROM           846  '846'

 L.2734       878  LOAD_STR                 'eflash_loader_cfg.ini'
              880  STORE_FAST               'config_file'
            882_0  COME_FROM           876  '876'
            882_1  COME_FROM           838  '838'

 L.2735       882  LOAD_FAST                'args'
              884  LOAD_ATTR                usage
          886_888  POP_JUMP_IF_FALSE   898  'to 898'

 L.2736       890  LOAD_FAST                'self'
              892  LOAD_METHOD              usage
              894  CALL_METHOD_0         0  '0 positional arguments'
              896  POP_TOP          
            898_0  COME_FROM           886  '886'

 L.2737       898  LOAD_FAST                'args'
              900  LOAD_ATTR                version
          902_904  POP_JUMP_IF_FALSE   930  'to 930'

 L.2738       906  LOAD_GLOBAL              conf_sign
          908_910  POP_JUMP_IF_TRUE    926  'to 926'

 L.2739       912  LOAD_GLOBAL              bflb_utils
              914  LOAD_METHOD              printf
              916  LOAD_STR                 'Version: '
              918  LOAD_GLOBAL              bflb_version
              920  LOAD_ATTR                eflash_loader_version_text
              922  CALL_METHOD_2         2  '2 positional arguments'
              924  POP_TOP          
            926_0  COME_FROM           908  '908'

 L.2740       926  LOAD_CONST               (True, 0)
              928  RETURN_VALUE     
            930_0  COME_FROM           902  '902'

 L.2741       930  LOAD_FAST                'load_str'
              932  LOAD_METHOD              replace
              934  LOAD_STR                 '*'
              936  LOAD_STR                 '\n'
              938  CALL_METHOD_2         2  '2 positional arguments'
              940  LOAD_METHOD              replace
              942  LOAD_STR                 '%'
              944  LOAD_STR                 ' '
              946  CALL_METHOD_2         2  '2 positional arguments'
              948  STORE_FAST               'load_str'

 L.2743       950  LOAD_FAST                'config_file'
              952  LOAD_CONST               None
              954  COMPARE_OP               is
          956_958  POP_JUMP_IF_FALSE   984  'to 984'
              960  LOAD_FAST                'load_str'
              962  LOAD_CONST               None
              964  COMPARE_OP               is
          966_968  POP_JUMP_IF_FALSE   984  'to 984'
              970  LOAD_FAST                'eflash_loader_cfg'
              972  LOAD_CONST               None
              974  COMPARE_OP               is
          976_978  POP_JUMP_IF_FALSE   984  'to 984'

 L.2744       980  LOAD_CONST               (False, 0)
              982  RETURN_VALUE     
            984_0  COME_FROM           976  '976'
            984_1  COME_FROM           966  '966'
            984_2  COME_FROM           956  '956'

 L.2745       984  LOAD_FAST                'load_str'
          986_988  POP_JUMP_IF_TRUE   1106  'to 1106'

 L.2746       990  LOAD_FAST                'eflash_loader_cfg'
              992  LOAD_CONST               None
              994  COMPARE_OP               is-not
          996_998  POP_JUMP_IF_FALSE  1006  'to 1006'

 L.2747      1000  LOAD_FAST                'eflash_loader_cfg'
             1002  STORE_FAST               'config_file'
             1004  JUMP_FORWARD       1018  'to 1018'
           1006_0  COME_FROM           996  '996'

 L.2749      1006  LOAD_GLOBAL              os
             1008  LOAD_ATTR                path
             1010  LOAD_METHOD              abspath
             1012  LOAD_FAST                'config_file'
             1014  CALL_METHOD_1         1  '1 positional argument'
             1016  STORE_FAST               'config_file'
           1018_0  COME_FROM          1004  '1004'

 L.2750      1018  LOAD_GLOBAL              isinstance
             1020  LOAD_FAST                'config_file'
             1022  LOAD_GLOBAL              BFConfigParser
             1024  CALL_FUNCTION_2       2  '2 positional arguments'
         1026_1028  POP_JUMP_IF_FALSE  1036  'to 1036'

 L.2751      1030  LOAD_FAST                'config_file'
             1032  STORE_FAST               'cfg'
             1034  JUMP_FORWARD       1104  'to 1104'
           1036_0  COME_FROM          1026  '1026'

 L.2753      1036  LOAD_GLOBAL              bflb_utils
             1038  LOAD_METHOD              printf
             1040  LOAD_STR                 'Config file: '
             1042  LOAD_FAST                'config_file'
             1044  CALL_METHOD_2         2  '2 positional arguments'
             1046  POP_TOP          

 L.2754      1048  LOAD_GLOBAL              os
             1050  LOAD_ATTR                path
             1052  LOAD_METHOD              exists
             1054  LOAD_FAST                'config_file'
             1056  CALL_METHOD_1         1  '1 positional argument'
         1058_1060  POP_JUMP_IF_FALSE  1080  'to 1080'

 L.2755      1062  LOAD_GLOBAL              BFConfigParser
             1064  CALL_FUNCTION_0       0  '0 positional arguments'
             1066  STORE_FAST               'cfg'

 L.2756      1068  LOAD_FAST                'cfg'
             1070  LOAD_METHOD              read
             1072  LOAD_FAST                'config_file'
             1074  CALL_METHOD_1         1  '1 positional argument'
             1076  POP_TOP          
             1078  JUMP_FORWARD       1104  'to 1104'
           1080_0  COME_FROM          1058  '1058'

 L.2758      1080  LOAD_GLOBAL              bflb_utils
             1082  LOAD_METHOD              printf
             1084  LOAD_STR                 'Config file not found'
             1086  CALL_METHOD_1         1  '1 positional argument'
             1088  POP_TOP          

 L.2759      1090  LOAD_FAST                'self'
             1092  LOAD_METHOD              error_code_print
             1094  LOAD_STR                 '000B'
             1096  CALL_METHOD_1         1  '1 positional argument'
             1098  POP_TOP          

 L.2760      1100  LOAD_CONST               (False, 0)
             1102  RETURN_VALUE     
           1104_0  COME_FROM          1078  '1078'
           1104_1  COME_FROM          1034  '1034'
             1104  JUMP_FORWARD       1124  'to 1124'
           1106_0  COME_FROM           986  '986'

 L.2762      1106  LOAD_GLOBAL              BFConfigParser
             1108  CALL_FUNCTION_0       0  '0 positional arguments'
             1110  STORE_FAST               'cfg'

 L.2763      1112  LOAD_GLOBAL              bflb_utils
             1114  LOAD_METHOD              printf
             1116  LOAD_STR                 'Config str: '
             1118  LOAD_FAST                'load_str'
             1120  CALL_METHOD_2         2  '2 positional arguments'
             1122  POP_TOP          
           1124_0  COME_FROM          1104  '1104'

 L.2764      1124  LOAD_FAST                'cfg'
             1126  LOAD_METHOD              has_option
             1128  LOAD_STR                 'LOAD_CFG'
             1130  LOAD_STR                 'local_log'
             1132  CALL_METHOD_2         2  '2 positional arguments'
         1134_1136  POP_JUMP_IF_FALSE  1200  'to 1200'

 L.2765      1138  LOAD_FAST                'cfg'
             1140  LOAD_METHOD              get
             1142  LOAD_STR                 'LOAD_CFG'
             1144  LOAD_STR                 'local_log'
             1146  CALL_METHOD_2         2  '2 positional arguments'
             1148  LOAD_STR                 'true'
             1150  COMPARE_OP               ==
         1152_1154  POP_JUMP_IF_FALSE  1184  'to 1184'

 L.2766      1156  LOAD_GLOBAL              bflb_utils
             1158  LOAD_METHOD              printf
             1160  LOAD_STR                 'local log enable'
             1162  CALL_METHOD_1         1  '1 positional argument'
             1164  POP_TOP          

 L.2767      1166  LOAD_GLOBAL              bflb_utils
             1168  LOAD_METHOD              local_log_enable
             1170  LOAD_CONST               True
             1172  CALL_METHOD_1         1  '1 positional argument'
             1174  POP_TOP          

 L.2768      1176  LOAD_FAST                'macaddr'
             1178  LOAD_FAST                'self'
             1180  STORE_ATTR               _input_macaddr
             1182  JUMP_FORWARD       1200  'to 1200'
           1184_0  COME_FROM          1152  '1152'

 L.2770      1184  LOAD_GLOBAL              bflb_utils
             1186  LOAD_METHOD              local_log_enable
             1188  LOAD_CONST               False
             1190  CALL_METHOD_1         1  '1 positional argument'
             1192  POP_TOP          

 L.2771      1194  LOAD_STR                 ''
             1196  LOAD_FAST                'self'
             1198  STORE_ATTR               _input_macaddr
           1200_0  COME_FROM          1182  '1182'
           1200_1  COME_FROM          1134  '1134'

 L.2773      1200  LOAD_FAST                'interface'
         1202_1204  POP_JUMP_IF_TRUE   1218  'to 1218'

 L.2774      1206  LOAD_FAST                'cfg'
             1208  LOAD_METHOD              get
             1210  LOAD_STR                 'LOAD_CFG'
             1212  LOAD_STR                 'interface'
             1214  CALL_METHOD_2         2  '2 positional arguments'
             1216  STORE_FAST               'interface'
           1218_0  COME_FROM          1202  '1202'

 L.2775      1218  LOAD_FAST                'port'
         1220_1222  POP_JUMP_IF_TRUE   1336  'to 1336'

 L.2776      1224  LOAD_FAST                'interface'
             1226  LOAD_STR                 'openocd'
             1228  COMPARE_OP               ==
         1230_1232  POP_JUMP_IF_FALSE  1264  'to 1264'

 L.2777      1234  LOAD_FAST                'cfg'
             1236  LOAD_METHOD              get
             1238  LOAD_STR                 'LOAD_CFG'
             1240  LOAD_STR                 'openocd_config'
             1242  CALL_METHOD_2         2  '2 positional arguments'
             1244  LOAD_FAST                'self'
             1246  STORE_ATTR               _bflb_com_device

 L.2778      1248  LOAD_FAST                'cfg'
             1250  LOAD_METHOD              get
             1252  LOAD_STR                 'LOAD_CFG'
             1254  LOAD_STR                 'device'
             1256  CALL_METHOD_2         2  '2 positional arguments'
             1258  LOAD_FAST                'self'
             1260  STORE_ATTR               _bflb_sn_device
             1262  JUMP_FORWARD       1334  'to 1334'
           1264_0  COME_FROM          1230  '1230'

 L.2779      1264  LOAD_FAST                'interface'
             1266  LOAD_STR                 'cklink'
             1268  COMPARE_OP               ==
         1270_1272  POP_JUMP_IF_FALSE  1320  'to 1320'

 L.2780      1274  LOAD_FAST                'cfg'
             1276  LOAD_METHOD              get
             1278  LOAD_STR                 'LOAD_CFG'
             1280  LOAD_STR                 'cklink_vidpid'
             1282  CALL_METHOD_2         2  '2 positional arguments'
             1284  LOAD_FAST                'self'
             1286  STORE_ATTR               _bflb_com_device

 L.2781      1288  LOAD_FAST                'cfg'
             1290  LOAD_METHOD              get
             1292  LOAD_STR                 'LOAD_CFG'
             1294  LOAD_STR                 'cklink_type'
             1296  CALL_METHOD_2         2  '2 positional arguments'
             1298  LOAD_STR                 ' '
             1300  BINARY_ADD       
             1302  LOAD_FAST                'cfg'
             1304  LOAD_METHOD              get
             1306  LOAD_STR                 'LOAD_CFG'
             1308  LOAD_STR                 'device'
             1310  CALL_METHOD_2         2  '2 positional arguments'
             1312  BINARY_ADD       
             1314  LOAD_FAST                'self'
             1316  STORE_ATTR               _bflb_sn_device
             1318  JUMP_FORWARD       1334  'to 1334'
           1320_0  COME_FROM          1270  '1270'

 L.2783      1320  LOAD_FAST                'cfg'
             1322  LOAD_METHOD              get
             1324  LOAD_STR                 'LOAD_CFG'
             1326  LOAD_STR                 'device'
             1328  CALL_METHOD_2         2  '2 positional arguments'
             1330  LOAD_FAST                'self'
             1332  STORE_ATTR               _bflb_com_device
           1334_0  COME_FROM          1318  '1318'
           1334_1  COME_FROM          1262  '1262'
             1334  JUMP_FORWARD       1342  'to 1342'
           1336_0  COME_FROM          1220  '1220'

 L.2785      1336  LOAD_FAST                'port'
             1338  LOAD_FAST                'self'
             1340  STORE_ATTR               _bflb_com_device
           1342_0  COME_FROM          1334  '1334'

 L.2786      1342  LOAD_GLOBAL              bflb_utils
             1344  LOAD_METHOD              printf
             1346  LOAD_STR                 'serial port is '
             1348  LOAD_FAST                'self'
             1350  LOAD_ATTR                _bflb_com_device
             1352  CALL_METHOD_2         2  '2 positional arguments'
             1354  POP_TOP          

 L.2787      1356  LOAD_GLOBAL              int
             1358  LOAD_FAST                'cfg'
             1360  LOAD_METHOD              get
             1362  LOAD_STR                 'LOAD_CFG'
             1364  LOAD_STR                 'verify'
             1366  CALL_METHOD_2         2  '2 positional arguments'
             1368  CALL_FUNCTION_1       1  '1 positional argument'
             1370  STORE_FAST               'verify'

 L.2788      1372  LOAD_GLOBAL              int
             1374  LOAD_FAST                'cfg'
             1376  LOAD_METHOD              get
             1378  LOAD_STR                 'LOAD_CFG'
             1380  LOAD_STR                 'erase'
             1382  CALL_METHOD_2         2  '2 positional arguments'
             1384  CALL_FUNCTION_1       1  '1 positional argument'
             1386  STORE_FAST               'erase'

 L.2789      1388  LOAD_FAST                'interface'
             1390  LOAD_STR                 'cklink'
             1392  COMPARE_OP               ==
         1394_1396  POP_JUMP_IF_FALSE  1406  'to 1406'

 L.2790      1398  LOAD_CONST               14344
             1400  LOAD_FAST                'self'
             1402  STORE_ATTR               _bflb_com_tx_size
             1404  JUMP_FORWARD       1424  'to 1424'
           1406_0  COME_FROM          1394  '1394'

 L.2792      1406  LOAD_GLOBAL              int
             1408  LOAD_FAST                'cfg'
             1410  LOAD_METHOD              get
             1412  LOAD_STR                 'LOAD_CFG'
             1414  LOAD_STR                 'tx_size'
             1416  CALL_METHOD_2         2  '2 positional arguments'
             1418  CALL_FUNCTION_1       1  '1 positional argument'
             1420  LOAD_FAST                'self'
             1422  STORE_ATTR               _bflb_com_tx_size
           1424_0  COME_FROM          1404  '1404'

 L.2793      1424  LOAD_CONST               False
             1426  STORE_FAST               'do_reset'

 L.2794      1428  LOAD_CONST               100
             1430  STORE_FAST               'reset_hold_time'

 L.2795      1432  LOAD_CONST               100
             1434  STORE_FAST               'shake_hand_delay'

 L.2796      1436  LOAD_CONST               True
             1438  STORE_FAST               'reset_revert'

 L.2797      1440  LOAD_CONST               0
             1442  STORE_FAST               'cutoff_time'

 L.2798      1444  LOAD_CONST               2
             1446  STORE_FAST               'shake_hand_retry'

 L.2799      1448  LOAD_CONST               1
             1450  STORE_FAST               'flash_burn_retry'

 L.2800      1452  LOAD_FAST                'cfg'
             1454  LOAD_METHOD              has_option
             1456  LOAD_STR                 'LOAD_CFG'
             1458  LOAD_STR                 'erase_time_out'
             1460  CALL_METHOD_2         2  '2 positional arguments'
         1462_1464  POP_JUMP_IF_FALSE  1484  'to 1484'

 L.2801      1466  LOAD_GLOBAL              int
             1468  LOAD_FAST                'cfg'
             1470  LOAD_METHOD              get
             1472  LOAD_STR                 'LOAD_CFG'
             1474  LOAD_STR                 'erase_time_out'
             1476  CALL_METHOD_2         2  '2 positional arguments'
             1478  CALL_FUNCTION_1       1  '1 positional argument'
             1480  LOAD_FAST                'self'
             1482  STORE_ATTR               _erase_time_out
           1484_0  COME_FROM          1462  '1462'

 L.2802      1484  LOAD_FAST                'cfg'
             1486  LOAD_METHOD              has_option
             1488  LOAD_STR                 'LOAD_CFG'
             1490  LOAD_STR                 'shake_hand_retry'
             1492  CALL_METHOD_2         2  '2 positional arguments'
         1494_1496  POP_JUMP_IF_FALSE  1514  'to 1514'

 L.2803      1498  LOAD_GLOBAL              int
             1500  LOAD_FAST                'cfg'
             1502  LOAD_METHOD              get
             1504  LOAD_STR                 'LOAD_CFG'
             1506  LOAD_STR                 'shake_hand_retry'
             1508  CALL_METHOD_2         2  '2 positional arguments'
             1510  CALL_FUNCTION_1       1  '1 positional argument'
             1512  STORE_FAST               'shake_hand_retry'
           1514_0  COME_FROM          1494  '1494'

 L.2804      1514  LOAD_FAST                'cfg'
             1516  LOAD_METHOD              has_option
             1518  LOAD_STR                 'LOAD_CFG'
             1520  LOAD_STR                 'flash_burn_retry'
             1522  CALL_METHOD_2         2  '2 positional arguments'
         1524_1526  POP_JUMP_IF_FALSE  1544  'to 1544'

 L.2805      1528  LOAD_GLOBAL              int
             1530  LOAD_FAST                'cfg'
             1532  LOAD_METHOD              get
             1534  LOAD_STR                 'LOAD_CFG'
             1536  LOAD_STR                 'flash_burn_retry'
             1538  CALL_METHOD_2         2  '2 positional arguments'
             1540  CALL_FUNCTION_1       1  '1 positional argument'
             1542  STORE_FAST               'flash_burn_retry'
           1544_0  COME_FROM          1524  '1524'

 L.2806      1544  LOAD_FAST                'cfg'
             1546  LOAD_METHOD              has_option
             1548  LOAD_STR                 'LOAD_CFG'
             1550  LOAD_STR                 'checksum_err_retry'
             1552  CALL_METHOD_2         2  '2 positional arguments'
         1554_1556  POP_JUMP_IF_FALSE  1576  'to 1576'

 L.2807      1558  LOAD_GLOBAL              int
             1560  LOAD_FAST                'cfg'
             1562  LOAD_METHOD              get
             1564  LOAD_STR                 'LOAD_CFG'
             1566  LOAD_STR                 'checksum_err_retry'
             1568  CALL_METHOD_2         2  '2 positional arguments'
             1570  CALL_FUNCTION_1       1  '1 positional argument'
             1572  LOAD_FAST                'self'
             1574  STORE_ATTR               _checksum_err_retry_limit
           1576_0  COME_FROM          1554  '1554'

 L.2808      1576  LOAD_FAST                'cfg'
             1578  LOAD_METHOD              has_option
             1580  LOAD_STR                 'LOAD_CFG'
             1582  LOAD_STR                 'chiptype'
             1584  CALL_METHOD_2         2  '2 positional arguments'
         1586_1588  POP_JUMP_IF_FALSE  1604  'to 1604'

 L.2809      1590  LOAD_FAST                'cfg'
             1592  LOAD_METHOD              get
             1594  LOAD_STR                 'LOAD_CFG'
             1596  LOAD_STR                 'chiptype'
             1598  CALL_METHOD_2         2  '2 positional arguments'
             1600  LOAD_FAST                'self'
             1602  STORE_ATTR               _chip_type
           1604_0  COME_FROM          1586  '1586'

 L.2810      1604  LOAD_FAST                'cfg'
             1606  LOAD_METHOD              has_option
             1608  LOAD_STR                 'LOAD_CFG'
             1610  LOAD_STR                 'cpu_reset_after_load'
             1612  CALL_METHOD_2         2  '2 positional arguments'
         1614_1616  POP_JUMP_IF_FALSE  1636  'to 1636'

 L.2811      1618  LOAD_FAST                'cfg'
             1620  LOAD_METHOD              get
             1622  LOAD_STR                 'LOAD_CFG'
             1624  LOAD_STR                 'cpu_reset_after_load'
             1626  CALL_METHOD_2         2  '2 positional arguments'
             1628  LOAD_STR                 'true'
             1630  COMPARE_OP               ==
             1632  LOAD_FAST                'self'
             1634  STORE_ATTR               _cpu_reset
           1636_0  COME_FROM          1614  '1614'

 L.2812      1636  LOAD_FAST                'cfg'
             1638  LOAD_METHOD              has_option
             1640  LOAD_STR                 'LOAD_CFG'
             1642  LOAD_STR                 'retry_delay_after_cpu_reset'
             1644  CALL_METHOD_2         2  '2 positional arguments'
         1646_1648  POP_JUMP_IF_FALSE  1682  'to 1682'

 L.2813      1650  LOAD_GLOBAL              int

 L.2814      1652  LOAD_FAST                'cfg'
             1654  LOAD_METHOD              get
             1656  LOAD_STR                 'LOAD_CFG'
             1658  LOAD_STR                 'retry_delay_after_cpu_reset'
             1660  CALL_METHOD_2         2  '2 positional arguments'
             1662  CALL_FUNCTION_1       1  '1 positional argument'
             1664  LOAD_FAST                'self'
             1666  STORE_ATTR               _retry_delay_after_cpu_reset

 L.2815      1668  LOAD_GLOBAL              bflb_utils
             1670  LOAD_METHOD              printf
             1672  LOAD_STR                 'retry delay: '
             1674  LOAD_FAST                'self'
             1676  LOAD_ATTR                _retry_delay_after_cpu_reset
             1678  CALL_METHOD_2         2  '2 positional arguments'
             1680  POP_TOP          
           1682_0  COME_FROM          1646  '1646'

 L.2816      1682  LOAD_FAST                'cfg'
             1684  LOAD_METHOD              has_option
             1686  LOAD_STR                 'LOAD_CFG'
             1688  LOAD_STR                 'eflash_loader_file'
             1690  CALL_METHOD_2         2  '2 positional arguments'
         1692_1694  POP_JUMP_IF_FALSE  1718  'to 1718'
             1696  LOAD_FAST                'eflash_loader_file'
             1698  LOAD_CONST               None
             1700  COMPARE_OP               is
         1702_1704  POP_JUMP_IF_FALSE  1718  'to 1718'

 L.2817      1706  LOAD_FAST                'cfg'
             1708  LOAD_METHOD              get
             1710  LOAD_STR                 'LOAD_CFG'
             1712  LOAD_STR                 'eflash_loader_file'
             1714  CALL_METHOD_2         2  '2 positional arguments'
             1716  STORE_FAST               'eflash_loader_file'
           1718_0  COME_FROM          1702  '1702'
           1718_1  COME_FROM          1692  '1692'

 L.2818      1718  LOAD_FAST                'cfg'
             1720  LOAD_METHOD              has_option
             1722  LOAD_STR                 'LOAD_CFG'
             1724  LOAD_STR                 'skip_mode'
             1726  CALL_METHOD_2         2  '2 positional arguments'
         1728_1730  POP_JUMP_IF_FALSE  1930  'to 1930'
             1732  LOAD_FAST                'self'
             1734  LOAD_ATTR                _skip_len
             1736  LOAD_CONST               0
             1738  COMPARE_OP               ==
         1740_1742  POP_JUMP_IF_FALSE  1930  'to 1930'

 L.2819      1744  LOAD_FAST                'cfg'
             1746  LOAD_METHOD              get
             1748  LOAD_STR                 'LOAD_CFG'
             1750  LOAD_STR                 'skip_mode'
             1752  CALL_METHOD_2         2  '2 positional arguments'
             1754  STORE_FAST               'skip_para'

 L.2820      1756  LOAD_FAST                'skip_para'
             1758  LOAD_CONST               0
             1760  BINARY_SUBSCR    
             1762  LOAD_CONST               0
             1764  LOAD_CONST               2
             1766  BUILD_SLICE_2         2 
             1768  BINARY_SUBSCR    
             1770  LOAD_STR                 '0x'
             1772  COMPARE_OP               ==
         1774_1776  POP_JUMP_IF_FALSE  1804  'to 1804'

 L.2821      1778  LOAD_GLOBAL              int
             1780  LOAD_FAST                'skip_para'
             1782  LOAD_CONST               0
             1784  BINARY_SUBSCR    
             1786  LOAD_CONST               2
             1788  LOAD_CONST               None
             1790  BUILD_SLICE_2         2 
             1792  BINARY_SUBSCR    
             1794  LOAD_CONST               16
             1796  CALL_FUNCTION_2       2  '2 positional arguments'
             1798  LOAD_FAST                'self'
             1800  STORE_ATTR               _skip_addr
             1802  JUMP_FORWARD       1820  'to 1820'
           1804_0  COME_FROM          1774  '1774'

 L.2823      1804  LOAD_GLOBAL              int
             1806  LOAD_FAST                'skip_para'
             1808  LOAD_CONST               0
             1810  BINARY_SUBSCR    
             1812  LOAD_CONST               10
             1814  CALL_FUNCTION_2       2  '2 positional arguments'
             1816  LOAD_FAST                'self'
             1818  STORE_ATTR               _skip_addr
           1820_0  COME_FROM          1802  '1802'

 L.2824      1820  LOAD_FAST                'skip_para'
             1822  LOAD_CONST               1
             1824  BINARY_SUBSCR    
             1826  LOAD_CONST               0
             1828  LOAD_CONST               2
             1830  BUILD_SLICE_2         2 
             1832  BINARY_SUBSCR    
             1834  LOAD_STR                 '0x'
             1836  COMPARE_OP               ==
         1838_1840  POP_JUMP_IF_FALSE  1868  'to 1868'

 L.2825      1842  LOAD_GLOBAL              int
             1844  LOAD_FAST                'skip_para'
             1846  LOAD_CONST               1
             1848  BINARY_SUBSCR    
             1850  LOAD_CONST               2
             1852  LOAD_CONST               None
             1854  BUILD_SLICE_2         2 
             1856  BINARY_SUBSCR    
             1858  LOAD_CONST               16
             1860  CALL_FUNCTION_2       2  '2 positional arguments'
             1862  LOAD_FAST                'self'
             1864  STORE_ATTR               _skip_len
             1866  JUMP_FORWARD       1884  'to 1884'
           1868_0  COME_FROM          1838  '1838'

 L.2827      1868  LOAD_GLOBAL              int
             1870  LOAD_FAST                'skip_para'
             1872  LOAD_CONST               1
             1874  BINARY_SUBSCR    
             1876  LOAD_CONST               10
             1878  CALL_FUNCTION_2       2  '2 positional arguments'
             1880  LOAD_FAST                'self'
             1882  STORE_ATTR               _skip_len
           1884_0  COME_FROM          1866  '1866'

 L.2828      1884  LOAD_FAST                'self'
             1886  LOAD_ATTR                _skip_len
             1888  LOAD_CONST               0
             1890  COMPARE_OP               >
         1892_1894  POP_JUMP_IF_FALSE  1930  'to 1930'

 L.2829      1896  LOAD_FAST                'erase'
             1898  LOAD_CONST               2
             1900  COMPARE_OP               ==
         1902_1904  POP_JUMP_IF_FALSE  1930  'to 1930'

 L.2830      1906  LOAD_GLOBAL              bflb_utils
             1908  LOAD_METHOD              printf
             1910  LOAD_STR                 'error: skip mode can not set flash chiperase!'
             1912  CALL_METHOD_1         1  '1 positional argument'
             1914  POP_TOP          

 L.2831      1916  LOAD_FAST                'self'
             1918  LOAD_METHOD              error_code_print
             1920  LOAD_STR                 '0044'
             1922  CALL_METHOD_1         1  '1 positional argument'
             1924  POP_TOP          

 L.2832      1926  LOAD_CONST               (False, 0)
             1928  RETURN_VALUE     
           1930_0  COME_FROM          1902  '1902'
           1930_1  COME_FROM          1892  '1892'
           1930_2  COME_FROM          1740  '1740'
           1930_3  COME_FROM          1728  '1728'

 L.2833      1930  LOAD_FAST                'self'
             1932  LOAD_ATTR                _bflb_auto_download
             1934  LOAD_CONST               False
             1936  COMPARE_OP               is
         1938_1940  POP_JUMP_IF_FALSE  1988  'to 1988'
             1942  LOAD_FAST                'cfg'
             1944  LOAD_METHOD              has_option
             1946  LOAD_STR                 'LOAD_CFG'
             1948  LOAD_STR                 'auto_burn'
             1950  CALL_METHOD_2         2  '2 positional arguments'
         1952_1954  POP_JUMP_IF_FALSE  1988  'to 1988'

 L.2834      1956  LOAD_STR                 'true'
             1958  LOAD_FAST                'cfg'
             1960  LOAD_METHOD              get
             1962  LOAD_STR                 'LOAD_CFG'
             1964  LOAD_STR                 'auto_burn'
             1966  CALL_METHOD_2         2  '2 positional arguments'
             1968  COMPARE_OP               ==
         1970_1972  POP_JUMP_IF_FALSE  1982  'to 1982'

 L.2835      1974  LOAD_CONST               True
             1976  LOAD_FAST                'self'
             1978  STORE_ATTR               _bflb_auto_download
             1980  JUMP_FORWARD       1988  'to 1988'
           1982_0  COME_FROM          1970  '1970'

 L.2837      1982  LOAD_CONST               False
             1984  LOAD_FAST                'self'
             1986  STORE_ATTR               _bflb_auto_download
           1988_0  COME_FROM          1980  '1980'
           1988_1  COME_FROM          1952  '1952'
           1988_2  COME_FROM          1938  '1938'

 L.2838      1988  LOAD_GLOBAL              bflb_utils
             1990  LOAD_METHOD              printf
             1992  LOAD_STR                 'cpu_reset='
             1994  LOAD_FAST                'self'
             1996  LOAD_ATTR                _cpu_reset
             1998  CALL_METHOD_2         2  '2 positional arguments'
             2000  POP_TOP          

 L.2839      2002  LOAD_FAST                'xtal_type'
             2004  LOAD_STR                 ''
             2006  COMPARE_OP               !=
         2008_2010  POP_JUMP_IF_FALSE  2050  'to 2050'

 L.2841      2012  LOAD_STR                 'chips/'
             2014  LOAD_FAST                'self'
             2016  LOAD_ATTR                _chip_name
             2018  LOAD_METHOD              lower
             2020  CALL_METHOD_0         0  '0 positional arguments'
             2022  BINARY_ADD       
             2024  LOAD_STR                 '/eflash_loader/eflash_loader_'
             2026  BINARY_ADD       
             2028  LOAD_FAST                'xtal_type'
             2030  LOAD_METHOD              replace
             2032  LOAD_STR                 '.'
             2034  LOAD_STR                 'p'
             2036  CALL_METHOD_2         2  '2 positional arguments'
             2038  LOAD_METHOD              lower
             2040  CALL_METHOD_0         0  '0 positional arguments'
             2042  BINARY_ADD       
             2044  LOAD_STR                 '.bin'
             2046  BINARY_ADD       
             2048  STORE_FAST               'eflash_loader_file'
           2050_0  COME_FROM          2008  '2008'

 L.2842      2050  LOAD_FAST                'load_file'
         2052_2054  POP_JUMP_IF_FALSE  2066  'to 2066'
             2056  LOAD_FAST                'eflash_loader_file'
         2058_2060  POP_JUMP_IF_TRUE   2066  'to 2066'

 L.2843      2062  LOAD_FAST                'load_file'
             2064  STORE_FAST               'eflash_loader_file'
           2066_0  COME_FROM          2058  '2058'
           2066_1  COME_FROM          2052  '2052'

 L.2844      2066  LOAD_FAST                'eflash_loader_bin'
             2068  LOAD_CONST               None
             2070  COMPARE_OP               is-not
         2072_2074  POP_JUMP_IF_FALSE  2082  'to 2082'

 L.2845      2076  LOAD_FAST                'eflash_loader_bin'
             2078  STORE_FAST               'eflash_loader_file'
             2080  JUMP_FORWARD       2106  'to 2106'
           2082_0  COME_FROM          2072  '2072'

 L.2846      2082  LOAD_FAST                'eflash_loader_file'
             2084  LOAD_CONST               None
             2086  COMPARE_OP               is-not
         2088_2090  POP_JUMP_IF_FALSE  2106  'to 2106'

 L.2847      2092  LOAD_GLOBAL              os
             2094  LOAD_ATTR                path
             2096  LOAD_METHOD              join
             2098  LOAD_GLOBAL              app_path
             2100  LOAD_FAST                'eflash_loader_file'
             2102  CALL_METHOD_2         2  '2 positional arguments'
             2104  STORE_FAST               'eflash_loader_file'
           2106_0  COME_FROM          2088  '2088'
           2106_1  COME_FROM          2080  '2080'

 L.2848      2106  LOAD_GLOBAL              bflb_utils
             2108  LOAD_METHOD              printf
             2110  LOAD_STR                 'chiptype: '
             2112  LOAD_FAST                'self'
             2114  LOAD_ATTR                _chip_type
             2116  CALL_METHOD_2         2  '2 positional arguments'
             2118  POP_TOP          

 L.2849      2120  LOAD_FAST                'interface'
             2122  LOAD_STR                 'uart'
             2124  COMPARE_OP               ==
         2126_2128  POP_JUMP_IF_TRUE   2140  'to 2140'
             2130  LOAD_FAST                'interface'
             2132  LOAD_STR                 'sdio'
             2134  COMPARE_OP               ==
         2136_2138  POP_JUMP_IF_FALSE  2496  'to 2496'
           2140_0  COME_FROM          2126  '2126'

 L.2850      2140  LOAD_GLOBAL              bflb_utils
             2142  LOAD_METHOD              printf
             2144  LOAD_STR                 '========= Interface is %s ========='
             2146  LOAD_FAST                'interface'
             2148  BINARY_MODULO    
             2150  CALL_METHOD_1         1  '1 positional argument'
             2152  POP_TOP          

 L.2851      2154  LOAD_GLOBAL              bflb_img_loader
             2156  LOAD_METHOD              BflbImgLoader

 L.2852      2158  LOAD_FAST                'self'
             2160  LOAD_ATTR                _chip_type
             2162  LOAD_FAST                'self'
             2164  LOAD_ATTR                _chip_name
             2166  LOAD_FAST                'interface'
             2168  LOAD_FAST                'create_cfg'
             2170  CALL_METHOD_4         4  '4 positional arguments'
             2172  LOAD_FAST                'self'
             2174  STORE_ATTR               _bflb_com_img_loader

 L.2853      2176  LOAD_FAST                'self'
             2178  LOAD_ATTR                _bflb_com_img_loader
             2180  LOAD_ATTR                bflb_boot_if
             2182  LOAD_FAST                'self'
             2184  STORE_ATTR               _bflb_com_if

 L.2854      2186  LOAD_FAST                'load_speed'
         2188_2190  POP_JUMP_IF_FALSE  2200  'to 2200'

 L.2855      2192  LOAD_FAST                'load_speed'
             2194  LOAD_FAST                'self'
             2196  STORE_ATTR               _bflb_com_speed
             2198  JUMP_FORWARD       2218  'to 2218'
           2200_0  COME_FROM          2188  '2188'

 L.2857      2200  LOAD_GLOBAL              int
             2202  LOAD_FAST                'cfg'
             2204  LOAD_METHOD              get
             2206  LOAD_STR                 'LOAD_CFG'
             2208  LOAD_STR                 'speed_uart_load'
             2210  CALL_METHOD_2         2  '2 positional arguments'
             2212  CALL_FUNCTION_1       1  '1 positional argument'
             2214  LOAD_FAST                'self'
             2216  STORE_ATTR               _bflb_com_speed
           2218_0  COME_FROM          2198  '2198'

 L.2858      2218  LOAD_GLOBAL              bflb_utils
             2220  LOAD_METHOD              printf
             2222  LOAD_STR                 'com speed: '
             2224  LOAD_FAST                'self'
             2226  LOAD_ATTR                _bflb_com_speed
             2228  CALL_METHOD_2         2  '2 positional arguments'
             2230  POP_TOP          

 L.2859      2232  LOAD_GLOBAL              int
             2234  LOAD_FAST                'cfg'
             2236  LOAD_METHOD              get
             2238  LOAD_STR                 'LOAD_CFG'
             2240  LOAD_STR                 'speed_uart_boot'
             2242  CALL_METHOD_2         2  '2 positional arguments'
             2244  CALL_FUNCTION_1       1  '1 positional argument'
             2246  LOAD_FAST                'self'
             2248  STORE_ATTR               _bflb_boot_speed

 L.2860      2250  LOAD_FAST                'self'
             2252  LOAD_ATTR                _isp_en
             2254  LOAD_CONST               True
             2256  COMPARE_OP               is
         2258_2260  POP_JUMP_IF_FALSE  2282  'to 2282'
             2262  LOAD_FAST                'self'
             2264  LOAD_ATTR                _chip_type
             2266  LOAD_STR                 'bl602'
             2268  COMPARE_OP               ==
         2270_2272  POP_JUMP_IF_FALSE  2282  'to 2282'

 L.2861      2274  LOAD_FAST                'self'
             2276  LOAD_ATTR                _bflb_com_speed
             2278  LOAD_FAST                'self'
             2280  STORE_ATTR               _bflb_boot_speed
           2282_0  COME_FROM          2270  '2270'
           2282_1  COME_FROM          2258  '2258'

 L.2862      2282  LOAD_FAST                'cfg'
             2284  LOAD_METHOD              has_option
             2286  LOAD_STR                 'LOAD_CFG'
             2288  LOAD_STR                 'reset_hold_time'
             2290  CALL_METHOD_2         2  '2 positional arguments'
         2292_2294  POP_JUMP_IF_FALSE  2312  'to 2312'

 L.2863      2296  LOAD_GLOBAL              int
             2298  LOAD_FAST                'cfg'
             2300  LOAD_METHOD              get
             2302  LOAD_STR                 'LOAD_CFG'
             2304  LOAD_STR                 'reset_hold_time'
             2306  CALL_METHOD_2         2  '2 positional arguments'
             2308  CALL_FUNCTION_1       1  '1 positional argument'
             2310  STORE_FAST               'reset_hold_time'
           2312_0  COME_FROM          2292  '2292'

 L.2864      2312  LOAD_FAST                'cfg'
             2314  LOAD_METHOD              has_option
             2316  LOAD_STR                 'LOAD_CFG'
             2318  LOAD_STR                 'shake_hand_delay'
             2320  CALL_METHOD_2         2  '2 positional arguments'
         2322_2324  POP_JUMP_IF_FALSE  2342  'to 2342'

 L.2865      2326  LOAD_GLOBAL              int
             2328  LOAD_FAST                'cfg'
             2330  LOAD_METHOD              get
             2332  LOAD_STR                 'LOAD_CFG'
             2334  LOAD_STR                 'shake_hand_delay'
             2336  CALL_METHOD_2         2  '2 positional arguments'
             2338  CALL_FUNCTION_1       1  '1 positional argument'
             2340  STORE_FAST               'shake_hand_delay'
           2342_0  COME_FROM          2322  '2322'

 L.2866      2342  LOAD_FAST                'cfg'
             2344  LOAD_METHOD              has_option
             2346  LOAD_STR                 'LOAD_CFG'
             2348  LOAD_STR                 'do_reset'
             2350  CALL_METHOD_2         2  '2 positional arguments'
         2352_2354  POP_JUMP_IF_FALSE  2372  'to 2372'

 L.2867      2356  LOAD_FAST                'cfg'
             2358  LOAD_METHOD              get
             2360  LOAD_STR                 'LOAD_CFG'
             2362  LOAD_STR                 'do_reset'
             2364  CALL_METHOD_2         2  '2 positional arguments'
             2366  LOAD_STR                 'true'
             2368  COMPARE_OP               ==
             2370  STORE_FAST               'do_reset'
           2372_0  COME_FROM          2352  '2352'

 L.2868      2372  LOAD_FAST                'cfg'
             2374  LOAD_METHOD              has_option
             2376  LOAD_STR                 'LOAD_CFG'
             2378  LOAD_STR                 'reset_revert'
             2380  CALL_METHOD_2         2  '2 positional arguments'
         2382_2384  POP_JUMP_IF_FALSE  2402  'to 2402'

 L.2869      2386  LOAD_FAST                'cfg'
             2388  LOAD_METHOD              get
             2390  LOAD_STR                 'LOAD_CFG'
             2392  LOAD_STR                 'reset_revert'
             2394  CALL_METHOD_2         2  '2 positional arguments'
             2396  LOAD_STR                 'true'
             2398  COMPARE_OP               ==
             2400  STORE_FAST               'reset_revert'
           2402_0  COME_FROM          2382  '2382'

 L.2870      2402  LOAD_FAST                'update_cutoff_time'
         2404_2406  POP_JUMP_IF_FALSE  2438  'to 2438'
             2408  LOAD_FAST                'cfg'
             2410  LOAD_METHOD              has_option
             2412  LOAD_STR                 'LOAD_CFG'
             2414  LOAD_STR                 'cutoff_time'
             2416  CALL_METHOD_2         2  '2 positional arguments'
         2418_2420  POP_JUMP_IF_FALSE  2438  'to 2438'

 L.2871      2422  LOAD_GLOBAL              int
             2424  LOAD_FAST                'cfg'
             2426  LOAD_METHOD              get
             2428  LOAD_STR                 'LOAD_CFG'
             2430  LOAD_STR                 'cutoff_time'
             2432  CALL_METHOD_2         2  '2 positional arguments'
             2434  CALL_FUNCTION_1       1  '1 positional argument'
             2436  STORE_FAST               'cutoff_time'
           2438_0  COME_FROM          2418  '2418'
           2438_1  COME_FROM          2404  '2404'

 L.2872      2438  LOAD_FAST                'cfg'
             2440  LOAD_METHOD              has_option
             2442  LOAD_STR                 'LOAD_CFG'
             2444  LOAD_STR                 'isp_mode_speed'
             2446  CALL_METHOD_2         2  '2 positional arguments'
         2448_2450  POP_JUMP_IF_FALSE  2794  'to 2794'
             2452  LOAD_FAST                'self'
             2454  LOAD_ATTR                _isp_en
             2456  LOAD_CONST               True
             2458  COMPARE_OP               is
         2460_2462  POP_JUMP_IF_FALSE  2794  'to 2794'

 L.2873      2464  LOAD_GLOBAL              int
             2466  LOAD_FAST                'cfg'
             2468  LOAD_METHOD              get
             2470  LOAD_STR                 'LOAD_CFG'
             2472  LOAD_STR                 'isp_mode_speed'
             2474  CALL_METHOD_2         2  '2 positional arguments'
             2476  CALL_FUNCTION_1       1  '1 positional argument'
             2478  STORE_FAST               'isp_mode_speed'

 L.2874      2480  LOAD_FAST                'self'
             2482  LOAD_ATTR                _bflb_com_if
             2484  LOAD_METHOD              if_set_isp_baudrate
             2486  LOAD_FAST                'isp_mode_speed'
             2488  CALL_METHOD_1         1  '1 positional argument'
             2490  POP_TOP          
         2492_2494  JUMP_FORWARD       2794  'to 2794'
           2496_0  COME_FROM          2136  '2136'

 L.2875      2496  LOAD_FAST                'interface'
             2498  LOAD_STR                 'jlink'
             2500  COMPARE_OP               ==
         2502_2504  POP_JUMP_IF_FALSE  2588  'to 2588'

 L.2876      2506  LOAD_GLOBAL              bflb_utils
             2508  LOAD_METHOD              printf
             2510  LOAD_STR                 '========= Interface is JLink ========='
             2512  CALL_METHOD_1         1  '1 positional argument'
             2514  POP_TOP          

 L.2877      2516  LOAD_GLOBAL              bflb_interface_jlink
             2518  LOAD_METHOD              BflbJLinkPort
             2520  CALL_METHOD_0         0  '0 positional arguments'
             2522  LOAD_FAST                'self'
             2524  STORE_ATTR               _bflb_com_if

 L.2878      2526  LOAD_FAST                'load_speed'
         2528_2530  POP_JUMP_IF_FALSE  2560  'to 2560'

 L.2879      2532  LOAD_FAST                'load_speed'
             2534  LOAD_CONST               1000
             2536  BINARY_FLOOR_DIVIDE
             2538  LOAD_FAST                'self'
             2540  STORE_ATTR               _bflb_com_speed

 L.2880      2542  LOAD_GLOBAL              bflb_utils
             2544  LOAD_METHOD              printf
             2546  LOAD_STR                 'com speed: %dk'
             2548  LOAD_FAST                'self'
             2550  LOAD_ATTR                _bflb_com_speed
             2552  BINARY_MODULO    
             2554  CALL_METHOD_1         1  '1 positional argument'
             2556  POP_TOP          
             2558  JUMP_FORWARD       2578  'to 2578'
           2560_0  COME_FROM          2528  '2528'

 L.2882      2560  LOAD_GLOBAL              int
             2562  LOAD_FAST                'cfg'
             2564  LOAD_METHOD              get
             2566  LOAD_STR                 'LOAD_CFG'
             2568  LOAD_STR                 'speed_jlink'
             2570  CALL_METHOD_2         2  '2 positional arguments'
             2572  CALL_FUNCTION_1       1  '1 positional argument'
             2574  LOAD_FAST                'self'
             2576  STORE_ATTR               _bflb_com_speed
           2578_0  COME_FROM          2558  '2558'

 L.2883      2578  LOAD_FAST                'self'
             2580  LOAD_ATTR                _bflb_com_speed
             2582  LOAD_FAST                'self'
             2584  STORE_ATTR               _bflb_boot_speed
             2586  JUMP_FORWARD       2794  'to 2794'
           2588_0  COME_FROM          2502  '2502'

 L.2884      2588  LOAD_FAST                'interface'
             2590  LOAD_STR                 'openocd'
             2592  COMPARE_OP               ==
         2594_2596  POP_JUMP_IF_FALSE  2680  'to 2680'

 L.2885      2598  LOAD_GLOBAL              bflb_utils
             2600  LOAD_METHOD              printf
             2602  LOAD_STR                 '========= Interface is Openocd ========='
             2604  CALL_METHOD_1         1  '1 positional argument'
             2606  POP_TOP          

 L.2886      2608  LOAD_GLOBAL              bflb_interface_openocd
             2610  LOAD_METHOD              BflbOpenocdPort
             2612  CALL_METHOD_0         0  '0 positional arguments'
             2614  LOAD_FAST                'self'
             2616  STORE_ATTR               _bflb_com_if

 L.2887      2618  LOAD_FAST                'load_speed'
         2620_2622  POP_JUMP_IF_FALSE  2652  'to 2652'

 L.2888      2624  LOAD_FAST                'load_speed'
             2626  LOAD_CONST               1000
             2628  BINARY_FLOOR_DIVIDE
             2630  LOAD_FAST                'self'
             2632  STORE_ATTR               _bflb_com_speed

 L.2889      2634  LOAD_GLOBAL              bflb_utils
             2636  LOAD_METHOD              printf
             2638  LOAD_STR                 'com speed: %dk'
             2640  LOAD_FAST                'self'
             2642  LOAD_ATTR                _bflb_com_speed
             2644  BINARY_MODULO    
             2646  CALL_METHOD_1         1  '1 positional argument'
             2648  POP_TOP          
             2650  JUMP_FORWARD       2670  'to 2670'
           2652_0  COME_FROM          2620  '2620'

 L.2891      2652  LOAD_GLOBAL              int
             2654  LOAD_FAST                'cfg'
             2656  LOAD_METHOD              get
             2658  LOAD_STR                 'LOAD_CFG'
             2660  LOAD_STR                 'speed_jlink'
             2662  CALL_METHOD_2         2  '2 positional arguments'
             2664  CALL_FUNCTION_1       1  '1 positional argument'
             2666  LOAD_FAST                'self'
             2668  STORE_ATTR               _bflb_com_speed
           2670_0  COME_FROM          2650  '2650'

 L.2892      2670  LOAD_FAST                'self'
             2672  LOAD_ATTR                _bflb_com_speed
             2674  LOAD_FAST                'self'
             2676  STORE_ATTR               _bflb_boot_speed
             2678  JUMP_FORWARD       2794  'to 2794'
           2680_0  COME_FROM          2594  '2594'

 L.2893      2680  LOAD_FAST                'interface'
             2682  LOAD_STR                 'cklink'
             2684  COMPARE_OP               ==
         2686_2688  POP_JUMP_IF_FALSE  2772  'to 2772'

 L.2894      2690  LOAD_GLOBAL              bflb_utils
             2692  LOAD_METHOD              printf
             2694  LOAD_STR                 '========= Interface is CKLink ========='
             2696  CALL_METHOD_1         1  '1 positional argument'
             2698  POP_TOP          

 L.2895      2700  LOAD_GLOBAL              bflb_interface_cklink
             2702  LOAD_METHOD              BflbCKLinkPort
             2704  CALL_METHOD_0         0  '0 positional arguments'
             2706  LOAD_FAST                'self'
             2708  STORE_ATTR               _bflb_com_if

 L.2896      2710  LOAD_FAST                'load_speed'
         2712_2714  POP_JUMP_IF_FALSE  2744  'to 2744'

 L.2897      2716  LOAD_FAST                'load_speed'
             2718  LOAD_CONST               1000
             2720  BINARY_FLOOR_DIVIDE
             2722  LOAD_FAST                'self'
             2724  STORE_ATTR               _bflb_com_speed

 L.2898      2726  LOAD_GLOBAL              bflb_utils
             2728  LOAD_METHOD              printf
             2730  LOAD_STR                 'com speed: %dk'
             2732  LOAD_FAST                'self'
             2734  LOAD_ATTR                _bflb_com_speed
             2736  BINARY_MODULO    
             2738  CALL_METHOD_1         1  '1 positional argument'
             2740  POP_TOP          
             2742  JUMP_FORWARD       2762  'to 2762'
           2744_0  COME_FROM          2712  '2712'

 L.2900      2744  LOAD_GLOBAL              int
             2746  LOAD_FAST                'cfg'
             2748  LOAD_METHOD              get
             2750  LOAD_STR                 'LOAD_CFG'
             2752  LOAD_STR                 'speed_jlink'
             2754  CALL_METHOD_2         2  '2 positional arguments'
             2756  CALL_FUNCTION_1       1  '1 positional argument'
             2758  LOAD_FAST                'self'
             2760  STORE_ATTR               _bflb_com_speed
           2762_0  COME_FROM          2742  '2742'

 L.2901      2762  LOAD_FAST                'self'
             2764  LOAD_ATTR                _bflb_com_speed
             2766  LOAD_FAST                'self'
             2768  STORE_ATTR               _bflb_boot_speed
             2770  JUMP_FORWARD       2794  'to 2794'
           2772_0  COME_FROM          2686  '2686'

 L.2903      2772  LOAD_GLOBAL              bflb_utils
             2774  LOAD_METHOD              printf
             2776  LOAD_FAST                'interface'
             2778  LOAD_STR                 ' is not supported '
             2780  BINARY_ADD       
             2782  CALL_METHOD_1         1  '1 positional argument'
             2784  POP_TOP          

 L.2904      2786  LOAD_CONST               False
             2788  LOAD_FAST                'flash_burn_retry'
             2790  BUILD_TUPLE_2         2 
             2792  RETURN_VALUE     
           2794_0  COME_FROM          2770  '2770'
           2794_1  COME_FROM          2678  '2678'
           2794_2  COME_FROM          2586  '2586'
           2794_3  COME_FROM          2492  '2492'
           2794_4  COME_FROM          2460  '2460'
           2794_5  COME_FROM          2448  '2448'

 L.2905      2794  LOAD_CONST               True
             2796  LOAD_FAST                'self'
             2798  STORE_ATTR               _need_shake_hand

 L.2906      2800  LOAD_CONST               False
             2802  STORE_FAST               'ram_load'

 L.2907      2804  LOAD_CONST               1
             2806  STORE_FAST               'load_function'

 L.2908      2808  LOAD_FAST                'args'
             2810  LOAD_ATTR                ram
         2812_2814  POP_JUMP_IF_FALSE  2832  'to 2832'
             2816  LOAD_FAST                'args'
             2818  LOAD_ATTR                file
         2820_2822  POP_JUMP_IF_FALSE  2832  'to 2832'

 L.2909      2824  LOAD_CONST               True
             2826  STORE_FAST               'ram_load'

 L.2910      2828  LOAD_FAST                'file'
             2830  STORE_FAST               'eflash_loader_file'
           2832_0  COME_FROM          2820  '2820'
           2832_1  COME_FROM          2812  '2812'

 L.2912  2832_2834  SETUP_EXCEPT       3658  'to 3658'

 L.2913      2836  LOAD_FAST                'args'
             2838  LOAD_ATTR                chipid
         2840_2842  POP_JUMP_IF_FALSE  2910  'to 2910'

 L.2914      2844  LOAD_FAST                'self'
             2846  LOAD_METHOD              get_boot_info
             2848  LOAD_FAST                'interface'
             2850  LOAD_FAST                'eflash_loader_file'
             2852  LOAD_FAST                'do_reset'

 L.2915      2854  LOAD_FAST                'reset_hold_time'
             2856  LOAD_FAST                'shake_hand_delay'

 L.2916      2858  LOAD_FAST                'reset_revert'
             2860  LOAD_FAST                'cutoff_time'

 L.2917      2862  LOAD_FAST                'shake_hand_retry'
             2864  CALL_METHOD_8         8  '8 positional arguments'
             2866  UNPACK_SEQUENCE_3     3 
             2868  STORE_FAST               'ret'
             2870  STORE_FAST               'bootinfo'
             2872  STORE_FAST               'res'

 L.2918      2874  LOAD_FAST                'ret'
             2876  LOAD_CONST               False
             2878  COMPARE_OP               is
         2880_2882  POP_JUMP_IF_FALSE  2902  'to 2902'

 L.2919      2884  LOAD_FAST                'self'
             2886  LOAD_METHOD              error_code_print
             2888  LOAD_STR                 '0003'
             2890  CALL_METHOD_1         1  '1 positional argument'
             2892  POP_TOP          

 L.2920      2894  LOAD_CONST               False
             2896  LOAD_FAST                'flash_burn_retry'
             2898  BUILD_TUPLE_2         2 
             2900  RETURN_VALUE     
           2902_0  COME_FROM          2880  '2880'

 L.2922      2902  LOAD_CONST               True
             2904  LOAD_FAST                'flash_burn_retry'
             2906  BUILD_TUPLE_2         2 
             2908  RETURN_VALUE     
           2910_0  COME_FROM          2840  '2840'

 L.2924      2910  LOAD_FAST                'cfg'
             2912  LOAD_METHOD              has_option
             2914  LOAD_STR                 'LOAD_CFG'
             2916  LOAD_STR                 'load_function'
             2918  CALL_METHOD_2         2  '2 positional arguments'
         2920_2922  POP_JUMP_IF_FALSE  2940  'to 2940'

 L.2925      2924  LOAD_GLOBAL              int
             2926  LOAD_FAST                'cfg'
             2928  LOAD_METHOD              get
             2930  LOAD_STR                 'LOAD_CFG'
             2932  LOAD_STR                 'load_function'
             2934  CALL_METHOD_2         2  '2 positional arguments'
             2936  CALL_FUNCTION_1       1  '1 positional argument'
             2938  STORE_FAST               'load_function'
           2940_0  COME_FROM          2920  '2920'

 L.2926      2940  LOAD_FAST                'cfg'
             2942  LOAD_METHOD              has_option
             2944  LOAD_STR                 'LOAD_CFG'
             2946  LOAD_STR                 'isp_shakehand_timeout'
             2948  CALL_METHOD_2         2  '2 positional arguments'
         2950_2952  POP_JUMP_IF_FALSE  2972  'to 2972'

 L.2927      2954  LOAD_GLOBAL              int
             2956  LOAD_FAST                'cfg'
             2958  LOAD_METHOD              get
             2960  LOAD_STR                 'LOAD_CFG'
             2962  LOAD_STR                 'isp_shakehand_timeout'
             2964  CALL_METHOD_2         2  '2 positional arguments'
             2966  CALL_FUNCTION_1       1  '1 positional argument'
             2968  LOAD_FAST                'self'
             2970  STORE_ATTR               _isp_shakehand_timeout
           2972_0  COME_FROM          2950  '2950'

 L.2928      2972  LOAD_FAST                'self'
             2974  LOAD_ATTR                _isp_en
             2976  LOAD_CONST               True
             2978  COMPARE_OP               is
         2980_2982  POP_JUMP_IF_FALSE  3042  'to 3042'

 L.2929      2984  LOAD_FAST                'self'
             2986  LOAD_ATTR                _isp_shakehand_timeout
             2988  LOAD_CONST               0
             2990  COMPARE_OP               ==
         2992_2994  POP_JUMP_IF_FALSE  3002  'to 3002'

 L.2930      2996  LOAD_CONST               5
             2998  LOAD_FAST                'self'
             3000  STORE_ATTR               _isp_shakehand_timeout
           3002_0  COME_FROM          2992  '2992'

 L.2931      3002  LOAD_FAST                'self'
             3004  LOAD_ATTR                _chip_type
             3006  LOAD_STR                 'bl702'
             3008  COMPARE_OP               ==
         3010_3012  POP_JUMP_IF_FALSE  3020  'to 3020'

 L.2932      3014  LOAD_CONST               0
             3016  STORE_FAST               'load_function'
             3018  JUMP_FORWARD       3042  'to 3042'
           3020_0  COME_FROM          3010  '3010'

 L.2933      3020  LOAD_FAST                'self'
             3022  LOAD_ATTR                _chip_type
             3024  LOAD_STR                 'bl602'
             3026  COMPARE_OP               ==
         3028_3030  POP_JUMP_IF_FALSE  3038  'to 3038'

 L.2934      3032  LOAD_CONST               1
             3034  STORE_FAST               'load_function'
             3036  JUMP_FORWARD       3042  'to 3042'
           3038_0  COME_FROM          3028  '3028'

 L.2936      3038  LOAD_CONST               2
             3040  STORE_FAST               'load_function'
           3042_0  COME_FROM          3036  '3036'
           3042_1  COME_FROM          3018  '3018'
           3042_2  COME_FROM          2980  '2980'

 L.2937      3042  LOAD_FAST                'ram_load'
         3044_3046  POP_JUMP_IF_FALSE  3052  'to 3052'

 L.2938      3048  LOAD_CONST               1
             3050  STORE_FAST               'load_function'
           3052_0  COME_FROM          3044  '3044'

 L.2939      3052  LOAD_FAST                'load_function'
             3054  LOAD_CONST               0
             3056  COMPARE_OP               ==
         3058_3060  POP_JUMP_IF_FALSE  3076  'to 3076'

 L.2940      3062  LOAD_GLOBAL              bflb_utils
             3064  LOAD_METHOD              printf
             3066  LOAD_STR                 'No need load eflash_loader.bin'
             3068  CALL_METHOD_1         1  '1 positional argument'
             3070  POP_TOP          
         3072_3074  JUMP_FORWARD       3654  'to 3654'
           3076_0  COME_FROM          3058  '3058'

 L.2941      3076  LOAD_FAST                'load_function'
             3078  LOAD_CONST               1
             3080  COMPARE_OP               ==
         3082_3084  POP_JUMP_IF_FALSE  3296  'to 3296'

 L.2942      3086  LOAD_CONST               False
             3088  STORE_FAST               'load_bin_pass'

 L.2943      3090  LOAD_GLOBAL              bflb_utils
             3092  LOAD_METHOD              printf
             3094  LOAD_STR                 'Eflash load helper file: '
             3096  LOAD_FAST                'eflash_loader_file'
             3098  CALL_METHOD_2         2  '2 positional arguments'
             3100  POP_TOP          

 L.2944      3102  LOAD_FAST                'self'
             3104  LOAD_METHOD              load_helper_bin
             3106  LOAD_FAST                'interface'
             3108  LOAD_FAST                'eflash_loader_file'
             3110  LOAD_FAST                'do_reset'

 L.2945      3112  LOAD_FAST                'reset_hold_time'
             3114  LOAD_FAST                'shake_hand_delay'

 L.2946      3116  LOAD_FAST                'reset_revert'
             3118  LOAD_FAST                'cutoff_time'

 L.2947      3120  LOAD_FAST                'shake_hand_retry'

 L.2948      3122  LOAD_FAST                'self'
             3124  LOAD_ATTR                _isp_shakehand_timeout
             3126  CALL_METHOD_9         9  '9 positional arguments'
             3128  UNPACK_SEQUENCE_3     3 
             3130  STORE_FAST               'ret'
             3132  STORE_FAST               'bootinfo'
             3134  STORE_FAST               'res'

 L.2949      3136  LOAD_FAST                'res'
             3138  LOAD_STR                 'shake hand fail'
             3140  COMPARE_OP               ==
         3142_3144  POP_JUMP_IF_FALSE  3156  'to 3156'

 L.2950      3146  LOAD_FAST                'self'
             3148  LOAD_METHOD              error_code_print
             3150  LOAD_STR                 '0050'
             3152  CALL_METHOD_1         1  '1 positional argument'
             3154  POP_TOP          
           3156_0  COME_FROM          3142  '3142'

 L.2951      3156  LOAD_FAST                'res'
             3158  LOAD_METHOD              startswith
             3160  LOAD_STR                 'repeat_burn'
             3162  CALL_METHOD_1         1  '1 positional argument'
             3164  LOAD_CONST               True
             3166  COMPARE_OP               is
         3168_3170  POP_JUMP_IF_FALSE  3180  'to 3180'

 L.2953      3172  LOAD_STR                 'repeat_burn'
             3174  LOAD_FAST                'flash_burn_retry'
             3176  BUILD_TUPLE_2         2 
             3178  RETURN_VALUE     
           3180_0  COME_FROM          3168  '3168'

 L.2954      3180  LOAD_FAST                'res'
             3182  LOAD_METHOD              startswith
             3184  LOAD_STR                 'error_shakehand'
             3186  CALL_METHOD_1         1  '1 positional argument'
             3188  LOAD_CONST               True
             3190  COMPARE_OP               is
         3192_3194  POP_JUMP_IF_FALSE  3240  'to 3240'

 L.2955      3196  LOAD_FAST                'self'
             3198  LOAD_ATTR                _cpu_reset
             3200  LOAD_CONST               True
             3202  COMPARE_OP               is
         3204_3206  POP_JUMP_IF_FALSE  3226  'to 3226'

 L.2956      3208  LOAD_FAST                'self'
             3210  LOAD_METHOD              error_code_print
             3212  LOAD_STR                 '0003'
             3214  CALL_METHOD_1         1  '1 positional argument'
             3216  POP_TOP          

 L.2957      3218  LOAD_CONST               False
             3220  LOAD_FAST                'flash_burn_retry'
             3222  BUILD_TUPLE_2         2 
             3224  RETURN_VALUE     
           3226_0  COME_FROM          3204  '3204'

 L.2959      3226  LOAD_CONST               True
             3228  STORE_FAST               'load_bin_pass'

 L.2960      3230  LOAD_GLOBAL              time
             3232  LOAD_METHOD              sleep
             3234  LOAD_CONST               4.5
             3236  CALL_METHOD_1         1  '1 positional argument'
             3238  POP_TOP          
           3240_0  COME_FROM          3192  '3192'

 L.2961      3240  LOAD_FAST                'ret'
             3242  LOAD_CONST               False
             3244  COMPARE_OP               is
         3246_3248  POP_JUMP_IF_FALSE  3278  'to 3278'
             3250  LOAD_FAST                'load_bin_pass'
             3252  LOAD_CONST               False
             3254  COMPARE_OP               ==
         3256_3258  POP_JUMP_IF_FALSE  3278  'to 3278'

 L.2962      3260  LOAD_FAST                'self'
             3262  LOAD_METHOD              error_code_print
             3264  LOAD_STR                 '0003'
             3266  CALL_METHOD_1         1  '1 positional argument'
             3268  POP_TOP          

 L.2963      3270  LOAD_CONST               False
             3272  LOAD_FAST                'flash_burn_retry'
             3274  BUILD_TUPLE_2         2 
             3276  RETURN_VALUE     
           3278_0  COME_FROM          3256  '3256'
           3278_1  COME_FROM          3246  '3246'

 L.2964      3278  LOAD_FAST                'ram_load'
         3280_3282  POP_JUMP_IF_FALSE  3654  'to 3654'

 L.2965      3284  LOAD_CONST               True
             3286  LOAD_FAST                'flash_burn_retry'
             3288  BUILD_TUPLE_2         2 
             3290  RETURN_VALUE     
         3292_3294  JUMP_FORWARD       3654  'to 3654'
           3296_0  COME_FROM          3082  '3082'

 L.2966      3296  LOAD_FAST                'load_function'
             3298  LOAD_CONST               2
             3300  COMPARE_OP               ==
         3302_3304  POP_JUMP_IF_FALSE  3654  'to 3654'

 L.2967      3306  LOAD_CONST               False
             3308  STORE_FAST               'load_bin_pass'

 L.2968      3310  LOAD_GLOBAL              bflb_utils
             3312  LOAD_METHOD              printf
             3314  LOAD_STR                 'Bootrom load'
             3316  CALL_METHOD_1         1  '1 positional argument'
             3318  POP_TOP          

 L.2969      3320  LOAD_FAST                'self'
             3322  LOAD_METHOD              get_boot_info
             3324  LOAD_FAST                'interface'
             3326  LOAD_FAST                'eflash_loader_file'
             3328  LOAD_FAST                'do_reset'

 L.2970      3330  LOAD_FAST                'reset_hold_time'
             3332  LOAD_FAST                'shake_hand_delay'

 L.2971      3334  LOAD_FAST                'reset_revert'
             3336  LOAD_FAST                'cutoff_time'

 L.2972      3338  LOAD_FAST                'shake_hand_retry'

 L.2973      3340  LOAD_FAST                'self'
             3342  LOAD_ATTR                _isp_shakehand_timeout
             3344  CALL_METHOD_9         9  '9 positional arguments'
             3346  UNPACK_SEQUENCE_3     3 
             3348  STORE_FAST               'ret'
             3350  STORE_FAST               'bootinfo'
             3352  STORE_FAST               'res'

 L.2974      3354  LOAD_FAST                'res'
             3356  LOAD_STR                 'shake hand fail'
             3358  COMPARE_OP               ==
         3360_3362  POP_JUMP_IF_FALSE  3374  'to 3374'

 L.2975      3364  LOAD_FAST                'self'
             3366  LOAD_METHOD              error_code_print
             3368  LOAD_STR                 '0050'
             3370  CALL_METHOD_1         1  '1 positional argument'
             3372  POP_TOP          
           3374_0  COME_FROM          3360  '3360'

 L.2976      3374  LOAD_FAST                'res'
             3376  LOAD_METHOD              startswith
             3378  LOAD_STR                 'repeat_burn'
             3380  CALL_METHOD_1         1  '1 positional argument'
             3382  LOAD_CONST               True
             3384  COMPARE_OP               is
         3386_3388  POP_JUMP_IF_FALSE  3398  'to 3398'

 L.2978      3390  LOAD_STR                 'repeat_burn'
             3392  LOAD_FAST                'flash_burn_retry'
             3394  BUILD_TUPLE_2         2 
             3396  RETURN_VALUE     
           3398_0  COME_FROM          3386  '3386'

 L.2979      3398  LOAD_FAST                'res'
             3400  LOAD_METHOD              startswith
             3402  LOAD_STR                 'error_shakehand'
             3404  CALL_METHOD_1         1  '1 positional argument'
             3406  LOAD_CONST               True
             3408  COMPARE_OP               is
         3410_3412  POP_JUMP_IF_FALSE  3458  'to 3458'

 L.2980      3414  LOAD_FAST                'self'
             3416  LOAD_ATTR                _cpu_reset
             3418  LOAD_CONST               True
             3420  COMPARE_OP               is
         3422_3424  POP_JUMP_IF_FALSE  3444  'to 3444'

 L.2981      3426  LOAD_FAST                'self'
             3428  LOAD_METHOD              error_code_print
             3430  LOAD_STR                 '0003'
             3432  CALL_METHOD_1         1  '1 positional argument'
             3434  POP_TOP          

 L.2982      3436  LOAD_CONST               False
             3438  LOAD_FAST                'flash_burn_retry'
             3440  BUILD_TUPLE_2         2 
             3442  RETURN_VALUE     
           3444_0  COME_FROM          3422  '3422'

 L.2984      3444  LOAD_CONST               True
             3446  STORE_FAST               'load_bin_pass'

 L.2985      3448  LOAD_GLOBAL              time
             3450  LOAD_METHOD              sleep
             3452  LOAD_CONST               4.5
             3454  CALL_METHOD_1         1  '1 positional argument'
             3456  POP_TOP          
           3458_0  COME_FROM          3410  '3410'

 L.2986      3458  LOAD_FAST                'ret'
             3460  LOAD_CONST               False
             3462  COMPARE_OP               is
         3464_3466  POP_JUMP_IF_FALSE  3496  'to 3496'
             3468  LOAD_FAST                'load_bin_pass'
             3470  LOAD_CONST               False
             3472  COMPARE_OP               ==
         3474_3476  POP_JUMP_IF_FALSE  3496  'to 3496'

 L.2987      3478  LOAD_FAST                'self'
             3480  LOAD_METHOD              error_code_print
             3482  LOAD_STR                 '0050'
             3484  CALL_METHOD_1         1  '1 positional argument'
             3486  POP_TOP          

 L.2988      3488  LOAD_CONST               False
             3490  LOAD_FAST                'flash_burn_retry'
             3492  BUILD_TUPLE_2         2 
             3494  RETURN_VALUE     
           3496_0  COME_FROM          3474  '3474'
           3496_1  COME_FROM          3464  '3464'

 L.2989      3496  LOAD_CONST               False
             3498  LOAD_FAST                'self'
             3500  STORE_ATTR               _need_shake_hand

 L.2990      3502  LOAD_GLOBAL              bytearray
             3504  LOAD_CONST               0
             3506  CALL_FUNCTION_1       1  '1 positional argument'
             3508  STORE_FAST               'clock_para'

 L.2991      3510  LOAD_FAST                'cfg'
             3512  LOAD_METHOD              has_option
             3514  LOAD_STR                 'LOAD_CFG'
             3516  LOAD_STR                 'clock_para'
             3518  CALL_METHOD_2         2  '2 positional arguments'
         3520_3522  POP_JUMP_IF_FALSE  3592  'to 3592'

 L.2992      3524  LOAD_FAST                'cfg'
             3526  LOAD_METHOD              get
             3528  LOAD_STR                 'LOAD_CFG'
             3530  LOAD_STR                 'clock_para'
             3532  CALL_METHOD_2         2  '2 positional arguments'
             3534  STORE_FAST               'clock_para_str'

 L.2993      3536  LOAD_FAST                'clock_para_str'
             3538  LOAD_STR                 ''
             3540  COMPARE_OP               !=
         3542_3544  POP_JUMP_IF_FALSE  3592  'to 3592'

 L.2994      3546  LOAD_GLOBAL              os
             3548  LOAD_ATTR                path
             3550  LOAD_METHOD              join
             3552  LOAD_GLOBAL              app_path
             3554  LOAD_FAST                'clock_para_str'
             3556  CALL_METHOD_2         2  '2 positional arguments'
             3558  STORE_FAST               'clock_para_file'

 L.2995      3560  LOAD_GLOBAL              bflb_utils
             3562  LOAD_METHOD              printf
             3564  LOAD_STR                 'clock para file: '
             3566  LOAD_FAST                'clock_para_file'
             3568  CALL_METHOD_2         2  '2 positional arguments'
             3570  POP_TOP          

 L.2996      3572  LOAD_FAST                'self'
             3574  LOAD_METHOD              clock_para_update
             3576  LOAD_GLOBAL              os
             3578  LOAD_ATTR                path
             3580  LOAD_METHOD              join

 L.2997      3582  LOAD_GLOBAL              app_path
             3584  LOAD_FAST                'clock_para_file'
             3586  CALL_METHOD_2         2  '2 positional arguments'
             3588  CALL_METHOD_1         1  '1 positional argument'
             3590  STORE_FAST               'clock_para'
           3592_0  COME_FROM          3542  '3542'
           3592_1  COME_FROM          3520  '3520'

 L.2998      3592  LOAD_GLOBAL              bflb_utils
             3594  LOAD_METHOD              printf
             3596  LOAD_STR                 'change bdrate: '
             3598  LOAD_FAST                'self'
             3600  LOAD_ATTR                _bflb_com_speed
             3602  CALL_METHOD_2         2  '2 positional arguments'
             3604  POP_TOP          

 L.2999      3606  LOAD_FAST                'self'
             3608  LOAD_METHOD              clock_pll_set
             3610  LOAD_FAST                'self'
             3612  LOAD_ATTR                _need_shake_hand
             3614  LOAD_CONST               True
             3616  LOAD_FAST                'self'
             3618  LOAD_ATTR                _bflb_com_speed

 L.3000      3620  LOAD_FAST                'clock_para'
             3622  CALL_METHOD_4         4  '4 positional arguments'
             3624  STORE_FAST               'ret'

 L.3001      3626  LOAD_FAST                'ret'
             3628  LOAD_CONST               False
             3630  COMPARE_OP               is
         3632_3634  POP_JUMP_IF_FALSE  3654  'to 3654'

 L.3002      3636  LOAD_GLOBAL              bflb_utils
             3638  LOAD_METHOD              printf
             3640  LOAD_STR                 'pll set fail!!'
             3642  CALL_METHOD_1         1  '1 positional argument'
             3644  POP_TOP          

 L.3003      3646  LOAD_CONST               False
             3648  LOAD_FAST                'flash_burn_retry'
             3650  BUILD_TUPLE_2         2 
             3652  RETURN_VALUE     
           3654_0  COME_FROM          3632  '3632'
           3654_1  COME_FROM          3302  '3302'
           3654_2  COME_FROM          3292  '3292'
           3654_3  COME_FROM          3280  '3280'
           3654_4  COME_FROM          3072  '3072'
             3654  POP_BLOCK        
             3656  JUMP_FORWARD       3718  'to 3718'
           3658_0  COME_FROM_EXCEPT   2832  '2832'

 L.3004      3658  DUP_TOP          
             3660  LOAD_GLOBAL              Exception
             3662  COMPARE_OP               exception-match
         3664_3666  POP_JUMP_IF_FALSE  3716  'to 3716'
             3668  POP_TOP          
             3670  STORE_FAST               'e'
             3672  POP_TOP          
             3674  SETUP_FINALLY      3704  'to 3704'

 L.3005      3676  LOAD_GLOBAL              bflb_utils
             3678  LOAD_METHOD              printf
             3680  LOAD_FAST                'e'
             3682  CALL_METHOD_1         1  '1 positional argument'
             3684  POP_TOP          

 L.3006      3686  LOAD_FAST                'self'
             3688  LOAD_METHOD              error_code_print
             3690  LOAD_STR                 '0003'
             3692  CALL_METHOD_1         1  '1 positional argument'
             3694  POP_TOP          

 L.3007      3696  LOAD_CONST               False
             3698  LOAD_FAST                'flash_burn_retry'
             3700  BUILD_TUPLE_2         2 
             3702  RETURN_VALUE     
           3704_0  COME_FROM_FINALLY  3674  '3674'
             3704  LOAD_CONST               None
             3706  STORE_FAST               'e'
             3708  DELETE_FAST              'e'
             3710  END_FINALLY      
             3712  POP_EXCEPT       
             3714  JUMP_FORWARD       3718  'to 3718'
           3716_0  COME_FROM          3664  '3664'
             3716  END_FINALLY      
           3718_0  COME_FROM          3714  '3714'
           3718_1  COME_FROM          3656  '3656'

 L.3008      3718  LOAD_GLOBAL              time
             3720  LOAD_METHOD              sleep
             3722  LOAD_CONST               0.1
             3724  CALL_METHOD_1         1  '1 positional argument'
             3726  POP_TOP          

 L.3010      3728  LOAD_FAST                'self'
             3730  LOAD_ATTR                _isp_en
             3732  LOAD_CONST               True
             3734  COMPARE_OP               is
         3736_3738  POP_JUMP_IF_FALSE  3812  'to 3812'
             3740  LOAD_FAST                'self'
             3742  LOAD_ATTR                _cpu_reset
             3744  LOAD_CONST               True
             3746  COMPARE_OP               is
         3748_3750  POP_JUMP_IF_FALSE  3812  'to 3812'

 L.3011      3752  LOAD_FAST                'self'
             3754  LOAD_ATTR                _chip_type
             3756  LOAD_STR                 'bl808'
             3758  COMPARE_OP               ==
         3760_3762  POP_JUMP_IF_TRUE   3800  'to 3800'

 L.3012      3764  LOAD_FAST                'self'
             3766  LOAD_ATTR                _chip_type
             3768  LOAD_STR                 'bl628'
             3770  COMPARE_OP               ==
         3772_3774  POP_JUMP_IF_TRUE   3800  'to 3800'

 L.3013      3776  LOAD_FAST                'self'
             3778  LOAD_ATTR                _chip_type
             3780  LOAD_STR                 'bl616'
             3782  COMPARE_OP               ==
         3784_3786  POP_JUMP_IF_TRUE   3800  'to 3800'

 L.3014      3788  LOAD_FAST                'self'
             3790  LOAD_ATTR                _chip_type
             3792  LOAD_STR                 'wb03'
             3794  COMPARE_OP               ==
         3796_3798  POP_JUMP_IF_FALSE  3812  'to 3812'
           3800_0  COME_FROM          3784  '3784'
           3800_1  COME_FROM          3772  '3772'
           3800_2  COME_FROM          3760  '3760'

 L.3016      3800  LOAD_FAST                'self'
             3802  LOAD_METHOD              clear_boot_status
             3804  LOAD_FAST                'self'
             3806  LOAD_ATTR                _need_shake_hand
             3808  CALL_METHOD_1         1  '1 positional argument'
             3810  POP_TOP          
           3812_0  COME_FROM          3796  '3796'
           3812_1  COME_FROM          3748  '3748'
           3812_2  COME_FROM          3736  '3736'

 L.3018      3812  LOAD_CONST               False
             3814  STORE_FAST               'macaddr_check'

 L.3019      3816  LOAD_GLOBAL              bytearray
             3818  LOAD_CONST               0
             3820  CALL_FUNCTION_1       1  '1 positional argument'
             3822  STORE_FAST               'mac_addr'

 L.3020      3824  LOAD_FAST                'cfg'
             3826  LOAD_METHOD              has_option
             3828  LOAD_STR                 'LOAD_CFG'
             3830  LOAD_STR                 'check_mac'
             3832  CALL_METHOD_2         2  '2 positional arguments'
         3834_3836  POP_JUMP_IF_FALSE  3854  'to 3854'

 L.3021      3838  LOAD_FAST                'cfg'
             3840  LOAD_METHOD              get
             3842  LOAD_STR                 'LOAD_CFG'
             3844  LOAD_STR                 'check_mac'
             3846  CALL_METHOD_2         2  '2 positional arguments'
             3848  LOAD_STR                 'true'
             3850  COMPARE_OP               ==
             3852  STORE_FAST               'macaddr_check'
           3854_0  COME_FROM          3834  '3834'

 L.3022      3854  LOAD_FAST                'macaddr_check'
         3856_3858  POP_JUMP_IF_FALSE  3992  'to 3992'
             3860  LOAD_FAST                'self'
             3862  LOAD_ATTR                _isp_en
             3864  LOAD_CONST               False
             3866  COMPARE_OP               is
         3868_3870  POP_JUMP_IF_FALSE  3992  'to 3992'

 L.3024      3872  LOAD_CONST               5
             3874  STORE_FAST               'check_macaddr_cnt'

 L.3025      3876  SETUP_LOOP         3950  'to 3950'
           3878_0  COME_FROM          3932  '3932'

 L.3026      3878  LOAD_FAST                'self'
             3880  LOAD_METHOD              efuse_read_mac_addr_process
             3882  LOAD_FAST                'self'
             3884  LOAD_ATTR                _need_shake_hand
             3886  CALL_METHOD_1         1  '1 positional argument'
             3888  UNPACK_SEQUENCE_2     2 
             3890  STORE_FAST               'ret'
             3892  STORE_FAST               'mac_addr'

 L.3027      3894  LOAD_FAST                'ret'
             3896  LOAD_CONST               False
             3898  COMPARE_OP               is
         3900_3902  POP_JUMP_IF_FALSE  3916  'to 3916'

 L.3028      3904  LOAD_GLOBAL              bflb_utils
             3906  LOAD_METHOD              printf
             3908  LOAD_STR                 'read mac addr fail!!'
             3910  CALL_METHOD_1         1  '1 positional argument'
             3912  POP_TOP          
             3914  JUMP_FORWARD       3918  'to 3918'
           3916_0  COME_FROM          3900  '3900'

 L.3030      3916  BREAK_LOOP       
           3918_0  COME_FROM          3914  '3914'

 L.3031      3918  LOAD_FAST                'check_macaddr_cnt'
             3920  LOAD_CONST               1
             3922  INPLACE_SUBTRACT 
             3924  STORE_FAST               'check_macaddr_cnt'

 L.3032      3926  LOAD_FAST                'check_macaddr_cnt'
             3928  LOAD_CONST               0
             3930  COMPARE_OP               ==
         3932_3934  POP_JUMP_IF_FALSE  3878  'to 3878'

 L.3033      3936  LOAD_CONST               False
             3938  LOAD_FAST                'flash_burn_retry'
             3940  BUILD_TUPLE_2         2 
             3942  RETURN_VALUE     
         3944_3946  JUMP_BACK          3878  'to 3878'
             3948  POP_BLOCK        
           3950_0  COME_FROM_LOOP     3876  '3876'

 L.3034      3950  LOAD_FAST                'mac_addr'
             3952  LOAD_FAST                'self'
             3954  LOAD_ATTR                _macaddr_check
             3956  COMPARE_OP               ==
         3958_3960  POP_JUMP_IF_FALSE  3980  'to 3980'

 L.3035      3962  LOAD_FAST                'self'
             3964  LOAD_METHOD              error_code_print
             3966  LOAD_STR                 '000A'
             3968  CALL_METHOD_1         1  '1 positional argument'
             3970  POP_TOP          

 L.3036      3972  LOAD_CONST               False
             3974  LOAD_FAST                'flash_burn_retry'
             3976  BUILD_TUPLE_2         2 
             3978  RETURN_VALUE     
           3980_0  COME_FROM          3958  '3958'

 L.3037      3980  LOAD_CONST               False
             3982  LOAD_FAST                'self'
             3984  STORE_ATTR               _need_shake_hand

 L.3038      3986  LOAD_CONST               True
             3988  LOAD_FAST                'self'
             3990  STORE_ATTR               _macaddr_check_status
           3992_0  COME_FROM          3868  '3868'
           3992_1  COME_FROM          3856  '3856'

 L.3041      3992  LOAD_FAST                'macaddr_callback'
             3994  LOAD_CONST               None
             3996  COMPARE_OP               is-not
         3998_4000  POP_JUMP_IF_FALSE  4100  'to 4100'

 L.3042      4002  LOAD_FAST                'macaddr_callback'

 L.3043      4004  LOAD_GLOBAL              binascii
             4006  LOAD_METHOD              hexlify
             4008  LOAD_FAST                'mac_addr'
             4010  CALL_METHOD_1         1  '1 positional argument'
             4012  LOAD_METHOD              decode
             4014  LOAD_STR                 'utf-8'
             4016  CALL_METHOD_1         1  '1 positional argument'
             4018  CALL_FUNCTION_1       1  '1 positional argument'
             4020  UNPACK_SEQUENCE_4     4 
             4022  STORE_FAST               'ret'
             4024  LOAD_FAST                'self'
             4026  STORE_ATTR               _efuse_data
             4028  LOAD_FAST                'self'
             4030  STORE_ATTR               _efuse_mask_data
             4032  STORE_FAST               'macaddr'

 L.3044      4034  LOAD_FAST                'ret'
             4036  LOAD_CONST               False
             4038  COMPARE_OP               is
         4040_4042  POP_JUMP_IF_FALSE  4052  'to 4052'

 L.3045      4044  LOAD_CONST               False
             4046  LOAD_FAST                'flash_burn_retry'
             4048  BUILD_TUPLE_2         2 
             4050  RETURN_VALUE     
           4052_0  COME_FROM          4040  '4040'

 L.3046      4052  LOAD_FAST                'self'
             4054  LOAD_ATTR                _efuse_data
             4056  LOAD_GLOBAL              bytearray
             4058  LOAD_CONST               0
             4060  CALL_FUNCTION_1       1  '1 positional argument'
             4062  COMPARE_OP               !=
         4064_4066  POP_JUMP_IF_FALSE  4084  'to 4084'

 L.3047      4068  LOAD_FAST                'self'
             4070  LOAD_ATTR                _efuse_mask_data
             4072  LOAD_GLOBAL              bytearray
             4074  LOAD_CONST               0
             4076  CALL_FUNCTION_1       1  '1 positional argument'
             4078  COMPARE_OP               !=
         4080_4082  POP_JUMP_IF_TRUE   4094  'to 4094'
           4084_0  COME_FROM          4064  '4064'
             4084  LOAD_FAST                'macaddr'
             4086  LOAD_STR                 ''
             4088  COMPARE_OP               !=
         4090_4092  POP_JUMP_IF_FALSE  4100  'to 4100'
           4094_0  COME_FROM          4080  '4080'

 L.3048      4094  LOAD_CONST               True
             4096  LOAD_FAST                'args'
             4098  STORE_ATTR               efuse
           4100_0  COME_FROM          4090  '4090'
           4100_1  COME_FROM          3998  '3998'

 L.3049      4100  LOAD_FAST                'callback'
         4102_4104  POP_JUMP_IF_FALSE  4120  'to 4120'

 L.3050      4106  LOAD_FAST                'callback'
             4108  LOAD_CONST               0
             4110  LOAD_CONST               100
             4112  LOAD_STR                 '进行'
             4114  LOAD_STR                 'blue'
             4116  CALL_FUNCTION_4       4  '4 positional arguments'
             4118  POP_TOP          
           4120_0  COME_FROM          4102  '4102'

 L.3052      4120  LOAD_FAST                'args'
             4122  LOAD_ATTR                flash
         4124_4126  POP_JUMP_IF_FALSE  5688  'to 5688'

 L.3054      4128  LOAD_CONST               0
             4130  STORE_FAST               'flash_pin'

 L.3055      4132  LOAD_CONST               0
             4134  STORE_FAST               'flash_clock_cfg'

 L.3056      4136  LOAD_CONST               0
             4138  STORE_FAST               'flash_io_mode'

 L.3057      4140  LOAD_CONST               0
             4142  STORE_FAST               'flash_clk_delay'

 L.3058      4144  LOAD_FAST                'cfg'
             4146  LOAD_METHOD              has_option
             4148  LOAD_STR                 'FLASH_CFG'
             4150  LOAD_STR                 'decompress_write'
             4152  CALL_METHOD_2         2  '2 positional arguments'
         4154_4156  POP_JUMP_IF_FALSE  4176  'to 4176'

 L.3059      4158  LOAD_FAST                'cfg'
             4160  LOAD_METHOD              get
             4162  LOAD_STR                 'FLASH_CFG'
             4164  LOAD_STR                 'decompress_write'
             4166  CALL_METHOD_2         2  '2 positional arguments'
             4168  LOAD_STR                 'true'
             4170  COMPARE_OP               ==
             4172  LOAD_FAST                'self'
             4174  STORE_ATTR               _decompress_write
           4176_0  COME_FROM          4154  '4154'

 L.3060      4176  LOAD_FAST                'self'
             4178  LOAD_ATTR                _chip_type
             4180  LOAD_STR                 'bl60x'
             4182  COMPARE_OP               ==
         4184_4186  POP_JUMP_IF_TRUE   4200  'to 4200'
             4188  LOAD_FAST                'self'
             4190  LOAD_ATTR                _chip_type
             4192  LOAD_STR                 'bl702'
             4194  COMPARE_OP               ==
         4196_4198  POP_JUMP_IF_FALSE  4206  'to 4206'
           4200_0  COME_FROM          4184  '4184'

 L.3061      4200  LOAD_CONST               False
             4202  LOAD_FAST                'self'
             4204  STORE_ATTR               _decompress_write
           4206_0  COME_FROM          4196  '4196'

 L.3062      4206  LOAD_GLOBAL              bflb_utils
             4208  LOAD_METHOD              printf
             4210  LOAD_STR                 'flash set para'
             4212  CALL_METHOD_1         1  '1 positional argument'
             4214  POP_TOP          

 L.3063      4216  LOAD_FAST                'cfg'
             4218  LOAD_METHOD              get
             4220  LOAD_STR                 'FLASH_CFG'
             4222  LOAD_STR                 'flash_pin'
             4224  CALL_METHOD_2         2  '2 positional arguments'
         4226_4228  POP_JUMP_IF_FALSE  4316  'to 4316'

 L.3064      4230  LOAD_FAST                'cfg'
             4232  LOAD_METHOD              get
             4234  LOAD_STR                 'FLASH_CFG'
             4236  LOAD_STR                 'flash_pin'
             4238  CALL_METHOD_2         2  '2 positional arguments'
             4240  STORE_FAST               'flash_pin_cfg'

 L.3065      4242  LOAD_FAST                'flash_pin_cfg'
             4244  LOAD_METHOD              startswith
             4246  LOAD_STR                 '0x'
             4248  CALL_METHOD_1         1  '1 positional argument'
         4250_4252  POP_JUMP_IF_FALSE  4266  'to 4266'

 L.3066      4254  LOAD_GLOBAL              int
             4256  LOAD_FAST                'flash_pin_cfg'
             4258  LOAD_CONST               16
             4260  CALL_FUNCTION_2       2  '2 positional arguments'
             4262  STORE_FAST               'flash_pin'
             4264  JUMP_FORWARD       4276  'to 4276'
           4266_0  COME_FROM          4250  '4250'

 L.3068      4266  LOAD_GLOBAL              int
             4268  LOAD_FAST                'flash_pin_cfg'
             4270  LOAD_CONST               10
             4272  CALL_FUNCTION_2       2  '2 positional arguments'
             4274  STORE_FAST               'flash_pin'
           4276_0  COME_FROM          4264  '4264'

 L.3069      4276  LOAD_FAST                'flash_pin'
             4278  LOAD_CONST               128
             4280  COMPARE_OP               ==
         4282_4284  POP_JUMP_IF_FALSE  4344  'to 4344'

 L.3070      4286  LOAD_FAST                'self'
             4288  LOAD_METHOD              get_flash_pin_from_bootinfo
             4290  LOAD_FAST                'self'
             4292  LOAD_ATTR                _chip_type
             4294  LOAD_FAST                'bootinfo'
             4296  CALL_METHOD_2         2  '2 positional arguments'
             4298  STORE_FAST               'flash_pin'

 L.3071      4300  LOAD_GLOBAL              bflb_utils
             4302  LOAD_METHOD              printf
             4304  LOAD_STR                 'get flash pin cfg from bootinfo: 0x%02X'
             4306  LOAD_FAST                'flash_pin'
             4308  BINARY_MODULO    
             4310  CALL_METHOD_1         1  '1 positional argument'
             4312  POP_TOP          
             4314  JUMP_FORWARD       4344  'to 4344'
           4316_0  COME_FROM          4226  '4226'

 L.3073      4316  LOAD_FAST                'self'
             4318  LOAD_ATTR                _chip_type
             4320  LOAD_STR                 'bl602'
             4322  COMPARE_OP               ==
         4324_4326  POP_JUMP_IF_TRUE   4340  'to 4340'
             4328  LOAD_FAST                'self'
             4330  LOAD_ATTR                _chip_type
             4332  LOAD_STR                 'bl702'
             4334  COMPARE_OP               ==
         4336_4338  POP_JUMP_IF_FALSE  4344  'to 4344'
           4340_0  COME_FROM          4324  '4324'

 L.3074      4340  LOAD_CONST               255
             4342  STORE_FAST               'flash_pin'
           4344_0  COME_FROM          4336  '4336'
           4344_1  COME_FROM          4314  '4314'
           4344_2  COME_FROM          4282  '4282'

 L.3075      4344  LOAD_FAST                'self'
             4346  LOAD_ATTR                _chip_type
             4348  LOAD_STR                 'bl60x'
             4350  COMPARE_OP               !=
         4352_4354  POP_JUMP_IF_FALSE  4536  'to 4536'

 L.3076      4356  LOAD_FAST                'cfg'
             4358  LOAD_METHOD              has_option
             4360  LOAD_STR                 'FLASH_CFG'
             4362  LOAD_STR                 'flash_clock_cfg'
             4364  CALL_METHOD_2         2  '2 positional arguments'
         4366_4368  POP_JUMP_IF_FALSE  4416  'to 4416'

 L.3077      4370  LOAD_FAST                'cfg'
             4372  LOAD_METHOD              get
             4374  LOAD_STR                 'FLASH_CFG'
             4376  LOAD_STR                 'flash_clock_cfg'
             4378  CALL_METHOD_2         2  '2 positional arguments'
             4380  STORE_FAST               'clock_div_cfg'

 L.3078      4382  LOAD_FAST                'clock_div_cfg'
             4384  LOAD_METHOD              startswith
             4386  LOAD_STR                 '0x'
             4388  CALL_METHOD_1         1  '1 positional argument'
         4390_4392  POP_JUMP_IF_FALSE  4406  'to 4406'

 L.3079      4394  LOAD_GLOBAL              int
             4396  LOAD_FAST                'clock_div_cfg'
             4398  LOAD_CONST               16
             4400  CALL_FUNCTION_2       2  '2 positional arguments'
             4402  STORE_FAST               'flash_clock_cfg'
             4404  JUMP_FORWARD       4416  'to 4416'
           4406_0  COME_FROM          4390  '4390'

 L.3081      4406  LOAD_GLOBAL              int
             4408  LOAD_FAST                'clock_div_cfg'
             4410  LOAD_CONST               10
             4412  CALL_FUNCTION_2       2  '2 positional arguments'
             4414  STORE_FAST               'flash_clock_cfg'
           4416_0  COME_FROM          4404  '4404'
           4416_1  COME_FROM          4366  '4366'

 L.3082      4416  LOAD_FAST                'cfg'
             4418  LOAD_METHOD              has_option
             4420  LOAD_STR                 'FLASH_CFG'
             4422  LOAD_STR                 'flash_io_mode'
             4424  CALL_METHOD_2         2  '2 positional arguments'
         4426_4428  POP_JUMP_IF_FALSE  4476  'to 4476'

 L.3083      4430  LOAD_FAST                'cfg'
             4432  LOAD_METHOD              get
             4434  LOAD_STR                 'FLASH_CFG'
             4436  LOAD_STR                 'flash_io_mode'
             4438  CALL_METHOD_2         2  '2 positional arguments'
             4440  STORE_FAST               'io_mode_cfg'

 L.3084      4442  LOAD_FAST                'io_mode_cfg'
             4444  LOAD_METHOD              startswith
             4446  LOAD_STR                 '0x'
             4448  CALL_METHOD_1         1  '1 positional argument'
         4450_4452  POP_JUMP_IF_FALSE  4466  'to 4466'

 L.3085      4454  LOAD_GLOBAL              int
             4456  LOAD_FAST                'io_mode_cfg'
             4458  LOAD_CONST               16
             4460  CALL_FUNCTION_2       2  '2 positional arguments'
             4462  STORE_FAST               'flash_io_mode'
             4464  JUMP_FORWARD       4476  'to 4476'
           4466_0  COME_FROM          4450  '4450'

 L.3087      4466  LOAD_GLOBAL              int
             4468  LOAD_FAST                'io_mode_cfg'
             4470  LOAD_CONST               10
             4472  CALL_FUNCTION_2       2  '2 positional arguments'
             4474  STORE_FAST               'flash_io_mode'
           4476_0  COME_FROM          4464  '4464'
           4476_1  COME_FROM          4426  '4426'

 L.3088      4476  LOAD_FAST                'cfg'
             4478  LOAD_METHOD              has_option
             4480  LOAD_STR                 'FLASH_CFG'
             4482  LOAD_STR                 'flash_clock_delay'
             4484  CALL_METHOD_2         2  '2 positional arguments'
         4486_4488  POP_JUMP_IF_FALSE  4536  'to 4536'

 L.3089      4490  LOAD_FAST                'cfg'
             4492  LOAD_METHOD              get
             4494  LOAD_STR                 'FLASH_CFG'
             4496  LOAD_STR                 'flash_clock_delay'
             4498  CALL_METHOD_2         2  '2 positional arguments'
             4500  STORE_FAST               'clk_delay_cfg'

 L.3090      4502  LOAD_FAST                'clk_delay_cfg'
             4504  LOAD_METHOD              startswith
             4506  LOAD_STR                 '0x'
             4508  CALL_METHOD_1         1  '1 positional argument'
         4510_4512  POP_JUMP_IF_FALSE  4526  'to 4526'

 L.3091      4514  LOAD_GLOBAL              int
             4516  LOAD_FAST                'clk_delay_cfg'
             4518  LOAD_CONST               16
             4520  CALL_FUNCTION_2       2  '2 positional arguments'
             4522  STORE_FAST               'flash_clk_delay'
             4524  JUMP_FORWARD       4536  'to 4536'
           4526_0  COME_FROM          4510  '4510'

 L.3093      4526  LOAD_GLOBAL              int
             4528  LOAD_FAST                'clk_delay_cfg'
             4530  LOAD_CONST               10
             4532  CALL_FUNCTION_2       2  '2 positional arguments'
             4534  STORE_FAST               'flash_clk_delay'
           4536_0  COME_FROM          4524  '4524'
           4536_1  COME_FROM          4486  '4486'
           4536_2  COME_FROM          4352  '4352'

 L.3097      4536  LOAD_FAST                'flash_pin'
             4538  LOAD_CONST               0
             4540  BINARY_LSHIFT    
             4542  LOAD_FAST                'flash_clock_cfg'
             4544  LOAD_CONST               8
             4546  BINARY_LSHIFT    
             4548  BINARY_ADD       
             4550  LOAD_FAST                'flash_io_mode'
             4552  LOAD_CONST               16
             4554  BINARY_LSHIFT    
             4556  BINARY_ADD       

 L.3098      4558  LOAD_FAST                'flash_clk_delay'
             4560  LOAD_CONST               24
             4562  BINARY_LSHIFT    
             4564  BINARY_ADD       
             4566  STORE_FAST               'flash_set'

 L.3099      4568  LOAD_FAST                'flash_set'
             4570  LOAD_CONST               66047
             4572  COMPARE_OP               !=
         4574_4576  POP_JUMP_IF_FALSE  4590  'to 4590'
             4578  LOAD_FAST                'self'
             4580  LOAD_ATTR                _chip_type
             4582  LOAD_STR                 'bl60x'
             4584  COMPARE_OP               !=
         4586_4588  POP_JUMP_IF_TRUE   4622  'to 4622'
           4590_0  COME_FROM          4574  '4574'

 L.3100      4590  LOAD_FAST                'flash_pin'
             4592  LOAD_CONST               0
             4594  COMPARE_OP               !=
         4596_4598  POP_JUMP_IF_FALSE  4612  'to 4612'
             4600  LOAD_FAST                'self'
             4602  LOAD_ATTR                _chip_type
             4604  LOAD_STR                 'bl60x'
             4606  COMPARE_OP               ==
         4608_4610  POP_JUMP_IF_TRUE   4622  'to 4622'
           4612_0  COME_FROM          4596  '4596'

 L.3101      4612  LOAD_FAST                'load_function'
             4614  LOAD_CONST               2
             4616  COMPARE_OP               ==
         4618_4620  POP_JUMP_IF_FALSE  4680  'to 4680'
           4622_0  COME_FROM          4608  '4608'
           4622_1  COME_FROM          4586  '4586'

 L.3102      4622  LOAD_GLOBAL              bflb_utils
             4624  LOAD_METHOD              printf
             4626  LOAD_STR                 'set flash cfg: %X'
             4628  LOAD_FAST                'flash_set'
             4630  BINARY_MODULO    
             4632  CALL_METHOD_1         1  '1 positional argument'
             4634  POP_TOP          

 L.3103      4636  LOAD_FAST                'self'
             4638  LOAD_METHOD              flash_set_para_main_process
             4640  LOAD_FAST                'flash_set'
             4642  LOAD_GLOBAL              bytearray
             4644  LOAD_CONST               0
             4646  CALL_FUNCTION_1       1  '1 positional argument'

 L.3104      4648  LOAD_FAST                'self'
             4650  LOAD_ATTR                _need_shake_hand
             4652  CALL_METHOD_3         3  '3 positional arguments'
             4654  STORE_FAST               'ret'

 L.3105      4656  LOAD_CONST               False
             4658  LOAD_FAST                'self'
             4660  STORE_ATTR               _need_shake_hand

 L.3106      4662  LOAD_FAST                'ret'
             4664  LOAD_CONST               False
             4666  COMPARE_OP               is
         4668_4670  POP_JUMP_IF_FALSE  4680  'to 4680'

 L.3107      4672  LOAD_CONST               False
             4674  LOAD_FAST                'flash_burn_retry'
             4676  BUILD_TUPLE_2         2 
             4678  RETURN_VALUE     
           4680_0  COME_FROM          4668  '4668'
           4680_1  COME_FROM          4618  '4618'

 L.3109      4680  LOAD_FAST                'self'
             4682  LOAD_METHOD              flash_read_jedec_id_process
             4684  LOAD_FAST                'self'
             4686  LOAD_ATTR                _need_shake_hand
             4688  CALL_METHOD_1         1  '1 positional argument'
             4690  UNPACK_SEQUENCE_2     2 
             4692  STORE_FAST               'ret'
             4694  STORE_FAST               'data'

 L.3110      4696  LOAD_FAST                'ret'
         4698_4700  POP_JUMP_IF_FALSE  4898  'to 4898'

 L.3111      4702  LOAD_CONST               False
             4704  LOAD_FAST                'self'
             4706  STORE_ATTR               _need_shake_hand

 L.3112      4708  LOAD_GLOBAL              binascii
             4710  LOAD_METHOD              hexlify
             4712  LOAD_FAST                'data'
             4714  CALL_METHOD_1         1  '1 positional argument'
             4716  LOAD_METHOD              decode
             4718  LOAD_STR                 'utf-8'
             4720  CALL_METHOD_1         1  '1 positional argument'
             4722  STORE_FAST               'data'

 L.3113      4724  LOAD_FAST                'data'
             4726  LOAD_CONST               6
             4728  LOAD_CONST               None
             4730  BUILD_SLICE_2         2 
             4732  BINARY_SUBSCR    
             4734  STORE_FAST               'id_valid_flag'

 L.3114      4736  LOAD_FAST                'data'
             4738  LOAD_CONST               0
             4740  LOAD_CONST               6
             4742  BUILD_SLICE_2         2 
             4744  BINARY_SUBSCR    
             4746  STORE_FAST               'read_id'

 L.3115      4748  LOAD_FAST                'read_id'
             4750  STORE_FAST               'read_flash_id'

 L.3116      4752  LOAD_FAST                'cfg'
             4754  LOAD_METHOD              has_option
             4756  LOAD_STR                 'FLASH_CFG'
             4758  LOAD_STR                 'flash_para'
             4760  CALL_METHOD_2         2  '2 positional arguments'
         4762_4764  POP_JUMP_IF_FALSE  4800  'to 4800'

 L.3117      4766  LOAD_GLOBAL              os
             4768  LOAD_ATTR                path
             4770  LOAD_METHOD              join
             4772  LOAD_GLOBAL              app_path
             4774  LOAD_FAST                'cfg'
             4776  LOAD_METHOD              get
             4778  LOAD_STR                 'FLASH_CFG'
             4780  LOAD_STR                 'flash_para'
             4782  CALL_METHOD_2         2  '2 positional arguments'
             4784  CALL_METHOD_2         2  '2 positional arguments'
             4786  STORE_FAST               'flash_para_file'

 L.3118      4788  LOAD_FAST                'self'
             4790  LOAD_METHOD              flash_para_update
             4792  LOAD_FAST                'flash_para_file'
             4794  LOAD_FAST                'read_id'
             4796  CALL_METHOD_2         2  '2 positional arguments'
             4798  POP_TOP          
           4800_0  COME_FROM          4762  '4762'

 L.3119      4800  LOAD_FAST                'id_valid_flag'
             4802  LOAD_STR                 '80'
             4804  COMPARE_OP               !=
         4806_4808  POP_JUMP_IF_FALSE  4862  'to 4862'

 L.3120      4810  LOAD_FAST                'self'
             4812  LOAD_ATTR                _chip_type
             4814  LOAD_STR                 'bl602'
             4816  COMPARE_OP               ==
         4818_4820  POP_JUMP_IF_TRUE   4834  'to 4834'
             4822  LOAD_FAST                'self'
             4824  LOAD_ATTR                _chip_type
             4826  LOAD_STR                 'bl702'
             4828  COMPARE_OP               ==
         4830_4832  POP_JUMP_IF_FALSE  4862  'to 4862'
           4834_0  COME_FROM          4818  '4818'

 L.3121      4834  LOAD_GLOBAL              bflb_utils
             4836  LOAD_METHOD              printf
             4838  LOAD_STR                 'eflash loader identify flash fail!'
             4840  CALL_METHOD_1         1  '1 positional argument'
             4842  POP_TOP          

 L.3122      4844  LOAD_FAST                'self'
             4846  LOAD_METHOD              error_code_print
             4848  LOAD_STR                 '0043'
             4850  CALL_METHOD_1         1  '1 positional argument'
             4852  POP_TOP          

 L.3123      4854  LOAD_CONST               False
             4856  LOAD_FAST                'flash_burn_retry'
             4858  BUILD_TUPLE_2         2 
             4860  RETURN_VALUE     
           4862_0  COME_FROM          4830  '4830'
           4862_1  COME_FROM          4806  '4806'

 L.3124      4862  LOAD_FAST                'self'
             4864  LOAD_METHOD              is_conf_exist
             4866  LOAD_FAST                'read_flash_id'
             4868  CALL_METHOD_1         1  '1 positional argument'
             4870  LOAD_CONST               False
             4872  COMPARE_OP               is
         4874_4876  POP_JUMP_IF_FALSE  4916  'to 4916'

 L.3125      4878  LOAD_FAST                'self'
             4880  LOAD_METHOD              error_code_print
             4882  LOAD_STR                 '003D'
             4884  CALL_METHOD_1         1  '1 positional argument'
             4886  POP_TOP          

 L.3126      4888  LOAD_CONST               False
             4890  LOAD_FAST                'flash_burn_retry'
             4892  BUILD_TUPLE_2         2 
             4894  RETURN_VALUE     
             4896  JUMP_FORWARD       4916  'to 4916'
           4898_0  COME_FROM          4698  '4698'

 L.3128      4898  LOAD_FAST                'self'
             4900  LOAD_METHOD              error_code_print
             4902  LOAD_STR                 '0030'
             4904  CALL_METHOD_1         1  '1 positional argument'
             4906  POP_TOP          

 L.3129      4908  LOAD_CONST               False
             4910  LOAD_FAST                'flash_burn_retry'
             4912  BUILD_TUPLE_2         2 
             4914  RETURN_VALUE     
           4916_0  COME_FROM          4896  '4896'
           4916_1  COME_FROM          4874  '4874'

 L.3131      4916  LOAD_FAST                'self'
             4918  LOAD_ATTR                _chip_type
             4920  LOAD_STR                 'bl616'
             4922  COMPARE_OP               ==
         4924_4926  POP_JUMP_IF_TRUE   4940  'to 4940'
             4928  LOAD_FAST                'self'
             4930  LOAD_ATTR                _chip_type
             4932  LOAD_STR                 'wb03'
             4934  COMPARE_OP               ==
         4936_4938  POP_JUMP_IF_FALSE  5688  'to 5688'
           4940_0  COME_FROM          4924  '4924'

 L.3132      4940  LOAD_FAST                'cfg'
             4942  LOAD_METHOD              has_option
             4944  LOAD_STR                 'FLASH2_CFG'
             4946  LOAD_STR                 'flash2_en'
             4948  CALL_METHOD_2         2  '2 positional arguments'
         4950_4952  POP_JUMP_IF_FALSE  5688  'to 5688'

 L.3133      4954  LOAD_FAST                'cfg'
             4956  LOAD_METHOD              get
             4958  LOAD_STR                 'FLASH2_CFG'
             4960  LOAD_STR                 'flash2_en'
             4962  CALL_METHOD_2         2  '2 positional arguments'
             4964  LOAD_STR                 'true'
             4966  COMPARE_OP               ==
             4968  LOAD_FAST                'self'
             4970  STORE_ATTR               _flash2_en

 L.3134      4972  LOAD_FAST                'self'
             4974  LOAD_ATTR                _flash2_en
             4976  LOAD_CONST               True
             4978  COMPARE_OP               is
         4980_4982  POP_JUMP_IF_FALSE  5688  'to 5688'

 L.3135      4984  LOAD_GLOBAL              int
             4986  LOAD_FAST                'cfg'
             4988  LOAD_METHOD              get
             4990  LOAD_STR                 'FLASH2_CFG'
             4992  LOAD_STR                 'flash1_size'
             4994  CALL_METHOD_2         2  '2 positional arguments'
             4996  CALL_FUNCTION_1       1  '1 positional argument'
             4998  LOAD_CONST               1024
             5000  BINARY_MULTIPLY  
             5002  LOAD_CONST               1024
             5004  BINARY_MULTIPLY  
             5006  LOAD_FAST                'self'
             5008  STORE_ATTR               _flash1_size

 L.3136      5010  LOAD_GLOBAL              int
             5012  LOAD_FAST                'cfg'
             5014  LOAD_METHOD              get
             5016  LOAD_STR                 'FLASH2_CFG'
             5018  LOAD_STR                 'flash2_size'
             5020  CALL_METHOD_2         2  '2 positional arguments'
             5022  CALL_FUNCTION_1       1  '1 positional argument'
             5024  LOAD_CONST               1024
             5026  BINARY_MULTIPLY  
             5028  LOAD_CONST               1024
             5030  BINARY_MULTIPLY  
             5032  LOAD_FAST                'self'
             5034  STORE_ATTR               _flash2_size

 L.3137      5036  LOAD_GLOBAL              bflb_utils
             5038  LOAD_METHOD              printf
             5040  LOAD_STR                 'flash2 set para'
             5042  CALL_METHOD_1         1  '1 positional argument'
             5044  POP_TOP          

 L.3138      5046  LOAD_CONST               0
             5048  STORE_FAST               'flash2_pin'

 L.3139      5050  LOAD_CONST               0
             5052  STORE_FAST               'flash2_clock_cfg'

 L.3140      5054  LOAD_CONST               0
             5056  STORE_FAST               'flash2_io_mode'

 L.3141      5058  LOAD_CONST               0
             5060  STORE_FAST               'flash2_clk_delay'

 L.3142      5062  LOAD_FAST                'cfg'
             5064  LOAD_METHOD              get
             5066  LOAD_STR                 'FLASH2_CFG'
             5068  LOAD_STR                 'flash2_pin'
             5070  CALL_METHOD_2         2  '2 positional arguments'
         5072_5074  POP_JUMP_IF_FALSE  5122  'to 5122'

 L.3143      5076  LOAD_FAST                'cfg'
             5078  LOAD_METHOD              get
             5080  LOAD_STR                 'FLASH2_CFG'
             5082  LOAD_STR                 'flash2_pin'
             5084  CALL_METHOD_2         2  '2 positional arguments'
             5086  STORE_FAST               'flash_pin_cfg'

 L.3144      5088  LOAD_FAST                'flash_pin_cfg'
             5090  LOAD_METHOD              startswith
             5092  LOAD_STR                 '0x'
             5094  CALL_METHOD_1         1  '1 positional argument'
         5096_5098  POP_JUMP_IF_FALSE  5112  'to 5112'

 L.3145      5100  LOAD_GLOBAL              int
             5102  LOAD_FAST                'flash_pin_cfg'
             5104  LOAD_CONST               16
             5106  CALL_FUNCTION_2       2  '2 positional arguments'
             5108  STORE_FAST               'flash2_pin'
             5110  JUMP_FORWARD       5122  'to 5122'
           5112_0  COME_FROM          5096  '5096'

 L.3147      5112  LOAD_GLOBAL              int
             5114  LOAD_FAST                'flash_pin_cfg'
             5116  LOAD_CONST               10
             5118  CALL_FUNCTION_2       2  '2 positional arguments'
             5120  STORE_FAST               'flash2_pin'
           5122_0  COME_FROM          5110  '5110'
           5122_1  COME_FROM          5072  '5072'

 L.3148      5122  LOAD_FAST                'cfg'
             5124  LOAD_METHOD              has_option
             5126  LOAD_STR                 'FLASH2_CFG'
             5128  LOAD_STR                 'flash2_clock_cfg'
             5130  CALL_METHOD_2         2  '2 positional arguments'
         5132_5134  POP_JUMP_IF_FALSE  5182  'to 5182'

 L.3149      5136  LOAD_FAST                'cfg'
             5138  LOAD_METHOD              get
             5140  LOAD_STR                 'FLASH2_CFG'
             5142  LOAD_STR                 'flash2_clock_cfg'
             5144  CALL_METHOD_2         2  '2 positional arguments'
             5146  STORE_FAST               'clock_div_cfg'

 L.3150      5148  LOAD_FAST                'clock_div_cfg'
             5150  LOAD_METHOD              startswith
             5152  LOAD_STR                 '0x'
             5154  CALL_METHOD_1         1  '1 positional argument'
         5156_5158  POP_JUMP_IF_FALSE  5172  'to 5172'

 L.3151      5160  LOAD_GLOBAL              int
             5162  LOAD_FAST                'clock_div_cfg'
             5164  LOAD_CONST               16
             5166  CALL_FUNCTION_2       2  '2 positional arguments'
             5168  STORE_FAST               'flash2_clock_cfg'
             5170  JUMP_FORWARD       5182  'to 5182'
           5172_0  COME_FROM          5156  '5156'

 L.3153      5172  LOAD_GLOBAL              int
             5174  LOAD_FAST                'clock_div_cfg'
             5176  LOAD_CONST               10
             5178  CALL_FUNCTION_2       2  '2 positional arguments'
             5180  STORE_FAST               'flash2_clock_cfg'
           5182_0  COME_FROM          5170  '5170'
           5182_1  COME_FROM          5132  '5132'

 L.3154      5182  LOAD_FAST                'cfg'
             5184  LOAD_METHOD              has_option
             5186  LOAD_STR                 'FLASH2_CFG'
             5188  LOAD_STR                 'flash2_io_mode'
             5190  CALL_METHOD_2         2  '2 positional arguments'
         5192_5194  POP_JUMP_IF_FALSE  5242  'to 5242'

 L.3155      5196  LOAD_FAST                'cfg'
             5198  LOAD_METHOD              get
             5200  LOAD_STR                 'FLASH2_CFG'
             5202  LOAD_STR                 'flash2_io_mode'
             5204  CALL_METHOD_2         2  '2 positional arguments'
             5206  STORE_FAST               'io_mode_cfg'

 L.3156      5208  LOAD_FAST                'io_mode_cfg'
             5210  LOAD_METHOD              startswith
             5212  LOAD_STR                 '0x'
             5214  CALL_METHOD_1         1  '1 positional argument'
         5216_5218  POP_JUMP_IF_FALSE  5232  'to 5232'

 L.3157      5220  LOAD_GLOBAL              int
             5222  LOAD_FAST                'io_mode_cfg'
             5224  LOAD_CONST               16
             5226  CALL_FUNCTION_2       2  '2 positional arguments'
             5228  STORE_FAST               'flash2_io_mode'
             5230  JUMP_FORWARD       5242  'to 5242'
           5232_0  COME_FROM          5216  '5216'

 L.3159      5232  LOAD_GLOBAL              int
             5234  LOAD_FAST                'io_mode_cfg'
             5236  LOAD_CONST               10
             5238  CALL_FUNCTION_2       2  '2 positional arguments'
             5240  STORE_FAST               'flash2_io_mode'
           5242_0  COME_FROM          5230  '5230'
           5242_1  COME_FROM          5192  '5192'

 L.3160      5242  LOAD_FAST                'cfg'
             5244  LOAD_METHOD              has_option
             5246  LOAD_STR                 'FLASH2_CFG'
             5248  LOAD_STR                 'flash2_clock_delay'
             5250  CALL_METHOD_2         2  '2 positional arguments'
         5252_5254  POP_JUMP_IF_FALSE  5302  'to 5302'

 L.3161      5256  LOAD_FAST                'cfg'
             5258  LOAD_METHOD              get
             5260  LOAD_STR                 'FLASH2_CFG'
             5262  LOAD_STR                 'flash2_clock_delay'
             5264  CALL_METHOD_2         2  '2 positional arguments'
             5266  STORE_FAST               'clk_delay_cfg'

 L.3162      5268  LOAD_FAST                'clk_delay_cfg'
             5270  LOAD_METHOD              startswith
             5272  LOAD_STR                 '0x'
             5274  CALL_METHOD_1         1  '1 positional argument'
         5276_5278  POP_JUMP_IF_FALSE  5292  'to 5292'

 L.3163      5280  LOAD_GLOBAL              int
             5282  LOAD_FAST                'clk_delay_cfg'
             5284  LOAD_CONST               16
             5286  CALL_FUNCTION_2       2  '2 positional arguments'
             5288  STORE_FAST               'flash2_clk_delay'
             5290  JUMP_FORWARD       5302  'to 5302'
           5292_0  COME_FROM          5276  '5276'

 L.3165      5292  LOAD_GLOBAL              int
             5294  LOAD_FAST                'clk_delay_cfg'
             5296  LOAD_CONST               10
             5298  CALL_FUNCTION_2       2  '2 positional arguments'
             5300  STORE_FAST               'flash2_clk_delay'
           5302_0  COME_FROM          5290  '5290'
           5302_1  COME_FROM          5252  '5252'

 L.3168      5302  LOAD_FAST                'flash2_pin'
             5304  LOAD_CONST               0
             5306  BINARY_LSHIFT    
             5308  LOAD_FAST                'flash2_clock_cfg'
             5310  LOAD_CONST               8
             5312  BINARY_LSHIFT    
             5314  BINARY_ADD       
             5316  LOAD_FAST                'flash2_io_mode'
             5318  LOAD_CONST               16
             5320  BINARY_LSHIFT    
             5322  BINARY_ADD       

 L.3169      5324  LOAD_FAST                'flash2_clk_delay'
             5326  LOAD_CONST               24
             5328  BINARY_LSHIFT    
             5330  BINARY_ADD       
             5332  STORE_FAST               'flash2_set'

 L.3170      5334  LOAD_FAST                'load_function'
             5336  LOAD_CONST               2
             5338  COMPARE_OP               ==
         5340_5342  POP_JUMP_IF_FALSE  5402  'to 5402'

 L.3171      5344  LOAD_GLOBAL              bflb_utils
             5346  LOAD_METHOD              printf
             5348  LOAD_STR                 'set flash2 cfg: %X'
             5350  LOAD_FAST                'flash2_set'
             5352  BINARY_MODULO    
             5354  CALL_METHOD_1         1  '1 positional argument'
             5356  POP_TOP          

 L.3172      5358  LOAD_FAST                'self'
             5360  LOAD_METHOD              flash_set_para_main_process
             5362  LOAD_FAST                'flash2_set'
             5364  LOAD_GLOBAL              bytearray
             5366  LOAD_CONST               0
             5368  CALL_FUNCTION_1       1  '1 positional argument'

 L.3173      5370  LOAD_FAST                'self'
             5372  LOAD_ATTR                _need_shake_hand
             5374  CALL_METHOD_3         3  '3 positional arguments'
             5376  STORE_FAST               'ret'

 L.3174      5378  LOAD_CONST               False
             5380  LOAD_FAST                'self'
             5382  STORE_ATTR               _need_shake_hand

 L.3175      5384  LOAD_FAST                'ret'
             5386  LOAD_CONST               False
             5388  COMPARE_OP               is
         5390_5392  POP_JUMP_IF_FALSE  5402  'to 5402'

 L.3176      5394  LOAD_CONST               False
             5396  LOAD_FAST                'flash_burn_retry'
             5398  BUILD_TUPLE_2         2 
             5400  RETURN_VALUE     
           5402_0  COME_FROM          5390  '5390'
           5402_1  COME_FROM          5340  '5340'

 L.3178      5402  LOAD_FAST                'self'
             5404  LOAD_METHOD              flash_switch_bank_process
             5406  LOAD_CONST               1
             5408  LOAD_FAST                'self'
             5410  LOAD_ATTR                _need_shake_hand
             5412  CALL_METHOD_2         2  '2 positional arguments'
             5414  STORE_FAST               'ret'

 L.3179      5416  LOAD_CONST               False
             5418  LOAD_FAST                'self'
             5420  STORE_ATTR               _need_shake_hand

 L.3180      5422  LOAD_FAST                'ret'
             5424  LOAD_CONST               False
             5426  COMPARE_OP               is
         5428_5430  POP_JUMP_IF_FALSE  5440  'to 5440'

 L.3181      5432  LOAD_CONST               False
             5434  LOAD_FAST                'flash_burn_retry'
             5436  BUILD_TUPLE_2         2 
             5438  RETURN_VALUE     
           5440_0  COME_FROM          5428  '5428'

 L.3183      5440  LOAD_FAST                'self'
             5442  LOAD_METHOD              flash_read_jedec_id_process
             5444  LOAD_FAST                'self'
             5446  LOAD_ATTR                _need_shake_hand
             5448  CALL_METHOD_1         1  '1 positional argument'
             5450  UNPACK_SEQUENCE_2     2 
             5452  STORE_FAST               'ret'
             5454  STORE_FAST               'data'

 L.3184      5456  LOAD_FAST                'ret'
         5458_5460  POP_JUMP_IF_FALSE  5632  'to 5632'

 L.3185      5462  LOAD_CONST               False
             5464  LOAD_FAST                'self'
             5466  STORE_ATTR               _need_shake_hand

 L.3186      5468  LOAD_GLOBAL              binascii
             5470  LOAD_METHOD              hexlify
             5472  LOAD_FAST                'data'
             5474  CALL_METHOD_1         1  '1 positional argument'
             5476  LOAD_METHOD              decode
             5478  LOAD_STR                 'utf-8'
             5480  CALL_METHOD_1         1  '1 positional argument'
             5482  STORE_FAST               'data'

 L.3187      5484  LOAD_FAST                'data'
             5486  LOAD_CONST               6
             5488  LOAD_CONST               None
             5490  BUILD_SLICE_2         2 
             5492  BINARY_SUBSCR    
             5494  STORE_FAST               'id2_valid_flag'

 L.3188      5496  LOAD_FAST                'data'
             5498  LOAD_CONST               0
             5500  LOAD_CONST               6
             5502  BUILD_SLICE_2         2 
             5504  BINARY_SUBSCR    
             5506  STORE_FAST               'read_id2'

 L.3189      5508  LOAD_FAST                'read_id2'
             5510  STORE_FAST               'read_flash2_id'

 L.3190      5512  LOAD_FAST                'cfg'
             5514  LOAD_METHOD              has_option
             5516  LOAD_STR                 'FLASH2_CFG'
             5518  LOAD_STR                 'flash2_para'
             5520  CALL_METHOD_2         2  '2 positional arguments'
         5522_5524  POP_JUMP_IF_FALSE  5650  'to 5650'

 L.3191      5526  LOAD_GLOBAL              os
             5528  LOAD_ATTR                path
             5530  LOAD_METHOD              join

 L.3192      5532  LOAD_GLOBAL              app_path
             5534  LOAD_FAST                'cfg'
             5536  LOAD_METHOD              get
             5538  LOAD_STR                 'FLASH2_CFG'
             5540  LOAD_STR                 'flash2_para'
             5542  CALL_METHOD_2         2  '2 positional arguments'
             5544  CALL_METHOD_2         2  '2 positional arguments'
             5546  STORE_FAST               'flash2_para_file'

 L.3193      5548  LOAD_FAST                'self'
             5550  LOAD_METHOD              flash_para_update
             5552  LOAD_FAST                'flash2_para_file'
             5554  LOAD_FAST                'read_id2'
             5556  CALL_METHOD_2         2  '2 positional arguments'
             5558  POP_TOP          

 L.3196      5560  LOAD_GLOBAL              open_file
             5562  LOAD_FAST                'flash2_para_file'
             5564  LOAD_STR                 'rb'
             5566  CALL_FUNCTION_2       2  '2 positional arguments'
             5568  STORE_FAST               'fp'

 L.3197      5570  LOAD_GLOBAL              bytearray
             5572  LOAD_FAST                'fp'
             5574  LOAD_METHOD              read
             5576  CALL_METHOD_0         0  '0 positional arguments'
             5578  CALL_FUNCTION_1       1  '1 positional argument'
             5580  STORE_FAST               'para_data'

 L.3198      5582  LOAD_FAST                'fp'
             5584  LOAD_METHOD              close
             5586  CALL_METHOD_0         0  '0 positional arguments'
             5588  POP_TOP          

 L.3199      5590  LOAD_CONST               b'\x11'
             5592  LOAD_FAST                'para_data'
             5594  LOAD_CONST               0
             5596  LOAD_CONST               1
             5598  BUILD_SLICE_2         2 
             5600  STORE_SUBSCR     

 L.3200      5602  LOAD_GLOBAL              open_file
             5604  LOAD_FAST                'flash2_para_file'
             5606  LOAD_STR                 'wb+'
             5608  CALL_FUNCTION_2       2  '2 positional arguments'
             5610  STORE_FAST               'fp'

 L.3201      5612  LOAD_FAST                'fp'
             5614  LOAD_METHOD              write
             5616  LOAD_FAST                'para_data'
             5618  CALL_METHOD_1         1  '1 positional argument'
             5620  POP_TOP          

 L.3202      5622  LOAD_FAST                'fp'
             5624  LOAD_METHOD              close
             5626  CALL_METHOD_0         0  '0 positional arguments'
             5628  POP_TOP          
             5630  JUMP_FORWARD       5650  'to 5650'
           5632_0  COME_FROM          5458  '5458'

 L.3204      5632  LOAD_FAST                'self'
             5634  LOAD_METHOD              error_code_print
             5636  LOAD_STR                 '0030'
             5638  CALL_METHOD_1         1  '1 positional argument'
             5640  POP_TOP          

 L.3205      5642  LOAD_CONST               False
             5644  LOAD_FAST                'flash_burn_retry'
             5646  BUILD_TUPLE_2         2 
             5648  RETURN_VALUE     
           5650_0  COME_FROM          5630  '5630'
           5650_1  COME_FROM          5522  '5522'

 L.3207      5650  LOAD_FAST                'self'
             5652  LOAD_METHOD              flash_switch_bank_process
             5654  LOAD_CONST               0
             5656  LOAD_FAST                'self'
             5658  LOAD_ATTR                _need_shake_hand
             5660  CALL_METHOD_2         2  '2 positional arguments'
             5662  STORE_FAST               'ret'

 L.3208      5664  LOAD_CONST               False
             5666  LOAD_FAST                'self'
             5668  STORE_ATTR               _need_shake_hand

 L.3209      5670  LOAD_FAST                'ret'
             5672  LOAD_CONST               False
             5674  COMPARE_OP               is
         5676_5678  POP_JUMP_IF_FALSE  5688  'to 5688'

 L.3210      5680  LOAD_CONST               False
             5682  LOAD_FAST                'flash_burn_retry'
             5684  BUILD_TUPLE_2         2 
             5686  RETURN_VALUE     
           5688_0  COME_FROM          5676  '5676'
           5688_1  COME_FROM          4980  '4980'
           5688_2  COME_FROM          4950  '4950'
           5688_3  COME_FROM          4936  '4936'
           5688_4  COME_FROM          4124  '4124'

 L.3213      5688  LOAD_FAST                'args'
             5690  LOAD_ATTR                none
         5692_5694  POP_JUMP_IF_FALSE  5704  'to 5704'

 L.3214      5696  LOAD_CONST               True
             5698  LOAD_FAST                'flash_burn_retry'
             5700  BUILD_TUPLE_2         2 
             5702  RETURN_VALUE     
           5704_0  COME_FROM          5692  '5692'

 L.3217      5704  LOAD_FAST                'args'
             5706  LOAD_ATTR                erase
         5708_5710  POP_JUMP_IF_FALSE  5850  'to 5850'

 L.3218      5712  LOAD_GLOBAL              bflb_utils
             5714  LOAD_METHOD              printf
             5716  LOAD_STR                 'Erase flash operation'
             5718  CALL_METHOD_1         1  '1 positional argument'
             5720  POP_TOP          

 L.3219      5722  LOAD_FAST                'self'
             5724  LOAD_ATTR                _skip_len
         5726_5728  POP_JUMP_IF_FALSE  5744  'to 5744'

 L.3220      5730  LOAD_GLOBAL              bflb_utils
             5732  LOAD_METHOD              printf
             5734  LOAD_STR                 'error: skip mode can not set flash chiperase!'
             5736  CALL_METHOD_1         1  '1 positional argument'
             5738  POP_TOP          

 L.3221      5740  LOAD_CONST               (False, 0)
             5742  RETURN_VALUE     
           5744_0  COME_FROM          5726  '5726'

 L.3222      5744  LOAD_FAST                'end'
             5746  LOAD_STR                 '0'
             5748  COMPARE_OP               ==
         5750_5752  POP_JUMP_IF_FALSE  5790  'to 5790'

 L.3223      5754  LOAD_CONST               0
             5756  STORE_FAST               'erase'

 L.3224      5758  LOAD_FAST                'self'
             5760  LOAD_METHOD              flash_chiperase_main_process
             5762  LOAD_FAST                'self'
             5764  LOAD_ATTR                _need_shake_hand
             5766  CALL_METHOD_1         1  '1 positional argument'
             5768  STORE_FAST               'ret'

 L.3225      5770  LOAD_FAST                'ret'
             5772  LOAD_CONST               False
             5774  COMPARE_OP               is
         5776_5778  POP_JUMP_IF_FALSE  5840  'to 5840'

 L.3226      5780  LOAD_CONST               False
             5782  LOAD_FAST                'flash_burn_retry'
             5784  BUILD_TUPLE_2         2 
             5786  RETURN_VALUE     
             5788  JUMP_FORWARD       5840  'to 5840'
           5790_0  COME_FROM          5750  '5750'

 L.3228      5790  LOAD_CONST               1
             5792  STORE_FAST               'erase'

 L.3229      5794  LOAD_FAST                'self'
             5796  LOAD_METHOD              flash_erase_main_process
             5798  LOAD_GLOBAL              int
             5800  LOAD_FAST                'start'
             5802  LOAD_CONST               16
             5804  CALL_FUNCTION_2       2  '2 positional arguments'
             5806  LOAD_GLOBAL              int
             5808  LOAD_FAST                'end'
             5810  LOAD_CONST               16
             5812  CALL_FUNCTION_2       2  '2 positional arguments'

 L.3230      5814  LOAD_FAST                'self'
             5816  LOAD_ATTR                _need_shake_hand
             5818  CALL_METHOD_3         3  '3 positional arguments'
             5820  STORE_FAST               'ret'

 L.3231      5822  LOAD_FAST                'ret'
             5824  LOAD_CONST               False
             5826  COMPARE_OP               is
         5828_5830  POP_JUMP_IF_FALSE  5840  'to 5840'

 L.3232      5832  LOAD_CONST               False
             5834  LOAD_FAST                'flash_burn_retry'
             5836  BUILD_TUPLE_2         2 
             5838  RETURN_VALUE     
           5840_0  COME_FROM          5828  '5828'
           5840_1  COME_FROM          5788  '5788'
           5840_2  COME_FROM          5776  '5776'

 L.3233      5840  LOAD_GLOBAL              bflb_utils
             5842  LOAD_METHOD              printf
             5844  LOAD_STR                 'Erase flash OK'
             5846  CALL_METHOD_1         1  '1 positional argument'
             5848  POP_TOP          
           5850_0  COME_FROM          5708  '5708'

 L.3235      5850  LOAD_FAST                'args'
             5852  LOAD_ATTR                write
         5854_5856  POP_JUMP_IF_FALSE  8968  'to 8968'

 L.3236      5858  LOAD_FAST                'args'
             5860  LOAD_ATTR                flash
         5862_5864  POP_JUMP_IF_TRUE   5892  'to 5892'
             5866  LOAD_FAST                'args'
             5868  LOAD_ATTR                efuse
         5870_5872  POP_JUMP_IF_TRUE   5892  'to 5892'

 L.3237      5874  LOAD_GLOBAL              bflb_utils
             5876  LOAD_METHOD              printf
             5878  LOAD_STR                 'No target select'
             5880  CALL_METHOD_1         1  '1 positional argument'
             5882  POP_TOP          

 L.3238      5884  LOAD_CONST               False
             5886  LOAD_FAST                'flash_burn_retry'
             5888  BUILD_TUPLE_2         2 
             5890  RETURN_VALUE     
           5892_0  COME_FROM          5870  '5870'
           5892_1  COME_FROM          5862  '5862'

 L.3239      5892  LOAD_GLOBAL              bflb_utils
             5894  LOAD_METHOD              printf
             5896  LOAD_STR                 'Program operation'
             5898  CALL_METHOD_1         1  '1 positional argument'
             5900  POP_TOP          

 L.3241      5902  LOAD_FAST                'args'
             5904  LOAD_ATTR                flash
         5906_5908  POP_JUMP_IF_FALSE  8062  'to 8062'

 L.3242      5910  LOAD_STR                 ''
             5912  STORE_FAST               'flash_para_file'

 L.3243      5914  LOAD_STR                 ''
             5916  STORE_FAST               'flash2_para_file'

 L.3244      5918  LOAD_FAST                'cfg'
             5920  LOAD_METHOD              has_option
             5922  LOAD_STR                 'FLASH_CFG'
             5924  LOAD_STR                 'flash_para'
             5926  CALL_METHOD_2         2  '2 positional arguments'
         5928_5930  POP_JUMP_IF_FALSE  5954  'to 5954'

 L.3245      5932  LOAD_GLOBAL              os
             5934  LOAD_ATTR                path
             5936  LOAD_METHOD              join
             5938  LOAD_GLOBAL              app_path
             5940  LOAD_FAST                'cfg'
             5942  LOAD_METHOD              get
             5944  LOAD_STR                 'FLASH_CFG'
             5946  LOAD_STR                 'flash_para'
             5948  CALL_METHOD_2         2  '2 positional arguments'
             5950  CALL_METHOD_2         2  '2 positional arguments'
             5952  STORE_FAST               'flash_para_file'
           5954_0  COME_FROM          5928  '5928'

 L.3246      5954  LOAD_FAST                'cfg'
             5956  LOAD_METHOD              has_option
             5958  LOAD_STR                 'FLASH2_CFG'
             5960  LOAD_STR                 'flash2_para'
             5962  CALL_METHOD_2         2  '2 positional arguments'
         5964_5966  POP_JUMP_IF_FALSE  5990  'to 5990'

 L.3247      5968  LOAD_GLOBAL              os
             5970  LOAD_ATTR                path
             5972  LOAD_METHOD              join
             5974  LOAD_GLOBAL              app_path
             5976  LOAD_FAST                'cfg'
             5978  LOAD_METHOD              get
             5980  LOAD_STR                 'FLASH2_CFG'
             5982  LOAD_STR                 'flash2_para'
             5984  CALL_METHOD_2         2  '2 positional arguments'
             5986  CALL_METHOD_2         2  '2 positional arguments'
             5988  STORE_FAST               'flash2_para_file'
           5990_0  COME_FROM          5964  '5964'

 L.3248      5990  LOAD_FAST                'romfs_data'
             5992  LOAD_STR                 ''
             5994  COMPARE_OP               !=
         5996_5998  POP_JUMP_IF_FALSE  6124  'to 6124'

 L.3249      6000  LOAD_FAST                'address'
             6002  LOAD_STR                 ''
             6004  COMPARE_OP               ==
         6006_6008  POP_JUMP_IF_FALSE  6038  'to 6038'

 L.3250      6010  LOAD_GLOBAL              bflb_utils
             6012  LOAD_METHOD              printf
             6014  LOAD_STR                 'Please set romfs load address'
             6016  CALL_METHOD_1         1  '1 positional argument'
             6018  POP_TOP          

 L.3251      6020  LOAD_FAST                'self'
             6022  LOAD_METHOD              error_code_print
             6024  LOAD_STR                 '0041'
             6026  CALL_METHOD_1         1  '1 positional argument'
             6028  POP_TOP          

 L.3252      6030  LOAD_CONST               False
             6032  LOAD_FAST                'flash_burn_retry'
             6034  BUILD_TUPLE_2         2 
             6036  RETURN_VALUE     
           6038_0  COME_FROM          6006  '6006'

 L.3253      6038  LOAD_GLOBAL              bflb_utils
             6040  LOAD_METHOD              printf
             6042  LOAD_STR                 'load romfs '
             6044  LOAD_FAST                'romfs_data'
             6046  CALL_METHOD_2         2  '2 positional arguments'
             6048  POP_TOP          

 L.3254      6050  LOAD_FAST                'self'
             6052  LOAD_METHOD              load_romfs_data
             6054  LOAD_FAST                'romfs_data'
             6056  LOAD_GLOBAL              int
             6058  LOAD_FAST                'address'
             6060  LOAD_CONST               16
             6062  CALL_FUNCTION_2       2  '2 positional arguments'
             6064  LOAD_FAST                'verify'

 L.3255      6066  LOAD_FAST                'self'
             6068  LOAD_ATTR                _need_shake_hand
             6070  LOAD_FAST                'callback'
             6072  CALL_METHOD_5         5  '5 positional arguments'
             6074  STORE_FAST               'ret'

 L.3256      6076  LOAD_FAST                'ret'
             6078  LOAD_CONST               False
             6080  COMPARE_OP               is
         6082_6084  POP_JUMP_IF_FALSE  6104  'to 6104'

 L.3257      6086  LOAD_FAST                'self'
             6088  LOAD_METHOD              error_code_print
             6090  LOAD_STR                 '0041'
             6092  CALL_METHOD_1         1  '1 positional argument'
             6094  POP_TOP          

 L.3258      6096  LOAD_CONST               False
             6098  LOAD_FAST                'flash_burn_retry'
             6100  BUILD_TUPLE_2         2 
             6102  RETURN_VALUE     
           6104_0  COME_FROM          6082  '6082'

 L.3259      6104  LOAD_CONST               False
             6106  LOAD_FAST                'self'
             6108  STORE_ATTR               _need_shake_hand

 L.3260      6110  LOAD_GLOBAL              bflb_utils
             6112  LOAD_METHOD              printf
             6114  LOAD_STR                 'Program romfs Finished'
             6116  CALL_METHOD_1         1  '1 positional argument'
             6118  POP_TOP          
         6120_6122  JUMP_FORWARD       8062  'to 8062'
           6124_0  COME_FROM          5996  '5996'

 L.3261      6124  LOAD_FAST                'fwbin'
         6126_6128  POP_JUMP_IF_FALSE  6264  'to 6264'

 L.3262      6130  LOAD_GLOBAL              bflb_utils
             6132  LOAD_METHOD              printf
             6134  LOAD_STR                 'load firmware bin '
             6136  LOAD_FAST                'fwbin'
             6138  CALL_METHOD_2         2  '2 positional arguments'
             6140  POP_TOP          

 L.3263      6142  LOAD_GLOBAL              os
             6144  LOAD_ATTR                path
             6146  LOAD_METHOD              abspath
             6148  LOAD_FAST                'fwbin'
             6150  CALL_METHOD_1         1  '1 positional argument'
             6152  STORE_FAST               'fwbin'

 L.3264      6154  LOAD_FAST                'self'
             6156  LOAD_METHOD              flash_cfg_option
             6158  LOAD_FAST                'read_flash_id'
             6160  LOAD_FAST                'flash_para_file'
             6162  LOAD_FAST                'flash_set'
             6164  LOAD_FAST                'id_valid_flag'
             6166  LOAD_FAST                'fwbin'

 L.3265      6168  LOAD_FAST                'config_file'
             6170  LOAD_FAST                'cfg'
             6172  LOAD_FAST                'create_img_callback'
             6174  LOAD_FAST                'create_simple_callback'
             6176  CALL_METHOD_9         9  '9 positional arguments'
             6178  STORE_FAST               'ret'

 L.3266      6180  LOAD_FAST                'ret'
             6182  LOAD_CONST               False
             6184  COMPARE_OP               is
         6186_6188  POP_JUMP_IF_FALSE  6198  'to 6198'

 L.3267      6190  LOAD_CONST               False
             6192  LOAD_FAST                'flash_burn_retry'
             6194  BUILD_TUPLE_2         2 
             6196  RETURN_VALUE     
           6198_0  COME_FROM          6186  '6186'

 L.3268      6198  LOAD_FAST                'self'
             6200  LOAD_METHOD              load_firmware_bin
             6202  LOAD_FAST                'fwbin'
             6204  LOAD_FAST                'verify'
             6206  LOAD_FAST                'self'
             6208  LOAD_ATTR                _need_shake_hand
             6210  LOAD_FAST                'callback'
             6212  CALL_METHOD_4         4  '4 positional arguments'
             6214  STORE_FAST               'ret'

 L.3269      6216  LOAD_FAST                'ret'
             6218  LOAD_CONST               False
             6220  COMPARE_OP               is
         6222_6224  POP_JUMP_IF_FALSE  6244  'to 6244'

 L.3270      6226  LOAD_FAST                'self'
             6228  LOAD_METHOD              error_code_print
             6230  LOAD_STR                 '003C'
             6232  CALL_METHOD_1         1  '1 positional argument'
             6234  POP_TOP          

 L.3271      6236  LOAD_CONST               False
             6238  LOAD_FAST                'flash_burn_retry'
             6240  BUILD_TUPLE_2         2 
             6242  RETURN_VALUE     
           6244_0  COME_FROM          6222  '6222'

 L.3272      6244  LOAD_CONST               False
             6246  LOAD_FAST                'self'
             6248  STORE_ATTR               _need_shake_hand

 L.3273      6250  LOAD_GLOBAL              bflb_utils
             6252  LOAD_METHOD              printf
             6254  LOAD_STR                 'Program fwbin Finished'
             6256  CALL_METHOD_1         1  '1 positional argument'
             6258  POP_TOP          
         6260_6262  JUMP_FORWARD       8062  'to 8062'
           6264_0  COME_FROM          6126  '6126'

 L.3274      6264  LOAD_FAST                'massbin'
         6266_6268  POP_JUMP_IF_FALSE  6418  'to 6418'

 L.3275      6270  LOAD_GLOBAL              bflb_utils
             6272  LOAD_METHOD              printf
             6274  LOAD_STR                 'load mass bin '
             6276  LOAD_FAST                'massbin'
             6278  CALL_METHOD_2         2  '2 positional arguments'
             6280  POP_TOP          

 L.3276      6282  LOAD_GLOBAL              bflb_utils
             6284  LOAD_METHOD              printf
             6286  LOAD_STR                 '========= programming mass '
             6288  LOAD_FAST                'massbin'
             6290  LOAD_STR                 ' to '
             6292  LOAD_GLOBAL              hex
             6294  LOAD_CONST               0
             6296  CALL_FUNCTION_1       1  '1 positional argument'
             6298  CALL_METHOD_4         4  '4 positional arguments'
             6300  POP_TOP          

 L.3277      6302  LOAD_GLOBAL              os
             6304  LOAD_ATTR                path
             6306  LOAD_METHOD              abspath
             6308  LOAD_FAST                'massbin'
             6310  CALL_METHOD_1         1  '1 positional argument'
             6312  STORE_FAST               'massbin'

 L.3278      6314  LOAD_FAST                'self'
             6316  LOAD_METHOD              flash_cfg_option
             6318  LOAD_FAST                'read_flash_id'
             6320  LOAD_FAST                'flash_para_file'
             6322  LOAD_FAST                'flash_set'
             6324  LOAD_FAST                'id_valid_flag'
             6326  LOAD_FAST                'massbin'

 L.3279      6328  LOAD_FAST                'config_file'
             6330  LOAD_FAST                'cfg'
             6332  LOAD_FAST                'create_img_callback'
             6334  LOAD_FAST                'create_simple_callback'
             6336  CALL_METHOD_9         9  '9 positional arguments'
             6338  STORE_FAST               'ret'

 L.3280      6340  LOAD_FAST                'ret'
             6342  LOAD_CONST               False
             6344  COMPARE_OP               is
         6346_6348  POP_JUMP_IF_FALSE  6358  'to 6358'

 L.3281      6350  LOAD_CONST               False
             6352  LOAD_FAST                'flash_burn_retry'
             6354  BUILD_TUPLE_2         2 
             6356  RETURN_VALUE     
           6358_0  COME_FROM          6346  '6346'

 L.3282      6358  LOAD_FAST                'self'
             6360  LOAD_METHOD              flash_load_specified
             6362  LOAD_FAST                'massbin'
             6364  LOAD_CONST               0
             6366  LOAD_CONST               1
             6368  LOAD_FAST                'verify'
             6370  LOAD_FAST                'self'
             6372  LOAD_ATTR                _need_shake_hand

 L.3283      6374  LOAD_FAST                'callback'
             6376  CALL_METHOD_6         6  '6 positional arguments'
             6378  STORE_FAST               'ret'

 L.3284      6380  LOAD_FAST                'ret'
             6382  LOAD_CONST               False
             6384  COMPARE_OP               is
         6386_6388  POP_JUMP_IF_FALSE  6398  'to 6398'

 L.3285      6390  LOAD_CONST               False
             6392  LOAD_FAST                'flash_burn_retry'
             6394  BUILD_TUPLE_2         2 
             6396  RETURN_VALUE     
           6398_0  COME_FROM          6386  '6386'

 L.3286      6398  LOAD_CONST               False
             6400  LOAD_FAST                'self'
             6402  STORE_ATTR               _need_shake_hand

 L.3287      6404  LOAD_GLOBAL              bflb_utils
             6406  LOAD_METHOD              printf
             6408  LOAD_STR                 'Program massbin Finished'
             6410  CALL_METHOD_1         1  '1 positional argument'
             6412  POP_TOP          
         6414_6416  JUMP_FORWARD       8062  'to 8062'
           6418_0  COME_FROM          6266  '6266'

 L.3289      6418  LOAD_FAST                'file'
         6420_6422  POP_JUMP_IF_FALSE  6450  'to 6450'

 L.3290      6424  LOAD_FAST                'file'
             6426  LOAD_METHOD              split
             6428  LOAD_STR                 ','
             6430  CALL_METHOD_1         1  '1 positional argument'
             6432  STORE_FAST               'flash_file'

 L.3291      6434  LOAD_FAST                'address'
             6436  LOAD_METHOD              split
             6438  LOAD_STR                 ','
             6440  CALL_METHOD_1         1  '1 positional argument'
             6442  STORE_FAST               'address'

 L.3292      6444  LOAD_CONST               1
             6446  STORE_FAST               'erase'
             6448  JUMP_FORWARD       6498  'to 6498'
           6450_0  COME_FROM          6420  '6420'

 L.3294      6450  LOAD_GLOBAL              re
             6452  LOAD_METHOD              compile
             6454  LOAD_STR                 '\\s+'
             6456  CALL_METHOD_1         1  '1 positional argument'
             6458  LOAD_METHOD              split
             6460  LOAD_FAST                'cfg'
             6462  LOAD_METHOD              get
             6464  LOAD_STR                 'FLASH_CFG'
             6466  LOAD_STR                 'file'
             6468  CALL_METHOD_2         2  '2 positional arguments'
             6470  CALL_METHOD_1         1  '1 positional argument'
             6472  STORE_FAST               'flash_file'

 L.3295      6474  LOAD_GLOBAL              re
             6476  LOAD_METHOD              compile
             6478  LOAD_STR                 '\\s+'
             6480  CALL_METHOD_1         1  '1 positional argument'
             6482  LOAD_METHOD              split
             6484  LOAD_FAST                'cfg'
             6486  LOAD_METHOD              get
             6488  LOAD_STR                 'FLASH_CFG'
             6490  LOAD_STR                 'address'
             6492  CALL_METHOD_2         2  '2 positional arguments'
             6494  CALL_METHOD_1         1  '1 positional argument'
             6496  STORE_FAST               'address'
           6498_0  COME_FROM          6448  '6448'

 L.3296      6498  LOAD_FAST                'csvfile'
         6500_6502  POP_JUMP_IF_FALSE  6620  'to 6620'
             6504  LOAD_FAST                'csvaddr'
         6506_6508  POP_JUMP_IF_FALSE  6620  'to 6620'

 L.3297      6510  LOAD_GLOBAL              bflb_utils
             6512  LOAD_METHOD              printf
             6514  LOAD_STR                 'factory info burn'
             6516  CALL_METHOD_1         1  '1 positional argument'
             6518  POP_TOP          

 L.3298      6520  LOAD_STR                 'chips/'
             6522  LOAD_FAST                'self'
             6524  LOAD_ATTR                _chip_name
             6526  LOAD_METHOD              lower
             6528  CALL_METHOD_0         0  '0 positional arguments'
             6530  BINARY_ADD       
             6532  LOAD_STR                 '/img_create_iot/media.bin'
             6534  BINARY_ADD       
             6536  STORE_FAST               'csvbin'

 L.3299      6538  LOAD_FAST                'self'
             6540  LOAD_METHOD              get_factory_config_info
             6542  LOAD_FAST                'csvfile'
             6544  LOAD_FAST                'csvbin'
             6546  CALL_METHOD_2         2  '2 positional arguments'
             6548  UNPACK_SEQUENCE_2     2 
             6550  STORE_FAST               'ret'
             6552  STORE_FAST               'csv_mac'

 L.3300      6554  LOAD_FAST                'ret'
             6556  LOAD_CONST               False
             6558  COMPARE_OP               is-not
         6560_6562  POP_JUMP_IF_FALSE  6602  'to 6602'

 L.3301      6564  LOAD_FAST                'flash_file'
             6566  LOAD_METHOD              append
             6568  LOAD_FAST                'csvbin'
             6570  CALL_METHOD_1         1  '1 positional argument'
             6572  POP_TOP          

 L.3302      6574  LOAD_FAST                'address'
             6576  LOAD_METHOD              append
             6578  LOAD_FAST                'csvaddr'
             6580  CALL_METHOD_1         1  '1 positional argument'
             6582  POP_TOP          

 L.3303      6584  LOAD_FAST                'csv_mac'
         6586_6588  POP_JUMP_IF_FALSE  6620  'to 6620'

 L.3304      6590  LOAD_FAST                'csv_mac'
             6592  STORE_FAST               'macaddr'

 L.3305      6594  LOAD_CONST               True
             6596  LOAD_FAST                'args'
             6598  STORE_ATTR               efuse
             6600  JUMP_FORWARD       6620  'to 6620'
           6602_0  COME_FROM          6560  '6560'

 L.3307      6602  LOAD_GLOBAL              bflb_utils
             6604  LOAD_METHOD              printf
             6606  LOAD_STR                 'create media.bin fail'
             6608  CALL_METHOD_1         1  '1 positional argument'
             6610  POP_TOP          

 L.3308      6612  LOAD_CONST               False
             6614  LOAD_FAST                'flash_burn_retry'
             6616  BUILD_TUPLE_2         2 
             6618  RETURN_VALUE     
           6620_0  COME_FROM          6600  '6600'
           6620_1  COME_FROM          6586  '6586'
           6620_2  COME_FROM          6506  '6506'
           6620_3  COME_FROM          6500  '6500'

 L.3310      6620  LOAD_FAST                'erase'
             6622  LOAD_CONST               2
             6624  COMPARE_OP               ==
         6626_6628  POP_JUMP_IF_FALSE  6670  'to 6670'

 L.3311      6630  LOAD_FAST                'self'
             6632  LOAD_METHOD              flash_chiperase_main_process
             6634  LOAD_FAST                'self'
             6636  LOAD_ATTR                _need_shake_hand
             6638  CALL_METHOD_1         1  '1 positional argument'
             6640  STORE_FAST               'ret'

 L.3312      6642  LOAD_FAST                'ret'
             6644  LOAD_CONST               False
             6646  COMPARE_OP               is
         6648_6650  POP_JUMP_IF_FALSE  6660  'to 6660'

 L.3313      6652  LOAD_CONST               False
             6654  LOAD_FAST                'flash_burn_retry'
             6656  BUILD_TUPLE_2         2 
             6658  RETURN_VALUE     
           6660_0  COME_FROM          6648  '6648'

 L.3314      6660  LOAD_CONST               False
             6662  LOAD_FAST                'self'
             6664  STORE_ATTR               _need_shake_hand

 L.3315      6666  LOAD_CONST               0
             6668  STORE_FAST               'erase'
           6670_0  COME_FROM          6626  '6626'

 L.3317      6670  LOAD_GLOBAL              len
             6672  LOAD_FAST                'flash_file'
             6674  CALL_FUNCTION_1       1  '1 positional argument'
             6676  LOAD_CONST               0
             6678  COMPARE_OP               >
         6680_6682  POP_JUMP_IF_FALSE  8052  'to 8052'

 L.3318      6684  LOAD_CONST               0
             6686  STORE_FAST               'size_before'

 L.3319      6688  LOAD_CONST               0
             6690  STORE_FAST               'size_all'

 L.3320      6692  LOAD_CONST               0
             6694  STORE_FAST               'i'

 L.3321      6696  SETUP_LOOP         6812  'to 6812'
             6698  LOAD_FAST                'flash_file'
             6700  GET_ITER         
             6702  FOR_ITER           6810  'to 6810'
             6704  STORE_FAST               'item'

 L.3322      6706  LOAD_FAST                'task_num'
             6708  LOAD_CONST               None
             6710  COMPARE_OP               !=
         6712_6714  POP_JUMP_IF_FALSE  6776  'to 6776'
             6716  LOAD_FAST                'self'
             6718  LOAD_ATTR                _csv_burn_en
             6720  LOAD_CONST               True
             6722  COMPARE_OP               is
         6724_6726  POP_JUMP_IF_FALSE  6776  'to 6776'

 L.3323      6728  LOAD_FAST                'size_all'
             6730  LOAD_GLOBAL              os
             6732  LOAD_ATTR                path
             6734  LOAD_METHOD              getsize

 L.3324      6736  LOAD_GLOBAL              os
             6738  LOAD_ATTR                path
             6740  LOAD_METHOD              join
             6742  LOAD_GLOBAL              app_path

 L.3325      6744  LOAD_GLOBAL              convert_path
             6746  LOAD_STR                 'task'
             6748  LOAD_GLOBAL              str
             6750  LOAD_FAST                'task_num'
             6752  CALL_FUNCTION_1       1  '1 positional argument'
             6754  BINARY_ADD       
             6756  LOAD_STR                 '/'
             6758  BINARY_ADD       

 L.3326      6760  LOAD_FAST                'item'
             6762  BINARY_ADD       
             6764  CALL_FUNCTION_1       1  '1 positional argument'
             6766  CALL_METHOD_2         2  '2 positional arguments'
             6768  CALL_METHOD_1         1  '1 positional argument'
             6770  INPLACE_ADD      
             6772  STORE_FAST               'size_all'
             6774  JUMP_BACK          6702  'to 6702'
           6776_0  COME_FROM          6724  '6724'
           6776_1  COME_FROM          6712  '6712'

 L.3328      6776  LOAD_FAST                'size_all'
             6778  LOAD_GLOBAL              os
             6780  LOAD_ATTR                path
             6782  LOAD_METHOD              getsize

 L.3329      6784  LOAD_GLOBAL              os
             6786  LOAD_ATTR                path
             6788  LOAD_METHOD              join
             6790  LOAD_GLOBAL              app_path
             6792  LOAD_GLOBAL              convert_path
             6794  LOAD_FAST                'item'
             6796  CALL_FUNCTION_1       1  '1 positional argument'
             6798  CALL_METHOD_2         2  '2 positional arguments'
             6800  CALL_METHOD_1         1  '1 positional argument'
             6802  INPLACE_ADD      
             6804  STORE_FAST               'size_all'
         6806_6808  JUMP_BACK          6702  'to 6702'
             6810  POP_BLOCK        
           6812_0  COME_FROM_LOOP     6696  '6696'

 L.3330  6812_6814  SETUP_EXCEPT       7984  'to 7984'

 L.3331      6816  LOAD_CONST               False
             6818  STORE_FAST               'ret'

 L.3332  6820_6822  SETUP_LOOP         7920  'to 7920'
             6824  LOAD_FAST                'i'
             6826  LOAD_GLOBAL              len
             6828  LOAD_FAST                'flash_file'
             6830  CALL_FUNCTION_1       1  '1 positional argument'
             6832  COMPARE_OP               <
         6834_6836  POP_JUMP_IF_FALSE  7918  'to 7918'

 L.3333      6838  LOAD_FAST                'task_num'
             6840  LOAD_CONST               None
             6842  COMPARE_OP               !=
         6844_6846  POP_JUMP_IF_FALSE  6920  'to 6920'
             6848  LOAD_FAST                'self'
             6850  LOAD_ATTR                _csv_burn_en
             6852  LOAD_CONST               True
             6854  COMPARE_OP               is
         6856_6858  POP_JUMP_IF_FALSE  6920  'to 6920'

 L.3334      6860  LOAD_STR                 'task'
             6862  LOAD_GLOBAL              str
             6864  LOAD_FAST                'task_num'
             6866  CALL_FUNCTION_1       1  '1 positional argument'
             6868  BINARY_ADD       
             6870  LOAD_STR                 '/'
             6872  BINARY_ADD       
             6874  LOAD_FAST                'flash_file'
             6876  LOAD_FAST                'i'
             6878  BINARY_SUBSCR    
             6880  BINARY_ADD       
             6882  LOAD_FAST                'flash_file'
             6884  LOAD_FAST                'i'
             6886  STORE_SUBSCR     

 L.3335      6888  LOAD_GLOBAL              os
             6890  LOAD_ATTR                path
             6892  LOAD_METHOD              getsize

 L.3336      6894  LOAD_GLOBAL              os
             6896  LOAD_ATTR                path
             6898  LOAD_METHOD              join
             6900  LOAD_GLOBAL              app_path
             6902  LOAD_GLOBAL              convert_path
             6904  LOAD_FAST                'flash_file'
             6906  LOAD_FAST                'i'
             6908  BINARY_SUBSCR    
             6910  CALL_FUNCTION_1       1  '1 positional argument'
             6912  CALL_METHOD_2         2  '2 positional arguments'
             6914  CALL_METHOD_1         1  '1 positional argument'
             6916  STORE_FAST               'size_current'
             6918  JUMP_FORWARD       6950  'to 6950'
           6920_0  COME_FROM          6856  '6856'
           6920_1  COME_FROM          6844  '6844'

 L.3338      6920  LOAD_GLOBAL              os
             6922  LOAD_ATTR                path
             6924  LOAD_METHOD              getsize

 L.3339      6926  LOAD_GLOBAL              os
             6928  LOAD_ATTR                path
             6930  LOAD_METHOD              join
             6932  LOAD_GLOBAL              app_path
             6934  LOAD_GLOBAL              convert_path
             6936  LOAD_FAST                'flash_file'
             6938  LOAD_FAST                'i'
             6940  BINARY_SUBSCR    
             6942  CALL_FUNCTION_1       1  '1 positional argument'
             6944  CALL_METHOD_2         2  '2 positional arguments'
             6946  CALL_METHOD_1         1  '1 positional argument'
             6948  STORE_FAST               'size_current'
           6950_0  COME_FROM          6918  '6918'

 L.3340      6950  LOAD_FAST                'callback'
         6952_6954  POP_JUMP_IF_FALSE  6968  'to 6968'

 L.3341      6956  LOAD_FAST                'callback'
             6958  LOAD_FAST                'size_before'
             6960  LOAD_FAST                'size_all'
             6962  LOAD_STR                 'program1'
             6964  CALL_FUNCTION_3       3  '3 positional arguments'
             6966  POP_TOP          
           6968_0  COME_FROM          6952  '6952'

 L.3342      6968  LOAD_FAST                'callback'
         6970_6972  POP_JUMP_IF_FALSE  6986  'to 6986'

 L.3343      6974  LOAD_FAST                'callback'
             6976  LOAD_FAST                'size_current'
             6978  LOAD_FAST                'size_all'
             6980  LOAD_STR                 'program2'
             6982  CALL_FUNCTION_3       3  '3 positional arguments'
             6984  POP_TOP          
           6986_0  COME_FROM          6970  '6970'

 L.3346      6986  LOAD_GLOBAL              bflb_utils
             6988  LOAD_METHOD              printf
             6990  LOAD_STR                 'Dealing Index '
             6992  LOAD_FAST                'i'
             6994  CALL_METHOD_2         2  '2 positional arguments'
             6996  POP_TOP          

 L.3347      6998  LOAD_FAST                'self'
             7000  LOAD_ATTR                _isp_en
             7002  LOAD_CONST               True
             7004  COMPARE_OP               is
         7006_7008  POP_JUMP_IF_FALSE  7032  'to 7032'

 L.3348      7010  LOAD_GLOBAL              bflb_utils
             7012  LOAD_METHOD              printf
             7014  LOAD_STR                 '========= programming '

 L.3349      7016  LOAD_GLOBAL              convert_path
             7018  LOAD_FAST                'flash_file'
             7020  LOAD_FAST                'i'
             7022  BINARY_SUBSCR    
             7024  CALL_FUNCTION_1       1  '1 positional argument'
             7026  CALL_METHOD_2         2  '2 positional arguments'
             7028  POP_TOP          
             7030  JUMP_FORWARD       7068  'to 7068'
           7032_0  COME_FROM          7006  '7006'

 L.3351      7032  LOAD_GLOBAL              bflb_utils
             7034  LOAD_METHOD              printf
             7036  LOAD_STR                 '========= programming '

 L.3352      7038  LOAD_GLOBAL              convert_path
             7040  LOAD_FAST                'flash_file'
             7042  LOAD_FAST                'i'
             7044  BINARY_SUBSCR    
             7046  CALL_FUNCTION_1       1  '1 positional argument'

 L.3353      7048  LOAD_STR                 ' to 0x%08X'
             7050  LOAD_GLOBAL              int
             7052  LOAD_FAST                'address'
             7054  LOAD_FAST                'i'
             7056  BINARY_SUBSCR    
             7058  LOAD_CONST               16
             7060  CALL_FUNCTION_2       2  '2 positional arguments'
             7062  BINARY_MODULO    
             7064  CALL_METHOD_3         3  '3 positional arguments'
             7066  POP_TOP          
           7068_0  COME_FROM          7030  '7030'

 L.3354      7068  LOAD_STR                 ''
             7070  STORE_FAST               'flash1_bin'

 L.3355      7072  LOAD_CONST               0
             7074  STORE_FAST               'flash1_bin_len'

 L.3356      7076  LOAD_STR                 ''
             7078  STORE_FAST               'flash2_bin'

 L.3357      7080  LOAD_CONST               0
             7082  STORE_FAST               'flash2_bin_len'

 L.3358      7084  LOAD_FAST                'self'
             7086  LOAD_ATTR                _chip_type
             7088  LOAD_STR                 'bl616'
             7090  COMPARE_OP               ==
         7092_7094  POP_JUMP_IF_TRUE   7108  'to 7108'
             7096  LOAD_FAST                'self'
             7098  LOAD_ATTR                _chip_type
             7100  LOAD_STR                 'wb03'
             7102  COMPARE_OP               ==
         7104_7106  POP_JUMP_IF_FALSE  7236  'to 7236'
           7108_0  COME_FROM          7092  '7092'

 L.3359      7108  LOAD_FAST                'self'
             7110  LOAD_ATTR                _flash1_size
             7112  LOAD_CONST               0
             7114  COMPARE_OP               !=
         7116_7118  POP_JUMP_IF_FALSE  7236  'to 7236'
             7120  LOAD_FAST                'self'
             7122  LOAD_ATTR                _flash1_size
             7124  LOAD_GLOBAL              int
             7126  LOAD_FAST                'address'
             7128  LOAD_FAST                'i'
             7130  BINARY_SUBSCR    
             7132  LOAD_CONST               16
             7134  CALL_FUNCTION_2       2  '2 positional arguments'
             7136  LOAD_FAST                'size_current'
             7138  BINARY_ADD       
             7140  COMPARE_OP               <
         7142_7144  POP_JUMP_IF_FALSE  7236  'to 7236'

 L.3360      7146  LOAD_FAST                'self'
             7148  LOAD_ATTR                _flash1_size
             7150  LOAD_GLOBAL              int
             7152  LOAD_FAST                'address'
             7154  LOAD_FAST                'i'
             7156  BINARY_SUBSCR    
             7158  LOAD_CONST               16
             7160  CALL_FUNCTION_2       2  '2 positional arguments'
             7162  COMPARE_OP               >
         7164_7166  POP_JUMP_IF_FALSE  7236  'to 7236'
             7168  LOAD_FAST                'self'
             7170  LOAD_ATTR                _flash2_select
             7172  LOAD_CONST               False
             7174  COMPARE_OP               is
         7176_7178  POP_JUMP_IF_FALSE  7236  'to 7236'

 L.3361      7180  LOAD_GLOBAL              bflb_utils
             7182  LOAD_METHOD              printf
             7184  LOAD_STR                 '%s file is overflow with flash1'

 L.3362      7186  LOAD_FAST                'flash_file'
             7188  LOAD_FAST                'i'
             7190  BINARY_SUBSCR    
             7192  BINARY_MODULO    
             7194  CALL_METHOD_1         1  '1 positional argument'
             7196  POP_TOP          

 L.3364      7198  LOAD_FAST                'self'
             7200  LOAD_METHOD              flash_loader_cut_flash_bin
             7202  LOAD_FAST                'flash_file'
             7204  LOAD_FAST                'i'
             7206  BINARY_SUBSCR    
             7208  LOAD_GLOBAL              int
             7210  LOAD_FAST                'address'
             7212  LOAD_FAST                'i'
             7214  BINARY_SUBSCR    
             7216  LOAD_CONST               16
             7218  CALL_FUNCTION_2       2  '2 positional arguments'
             7220  LOAD_FAST                'self'
             7222  LOAD_ATTR                _flash1_size
             7224  CALL_METHOD_3         3  '3 positional arguments'
             7226  UNPACK_SEQUENCE_4     4 
             7228  STORE_FAST               'flash1_bin'
             7230  STORE_FAST               'flash1_bin_len'
             7232  STORE_FAST               'flash2_bin'
             7234  STORE_FAST               'flash2_bin_len'
           7236_0  COME_FROM          7176  '7176'
           7236_1  COME_FROM          7164  '7164'
           7236_2  COME_FROM          7142  '7142'
           7236_3  COME_FROM          7116  '7116'
           7236_4  COME_FROM          7104  '7104'

 L.3365      7236  LOAD_FAST                'flash1_bin'
             7238  LOAD_STR                 ''
             7240  COMPARE_OP               !=
         7242_7244  POP_JUMP_IF_FALSE  7570  'to 7570'
             7246  LOAD_FAST                'flash2_bin'
             7248  LOAD_STR                 ''
             7250  COMPARE_OP               !=
         7252_7254  POP_JUMP_IF_FALSE  7570  'to 7570'

 L.3366      7256  LOAD_FAST                'self'
             7258  LOAD_METHOD              flash_cfg_option
             7260  LOAD_FAST                'read_flash_id'
             7262  LOAD_FAST                'flash_para_file'
             7264  LOAD_FAST                'flash_set'
             7266  LOAD_FAST                'id_valid_flag'
             7268  LOAD_FAST                'flash1_bin'

 L.3367      7270  LOAD_FAST                'config_file'
             7272  LOAD_FAST                'cfg'
             7274  LOAD_FAST                'create_img_callback'
             7276  LOAD_FAST                'create_simple_callback'
             7278  CALL_METHOD_9         9  '9 positional arguments'
             7280  STORE_FAST               'ret'

 L.3368      7282  LOAD_FAST                'ret'
             7284  LOAD_CONST               False
             7286  COMPARE_OP               is
         7288_7290  POP_JUMP_IF_FALSE  7300  'to 7300'

 L.3369      7292  LOAD_CONST               False
             7294  LOAD_FAST                'flash_burn_retry'
             7296  BUILD_TUPLE_2         2 
             7298  RETURN_VALUE     
           7300_0  COME_FROM          7288  '7288'

 L.3370      7300  LOAD_GLOBAL              bflb_utils
             7302  LOAD_METHOD              printf
             7304  LOAD_STR                 '========= programming '

 L.3371      7306  LOAD_GLOBAL              convert_path
             7308  LOAD_FAST                'flash1_bin'
             7310  CALL_FUNCTION_1       1  '1 positional argument'

 L.3372      7312  LOAD_STR                 ' to 0x%08X'
             7314  LOAD_GLOBAL              int
             7316  LOAD_FAST                'address'
             7318  LOAD_FAST                'i'
             7320  BINARY_SUBSCR    
             7322  LOAD_CONST               16
             7324  CALL_FUNCTION_2       2  '2 positional arguments'
             7326  BINARY_MODULO    
             7328  CALL_METHOD_3         3  '3 positional arguments'
             7330  POP_TOP          

 L.3373      7332  LOAD_FAST                'self'
             7334  LOAD_METHOD              flash_load_specified
             7336  LOAD_GLOBAL              convert_path
             7338  LOAD_FAST                'flash1_bin'
             7340  CALL_FUNCTION_1       1  '1 positional argument'

 L.3374      7342  LOAD_GLOBAL              int
             7344  LOAD_FAST                'address'
             7346  LOAD_FAST                'i'
             7348  BINARY_SUBSCR    
             7350  LOAD_CONST               16
             7352  CALL_FUNCTION_2       2  '2 positional arguments'
             7354  LOAD_FAST                'erase'

 L.3375      7356  LOAD_FAST                'verify'
             7358  LOAD_FAST                'self'
             7360  LOAD_ATTR                _need_shake_hand

 L.3376      7362  LOAD_FAST                'callback'
             7364  CALL_METHOD_6         6  '6 positional arguments'
             7366  STORE_FAST               'ret'

 L.3377      7368  LOAD_FAST                'ret'
             7370  LOAD_CONST               False
             7372  COMPARE_OP               is
         7374_7376  POP_JUMP_IF_FALSE  7386  'to 7386'

 L.3378      7378  LOAD_CONST               False
             7380  LOAD_FAST                'flash_burn_retry'
             7382  BUILD_TUPLE_2         2 
             7384  RETURN_VALUE     
           7386_0  COME_FROM          7374  '7374'

 L.3379      7386  LOAD_FAST                'self'
             7388  LOAD_METHOD              flash_switch_bank_process
             7390  LOAD_CONST               1
             7392  LOAD_FAST                'self'
             7394  LOAD_ATTR                _need_shake_hand
             7396  CALL_METHOD_2         2  '2 positional arguments'
             7398  STORE_FAST               'ret'

 L.3380      7400  LOAD_CONST               False
             7402  LOAD_FAST                'self'
             7404  STORE_ATTR               _need_shake_hand

 L.3381      7406  LOAD_FAST                'ret'
             7408  LOAD_CONST               False
             7410  COMPARE_OP               is
         7412_7414  POP_JUMP_IF_FALSE  7424  'to 7424'

 L.3382      7416  LOAD_CONST               False
             7418  LOAD_FAST                'flash_burn_retry'
             7420  BUILD_TUPLE_2         2 
             7422  RETURN_VALUE     
           7424_0  COME_FROM          7412  '7412'

 L.3383      7424  LOAD_FAST                'self'
             7426  LOAD_METHOD              flash_cfg_option
             7428  LOAD_FAST                'read_flash2_id'
             7430  LOAD_FAST                'flash2_para_file'
             7432  LOAD_FAST                'flash2_set'
             7434  LOAD_FAST                'id2_valid_flag'
             7436  LOAD_FAST                'flash_file'
             7438  LOAD_FAST                'i'
             7440  BINARY_SUBSCR    

 L.3384      7442  LOAD_FAST                'config_file'
             7444  LOAD_FAST                'cfg'
             7446  LOAD_FAST                'create_img_callback'
             7448  LOAD_FAST                'create_simple_callback'
             7450  CALL_METHOD_9         9  '9 positional arguments'
             7452  STORE_FAST               'ret'

 L.3385      7454  LOAD_FAST                'ret'
             7456  LOAD_CONST               False
             7458  COMPARE_OP               is
         7460_7462  POP_JUMP_IF_FALSE  7472  'to 7472'

 L.3386      7464  LOAD_CONST               False
             7466  LOAD_FAST                'flash_burn_retry'
             7468  BUILD_TUPLE_2         2 
             7470  RETURN_VALUE     
           7472_0  COME_FROM          7460  '7460'

 L.3387      7472  LOAD_GLOBAL              bflb_utils
             7474  LOAD_METHOD              printf

 L.3388      7476  LOAD_STR                 '========= programming '
             7478  LOAD_GLOBAL              convert_path
             7480  LOAD_FAST                'flash2_bin'
             7482  CALL_FUNCTION_1       1  '1 positional argument'

 L.3389      7484  LOAD_STR                 ' to 0x%08X'
             7486  LOAD_GLOBAL              int
             7488  LOAD_FAST                'address'
             7490  LOAD_FAST                'i'
             7492  BINARY_SUBSCR    
             7494  LOAD_CONST               16
             7496  CALL_FUNCTION_2       2  '2 positional arguments'
             7498  LOAD_FAST                'flash1_bin_len'
             7500  BINARY_ADD       
             7502  BINARY_MODULO    
             7504  CALL_METHOD_3         3  '3 positional arguments'
             7506  POP_TOP          

 L.3390      7508  LOAD_FAST                'self'
             7510  LOAD_METHOD              flash_load_specified

 L.3391      7512  LOAD_GLOBAL              convert_path
             7514  LOAD_FAST                'flash2_bin'
             7516  CALL_FUNCTION_1       1  '1 positional argument'

 L.3392      7518  LOAD_GLOBAL              int
             7520  LOAD_FAST                'address'
             7522  LOAD_FAST                'i'
             7524  BINARY_SUBSCR    
             7526  LOAD_CONST               16
             7528  CALL_FUNCTION_2       2  '2 positional arguments'
             7530  LOAD_FAST                'flash1_bin_len'
             7532  BINARY_ADD       
             7534  LOAD_FAST                'erase'
             7536  LOAD_FAST                'verify'

 L.3393      7538  LOAD_FAST                'self'
             7540  LOAD_ATTR                _need_shake_hand
             7542  LOAD_FAST                'callback'
             7544  CALL_METHOD_6         6  '6 positional arguments'
             7546  STORE_FAST               'ret'

 L.3394      7548  LOAD_FAST                'ret'
             7550  LOAD_CONST               False
             7552  COMPARE_OP               is
         7554_7556  POP_JUMP_IF_FALSE  7844  'to 7844'

 L.3395      7558  LOAD_CONST               False
             7560  LOAD_FAST                'flash_burn_retry'
             7562  BUILD_TUPLE_2         2 
             7564  RETURN_VALUE     
         7566_7568  JUMP_FORWARD       7844  'to 7844'
           7570_0  COME_FROM          7252  '7252'
           7570_1  COME_FROM          7242  '7242'

 L.3397      7570  LOAD_FAST                'self'
             7572  LOAD_ATTR                _flash2_en
             7574  LOAD_CONST               False
             7576  COMPARE_OP               is
         7578_7580  POP_JUMP_IF_TRUE   7616  'to 7616'

 L.3398      7582  LOAD_FAST                'self'
             7584  LOAD_ATTR                _flash2_select
             7586  LOAD_CONST               False
             7588  COMPARE_OP               is
         7590_7592  POP_JUMP_IF_FALSE  7666  'to 7666'

 L.3399      7594  LOAD_GLOBAL              int
             7596  LOAD_FAST                'address'
             7598  LOAD_FAST                'i'
             7600  BINARY_SUBSCR    
             7602  LOAD_CONST               16
             7604  CALL_FUNCTION_2       2  '2 positional arguments'
             7606  LOAD_FAST                'self'
             7608  LOAD_ATTR                _flash1_size
             7610  COMPARE_OP               <
         7612_7614  POP_JUMP_IF_FALSE  7666  'to 7666'
           7616_0  COME_FROM          7578  '7578'

 L.3400      7616  LOAD_FAST                'self'
             7618  LOAD_METHOD              flash_cfg_option
             7620  LOAD_FAST                'read_flash_id'
             7622  LOAD_FAST                'flash_para_file'
             7624  LOAD_FAST                'flash_set'
             7626  LOAD_FAST                'id_valid_flag'
             7628  LOAD_FAST                'flash_file'
             7630  LOAD_FAST                'i'
             7632  BINARY_SUBSCR    

 L.3401      7634  LOAD_FAST                'config_file'
             7636  LOAD_FAST                'cfg'
             7638  LOAD_FAST                'create_img_callback'
             7640  LOAD_FAST                'create_simple_callback'
             7642  CALL_METHOD_9         9  '9 positional arguments'
             7644  STORE_FAST               'ret'

 L.3402      7646  LOAD_FAST                'ret'
             7648  LOAD_CONST               False
             7650  COMPARE_OP               is
         7652_7654  POP_JUMP_IF_FALSE  7786  'to 7786'

 L.3403      7656  LOAD_CONST               False
             7658  LOAD_FAST                'flash_burn_retry'
             7660  BUILD_TUPLE_2         2 
             7662  RETURN_VALUE     
             7664  JUMP_FORWARD       7786  'to 7786'
           7666_0  COME_FROM          7612  '7612'
           7666_1  COME_FROM          7590  '7590'

 L.3405      7666  LOAD_FAST                'self'
             7668  LOAD_ATTR                _flash2_select
             7670  LOAD_CONST               False
             7672  COMPARE_OP               is
         7674_7676  POP_JUMP_IF_FALSE  7738  'to 7738'
             7678  LOAD_GLOBAL              int

 L.3406      7680  LOAD_FAST                'address'
             7682  LOAD_FAST                'i'
             7684  BINARY_SUBSCR    
             7686  LOAD_CONST               16
             7688  CALL_FUNCTION_2       2  '2 positional arguments'
             7690  LOAD_FAST                'self'
             7692  LOAD_ATTR                _flash1_size
             7694  COMPARE_OP               >=
         7696_7698  POP_JUMP_IF_FALSE  7738  'to 7738'

 L.3407      7700  LOAD_FAST                'self'
             7702  LOAD_METHOD              flash_switch_bank_process

 L.3408      7704  LOAD_CONST               1
             7706  LOAD_FAST                'self'
             7708  LOAD_ATTR                _need_shake_hand
             7710  CALL_METHOD_2         2  '2 positional arguments'
             7712  STORE_FAST               'ret'

 L.3409      7714  LOAD_CONST               False
             7716  LOAD_FAST                'self'
             7718  STORE_ATTR               _need_shake_hand

 L.3410      7720  LOAD_FAST                'ret'
             7722  LOAD_CONST               False
             7724  COMPARE_OP               is
         7726_7728  POP_JUMP_IF_FALSE  7738  'to 7738'

 L.3411      7730  LOAD_CONST               False
             7732  LOAD_FAST                'flash_burn_retry'
             7734  BUILD_TUPLE_2         2 
             7736  RETURN_VALUE     
           7738_0  COME_FROM          7726  '7726'
           7738_1  COME_FROM          7696  '7696'
           7738_2  COME_FROM          7674  '7674'

 L.3412      7738  LOAD_FAST                'self'
             7740  LOAD_METHOD              flash_cfg_option
             7742  LOAD_FAST                'read_flash2_id'
             7744  LOAD_FAST                'flash2_para_file'
             7746  LOAD_FAST                'flash2_set'
             7748  LOAD_FAST                'id2_valid_flag'
             7750  LOAD_FAST                'flash_file'
             7752  LOAD_FAST                'i'
             7754  BINARY_SUBSCR    

 L.3413      7756  LOAD_FAST                'config_file'
             7758  LOAD_FAST                'cfg'
             7760  LOAD_FAST                'create_img_callback'
             7762  LOAD_FAST                'create_simple_callback'
             7764  CALL_METHOD_9         9  '9 positional arguments'
             7766  STORE_FAST               'ret'

 L.3414      7768  LOAD_FAST                'ret'
             7770  LOAD_CONST               False
             7772  COMPARE_OP               is
         7774_7776  POP_JUMP_IF_FALSE  7786  'to 7786'

 L.3415      7778  LOAD_CONST               False
             7780  LOAD_FAST                'flash_burn_retry'
             7782  BUILD_TUPLE_2         2 
             7784  RETURN_VALUE     
           7786_0  COME_FROM          7774  '7774'
           7786_1  COME_FROM          7664  '7664'
           7786_2  COME_FROM          7652  '7652'

 L.3416      7786  LOAD_FAST                'self'
             7788  LOAD_METHOD              flash_load_specified
             7790  LOAD_GLOBAL              convert_path
             7792  LOAD_FAST                'flash_file'
             7794  LOAD_FAST                'i'
             7796  BINARY_SUBSCR    
             7798  CALL_FUNCTION_1       1  '1 positional argument'

 L.3417      7800  LOAD_GLOBAL              int
             7802  LOAD_FAST                'address'
             7804  LOAD_FAST                'i'
             7806  BINARY_SUBSCR    
             7808  LOAD_CONST               16
             7810  CALL_FUNCTION_2       2  '2 positional arguments'
             7812  LOAD_FAST                'erase'

 L.3418      7814  LOAD_FAST                'verify'
             7816  LOAD_FAST                'self'
             7818  LOAD_ATTR                _need_shake_hand

 L.3419      7820  LOAD_FAST                'callback'
             7822  CALL_METHOD_6         6  '6 positional arguments'
             7824  STORE_FAST               'ret'

 L.3420      7826  LOAD_FAST                'ret'
             7828  LOAD_CONST               False
             7830  COMPARE_OP               is
         7832_7834  POP_JUMP_IF_FALSE  7844  'to 7844'

 L.3421      7836  LOAD_CONST               False
             7838  LOAD_FAST                'flash_burn_retry'
             7840  BUILD_TUPLE_2         2 
             7842  RETURN_VALUE     
           7844_0  COME_FROM          7832  '7832'
           7844_1  COME_FROM          7566  '7566'
           7844_2  COME_FROM          7554  '7554'

 L.3422      7844  LOAD_FAST                'size_before'
             7846  LOAD_GLOBAL              os
             7848  LOAD_ATTR                path
             7850  LOAD_METHOD              getsize

 L.3423      7852  LOAD_GLOBAL              os
             7854  LOAD_ATTR                path
             7856  LOAD_METHOD              join
             7858  LOAD_GLOBAL              app_path
             7860  LOAD_GLOBAL              convert_path
             7862  LOAD_FAST                'flash_file'
             7864  LOAD_FAST                'i'
             7866  BINARY_SUBSCR    
             7868  CALL_FUNCTION_1       1  '1 positional argument'
             7870  CALL_METHOD_2         2  '2 positional arguments'
             7872  CALL_METHOD_1         1  '1 positional argument'
             7874  INPLACE_ADD      
             7876  STORE_FAST               'size_before'

 L.3424      7878  LOAD_FAST                'i'
             7880  LOAD_CONST               1
             7882  INPLACE_ADD      
             7884  STORE_FAST               'i'

 L.3425      7886  LOAD_FAST                'callback'
         7888_7890  POP_JUMP_IF_FALSE  7908  'to 7908'

 L.3426      7892  LOAD_FAST                'callback'
             7894  LOAD_FAST                'i'
             7896  LOAD_GLOBAL              len
             7898  LOAD_FAST                'flash_file'
             7900  CALL_FUNCTION_1       1  '1 positional argument'
             7902  LOAD_STR                 'program'
             7904  CALL_FUNCTION_3       3  '3 positional arguments'
             7906  POP_TOP          
           7908_0  COME_FROM          7888  '7888'

 L.3427      7908  LOAD_CONST               False
             7910  LOAD_FAST                'self'
             7912  STORE_ATTR               _need_shake_hand
         7914_7916  JUMP_BACK          6824  'to 6824'
           7918_0  COME_FROM          6834  '6834'
             7918  POP_BLOCK        
           7920_0  COME_FROM_LOOP     6820  '6820'

 L.3428      7920  LOAD_FAST                'self'
             7922  LOAD_ATTR                _flash2_select
             7924  LOAD_CONST               True
             7926  COMPARE_OP               is
         7928_7930  POP_JUMP_IF_FALSE  7970  'to 7970'

 L.3429      7932  LOAD_FAST                'self'
             7934  LOAD_METHOD              flash_switch_bank_process
             7936  LOAD_CONST               0
             7938  LOAD_FAST                'self'
             7940  LOAD_ATTR                _need_shake_hand
             7942  CALL_METHOD_2         2  '2 positional arguments'
             7944  STORE_FAST               'ret'

 L.3430      7946  LOAD_CONST               False
             7948  LOAD_FAST                'self'
             7950  STORE_ATTR               _need_shake_hand

 L.3431      7952  LOAD_FAST                'ret'
             7954  LOAD_CONST               False
             7956  COMPARE_OP               is
         7958_7960  POP_JUMP_IF_FALSE  7970  'to 7970'

 L.3432      7962  LOAD_CONST               False
             7964  LOAD_FAST                'flash_burn_retry'
             7966  BUILD_TUPLE_2         2 
             7968  RETURN_VALUE     
           7970_0  COME_FROM          7958  '7958'
           7970_1  COME_FROM          7928  '7928'

 L.3433      7970  LOAD_GLOBAL              bflb_utils
             7972  LOAD_METHOD              printf
             7974  LOAD_STR                 'Program Finished'
             7976  CALL_METHOD_1         1  '1 positional argument'
             7978  POP_TOP          
             7980  POP_BLOCK        
             7982  JUMP_FORWARD       8050  'to 8050'
           7984_0  COME_FROM_EXCEPT   6812  '6812'

 L.3434      7984  DUP_TOP          
             7986  LOAD_GLOBAL              Exception
             7988  COMPARE_OP               exception-match
         7990_7992  POP_JUMP_IF_FALSE  8048  'to 8048'
             7994  POP_TOP          
             7996  STORE_FAST               'e'
             7998  POP_TOP          
             8000  SETUP_FINALLY      8036  'to 8036'

 L.3435      8002  LOAD_GLOBAL              bflb_utils
             8004  LOAD_METHOD              printf
             8006  LOAD_FAST                'e'
             8008  CALL_METHOD_1         1  '1 positional argument'
             8010  POP_TOP          

 L.3436      8012  LOAD_GLOBAL              traceback
             8014  LOAD_ATTR                print_exc
             8016  LOAD_GLOBAL              NUM_ERR
             8018  LOAD_GLOBAL              sys
             8020  LOAD_ATTR                stdout
             8022  LOAD_CONST               ('limit', 'file')
             8024  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             8026  POP_TOP          

 L.3437      8028  LOAD_CONST               False
             8030  LOAD_FAST                'flash_burn_retry'
             8032  BUILD_TUPLE_2         2 
             8034  RETURN_VALUE     
           8036_0  COME_FROM_FINALLY  8000  '8000'
             8036  LOAD_CONST               None
             8038  STORE_FAST               'e'
             8040  DELETE_FAST              'e'
             8042  END_FINALLY      
             8044  POP_EXCEPT       
             8046  JUMP_FORWARD       8050  'to 8050'
           8048_0  COME_FROM          7990  '7990'
             8048  END_FINALLY      
           8050_0  COME_FROM          8046  '8046'
           8050_1  COME_FROM          7982  '7982'
             8050  JUMP_FORWARD       8062  'to 8062'
           8052_0  COME_FROM          6680  '6680'

 L.3439      8052  LOAD_GLOBAL              bflb_utils
             8054  LOAD_METHOD              printf
             8056  LOAD_STR                 'No input file to program to flash'
             8058  CALL_METHOD_1         1  '1 positional argument'
             8060  POP_TOP          
           8062_0  COME_FROM          8050  '8050'
           8062_1  COME_FROM          6414  '6414'
           8062_2  COME_FROM          6260  '6260'
           8062_3  COME_FROM          6120  '6120'
           8062_4  COME_FROM          5906  '5906'

 L.3441      8062  LOAD_FAST                'args'
             8064  LOAD_ATTR                efuse
         8066_8068  POP_JUMP_IF_FALSE  8968  'to 8968'

 L.3442      8070  LOAD_CONST               True
             8072  STORE_FAST               'loadflag'

 L.3443      8074  LOAD_FAST                'macaddr'
         8076_8078  POP_JUMP_IF_FALSE  8208  'to 8208'

 L.3445      8080  LOAD_GLOBAL              bflb_utils
             8082  LOAD_METHOD              printf
             8084  LOAD_STR                 'write efuse macaddr '
             8086  LOAD_FAST                'macaddr'
             8088  CALL_METHOD_2         2  '2 positional arguments'
             8090  POP_TOP          

 L.3446      8092  LOAD_FAST                'cfg'
             8094  LOAD_METHOD              get
             8096  LOAD_STR                 'EFUSE_CFG'
             8098  LOAD_STR                 'security_write'
             8100  CALL_METHOD_2         2  '2 positional arguments'
             8102  LOAD_STR                 'true'
             8104  COMPARE_OP               ==
             8106  STORE_FAST               'security_write'

 L.3447      8108  LOAD_FAST                'self'
             8110  LOAD_ATTR                _chip_type
             8112  LOAD_STR                 'bl702'
             8114  COMPARE_OP               ==
         8116_8118  POP_JUMP_IF_TRUE   8132  'to 8132'
             8120  LOAD_FAST                'self'
             8122  LOAD_ATTR                _chip_type
             8124  LOAD_STR                 'bl702l'
             8126  COMPARE_OP               ==
         8128_8130  POP_JUMP_IF_FALSE  8154  'to 8154'
           8132_0  COME_FROM          8116  '8116'

 L.3448      8132  LOAD_FAST                'self'
             8134  LOAD_ATTR                efuse_load_702_macaddr
             8136  LOAD_FAST                'macaddr'

 L.3449      8138  LOAD_CONST               1

 L.3450      8140  LOAD_FAST                'self'
             8142  LOAD_ATTR                _need_shake_hand

 L.3451      8144  LOAD_FAST                'security_write'
             8146  LOAD_CONST               ('verify', 'shakehand', 'security_write')
             8148  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             8150  STORE_FAST               'ret'
             8152  JUMP_FORWARD       8174  'to 8174'
           8154_0  COME_FROM          8128  '8128'

 L.3453      8154  LOAD_FAST                'self'
             8156  LOAD_ATTR                efuse_load_macaddr
             8158  LOAD_FAST                'macaddr'

 L.3454      8160  LOAD_CONST               1

 L.3455      8162  LOAD_FAST                'self'
             8164  LOAD_ATTR                _need_shake_hand

 L.3456      8166  LOAD_FAST                'security_write'
             8168  LOAD_CONST               ('verify', 'shakehand', 'security_write')
             8170  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             8172  STORE_FAST               'ret'
           8174_0  COME_FROM          8152  '8152'

 L.3457      8174  LOAD_FAST                'ret'
             8176  LOAD_CONST               False
             8178  COMPARE_OP               is
         8180_8182  POP_JUMP_IF_FALSE  8202  'to 8202'

 L.3458      8184  LOAD_GLOBAL              bflb_utils
             8186  LOAD_METHOD              printf
             8188  LOAD_STR                 'load macaddr fail'
             8190  CALL_METHOD_1         1  '1 positional argument'
             8192  POP_TOP          

 L.3459      8194  LOAD_CONST               False
             8196  LOAD_FAST                'flash_burn_retry'
             8198  BUILD_TUPLE_2         2 
             8200  RETURN_VALUE     
           8202_0  COME_FROM          8180  '8180'

 L.3460      8202  LOAD_CONST               False
             8204  LOAD_FAST                'self'
             8206  STORE_ATTR               _need_shake_hand
           8208_0  COME_FROM          8076  '8076'

 L.3461      8208  LOAD_FAST                'aeskey'
         8210_8212  POP_JUMP_IF_FALSE  8282  'to 8282'

 L.3462      8214  LOAD_CONST               False
             8216  STORE_FAST               'loadflag'

 L.3463      8218  LOAD_GLOBAL              bflb_utils
             8220  LOAD_METHOD              printf
             8222  LOAD_STR                 'write efuse aes key '
             8224  LOAD_FAST                'aeskey'
             8226  CALL_METHOD_2         2  '2 positional arguments'
             8228  POP_TOP          

 L.3464      8230  LOAD_FAST                'self'
             8232  LOAD_ATTR                efuse_load_aes_key
             8234  LOAD_STR                 'flash_aes_key'
             8236  LOAD_FAST                'aeskey'
             8238  LOAD_STR                 ''
             8240  BUILD_LIST_2          2 

 L.3465      8242  LOAD_CONST               1

 L.3466      8244  LOAD_FAST                'self'
             8246  LOAD_ATTR                _need_shake_hand
             8248  LOAD_CONST               ('verify', 'shakehand')
             8250  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             8252  STORE_FAST               'ret'

 L.3467      8254  LOAD_FAST                'ret'
             8256  LOAD_CONST               False
             8258  COMPARE_OP               is
         8260_8262  POP_JUMP_IF_FALSE  8282  'to 8282'

 L.3468      8264  LOAD_GLOBAL              bflb_utils
             8266  LOAD_METHOD              printf
             8268  LOAD_STR                 'load aes key fail'
             8270  CALL_METHOD_1         1  '1 positional argument'
             8272  POP_TOP          

 L.3469      8274  LOAD_CONST               False
             8276  LOAD_FAST                'flash_burn_retry'
             8278  BUILD_TUPLE_2         2 
             8280  RETURN_VALUE     
           8282_0  COME_FROM          8260  '8260'
           8282_1  COME_FROM          8210  '8210'

 L.3470      8282  LOAD_FAST                'load_data'
         8284_8286  POP_JUMP_IF_FALSE  8380  'to 8380'
             8288  LOAD_FAST                'address'
         8290_8292  POP_JUMP_IF_FALSE  8380  'to 8380'

 L.3471      8294  LOAD_CONST               False
             8296  STORE_FAST               'loadflag'

 L.3472      8298  LOAD_GLOBAL              bflb_utils
             8300  LOAD_METHOD              printf
             8302  LOAD_STR                 'write efuse data '
             8304  LOAD_FAST                'load_data'
             8306  LOAD_STR                 ' to '
             8308  LOAD_FAST                'address'
             8310  CALL_METHOD_4         4  '4 positional arguments'
             8312  POP_TOP          

 L.3473      8314  LOAD_FAST                'cfg'
             8316  LOAD_METHOD              get
             8318  LOAD_STR                 'EFUSE_CFG'
             8320  LOAD_STR                 'security_write'
             8322  CALL_METHOD_2         2  '2 positional arguments'
             8324  LOAD_STR                 'true'
             8326  COMPARE_OP               ==
             8328  STORE_FAST               'security_write'

 L.3474      8330  LOAD_FAST                'self'
             8332  LOAD_METHOD              efuse_load_data_process
             8334  LOAD_FAST                'load_data'
             8336  LOAD_FAST                'address'
             8338  LOAD_FAST                'efuse_load_func'
             8340  LOAD_FAST                'verify'

 L.3475      8342  LOAD_FAST                'self'
             8344  LOAD_ATTR                _need_shake_hand
             8346  LOAD_FAST                'security_write'
             8348  CALL_METHOD_6         6  '6 positional arguments'
             8350  STORE_FAST               'ret'

 L.3476      8352  LOAD_FAST                'ret'
             8354  LOAD_CONST               False
             8356  COMPARE_OP               is
         8358_8360  POP_JUMP_IF_FALSE  8380  'to 8380'

 L.3477      8362  LOAD_GLOBAL              bflb_utils
             8364  LOAD_METHOD              printf
             8366  LOAD_STR                 'write efuse data fail'
             8368  CALL_METHOD_1         1  '1 positional argument'
             8370  POP_TOP          

 L.3478      8372  LOAD_CONST               False
             8374  LOAD_FAST                'flash_burn_retry'
             8376  BUILD_TUPLE_2         2 
             8378  RETURN_VALUE     
           8380_0  COME_FROM          8358  '8358'
           8380_1  COME_FROM          8290  '8290'
           8380_2  COME_FROM          8284  '8284'

 L.3479      8380  LOAD_FAST                'efuse_para'
         8382_8384  POP_JUMP_IF_FALSE  8674  'to 8674'

 L.3480      8386  LOAD_CONST               False
             8388  STORE_FAST               'loadflag'

 L.3481      8390  LOAD_GLOBAL              bflb_utils
             8392  LOAD_METHOD              printf
             8394  LOAD_STR                 'write efuse para'
             8396  CALL_METHOD_1         1  '1 positional argument'
             8398  POP_TOP          

 L.3483      8400  LOAD_STR                 'chips/'
             8402  LOAD_FAST                'self'
             8404  LOAD_ATTR                _chip_name
             8406  LOAD_METHOD              lower
             8408  CALL_METHOD_0         0  '0 positional arguments'
             8410  BINARY_ADD       
             8412  LOAD_STR                 '/img_create_iot/efuse_bootheader_cfg.ini'
             8414  BINARY_ADD       
             8416  STORE_FAST               'cfgfile'

 L.3484      8418  LOAD_GLOBAL              os
             8420  LOAD_ATTR                path
             8422  LOAD_METHOD              isfile
             8424  LOAD_FAST                'cfgfile'
             8426  CALL_METHOD_1         1  '1 positional argument'
             8428  LOAD_CONST               False
             8430  COMPARE_OP               is
         8432_8434  POP_JUMP_IF_FALSE  8462  'to 8462'

 L.3485      8436  LOAD_GLOBAL              shutil
             8438  LOAD_METHOD              copyfile

 L.3486      8440  LOAD_STR                 'chips/'
             8442  LOAD_FAST                'self'
             8444  LOAD_ATTR                _chip_name
             8446  LOAD_METHOD              lower
             8448  CALL_METHOD_0         0  '0 positional arguments'
             8450  BINARY_ADD       

 L.3487      8452  LOAD_STR                 '/efuse_bootheader/efuse_bootheader_cfg.conf'
             8454  BINARY_ADD       
             8456  LOAD_FAST                'cfgfile'
             8458  CALL_METHOD_2         2  '2 positional arguments'
             8460  POP_TOP          
           8462_0  COME_FROM          8432  '8432'

 L.3488      8462  LOAD_GLOBAL              __import__
             8464  LOAD_STR                 'libs.'
             8466  LOAD_FAST                'self'
             8468  LOAD_ATTR                _chip_type
             8470  BINARY_ADD       
             8472  LOAD_FAST                'self'
             8474  LOAD_ATTR                _chip_type
             8476  BUILD_LIST_1          1 
             8478  LOAD_CONST               ('fromlist',)
             8480  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             8482  STORE_FAST               'sub_module'

 L.3489      8484  LOAD_GLOBAL              bflb_efuse_boothd_create
             8486  LOAD_METHOD              update_data_from_cfg

 L.3490      8488  LOAD_FAST                'sub_module'
             8490  LOAD_ATTR                efuse_cfg_keys
             8492  LOAD_ATTR                efuse_cfg_keys
             8494  LOAD_FAST                'cfgfile'
             8496  LOAD_STR                 'EFUSE_CFG'
             8498  CALL_METHOD_3         3  '3 positional arguments'
             8500  UNPACK_SEQUENCE_2     2 
             8502  STORE_FAST               'efuse_data'
             8504  STORE_FAST               'mask'

 L.3491      8506  LOAD_CONST               True
             8508  STORE_FAST               'efuse_load'

 L.3492      8510  LOAD_CONST               1
             8512  STORE_FAST               'efuse_verify'

 L.3493      8514  LOAD_FAST                'cfg'
             8516  LOAD_METHOD              has_option
             8518  LOAD_STR                 'EFUSE_CFG'
             8520  LOAD_STR                 'burn_en'
             8522  CALL_METHOD_2         2  '2 positional arguments'
         8524_8526  POP_JUMP_IF_FALSE  8544  'to 8544'

 L.3494      8528  LOAD_FAST                'cfg'
             8530  LOAD_METHOD              get
             8532  LOAD_STR                 'EFUSE_CFG'
             8534  LOAD_STR                 'burn_en'
             8536  CALL_METHOD_2         2  '2 positional arguments'
             8538  LOAD_STR                 'true'
             8540  COMPARE_OP               ==
             8542  STORE_FAST               'efuse_load'
           8544_0  COME_FROM          8524  '8524'

 L.3495      8544  LOAD_FAST                'cfg'
             8546  LOAD_METHOD              has_option
             8548  LOAD_STR                 'EFUSE_CFG'
             8550  LOAD_STR                 'factory_mode'
             8552  CALL_METHOD_2         2  '2 positional arguments'
         8554_8556  POP_JUMP_IF_FALSE  8580  'to 8580'

 L.3496      8558  LOAD_FAST                'cfg'
             8560  LOAD_METHOD              get
             8562  LOAD_STR                 'EFUSE_CFG'
             8564  LOAD_STR                 'factory_mode'
             8566  CALL_METHOD_2         2  '2 positional arguments'
             8568  LOAD_STR                 'true'
             8570  COMPARE_OP               !=
         8572_8574  POP_JUMP_IF_FALSE  8580  'to 8580'

 L.3497      8576  LOAD_CONST               0
             8578  STORE_FAST               'efuse_verify'
           8580_0  COME_FROM          8572  '8572'
           8580_1  COME_FROM          8554  '8554'

 L.3498      8580  LOAD_FAST                'cfg'
             8582  LOAD_METHOD              get
             8584  LOAD_STR                 'EFUSE_CFG'
             8586  LOAD_STR                 'security_write'
             8588  CALL_METHOD_2         2  '2 positional arguments'
             8590  LOAD_STR                 'true'
             8592  COMPARE_OP               ==
             8594  STORE_FAST               'security_write'

 L.3499      8596  LOAD_FAST                'efuse_load'
         8598_8600  POP_JUMP_IF_FALSE  8664  'to 8664'

 L.3500      8602  LOAD_FAST                'self'
             8604  LOAD_METHOD              efuse_load_specified
             8606  LOAD_CONST               None
             8608  LOAD_CONST               None
             8610  LOAD_FAST                'efuse_data'
             8612  LOAD_FAST                'mask'
             8614  LOAD_FAST                'efuse_verify'

 L.3501      8616  LOAD_FAST                'self'
             8618  LOAD_ATTR                _need_shake_hand
             8620  LOAD_FAST                'security_write'
             8622  CALL_METHOD_7         7  '7 positional arguments'
             8624  STORE_FAST               'ret'

 L.3502      8626  LOAD_FAST                'callback'
         8628_8630  POP_JUMP_IF_FALSE  8644  'to 8644'

 L.3503      8632  LOAD_FAST                'callback'
             8634  LOAD_CONST               1
             8636  LOAD_CONST               1
             8638  LOAD_STR                 'APP_WR'
             8640  CALL_FUNCTION_3       3  '3 positional arguments'
             8642  POP_TOP          
           8644_0  COME_FROM          8628  '8628'

 L.3504      8644  LOAD_FAST                'ret'
             8646  LOAD_CONST               False
             8648  COMPARE_OP               is
         8650_8652  POP_JUMP_IF_FALSE  8674  'to 8674'

 L.3505      8654  LOAD_CONST               False
             8656  LOAD_FAST                'flash_burn_retry'
             8658  BUILD_TUPLE_2         2 
             8660  RETURN_VALUE     
             8662  JUMP_FORWARD       8674  'to 8674'
           8664_0  COME_FROM          8598  '8598'

 L.3507      8664  LOAD_GLOBAL              bflb_utils
             8666  LOAD_METHOD              printf
             8668  LOAD_STR                 'efuse load disalbe'
             8670  CALL_METHOD_1         1  '1 positional argument'
             8672  POP_TOP          
           8674_0  COME_FROM          8662  '8662'
           8674_1  COME_FROM          8650  '8650'
           8674_2  COME_FROM          8382  '8382'

 L.3508      8674  LOAD_FAST                'loadflag'
             8676  LOAD_CONST               True
             8678  COMPARE_OP               is
         8680_8682  POP_JUMP_IF_FALSE  8962  'to 8962'

 L.3509      8684  LOAD_FAST                'efusefile'
         8686_8688  POP_JUMP_IF_FALSE  8708  'to 8708'

 L.3510      8690  LOAD_FAST                'efusefile'
             8692  STORE_FAST               'efuse_file'

 L.3511      8694  LOAD_FAST                'efuse_file'
             8696  LOAD_METHOD              replace
             8698  LOAD_STR                 '.bin'
             8700  LOAD_STR                 '_mask.bin'
             8702  CALL_METHOD_2         2  '2 positional arguments'
             8704  STORE_FAST               'mask_file'
             8706  JUMP_FORWARD       8732  'to 8732'
           8708_0  COME_FROM          8686  '8686'

 L.3513      8708  LOAD_FAST                'cfg'
             8710  LOAD_METHOD              get
             8712  LOAD_STR                 'EFUSE_CFG'
             8714  LOAD_STR                 'file'
             8716  CALL_METHOD_2         2  '2 positional arguments'
             8718  STORE_FAST               'efuse_file'

 L.3514      8720  LOAD_FAST                'cfg'
             8722  LOAD_METHOD              get
             8724  LOAD_STR                 'EFUSE_CFG'
             8726  LOAD_STR                 'maskfile'
             8728  CALL_METHOD_2         2  '2 positional arguments'
             8730  STORE_FAST               'mask_file'
           8732_0  COME_FROM          8706  '8706'

 L.3515      8732  LOAD_FAST                'task_num'
             8734  LOAD_CONST               None
             8736  COMPARE_OP               !=
         8738_8740  POP_JUMP_IF_FALSE  8774  'to 8774'
             8742  LOAD_FAST                'self'
             8744  LOAD_ATTR                _csv_burn_en
             8746  LOAD_CONST               True
             8748  COMPARE_OP               is
         8750_8752  POP_JUMP_IF_FALSE  8774  'to 8774'

 L.3516      8754  LOAD_STR                 'task'
             8756  LOAD_GLOBAL              str
             8758  LOAD_FAST                'task_num'
             8760  CALL_FUNCTION_1       1  '1 positional argument'
             8762  BINARY_ADD       
             8764  LOAD_STR                 '/'
             8766  BINARY_ADD       
             8768  LOAD_FAST                'efuse_file'
             8770  BINARY_ADD       
             8772  STORE_FAST               'efuse_file'
           8774_0  COME_FROM          8750  '8750'
           8774_1  COME_FROM          8738  '8738'

 L.3517      8774  LOAD_CONST               True
             8776  STORE_FAST               'efuse_load'

 L.3518      8778  LOAD_CONST               1
             8780  STORE_FAST               'efuse_verify'

 L.3519      8782  LOAD_FAST                'cfg'
             8784  LOAD_METHOD              has_option
             8786  LOAD_STR                 'EFUSE_CFG'
             8788  LOAD_STR                 'burn_en'
             8790  CALL_METHOD_2         2  '2 positional arguments'
         8792_8794  POP_JUMP_IF_FALSE  8812  'to 8812'

 L.3520      8796  LOAD_FAST                'cfg'
             8798  LOAD_METHOD              get
             8800  LOAD_STR                 'EFUSE_CFG'
             8802  LOAD_STR                 'burn_en'
             8804  CALL_METHOD_2         2  '2 positional arguments'
             8806  LOAD_STR                 'true'
             8808  COMPARE_OP               ==
             8810  STORE_FAST               'efuse_load'
           8812_0  COME_FROM          8792  '8792'

 L.3521      8812  LOAD_FAST                'cfg'
             8814  LOAD_METHOD              has_option
             8816  LOAD_STR                 'EFUSE_CFG'
             8818  LOAD_STR                 'factory_mode'
             8820  CALL_METHOD_2         2  '2 positional arguments'
         8822_8824  POP_JUMP_IF_FALSE  8848  'to 8848'

 L.3522      8826  LOAD_FAST                'cfg'
             8828  LOAD_METHOD              get
             8830  LOAD_STR                 'EFUSE_CFG'
             8832  LOAD_STR                 'factory_mode'
             8834  CALL_METHOD_2         2  '2 positional arguments'
             8836  LOAD_STR                 'true'
             8838  COMPARE_OP               !=
         8840_8842  POP_JUMP_IF_FALSE  8848  'to 8848'

 L.3523      8844  LOAD_CONST               0
             8846  STORE_FAST               'efuse_verify'
           8848_0  COME_FROM          8840  '8840'
           8848_1  COME_FROM          8822  '8822'

 L.3524      8848  LOAD_FAST                'cfg'
             8850  LOAD_METHOD              get
             8852  LOAD_STR                 'EFUSE_CFG'
             8854  LOAD_STR                 'security_write'
             8856  CALL_METHOD_2         2  '2 positional arguments'
             8858  LOAD_STR                 'true'
             8860  COMPARE_OP               ==
             8862  STORE_FAST               'security_write'

 L.3525      8864  LOAD_FAST                'efuse_load'
         8866_8868  POP_JUMP_IF_FALSE  8952  'to 8952'
             8870  LOAD_FAST                'self'
             8872  LOAD_ATTR                _isp_en
             8874  LOAD_CONST               False
             8876  COMPARE_OP               is
         8878_8880  POP_JUMP_IF_FALSE  8952  'to 8952'

 L.3526      8882  LOAD_FAST                'self'
             8884  LOAD_METHOD              efuse_load_specified
             8886  LOAD_FAST                'efuse_file'
             8888  LOAD_FAST                'mask_file'
             8890  LOAD_GLOBAL              bytearray
             8892  LOAD_CONST               0
             8894  CALL_FUNCTION_1       1  '1 positional argument'

 L.3527      8896  LOAD_GLOBAL              bytearray
             8898  LOAD_CONST               0
             8900  CALL_FUNCTION_1       1  '1 positional argument'
             8902  LOAD_FAST                'efuse_verify'

 L.3528      8904  LOAD_FAST                'self'
             8906  LOAD_ATTR                _need_shake_hand
             8908  LOAD_FAST                'security_write'
             8910  CALL_METHOD_7         7  '7 positional arguments'
             8912  STORE_FAST               'ret'

 L.3529      8914  LOAD_FAST                'callback'
         8916_8918  POP_JUMP_IF_FALSE  8932  'to 8932'

 L.3530      8920  LOAD_FAST                'callback'
             8922  LOAD_CONST               1
             8924  LOAD_CONST               1
             8926  LOAD_STR                 'APP_WR'
             8928  CALL_FUNCTION_3       3  '3 positional arguments'
             8930  POP_TOP          
           8932_0  COME_FROM          8916  '8916'

 L.3531      8932  LOAD_FAST                'ret'
             8934  LOAD_CONST               False
             8936  COMPARE_OP               is
         8938_8940  POP_JUMP_IF_FALSE  8962  'to 8962'

 L.3532      8942  LOAD_CONST               False
             8944  LOAD_FAST                'flash_burn_retry'
             8946  BUILD_TUPLE_2         2 
             8948  RETURN_VALUE     
             8950  JUMP_FORWARD       8962  'to 8962'
           8952_0  COME_FROM          8878  '8878'
           8952_1  COME_FROM          8866  '8866'

 L.3534      8952  LOAD_GLOBAL              bflb_utils
             8954  LOAD_METHOD              printf
             8956  LOAD_STR                 'efuse load disalbe'
             8958  CALL_METHOD_1         1  '1 positional argument'
             8960  POP_TOP          
           8962_0  COME_FROM          8950  '8950'
           8962_1  COME_FROM          8938  '8938'
           8962_2  COME_FROM          8680  '8680'

 L.3535      8962  LOAD_CONST               False
             8964  LOAD_FAST                'self'
             8966  STORE_ATTR               _need_shake_hand
           8968_0  COME_FROM          8066  '8066'
           8968_1  COME_FROM          5854  '5854'

 L.3537      8968  LOAD_FAST                'args'
             8970  LOAD_ATTR                read
         8972_8974  POP_JUMP_IF_FALSE  9190  'to 9190'

 L.3538      8976  LOAD_GLOBAL              bflb_utils
             8978  LOAD_METHOD              printf
             8980  LOAD_STR                 'Read operation'
             8982  CALL_METHOD_1         1  '1 positional argument'
             8984  POP_TOP          

 L.3539      8986  LOAD_FAST                'args'
             8988  LOAD_ATTR                flash
         8990_8992  POP_JUMP_IF_TRUE   9020  'to 9020'
             8994  LOAD_FAST                'args'
             8996  LOAD_ATTR                efuse
         8998_9000  POP_JUMP_IF_TRUE   9020  'to 9020'

 L.3540      9002  LOAD_GLOBAL              bflb_utils
             9004  LOAD_METHOD              printf
             9006  LOAD_STR                 'No target select'
             9008  CALL_METHOD_1         1  '1 positional argument'
             9010  POP_TOP          

 L.3541      9012  LOAD_CONST               False
             9014  LOAD_FAST                'flash_burn_retry'
             9016  BUILD_TUPLE_2         2 
             9018  RETURN_VALUE     
           9020_0  COME_FROM          8998  '8998'
           9020_1  COME_FROM          8990  '8990'

 L.3542      9020  LOAD_FAST                'args'
             9022  LOAD_ATTR                flash
         9024_9026  POP_JUMP_IF_FALSE  9122  'to 9122'

 L.3543      9028  LOAD_FAST                'start'
         9030_9032  POP_JUMP_IF_FALSE  9040  'to 9040'
             9034  LOAD_FAST                'end'
         9036_9038  POP_JUMP_IF_TRUE   9052  'to 9052'
           9040_0  COME_FROM          9030  '9030'

 L.3544      9040  LOAD_FAST                'self'
             9042  LOAD_METHOD              flash_read_jedec_id_process
             9044  LOAD_FAST                'callback'
             9046  CALL_METHOD_1         1  '1 positional argument'
             9048  POP_TOP          
             9050  JUMP_FORWARD       9122  'to 9122'
           9052_0  COME_FROM          9036  '9036'

 L.3546      9052  LOAD_GLOBAL              int
             9054  LOAD_FAST                'start'
             9056  LOAD_CONST               16
             9058  CALL_FUNCTION_2       2  '2 positional arguments'
             9060  STORE_FAST               'start_addr'

 L.3547      9062  LOAD_GLOBAL              int
             9064  LOAD_FAST                'end'
             9066  LOAD_CONST               16
             9068  CALL_FUNCTION_2       2  '2 positional arguments'
             9070  STORE_FAST               'end_addr'

 L.3548      9072  LOAD_FAST                'self'
             9074  LOAD_METHOD              flash_read_main_process
             9076  LOAD_FAST                'start_addr'

 L.3549      9078  LOAD_FAST                'end_addr'
             9080  LOAD_FAST                'start_addr'
             9082  BINARY_SUBTRACT  
             9084  LOAD_CONST               1
             9086  BINARY_ADD       

 L.3550      9088  LOAD_FAST                'self'
             9090  LOAD_ATTR                _need_shake_hand
             9092  LOAD_FAST                'file'

 L.3551      9094  LOAD_FAST                'callback'
             9096  CALL_METHOD_5         5  '5 positional arguments'
             9098  UNPACK_SEQUENCE_2     2 
             9100  STORE_FAST               'ret'
             9102  STORE_FAST               'readdata'

 L.3552      9104  LOAD_FAST                'ret'
             9106  LOAD_CONST               False
             9108  COMPARE_OP               is
         9110_9112  POP_JUMP_IF_FALSE  9122  'to 9122'

 L.3553      9114  LOAD_CONST               False
             9116  LOAD_FAST                'flash_burn_retry'
             9118  BUILD_TUPLE_2         2 
             9120  RETURN_VALUE     
           9122_0  COME_FROM          9110  '9110'
           9122_1  COME_FROM          9050  '9050'
           9122_2  COME_FROM          9024  '9024'

 L.3554      9122  LOAD_FAST                'args'
             9124  LOAD_ATTR                efuse
         9126_9128  POP_JUMP_IF_FALSE  9190  'to 9190'

 L.3555      9130  LOAD_GLOBAL              int
             9132  LOAD_FAST                'start'
             9134  LOAD_CONST               16
             9136  CALL_FUNCTION_2       2  '2 positional arguments'
             9138  STORE_FAST               'start_addr'

 L.3556      9140  LOAD_GLOBAL              int
             9142  LOAD_FAST                'end'
             9144  LOAD_CONST               16
             9146  CALL_FUNCTION_2       2  '2 positional arguments'
             9148  STORE_FAST               'end_addr'

 L.3557      9150  LOAD_FAST                'self'
             9152  LOAD_METHOD              efuse_read_main_process
             9154  LOAD_FAST                'start_addr'
             9156  LOAD_FAST                'end_addr'
             9158  LOAD_FAST                'start_addr'
             9160  BINARY_SUBTRACT  
             9162  LOAD_CONST               1
             9164  BINARY_ADD       

 L.3558      9166  LOAD_FAST                'self'
             9168  LOAD_ATTR                _need_shake_hand
             9170  LOAD_FAST                'file'
             9172  CALL_METHOD_4         4  '4 positional arguments'
             9174  LOAD_CONST               False
             9176  COMPARE_OP               is
         9178_9180  POP_JUMP_IF_FALSE  9190  'to 9190'

 L.3559      9182  LOAD_CONST               False
             9184  LOAD_FAST                'flash_burn_retry'
             9186  BUILD_TUPLE_2         2 
             9188  RETURN_VALUE     
           9190_0  COME_FROM          9178  '9178'
           9190_1  COME_FROM          9126  '9126'
           9190_2  COME_FROM          8972  '8972'

 L.3560      9190  LOAD_FAST                'self'
             9192  LOAD_ATTR                _isp_en
             9194  LOAD_CONST               True
             9196  COMPARE_OP               is
         9198_9200  POP_JUMP_IF_FALSE  9234  'to 9234'
             9202  LOAD_FAST                'self'
             9204  LOAD_ATTR                _chip_type
             9206  LOAD_STR                 'bl702'
             9208  COMPARE_OP               ==
         9210_9212  POP_JUMP_IF_TRUE   9226  'to 9226'
             9214  LOAD_FAST                'self'
             9216  LOAD_ATTR                _chip_type
             9218  LOAD_STR                 'bl702l'
             9220  COMPARE_OP               ==
         9222_9224  POP_JUMP_IF_FALSE  9234  'to 9234'
           9226_0  COME_FROM          9210  '9210'

 L.3561      9226  LOAD_FAST                'self'
             9228  LOAD_METHOD              reset_cpu
             9230  CALL_METHOD_0         0  '0 positional arguments'
             9232  POP_TOP          
           9234_0  COME_FROM          9222  '9222'
           9234_1  COME_FROM          9198  '9198'

 L.3562      9234  LOAD_FAST                'macaddr_check'
             9236  LOAD_CONST               True
             9238  COMPARE_OP               is
         9240_9242  POP_JUMP_IF_FALSE  9250  'to 9250'

 L.3563      9244  LOAD_FAST                'bootinfo'
             9246  LOAD_FAST                'self'
             9248  STORE_ATTR               _bootinfo
           9250_0  COME_FROM          9240  '9240'

 L.3564      9250  LOAD_FAST                'mac_addr'
             9252  LOAD_FAST                'self'
             9254  STORE_ATTR               _macaddr_check

 L.3565      9256  LOAD_CONST               False
             9258  LOAD_FAST                'self'
             9260  STORE_ATTR               _macaddr_check_status

 L.3566      9262  LOAD_CONST               True
             9264  LOAD_FAST                'flash_burn_retry'
             9266  BUILD_TUPLE_2         2 
             9268  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 3812_0

    def usage(self):
        bflb_utils.printf('-e --start=00000000 --end=0000FFFF -c config.ini')
        bflb_utils.printf('-w --flash -c config.ini')
        bflb_utils.printf('-w --flash --file=1.bin,2.bin --addr=00000000,00001000 -c config.ini')
        bflb_utils.printf('-r --flash --start=00000000 --end=0000FFFF --file=flash.bin -c config.ini')


def run():
    log_file = os.path.join(app_path, 'log')
    if not os.path.exists(log_file):
        os.makedirs(log_file)
    parser = eflash_loader_parser_init()
    args = parser.parse_args()
    bflb_utils.printf('Chipname: %s' % args.chipname)
    eflash_loader_obj = BflbEflashLoader(args.chipname, gol.dict_chip_cmd[args.chipname])
    gol.chip_name = args.chipname
    if conf_sign:
        reload(cgc)
    while 1:
        try:
            ret = eflash_loader_obj.efuse_flash_loader(args, None, None)
            if ret is not True:
                eflash_loader_obj.error_code_print('0005')
            eflash_loader_obj.close_port()
            time.sleep(2)
        except Exception as e:
            try:
                bflb_utils.printf(e)
            finally:
                e = None
                del e

        time.sleep(0.2)
        if not args.auto:
            break


if __name__ == '__main__':
    run()