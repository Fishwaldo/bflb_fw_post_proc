# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
# [GCC 9.4.0]
# Embedded file name: libs/bflb_interface_cklink.py
import os, time, binascii, subprocess, config as gol, cklink
try:
    import bflb_path
except ImportError:
    from libs import bflb_path

from libs import bflb_utils
from libs.bflb_utils import app_path
dir_dll = os.path.join(app_path, 'utils/cklink')

class BflbCKLinkPort(object):

    def __init__(self, vid=0, pid=0):
        self._speed = 5000
        self._rx_timeout = 10000
        self._cklink_shake_hand_addr = '20000000'
        self._cklink_data_addr = '20000004'
        self._cklink_run_addr = '22010000'
        self._cklink_reg_pc = 32
        self._inited = False
        self._chiptype = 'bl808'
        self._chipname = 'bl808'
        self.vid = vid
        self.pid = pid
        self.link = gol.obj_cklink

    def if_init(self, device, sn, rate, chiptype='bl808', chipname='bl808'):
        if self._inited is False:
            dev = device.split('|')
            vid = int(dev[0].replace('0x', ''), 16)
            pid = int(dev[1].replace('0x', ''), 16)
            serial = str(sn)
            bflb_utils.printf('SN is ' + serial)
            sub_module = __import__(('libs.' + chiptype), fromlist=[chiptype])
            self._cklink_shake_hand_addr = sub_module.cklink_load_cfg.cklink_shake_hand_addr
            self._cklink_data_addr = sub_module.cklink_load_cfg.cklink_data_addr
            self._cklink_run_addr = sub_module.cklink_load_cfg.cklink_run_addr
            self._cklink_vid = vid
            self._cklink_pid = pid
            self._speed = rate
            self._inited = True
            self._chiptype = chiptype
            self._chipname = chipname
            if not self.link:
                self.link = cklink.CKLink(dlldir=dir_dll, vid=(self._cklink_vid),
                  pid=(self._cklink_pid),
                  sn=serial,
                  arch=2,
                  cdi=0)
                gol.obj_cklink = self.link
            self.link.open()
            if self.link.connected():
                self.link.reset(1)
            return False

    def if_close(self):
        if self.link:
            try:
                try:
                    self.link.close()
                except Exception as e:
                    try:
                        print(e)
                    finally:
                        e = None
                        del e

            finally:
                self._inited = False

    def if_clear_buf(self):
        pass

    def if_set_rx_timeout(self, val):
        self._rx_timeout = val * 1000

    def if_get_rate(self):
        return self._speed

    def halt_cpu(self):
        return self.link.halt()

    def resume_cpu(self):
        return self.link.resume()

    def reset_cpu(self):
        return self.link.reset(1)

    def set_pc_msp(self, pc, msp):
        self.halt_cpu()
        if self._chiptype == 'bl602' or self._chiptype == 'bl702' or self._chiptype == 'bl702l':
            addr = int(self._cklink_run_addr, 16)
            self.link.write_cpu_reg(self._cklink_reg_pc, addr)

    def if_raw_write(self, addr, data_send):
        self.halt_cpu()
        addr_int = int(addr, 16)
        data_send = bytes(data_send)
        self.link.write_memory(addr_int, data_send)
        self.resume_cpu()

    def if_write(self, data_send):
        self.if_raw_write(self._cklink_data_addr, data_send)
        self.if_raw_write(self._cklink_shake_hand_addr, binascii.unhexlify('48524459'))

    def if_read(self, data_len):
        start_time = time.time() * 1000
        while True:
            self.halt_cpu()
            ready = self.link.read_memory(int(self._cklink_shake_hand_addr, 16), 4)
            if len(ready) >= 1:
                ready = binascii.hexlify(ready).decode()
                if ready == '5341434b':
                    self.resume_cpu()
                    break
            elapsed = time.time() * 1000 - start_time
            if elapsed >= self._rx_timeout:
                return (
                 0, 'waiting response time out'.encode('utf-8'))
            self.resume_cpu()
            time.sleep(0.001)

        data = self.if_raw_read(self._cklink_data_addr, data_len)
        if len(data) != data_len:
            return (
             0, data)
        return (
         1, data)

    def if_raw_read(self, addr, data_len):
        return self.if_raw_read8(addr, data_len)

    def if_raw_read8(self, addr, data_len):
        self.halt_cpu()
        data = self.link.read_memory(int(addr, 16), data_len)
        self.resume_cpu()
        return bytearray(data)

    def if_shakehand(self, do_reset=False, reset_hold_time=100, shake_hand_delay=100, reset_revert=True, cutoff_time=0, shake_hand_retry=2, isp_timeout=0, boot_load=False):
        self.if_write(bytearray(1))
        success, ack = self.if_read(2)
        bflb_utils.printf(binascii.hexlify(ack))
        if ack.find(b'O') != -1 or ack.find(b'K') != -1:
            time.sleep(0.03)
            return 'OK'
        return 'FL'

    def if_deal_ack(self):
        success, ack = self.if_read(2)
        if success == 0:
            bflb_utils.printf('ack:' + str(binascii.hexlify(ack)))
            return ack.decode('utf-8')
        if ack.find(b'O') != -1 or ack.find(b'K') != -1:
            return 'OK'
        if ack.find(b'P') != -1 or ack.find(b'D') != -1:
            return 'PD'
        success, err_code = self.if_read(4)
        if success == 0:
            bflb_utils.printf('err_code:' + str(binascii.hexlify(err_code)))
            return 'FL'
        err_code_str = str(binascii.hexlify(err_code[3:4] + err_code[2:3]).decode('utf-8'))
        ack = 'FL'
        try:
            ret = ack + err_code_str + '(' + bflb_utils.get_bflb_error_code(err_code_str) + ')'
        except Exception:
            ret = ack + err_code_str + ' unknown'

        bflb_utils.printf(ret)
        return ret

    def if_deal_response(self):
        ack = self.if_deal_ack()
        if ack == 'OK':
            success, len_bytes = self.if_read(16)
            if success == 0:
                bflb_utils.printf('Get length error')
                bflb_utils.printf(binascii.hexlify(len_bytes))
                return ('Get length error', len_bytes)
            tmp = bflb_utils.bytearray_reverse(len_bytes[2:4])
            data_len = bflb_utils.bytearray_to_int(tmp)
            success, data_bytes = self.if_read(data_len + 4)
            if success == 0:
                bflb_utils.printf('Read data error')
                return ('Read data error', data_bytes)
            data_bytes = data_bytes[4:]
            if len(data_bytes) != data_len:
                bflb_utils.printf('Not get excepted length')
                return ('Not get excepted length', data_bytes)
            return (
             ack, data_bytes)
        bflb_utils.printf('Not ack OK')
        bflb_utils.printf(ack)
        return (ack, None)


if __name__ == '__main__':
    eflash_loader_t = BflbCKLinkPort()
    eflash_loader_t.if_init('', 100, 'bl702')
    bflb_utils.printf('read test')
    bflb_utils.printf(eflash_loader_t.if_raw_read('21000000', 2))
    bflb_utils.printf(eflash_loader_t.if_raw_read('21000000', 4))
    bflb_utils.printf(eflash_loader_t.if_raw_read('21000000', 10))
    bflb_utils.printf(eflash_loader_t.if_raw_read('21000000', 16))
    bflb_utils.printf(eflash_loader_t.if_raw_read('21000001', 2))
    bflb_utils.printf(eflash_loader_t.if_raw_read('21000001', 4))
    bflb_utils.printf(eflash_loader_t.if_raw_read('21000001', 10))
    bflb_utils.printf(eflash_loader_t.if_raw_read('21000001', 16))
    bflb_utils.printf(eflash_loader_t.if_raw_read('21000002', 2))
    bflb_utils.printf(eflash_loader_t.if_raw_read('21000002', 4))
    bflb_utils.printf(eflash_loader_t.if_raw_read('21000002', 10))
    bflb_utils.printf(eflash_loader_t.if_raw_read('21000002', 16))
    bflb_utils.printf('write test')
    data = bytearray([
     1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 
     2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 
     3, 4, 
     1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4])
    eflash_loader_t.if_raw_write('42020000', data)
    bflb_utils.printf(eflash_loader_t.if_raw_read('42020000', 62))