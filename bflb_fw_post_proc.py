# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
# [GCC 9.4.0]
# Embedded file name: libs/bflb_fw_post_proc.py
import re, os, sys, time, shutil
try:
    import bflb_path
except ImportError:
    from libs import bflb_path

from libs import bflb_utils
from libs import bflb_pt_creater as partition
from libs import bflb_ro_params_device_tree as bl_ro_device_tree
chip_dict = ('bl602', 'bl604', 'bl702', 'bl704', 'bl706', 'bl702l', 'bl704l', 'bl606p',
             'bl808', 'bl616', 'bl618')

def get_nicky_name(chipname):
    if chipname == 'bl604':
        return 'bl602'
    if chipname == 'bl704' or chipname == 'bl706':
        return 'bl702'
    if chipname == 'bl704l':
        return 'bl702l'
    if chipname == 'bl618':
        return 'bl616'
    return chipname


def parse_header(bin):
    try:
        with open(bin, 'rb') as (fp):
            content = fp.read()
            if content[0:4] == b'BFNP' or content[0:4] == b'BFAP':
                return True
    except Exception as e:
        try:
            bflb_utils.printf(e)
            bflb_utils.printf('[Warning] Check header fail')
        finally:
            e = None
            del e

    return False


def get_value_file(path, chipname, cpu_id=None):
    if cpu_id:
        path = path.replace('$(CHIPNAME)', chipname + '_' + cpu_id)
    else:
        path = path.replace('$(CHIPNAME)', chipname)
    if os.path.isabs(path):
        path = os.path.abspath(path)
    if not os.path.exists(path):
        dir_path = os.path.dirname(path)
        file_name = os.path.basename(path)
        try:
            all_file_list = os.listdir(dir_path)
        except Exception as e:
            try:
                bflb_utils.printf(e)
                return
            finally:
                e = None
                del e

        result = []
        if '*' in file_name:
            file_name = file_name.replace('.', '\\.').replace('*', '.*[一-龥]*')
        for one_name in all_file_list:
            pattern = re.compile(file_name)
            result += pattern.findall(one_name)

        if len(result) > 1:
            bflb_utils.printf('[Error] Multiple files were matched! ')
            return
        if len(result) == 0:
            error = '[Error]: ' + path + ' image file is not existed'
            bflb_utils.printf(error)
            return
        path = os.path.join(dir_path, result[0])
    return path


def get_img_file_list(files, chipname, cpu_id):
    file_list = files.split(',')
    final = []
    for file in file_list:
        ret = get_value_file(file, chipname, cpu_id)
        if ret != None:
            final.append(ret)
        else:
            bflb_utils.printf('[Error] Get ', file, ' Fail!!!!')

    return final


def parse_rfpa(bin, dts_bytearray):
    try:
        length = len(dts_bytearray)
        with open(bin, 'rb') as (fp):
            content = fp.read()
            bin_bytearray = bytearray(content)
            if content[0:4] == b'BFNP':
                if content[4096:4100] == b'BFAP' or content[4096:4100] == b'BFNP':
                    if content[9216:9224] == b'BLRFPARA':
                        bflb_utils.printf('8K header found,append dts file')
                        bin_bytearray[9224:9224 + length] = dts_bytearray
                        with open(bin, 'wb') as (fp):
                            fp.write(bin_bytearray)
                        return
            if content[0:4] == b'BFNP':
                if content[5120:5128] == b'BLRFPARA':
                    bflb_utils.printf('4K header found,append dts file')
                    bin_bytearray[5128:5128 + length] = dts_bytearray
                    with open(bin, 'wb') as (fp):
                        fp.write(bin_bytearray)
                    return
            if content[1024:1032] == b'BLRFPARA':
                bflb_utils.printf('Raw image found,append dts file')
                bin_bytearray[1032:1032 + length] = dts_bytearray
                with open(bin, 'wb') as (fp):
                    fp.write(bin_bytearray)
                return
            bflb_utils.printf('BLRFPARA magic not found, skip append dts file')
    except Exception as e:
        try:
            bflb_utils.printf(e)
            bflb_utils.printf('[Error] Append dts file fail')
        finally:
            e = None
            del e


def found_file(dir, suffix):
    files = []
    for file in os.listdir(dir):
        if file.endswith(suffix):
            files.append(file)

    return files


def found_boot2_mfg_file(dir, target):
    files = []
    for file in os.listdir(dir):
        if file.startswith(target) and file.endswith('.bin'):
            files.append(file)

    return files


def create_partiton_table(search_dir, imgfile):
    files = found_file(search_dir, '.toml')
    if len(files) == 0:
        bflb_utils.printf('[Warning] No partiton file found in ', search_dir, ',go on next steps')
        return
    if len(files) > 1:
        bflb_utils.printf('[Error] More than one partition file found in ', search_dir, ',go on next steps')
        return
    bflb_utils.printf('Create partition using ', files[0])
    pt_helper = partition.PtCreater(os.path.join(search_dir, files[0]))
    filedir, ext = os.path.split(imgfile)
    pt_helper.create_pt_table(os.path.join(filedir, 'partition.bin'))


def append_dts_file(search_dir, imgfile):
    files = found_file(search_dir, '.dts')
    if len(files) == 0:
        bflb_utils.printf('[Warning] No dts file found in ', search_dir, ',go on next steps')
        return
    if len(files) > 1:
        bflb_utils.printf('[Error] More than one dts file found in ', search_dir, ',go on next steps')
        return
    bflb_utils.printf('Create dts using ', files[0])
    try:
        dts_hex = bl_ro_device_tree.bl_dts2hex(os.path.join(search_dir, files[0]))
        dts_bytearray = bflb_utils.hexstr_to_bytearray(dts_hex)
    except Exception as e:
        try:
            bflb_utils.printf(e)
            bflb_utils.printf('[Error] Create fail!!!, go on next steps')
            return
        finally:
            e = None
            del e

    parse_rfpa(imgfile, dts_bytearray)


def copy_boot2_file(search_dir, imgfile):
    files = found_boot2_mfg_file(search_dir, 'boot')
    if len(files) == 0:
        bflb_utils.printf('[Warning] No boot2/bootloader file found in ', search_dir, ',go on next steps')
        return
    if len(files) > 1:
        bflb_utils.printf('[Error] More than one boot2/bootloader file found in ', search_dir, ',go on next steps')
        return
    bflb_utils.printf('Copy ', files[0])
    try:
        filedir, ext = os.path.split(imgfile)
        shutil.copy(os.path.join(search_dir, files[0]), filedir)
    except Exception as e:
        try:
            bflb_utils.printf(e)
            bflb_utils.printf('[Warning] Copy boot2/bootloader fail!!!, go on next steps')
        finally:
            e = None
            del e


def copy_mfg_file(search_dir, imgfile):
    files = found_boot2_mfg_file(search_dir, 'mfg')
    if len(files) == 0:
        bflb_utils.printf('[Warning] No mfg file found in ', search_dir, ',go on next steps')
        return
    if len(files) > 1:
        bflb_utils.printf('[Error] More than one mfg file found in ', search_dir, ',go on next steps')
        return
    bflb_utils.printf('Copy ', files[0])
    try:
        filedir, ext = os.path.split(imgfile)
        shutil.copy(os.path.join(search_dir, files[0]), filedir)
    except Exception as e:
        try:
            bflb_utils.printf(e)
            bflb_utils.printf('[Error] Copy mfg fail!!!, go on next steps')
        finally:
            e = None
            del e


def firmware_post_process(args, chipname='bl60x'):
    chipname = get_nicky_name(chipname.lower())
    sub_module = __import__(('libs.' + chipname), fromlist=[chipname])
    sub_module.firmware_post_process_do.firmware_post_proc(args)


def run():
    parser = bflb_utils.firmware_post_proc_parser_init()
    args = parser.parse_args()
    bflb_utils.printf('Chipname: %s' % args.chipname)
    if args.aesiv != None:
        if len(args.aesiv) != 32:
            bflb_utils.printf('[Error] AES IV length error')
            return
        if args.aesiv[24:32] != '00000000':
            bflb_utils.printf('[Error] AES IV should end with 00000000')
            return
    if args.chipname.lower() in chip_dict:
        img_file_list = None
        if args.imgfile != None:
            img_file_list = get_img_file_list(args.imgfile, args.chipname, args.cpuid)
        if args.brdcfgdir != None:
            bflb_utils.printf('Board config dir: %s' % args.brdcfgdir)
            create_partiton_table(args.brdcfgdir, img_file_list[0])
            append_dts_file(args.brdcfgdir, img_file_list[0])
            copy_boot2_file(args.brdcfgdir, img_file_list[0])
            copy_mfg_file(args.brdcfgdir, img_file_list[0])
        for img_file in img_file_list:
            bflb_utils.printf('\r\nProcess ', img_file)
            args.imgfile = img_file
            if parse_header(args.imgfile) == False:
                bflb_utils.printf('[Warning] No boot header found,skip!!!')
                break
            firmware_post_process(args, args.chipname)

    else:
        bflb_utils.printf('[Error] Please set correct chipname config, exit!!!')


if __name__ == '__main__':
    run()