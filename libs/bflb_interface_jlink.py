# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
# [GCC 9.4.0]
# Embedded file name: libs/bflb_interface_jlink.py
import re, os, sys, time, binascii, traceback, struct, subprocess, pylink
try:
    import bflb_path
except ImportError:
    from libs import bflb_path

from libs import bflb_utils
from libs.bflb_utils import app_path
python_version = struct.calcsize('P') * 8
if python_version == 64:
    path_dll = os.path.join(app_path, 'utils/jlink', 'JLink_x64.dll')
else:
    path_dll = os.path.join(app_path, 'utils/jlink', 'JLinkARM.dll')

class BflbJLinkPort(object):

    def __init__(self):
        self._speed = 5000
        self._rx_timeout = 10000
        self._jlink_shake_hand_addr = '20000000'
        self._jlink_data_addr = '20000004'
        self._inited = False
        self._chiptype = 'bl60x'
        self._chipname = 'bl60x'
        self._jlink_run_addr = '22010000'
        self._jlink = None

    def if_init(self, device, rate, chiptype='bl60x', chipname='bl60x'):
        if self._inited is False:
            sub_module = __import__(('libs.' + chiptype), fromlist=[chiptype])
            self._jlink_shake_hand_addr = sub_module.jlink_load_cfg.jlink_shake_hand_addr
            self._jlink_data_addr = sub_module.jlink_load_cfg.jlink_data_addr
            if sys.platform == 'win32':
                obj_dll = pylink.Library(dllpath=path_dll)
                self._jlink = pylink.JLink(lib=obj_dll)
                self.jlink_path = os.path.join(app_path, 'utils/jlink', 'JLink.exe')
            else:
                self._jlink = pylink.JLink()
                self.jlink_path = 'JLinkExe'
            match = re.search('\\d{8,10}', device, re.I)
            if match is not None:
                bflb_utils.printf(device)
                self._jlink.open(serial_no=(int(device)))
            else:
                self._jlink.open()
            tif_set = sub_module.jlink_load_cfg.jlink_set_tif
            self._jlink.set_tif(tif_set)
            self._speed = rate
            core_type = sub_module.jlink_load_cfg.jlink_core_type
            self._jlink.connect(core_type, rate)
            self._inited = True
            self._chiptype = chiptype
            self._chipname = chipname
            self._jlink_run_addr = sub_module.jlink_load_cfg.jlink_run_addr
            self._device = device

    def if_clear_buf(self):
        pass

    def if_set_rx_timeout(self, val):
        self._rx_timeout = val * 1000

    def if_get_rate(self):
        return self._speed

    def halt_cpu(self):
        if self._jlink.halted() is False:
            self._jlink.halt()
        if self._jlink.halted():
            return True
        bflb_utils.printf("couldn't halt cpu")
        return False

    def reset_cpu(self, ms=0, halt=True):
        if self._chiptype != 'bl60x':
            self._jlink.set_reset_pin_low()
            self._jlink.set_reset_pin_high()
        return self._jlink.reset(ms, False)

    def set_pc_msp(self, pc, msp):
        if self._jlink.halted() is False:
            self._jlink.halt()
        elif self._jlink.halted():
            if not self._chiptype == 'bl602':
                if self._chiptype == 'bl702' or self._chiptype == 'bl702l':
                    jlink_script = 'jlink.cmd'
                    fp = open(jlink_script, 'w+')
                    cmd = 'h\r\nSetPC ' + str(self._jlink_run_addr) + '\r\nexit'
                    bflb_utils.printf(cmd)
                    fp.write(cmd)
                    fp.close()
                    if self._device:
                        jlink_cmd = self.jlink_path + ' -device RISC-V -Speed {0} -SelectEmuBySN {1}                     -IF JTAG -jtagconf -1,-1 -autoconnect 1 -CommanderScript jlink.cmd'.format(str(self._speed), str(self._device))
                    else:
                        jlink_cmd = self.jlink_path + ' -device RISC-V -Speed {0}                     -IF JTAG -jtagconf -1,-1 -autoconnect 1 -CommanderScript jlink.cmd'.format(str(self._speed))
                    bflb_utils.printf(jlink_cmd)
                    p = subprocess.Popen(jlink_cmd, shell=True,
                      stdin=(subprocess.PIPE),
                      stdout=(subprocess.PIPE),
                      stderr=(subprocess.PIPE))
                    out, err = p.communicate()
                    bflb_utils.printf(out, err)
                    os.remove(jlink_script)
            else:
                self._jlink.register_write(15, int(pc, 16))
                self._jlink.register_write(13, int(msp, 16))
                self._jlink.restart()
        else:
            bflb_utils.printf("couldn't halt cpu")

    def if_write(self, data_send):
        self.if_raw_write(self._jlink_data_addr, data_send)
        data_list = []
        data_list.append(int('59445248', 16))
        self._jlink.memory_write((int(self._jlink_shake_hand_addr, 16)), data_list, nbits=32)

    def if_raw_write(self, addr, data_send):
        addr_int = int(addr, 16)
        len2 = len(data_send) % 4
        len1 = len(data_send) - len2
        if len1 != 0:
            data_list = []
            for i in range(int(len1 / 4)):
                data_list.append(data_send[4 * i] + (data_send[4 * i + 1] << 8) + (data_send[4 * i + 2] << 16) + (data_send[4 * i + 3] << 24))

            self._jlink.memory_write(addr_int, data_list, nbits=32)
        if len2 != 0:
            data_list = []
            for i in range(len2):
                data_list.append(data_send[len1 + i])

            self._jlink.memory_write((addr_int + len1), data_list, nbits=8)

    def if_raw_write8(self, addr, data_send):
        data_list = []
        for data in data_send:
            data_list.append(data)

        self._jlink.memory_write((int(addr, 16)), data_list, nbits=8)

    def if_raw_write16(self, addr, data_send):
        data_list = []
        for i in range(int(len(data_send) / 2)):
            data_list.append(data_send[2 * i] + (data_send[2 * i + 1] << 8))

        self._jlink.memory_write((int(addr, 16)), data_list, nbits=16)

    def if_raw_write32(self, addr, data_send):
        data_list = []
        for i in range(int(len(data_send) / 4)):
            data_list.append(data_send[4 * i] + (data_send[4 * i + 1] << 8) + (data_send[4 * i + 2] << 16) + (data_send[4 * i + 3] << 24))

        self._jlink.memory_write((int(addr, 16)), data_list, nbits=32)

    def if_read(self, data_len):
        start_time = time.time() * 1000
        while True:
            ready = self._jlink.memory_read((int(self._jlink_shake_hand_addr, 16)), 1, nbits=32)
            if len(ready) >= 1:
                if ready[0] == int('4B434153', 16):
                    break
            elapsed = time.time() * 1000 - start_time
            if elapsed >= self._rx_timeout:
                return (
                 0, 'waiting response time out'.encode('utf-8'))
            time.sleep(0.001)

        data = self.if_raw_read(self._jlink_data_addr, data_len)
        if len(data) != data_len:
            return (
             0, data)
        return (
         1, data)

    def if_raw_read(self, addr, data_len):
        addr_int = int(addr, 16)
        if addr_int % 4 == 0:
            len2 = data_len % 4
            len1 = data_len - len2
            data1 = bytearray(0)
            data2 = bytearray(0)
            if len1 != 0:
                data1 = self._jlink.memory_read(addr_int, (int(len1 / 4)), nbits=32)
            if len2 != 0:
                data2 = self._jlink.memory_read((addr_int + len1), len2, nbits=8)
            data = bytearray(0)
            for tmp in data1:
                data += bflb_utils.int_to_4bytearray_l(tmp)

            data += bytearray(data2)
            return data
        return self.if_raw_read8(addr, data_len)

    def if_raw_read8(self, addr, data_len):
        data = self._jlink.memory_read((int(addr, 16)), data_len, nbits=8)
        return bytearray(data)

    def if_raw_read16(self, addr, data_len):
        raw_data = self._jlink.memory_read((int(addr, 16)), (data_len / 2), nbits=16)
        data = bytearray(0)
        for tmp in raw_data:
            data += bflb_utils.int_to_2bytearray_l(tmp)

        return bytearray(data)

    def if_raw_read32(self, addr, data_len):
        raw_data = self._jlink.memory_read((int(addr, 16)), (data_len / 4), nbits=32)
        data = bytearray(0)
        for tmp in raw_data:
            data += bflb_utils.int_to_4bytearray_l(tmp)

        return bytearray(data)

    def if_shakehand(self, do_reset=False, reset_hold_time=100, shake_hand_delay=100, reset_revert=True, cutoff_time=0, shake_hand_retry=2, isp_timeout=0, boot_load=False):
        self.if_write(bytearray(1))
        success, ack = self.if_read(2)
        bflb_utils.printf(binascii.hexlify(ack))
        if ack.find(b'O') != -1 or ack.find(b'K') != -1:
            time.sleep(0.03)
            return 'OK'
        return 'FL'

    def if_close(self):
        if self._jlink:
            self._jlink.close()
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
        eflash_loader_t = BflbJLinkPort()
        eflash_loader_t.if_init('', 1000, 'bl602')
        bflb_utils.printf('reset test')
        res = eflash_loader_t.reset_cpu(0, False)
        bflb_utils.printf(res)
    except Exception as e:
        try:
            NUM_ERR = 5
            bflb_utils.printf(e)
            traceback.print_exc(limit=NUM_ERR, file=(sys.stdout))
        finally:
            e = None
            del e