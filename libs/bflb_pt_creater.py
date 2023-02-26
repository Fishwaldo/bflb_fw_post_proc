# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
# [GCC 9.4.0]
# Embedded file name: libs/bflb_pt_creater.py
from libs import bflb_utils
from libs import bflb_toml as toml

class PtCreater(object):

    def __init__(self, config_file):
        self.parsed_toml = toml.load(config_file)
        self.entry_max = 16
        self.pt_new = False

    def __create_pt_table_do(self, lists, file):
        entry_table = bytearray(36 * self.entry_max)
        entry_cnt = 0
        for item in lists:
            entry_type = item['type']
            entry_name = item['name']
            entry_device = item['device']
            entry_addr0 = item['address0']
            entry_addr1 = item['address1']
            entry_maxlen0 = item['size0']
            entry_maxlen1 = item['size1']
            entry_len = item['len']
            entry_table[36 * entry_cnt + 0] = bflb_utils.int_to_2bytearray_l(entry_type)[0]
            if 'activeindex' in item:
                entry_activeindex = item['activeindex']
                entry_table[36 * entry_cnt + 2] = bflb_utils.int_to_2bytearray_l(entry_activeindex)[0]
            if len(entry_name) >= 8:
                bflb_utils.printf('%s entry name is too long!' % entry_name)
                return False
            entry_table[36 * entry_cnt + 3:36 * entry_cnt + 3 + len(entry_name)] = bytearray(entry_name, 'utf-8') + bytearray(0)
            entry_table[36 * entry_cnt + 12:36 * entry_cnt + 16] = bflb_utils.int_to_4bytearray_l(entry_addr0)
            entry_table[36 * entry_cnt + 16:36 * entry_cnt + 20] = bflb_utils.int_to_4bytearray_l(entry_addr1)
            entry_table[36 * entry_cnt + 20:36 * entry_cnt + 24] = bflb_utils.int_to_4bytearray_l(entry_maxlen0)
            entry_table[36 * entry_cnt + 24:36 * entry_cnt + 28] = bflb_utils.int_to_4bytearray_l(entry_maxlen1)
            entry_table[36 * entry_cnt + 28:36 * entry_cnt + 32] = bflb_utils.int_to_4bytearray_l(entry_len)
            if 'age' in item:
                entry_age = item['age']
                entry_table[36 * entry_cnt + 32:36 * entry_cnt + 36] = bflb_utils.int_to_4bytearray_l(entry_age)
            entry_cnt += 1

        pt_table = bytearray(16)
        pt_table[0] = 66
        pt_table[1] = 70
        pt_table[2] = 80
        pt_table[3] = 84
        pt_table[6:8] = bflb_utils.int_to_2bytearray_l(int(entry_cnt))
        pt_table[12:16] = bflb_utils.get_crc32_bytearray(pt_table[0:12])
        entry_table[36 * entry_cnt:36 * entry_cnt + 4] = bflb_utils.get_crc32_bytearray(entry_table[0:36 * entry_cnt])
        data = pt_table + entry_table[0:36 * entry_cnt + 4]
        fp = open(file, 'wb+')
        fp.write(data)
        fp.close()
        return True

    def create_pt_table(self, file):
        self.pt_new = True
        return self._PtCreater__create_pt_table_do(self.parsed_toml['pt_entry'], file)

    def get_pt_table_addr(self):
        addr0 = self.parsed_toml['pt_table']['address0']
        addr1 = self.parsed_toml['pt_table']['address1']
        return (addr0, addr1)

    def construct_table(self):
        parcel = {}
        name_list = []
        if self.pt_new is True:
            parcel['pt_new'] = True
        else:
            parcel['pt_new'] = False
        parcel['pt_addr0'] = self.parsed_toml['pt_table']['address0']
        parcel['pt_addr1'] = self.parsed_toml['pt_table']['address1']
        version_sign = 1
        try:
            if 'version' in self.parsed_toml['pt_table']:
                if self.parsed_toml['pt_table']['version'] == 2:
                    version_sign = 2
                    parcel['version'] = 2
        except:
            pass

        if version_sign == 1:
            for tbl_item in self.parsed_toml['pt_entry']:
                name = tbl_item['name'].lower()
                if name.upper() == 'FW_CPU0':
                    parcel['fw_cpu0_addr'] = tbl_item['address0']
                    parcel['fw_cpu0_len'] = tbl_item['size0']
                    parcel['fw1_cpu0_addr'] = tbl_item['address1']
                    parcel['fw1_cpu0_len'] = tbl_item['size1']
                    parcel['fw1_cpu0_header'] = 1
                else:
                    if name.upper() == 'FW_GRP0':
                        parcel['fw_group0_addr'] = tbl_item['address0']
                        parcel['fw_group0_len'] = tbl_item['size0']
                        parcel['fw1_group0_addr'] = tbl_item['address1']
                        parcel['fw1_group0_len'] = tbl_item['size1']
                        parcel['fw1_group0_header'] = 1
                    else:
                        if name.upper() == 'FW_GRP1':
                            parcel['fw_group1_addr'] = tbl_item['address0']
                            parcel['fw_group1_len'] = tbl_item['size0']
                            parcel['fw1_group1_addr'] = tbl_item['address1']
                            parcel['fw1_group1_len'] = tbl_item['size1']
                            parcel['fw1_group1_header'] = 1
                        else:
                            if name.lower() == 'factory':
                                parcel['factory_addr'] = tbl_item['address0']
                                parcel['factory_len'] = tbl_item['size0']
                                parcel['factory_header'] = 0
                            else:
                                if name.upper() == 'FW':
                                    parcel['fw_addr'] = tbl_item['address0']
                                    parcel['fw_len'] = tbl_item['size0']
                                    parcel['fw1_addr'] = tbl_item['address1']
                                    parcel['fw1_len'] = tbl_item['size1']
                                    parcel['fw_header'] = 1
                                else:
                                    if name.upper() == 'D0FW':
                                        parcel['d0fw_addr'] = tbl_item['address0']
                                        parcel['d0fw_len'] = tbl_item['size0']
                                        parcel['d0fw1_addr'] = tbl_item['address1']
                                        parcel['d0fw1_len'] = tbl_item['size1']
                                        parcel['d0fw_header'] = 1
                                    else:
                                        if name.lower() == 'imtb':
                                            parcel['imtb_addr'] = tbl_item['address0']
                                            parcel['imtb_len'] = tbl_item['size0']
                                            parcel['imtb_header'] = 0
                                        else:
                                            if name.lower() == 'media':
                                                parcel['media_addr'] = tbl_item['address0']
                                                parcel['media_len'] = tbl_item['size0']
                                                parcel['media_header'] = 0
                                            else:
                                                if name.lower() == 'kv':
                                                    parcel['kv_addr'] = tbl_item['address0']
                                                    parcel['kv_len'] = tbl_item['size0']
                                                    parcel['kv_header'] = 0
                                                else:
                                                    if name.lower() == 'yocboot':
                                                        parcel['yocboot_addr'] = tbl_item['address0']
                                                        parcel['yocboot_len'] = tbl_item['size0']
                                                        parcel['yocboot_header'] = 1
                                                    else:
                                                        if name.lower() == 'mfg':
                                                            parcel['mfg_addr'] = tbl_item['address0']
                                                            parcel['mfg_len'] = tbl_item['size0']
                                                            parcel['mfg_header'] = 1
                                                        else:
                                                            if name.lower() == 'imgload':
                                                                parcel['imgload_addr'] = tbl_item['address0']
                                                                parcel['imgload_len'] = tbl_item['size0']
                                                                parcel['imgload_header'] = 1
                                                            else:
                                                                if name.lower() == 'sbi':
                                                                    parcel['sbi_addr'] = tbl_item['address0']
                                                                    parcel['sbi_len'] = tbl_item['size0']
                                                                    parcel['sbi_header'] = 1
                                                                else:
                                                                    if name.lower() == 'kernel':
                                                                        parcel['kernel_addr'] = tbl_item['address0']
                                                                        parcel['kernel_len'] = tbl_item['size0']
                                                                        parcel['kernel_header'] = 1
                                                                    else:
                                                                        if name.lower() == 'rootfs':
                                                                            parcel['rootfs_addr'] = tbl_item['address0']
                                                                            parcel['rootfs_len'] = tbl_item['size0']
                                                                            parcel['rootfs_header'] = 0
                                                                        else:
                                                                            if name.lower() == 'dtb':
                                                                                parcel['dtb_addr'] = tbl_item['address0']
                                                                                parcel['dtb_len'] = tbl_item['size0']
                                                                                parcel['dtb_header'] = 1
                                                                            else:
                                                                                parcel[name + '_addr'] = tbl_item['address0']
                                                                                parcel[name + '_len'] = tbl_item['size0']
                                                                                parcel[name + '_header'] = 0
                name_list.append(name.lower())

        else:
            if version_sign == 2:
                for tbl_item in self.parsed_toml['pt_entry']:
                    name = tbl_item['name'].lower().replace(' ', '_')
                    parcel[name + '_addr'] = tbl_item['address0']
                    parcel[name + '_len'] = tbl_item['size0']
                    parcel[name + '_header'] = tbl_item['header']
                    if name.startswith('fw'):
                        parcel[name.replace('fw', 'fw1') + '_addr'] = tbl_item['address1']
                        parcel[name.replace('fw', 'fw1') + '_len'] = tbl_item['size1']
                    try:
                        if 'security' in tbl_item:
                            parcel[name + '_security'] = tbl_item['security']
                    except:
                        pass

                    name_list.append(name)

        if len(name_list) > 0:
            return (
             parcel, name_list)
        return (parcel, [])


if __name__ == '__main__':
    pt_helper = PtCreater('partition_cfg.toml')
    pt_helper.create_pt_table('partition_test.bin')
    pt_helper.get_pt_table_addr()