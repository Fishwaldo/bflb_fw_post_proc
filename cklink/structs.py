# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
# [GCC 9.4.0]
# Embedded file name: cklink/structs.py
import ctypes
fn1_type = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char)
fn2_type = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)

class ValueOfReg(ctypes.Union):
    _fields_ = [
     (
      'val8', ctypes.c_ubyte),
     (
      'val16', ctypes.c_ushort),
     (
      'val32', ctypes.c_uint),
     (
      'val64', ctypes.c_uint64),
     (
      'valf', ctypes.c_float),
     (
      'vald', ctypes.c_double),
     (
      'raw', ctypes.c_ubyte * 16)]


class Register(ctypes.Structure):
    __doc__ = 'Register info structure.\n\n    Attributes:\n\n    '
    _fields_ = [
     (
      'name', ctypes.c_char * 32),
     (
      'num', ctypes.c_int),
     (
      'type', ctypes.c_int),
     (
      'length', ctypes.c_int),
     (
      'value', ValueOfReg)]


class LinkDevice(ctypes.Structure):
    __doc__ = 'Link device info structure.\n\n    Attributes:\n\n    '
    _fields_ = [
     (
      'device', ctypes.c_void_p),
     (
      'handler', ctypes.c_void_p),
     (
      'vid', ctypes.c_int),
     (
      'pid', ctypes.c_int),
     (
      'bcdDevice', ctypes.c_int),
     (
      'dev_str', ctypes.c_char * 200),
     (
      'sn', ctypes.c_char * 200),
     (
      'state', ctypes.c_int)]


class LinkCfg(ctypes.Structure):
    __doc__ = 'Link Cfg info structure.\n\n    Attributes:\n\n    '
    _fields_ = [
     (
      'vid', ctypes.c_ushort),
     (
      'pid', ctypes.c_ushort),
     (
      'root_path', ctypes.c_char_p),
     (
      'mtcr_delay', ctypes.c_int),
     (
      'cdi', ctypes.c_int),
     (
      'nrst_delay', ctypes.c_int),
     (
      'trst_delay', ctypes.c_int),
     (
      'trst_en', ctypes.c_ubyte),
     (
      'ice_clk', ctypes.c_uint),
     (
      'serial', ctypes.c_char_p),
     (
      'config_path', ctypes.c_char_p)]


class MiscCfg(ctypes.Structure):
    __doc__ = 'Misc cfg info structure.\n\n    Attributes:\n\n    '
    _fields_ = [
     (
      'verbose', ctypes.c_int),
     (
      'print_version', ctypes.c_int),
     (
      'msgout', fn2_type),
     (
      'errout', fn2_type),
     (
      'return_after_ice_connection', ctypes.c_ubyte)]


class ArchCfg(ctypes.Structure):
    __doc__ = 'Arch Cfg info structure.\n\n    Attributes:\n\n    '
    _fields_ = [
     (
      'debug_arch', ctypes.c_int),
     (
      'no_cpuid_check', ctypes.c_uint),
     (
      'isa_version', ctypes.c_int),
     (
      'hacr_width', ctypes.c_int),
     (
      'tdesc_xml_file', ctypes.c_char_p),
     (
      'script', ctypes.c_char_p),
     (
      'target_init_script', ctypes.c_char_p),
     (
      'pre_reset', ctypes.c_ubyte),
     (
      'no_cache_flush', ctypes.c_ubyte),
     (
      'cache_flush_delay', ctypes.c_uint),
     (
      'rst_sleep', ctypes.c_int),
     (
      'idle_delay', ctypes.c_uint),
     (
      'ndmrst_delay', ctypes.c_uint),
     (
      'hartrst_delay', ctypes.c_uint)]


class SocketCfg(ctypes.Structure):
    __doc__ = 'Socket cfg info structure.\n\n    Attributes:\n\n    '
    _fields_ = [
     (
      'onlyserver', ctypes.c_ubyte),
     (
      'port', ctypes.c_int),
     (
      'is_multicore_threads', ctypes.c_ubyte)]


class DcommCfg(ctypes.Structure):
    __doc__ = 'Dcomm cfg info structure.\n\n    Attributes:\n\n    '
    _fields_ = [
     (
      'type', ctypes.c_int),
     (
      'on_target_stdout', fn1_type),
     (
      'on_remote_stdout', fn1_type)]


class DsamplingCfg(ctypes.Structure):
    __doc__ = 'Dsampling cfg info structure.\n\n    Attributes:\n\n    '
    _fields_ = [
     (
      'sampling', ctypes.c_int),
     (
      'sampling_freq', ctypes.c_uint),
     (
      'sampling_port', ctypes.c_int),
     (
      'sampling_cpu', ctypes.c_uint),
     (
      'type', ctypes.c_int)]


class FunctionalCfg(ctypes.Structure):
    __doc__ = 'Functional Cfg info structure.\n\n    Attributes:\n\n    '
    _fields_ = [
     (
      'ddc_flag', ctypes.c_ubyte),
     (
      'local_semi', ctypes.c_ubyte),
     (
      'cmdline_en', ctypes.c_ubyte),
     (
      'cmd_script_path', ctypes.c_char_p),
     (
      'speeded_up', ctypes.c_int),
     (
      'dcomm', DcommCfg),
     (
      'dsampling', DsamplingCfg)]


class Target(ctypes.Structure):
    pass


class DebuggerDerverCfg(ctypes.Structure):
    __doc__ = 'Debugger Derver Cfg info structure.\n\n    Attributes:\n\n    '
    _fields_ = [
     (
      'priv', ctypes.c_void_p),
     (
      'root_path', ctypes.c_char_p),
     (
      'ide_flag', ctypes.c_uint),
     (
      'do_link_upgrade', ctypes.c_uint),
     (
      'link', LinkCfg),
     (
      'misc', MiscCfg),
     (
      'arch', ArchCfg),
     (
      'socket', SocketCfg),
     (
      'function', FunctionalCfg),
     (
      'target', Target),
     (
      'list_ice', ctypes.c_int),
     (
      'list_vendor', ctypes.c_uint),
     (
      'vendor_name', ctypes.c_char_p),
     (
      'log_file_name', ctypes.c_char_p)]