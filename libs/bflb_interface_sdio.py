# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
# [GCC 9.4.0]
# Embedded file name: libs/bflb_interface_sdio.py
import os, sys, time, binascii, traceback, subprocess, threading, socket
try:
    import bflb_path
except ImportError:
    from libs import bflb_path

from libs import bflb_utils

class BflbSdioPort(object):

    def __init__(self):
        self._speed = 5000
        self._rx_timeout = 10000
        self._inited = False
        self._chiptype = 'bl60x'
        self._chipname = 'bl60x'
        self._udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._send_address = None

    def if_init(self, device, rate, chiptype='bl60x', chipname='bl60x'):
        if self._inited is False:
            host = socket.gethostname()
            self._send_address = (
             host, device)
            self._inited = True
            self._chiptype = chiptype
            self._chipname = chipname
        return True

    def if_clear_buf(self):
        pass

    def if_set_rx_timeout(self, val):
        self._rx_timeout = val * 1000

    def if_get_rate(self):
        return self._speed

    def if_write(self, data_send):
        self._udp_socket.sendto(data_send, self._send_address)

    def if_read(self, data_len):
        recv_data, recv_addr = self._udp_socket.recvfrom(data_len)
        if len(recv_data) != data_len:
            return (
             0, recv_data)
        return (
         1, recv_data)

    def _if_get_sync_bytes(self, length):
        data = bytearray(length)
        i = 0
        while i < length:
            data[i] = 85
            i += 1

        return data

    def if_shakehand(self, do_reset=False, reset_hold_time=100, shake_hand_delay=100, reset_revert=True, cutoff_time=0, shake_hand_retry=2, isp_timeout=0, boot_load=False):
        self.if_write(bytearray(self._if_get_sync_bytes(8)))
        success, ack = self.if_read(2)
        bflb_utils.printf(binascii.hexlify(ack))
        if ack.find(b'O') != -1 or ack.find(b'K') != -1:
            time.sleep(0.03)
            return 'OK'
        return 'FL'

    def if_close(self):
        self._udp_socket.close()
        self._inited = False

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
            success, len_bytes = self.if_read(4)
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
    try:
        eflash_loader_t = BflbSdioPort()
        eflash_loader_t.if_init('', 10086, 'bl602')
        bflb_utils.printf('shakehand test')
        eflash_loader_t.if_shakehand()
    except Exception as e:
        try:
            NUM_ERR = 5
            bflb_utils.printf(e)
            traceback.print_exc(limit=NUM_ERR, file=(sys.stdout))
        finally:
            e = None
            del e