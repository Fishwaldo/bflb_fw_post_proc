# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
# [GCC 9.4.0]
# Embedded file name: libs/wb03/img_create_do.py
import os, sys, hashlib, binascii, codecs, ecdsa
from CryptoPlus.Cipher import AES as AES_XTS
from libs import bflb_utils
from libs.bflb_utils import img_create_sha256_data, img_create_encrypt_data
from libs.bflb_configobj import BFConfigParser
from libs.wb03.flash_select_do import create_flashcfg_table
from libs.wb03.bootheader_cfg_keys import custom_config_len as custom_cfg_len
from libs.wb03.bootheader_cfg_keys import flashcfg_table_start_pos as flashcfg_table_start
from libs.wb03.bootheader_cfg_keys import bootcpucfg_start_pos as bootcpucfg_start
from libs.wb03.bootheader_cfg_keys import bootcpucfg_len as bootcpucfg_length
from libs.wb03.bootheader_cfg_keys import bootcpucfg_m0_index as bootcpucfg_m0_index_number
from libs.wb03.bootheader_cfg_keys import bootcfg_start_pos as bootcfg_start
from libs.wb03.bootheader_cfg_keys import bootheader_len as header_len
keyslot0 = 28
keyslot1 = keyslot0 + 16
keyslot2 = keyslot1 + 16
keyslot3 = keyslot2 + 16
keyslot3_end = keyslot3 + 16
keyslot4 = 128
keyslot5 = keyslot4 + 16
keyslot6 = keyslot5 + 16
keyslot7 = keyslot6 + 16
keyslot8 = keyslot7 + 16
keyslot9 = keyslot8 + 16
keyslot10 = keyslot9 + 16
keyslot10_end = keyslot10 + 16
keyslot11 = keyslot3_end + 16
keyslot11_end = keyslot11 + 16
wr_lock_boot_mode = 14
wr_lock_dbg_pwd = 15
wr_lock_wifi_mac = 16
wr_lock_key_slot_0 = 17
wr_lock_key_slot_1 = 18
wr_lock_key_slot_2 = 19
wr_lock_key_slot_3 = 20
wr_lock_sw_usage_0 = 21
wr_lock_sw_usage_1 = 22
wr_lock_sw_usage_2 = 23
wr_lock_sw_usage_3 = 24
wr_lock_key_slot_11 = 25
rd_lock_dbg_pwd = 26
rd_lock_key_slot_0 = 27
rd_lock_key_slot_1 = 28
rd_lock_key_slot_2 = 29
rd_lock_key_slot_3 = 30
rd_lock_key_slot_11 = 31
wr_lock_key_slot_4 = 15
wr_lock_key_slot_5 = 16
wr_lock_key_slot_6 = 17
wr_lock_key_slot_7 = 18
wr_lock_key_slot_8 = 19
wr_lock_key_slot_9 = 20
wr_lock_key_slot_10 = 21
rd_lock_key_slot_4 = 25
rd_lock_key_slot_5 = 26
rd_lock_key_slot_6 = 27
rd_lock_key_slot_7 = 28
rd_lock_key_slot_8 = 29
rd_lock_key_slot_9 = 30
rd_lock_key_slot_10 = 31

def bytearray_data_merge(data1, data2, len):
    for i in range(len):
        data1[i] |= data2[i]

    return data1


def img_update_efuse_group0--- This code section failed: ---

 L.  91         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'cfg'
                4  LOAD_METHOD              get
                6  LOAD_STR                 'Img_Group0_Cfg'
                8  LOAD_STR                 'efuse_file'
               10  CALL_METHOD_2         2  '2 positional arguments'
               12  LOAD_STR                 'rb'
               14  CALL_FUNCTION_2       2  '2 positional arguments'
               16  STORE_FAST               'fp'

 L.  92        18  LOAD_GLOBAL              bytearray
               20  LOAD_FAST                'fp'
               22  LOAD_METHOD              read
               24  CALL_METHOD_0         0  '0 positional arguments'
               26  CALL_FUNCTION_1       1  '1 positional argument'
               28  LOAD_GLOBAL              bytearray
               30  LOAD_CONST               0
               32  CALL_FUNCTION_1       1  '1 positional argument'
               34  BINARY_ADD       
               36  STORE_FAST               'efuse_data'

 L.  93        38  LOAD_FAST                'fp'
               40  LOAD_METHOD              close
               42  CALL_METHOD_0         0  '0 positional arguments'
               44  POP_TOP          

 L.  94        46  LOAD_GLOBAL              open
               48  LOAD_FAST                'cfg'
               50  LOAD_METHOD              get
               52  LOAD_STR                 'Img_Group0_Cfg'
               54  LOAD_STR                 'efuse_mask_file'
               56  CALL_METHOD_2         2  '2 positional arguments'
               58  LOAD_STR                 'rb'
               60  CALL_FUNCTION_2       2  '2 positional arguments'
               62  STORE_FAST               'fp'

 L.  95        64  LOAD_GLOBAL              bytearray
               66  LOAD_FAST                'fp'
               68  LOAD_METHOD              read
               70  CALL_METHOD_0         0  '0 positional arguments'
               72  CALL_FUNCTION_1       1  '1 positional argument'
               74  LOAD_GLOBAL              bytearray
               76  LOAD_CONST               0
               78  CALL_FUNCTION_1       1  '1 positional argument'
               80  BINARY_ADD       
               82  STORE_FAST               'efuse_mask_data'

 L.  96        84  LOAD_FAST                'fp'
               86  LOAD_METHOD              close
               88  CALL_METHOD_0         0  '0 positional arguments'
               90  POP_TOP          

 L.  98        92  LOAD_GLOBAL              bytearray
               94  LOAD_METHOD              fromhex
               96  LOAD_STR                 'FFFFFFFF'
               98  CALL_METHOD_1         1  '1 positional argument'
              100  STORE_FAST               'mask_4bytes'

 L. 101       102  LOAD_FAST                'flash_encryp_type'
              104  LOAD_CONST               3
              106  COMPARE_OP               >=
              108  POP_JUMP_IF_FALSE   128  'to 128'

 L. 102       110  LOAD_FAST                'efuse_data'
              112  LOAD_CONST               0
              114  DUP_TOP_TWO      
              116  BINARY_SUBSCR    
              118  LOAD_CONST               3
              120  INPLACE_OR       
              122  ROT_THREE        
              124  STORE_SUBSCR     
              126  JUMP_FORWARD        144  'to 144'
            128_0  COME_FROM           108  '108'

 L. 104       128  LOAD_FAST                'efuse_data'
              130  LOAD_CONST               0
              132  DUP_TOP_TWO      
              134  BINARY_SUBSCR    
              136  LOAD_FAST                'flash_encryp_type'
              138  INPLACE_OR       
              140  ROT_THREE        
              142  STORE_SUBSCR     
            144_0  COME_FROM           126  '126'

 L. 106       144  LOAD_FAST                'sign'
              146  LOAD_CONST               0
              148  COMPARE_OP               >
              150  POP_JUMP_IF_FALSE   188  'to 188'

 L. 107       152  LOAD_FAST                'efuse_data'
              154  LOAD_CONST               92
              156  DUP_TOP_TWO      
              158  BINARY_SUBSCR    
              160  LOAD_FAST                'sign'
              162  LOAD_CONST               7
              164  BINARY_LSHIFT    
              166  INPLACE_OR       
              168  ROT_THREE        
              170  STORE_SUBSCR     

 L. 108       172  LOAD_FAST                'efuse_mask_data'
              174  LOAD_CONST               92
              176  DUP_TOP_TWO      
              178  BINARY_SUBSCR    
              180  LOAD_CONST               255
              182  INPLACE_OR       
              184  ROT_THREE        
              186  STORE_SUBSCR     
            188_0  COME_FROM           150  '150'

 L. 110       188  LOAD_FAST                'flash_encryp_type'
              190  LOAD_CONST               0
              192  COMPARE_OP               >
              194  POP_JUMP_IF_FALSE   212  'to 212'

 L. 111       196  LOAD_FAST                'efuse_data'
              198  LOAD_CONST               0
              200  DUP_TOP_TWO      
              202  BINARY_SUBSCR    
              204  LOAD_CONST               48
              206  INPLACE_OR       
              208  ROT_THREE        
              210  STORE_SUBSCR     
            212_0  COME_FROM           194  '194'

 L. 112       212  LOAD_FAST                'efuse_mask_data'
              214  LOAD_CONST               0
              216  DUP_TOP_TWO      
              218  BINARY_SUBSCR    
              220  LOAD_CONST               255
              222  INPLACE_OR       
              224  ROT_THREE        
              226  STORE_SUBSCR     

 L. 113       228  LOAD_CONST               0
              230  STORE_FAST               'rw_lock0'

 L. 114       232  LOAD_CONST               0
              234  STORE_FAST               'rw_lock1'

 L. 115       236  LOAD_FAST                'pk_hash'
              238  LOAD_CONST               None
              240  COMPARE_OP               is-not
          242_244  POP_JUMP_IF_FALSE   298  'to 298'

 L. 116       246  LOAD_FAST                'pk_hash'
              248  LOAD_FAST                'efuse_data'
              250  LOAD_GLOBAL              keyslot0
              252  LOAD_GLOBAL              keyslot2
              254  BUILD_SLICE_2         2 
              256  STORE_SUBSCR     

 L. 117       258  LOAD_FAST                'mask_4bytes'
              260  LOAD_CONST               8
              262  BINARY_MULTIPLY  
              264  LOAD_FAST                'efuse_mask_data'
              266  LOAD_GLOBAL              keyslot0
              268  LOAD_GLOBAL              keyslot2
              270  BUILD_SLICE_2         2 
              272  STORE_SUBSCR     

 L. 118       274  LOAD_FAST                'rw_lock0'
              276  LOAD_CONST               1
              278  LOAD_GLOBAL              wr_lock_key_slot_0
              280  BINARY_LSHIFT    
              282  INPLACE_OR       
              284  STORE_FAST               'rw_lock0'

 L. 119       286  LOAD_FAST                'rw_lock0'
              288  LOAD_CONST               1
              290  LOAD_GLOBAL              wr_lock_key_slot_1
              292  BINARY_LSHIFT    
              294  INPLACE_OR       
              296  STORE_FAST               'rw_lock0'
            298_0  COME_FROM           242  '242'

 L. 120       298  LOAD_FAST                'flash_key'
              300  LOAD_CONST               None
              302  COMPARE_OP               is-not
          304_306  POP_JUMP_IF_FALSE   590  'to 590'

 L. 121       308  LOAD_FAST                'flash_encryp_type'
              310  LOAD_CONST               1
              312  COMPARE_OP               ==
          314_316  POP_JUMP_IF_FALSE   356  'to 356'

 L. 123       318  LOAD_FAST                'flash_key'
              320  LOAD_CONST               0
              322  LOAD_CONST               16
              324  BUILD_SLICE_2         2 
              326  BINARY_SUBSCR    
              328  LOAD_FAST                'efuse_data'
              330  LOAD_GLOBAL              keyslot2
              332  LOAD_GLOBAL              keyslot3
              334  BUILD_SLICE_2         2 
              336  STORE_SUBSCR     

 L. 124       338  LOAD_FAST                'mask_4bytes'
              340  LOAD_CONST               4
              342  BINARY_MULTIPLY  
              344  LOAD_FAST                'efuse_mask_data'
              346  LOAD_GLOBAL              keyslot2
              348  LOAD_GLOBAL              keyslot3
              350  BUILD_SLICE_2         2 
              352  STORE_SUBSCR     
              354  JUMP_FORWARD        566  'to 566'
            356_0  COME_FROM           314  '314'

 L. 125       356  LOAD_FAST                'flash_encryp_type'
              358  LOAD_CONST               2
              360  COMPARE_OP               ==
          362_364  POP_JUMP_IF_FALSE   420  'to 420'

 L. 127       366  LOAD_FAST                'flash_key'
              368  LOAD_FAST                'efuse_data'
              370  LOAD_GLOBAL              keyslot2
              372  LOAD_GLOBAL              keyslot3_end
              374  BUILD_SLICE_2         2 
              376  STORE_SUBSCR     

 L. 128       378  LOAD_FAST                'mask_4bytes'
              380  LOAD_CONST               8
              382  BINARY_MULTIPLY  
              384  LOAD_FAST                'efuse_mask_data'
              386  LOAD_GLOBAL              keyslot2
              388  LOAD_GLOBAL              keyslot3_end
              390  BUILD_SLICE_2         2 
              392  STORE_SUBSCR     

 L. 129       394  LOAD_FAST                'rw_lock0'
              396  LOAD_CONST               1
              398  LOAD_GLOBAL              wr_lock_key_slot_3
              400  BINARY_LSHIFT    
              402  INPLACE_OR       
              404  STORE_FAST               'rw_lock0'

 L. 130       406  LOAD_FAST                'rw_lock0'
              408  LOAD_CONST               1
              410  LOAD_GLOBAL              rd_lock_key_slot_3
              412  BINARY_LSHIFT    
              414  INPLACE_OR       
              416  STORE_FAST               'rw_lock0'
              418  JUMP_FORWARD        566  'to 566'
            420_0  COME_FROM           362  '362'

 L. 131       420  LOAD_FAST                'flash_encryp_type'
              422  LOAD_CONST               3
              424  COMPARE_OP               ==
          426_428  POP_JUMP_IF_FALSE   484  'to 484'

 L. 133       430  LOAD_FAST                'flash_key'
              432  LOAD_FAST                'efuse_data'
              434  LOAD_GLOBAL              keyslot2
              436  LOAD_GLOBAL              keyslot3_end
              438  BUILD_SLICE_2         2 
              440  STORE_SUBSCR     

 L. 134       442  LOAD_FAST                'mask_4bytes'
              444  LOAD_CONST               8
              446  BINARY_MULTIPLY  
              448  LOAD_FAST                'efuse_mask_data'
              450  LOAD_GLOBAL              keyslot2
              452  LOAD_GLOBAL              keyslot3_end
              454  BUILD_SLICE_2         2 
              456  STORE_SUBSCR     

 L. 135       458  LOAD_FAST                'rw_lock0'
              460  LOAD_CONST               1
              462  LOAD_GLOBAL              wr_lock_key_slot_3
              464  BINARY_LSHIFT    
              466  INPLACE_OR       
              468  STORE_FAST               'rw_lock0'

 L. 136       470  LOAD_FAST                'rw_lock0'
              472  LOAD_CONST               1
              474  LOAD_GLOBAL              rd_lock_key_slot_3
              476  BINARY_LSHIFT    
              478  INPLACE_OR       
              480  STORE_FAST               'rw_lock0'
              482  JUMP_FORWARD        566  'to 566'
            484_0  COME_FROM           426  '426'

 L. 137       484  LOAD_FAST                'flash_encryp_type'
              486  LOAD_CONST               4
              488  COMPARE_OP               ==
          490_492  POP_JUMP_IF_TRUE    514  'to 514'

 L. 138       494  LOAD_FAST                'flash_encryp_type'
              496  LOAD_CONST               5
              498  COMPARE_OP               ==
          500_502  POP_JUMP_IF_TRUE    514  'to 514'

 L. 139       504  LOAD_FAST                'flash_encryp_type'
              506  LOAD_CONST               6
              508  COMPARE_OP               ==
          510_512  POP_JUMP_IF_FALSE   566  'to 566'
            514_0  COME_FROM           500  '500'
            514_1  COME_FROM           490  '490'

 L. 141       514  LOAD_FAST                'flash_key'
              516  LOAD_FAST                'efuse_data'
              518  LOAD_GLOBAL              keyslot2
              520  LOAD_GLOBAL              keyslot3_end
              522  BUILD_SLICE_2         2 
              524  STORE_SUBSCR     

 L. 142       526  LOAD_FAST                'mask_4bytes'
              528  LOAD_CONST               8
              530  BINARY_MULTIPLY  
              532  LOAD_FAST                'efuse_mask_data'
              534  LOAD_GLOBAL              keyslot2
              536  LOAD_GLOBAL              keyslot3_end
              538  BUILD_SLICE_2         2 
              540  STORE_SUBSCR     

 L. 143       542  LOAD_FAST                'rw_lock0'
              544  LOAD_CONST               1
              546  LOAD_GLOBAL              wr_lock_key_slot_3
              548  BINARY_LSHIFT    
              550  INPLACE_OR       
              552  STORE_FAST               'rw_lock0'

 L. 144       554  LOAD_FAST                'rw_lock0'
              556  LOAD_CONST               1
              558  LOAD_GLOBAL              rd_lock_key_slot_3
              560  BINARY_LSHIFT    
              562  INPLACE_OR       
              564  STORE_FAST               'rw_lock0'
            566_0  COME_FROM           510  '510'
            566_1  COME_FROM           482  '482'
            566_2  COME_FROM           418  '418'
            566_3  COME_FROM           354  '354'

 L. 146       566  LOAD_FAST                'rw_lock0'
              568  LOAD_CONST               1
              570  LOAD_GLOBAL              wr_lock_key_slot_2
              572  BINARY_LSHIFT    
              574  INPLACE_OR       
              576  STORE_FAST               'rw_lock0'

 L. 147       578  LOAD_FAST                'rw_lock0'
              580  LOAD_CONST               1
              582  LOAD_GLOBAL              rd_lock_key_slot_2
              584  BINARY_LSHIFT    
              586  INPLACE_OR       
              588  STORE_FAST               'rw_lock0'
            590_0  COME_FROM           304  '304'

 L. 149       590  LOAD_FAST                'sec_eng_key'
              592  LOAD_CONST               None
              594  COMPARE_OP               is-not
          596_598  POP_JUMP_IF_FALSE  1930  'to 1930'

 L. 150       600  LOAD_FAST                'flash_encryp_type'
              602  LOAD_CONST               0
              604  COMPARE_OP               ==
          606_608  POP_JUMP_IF_FALSE  1082  'to 1082'

 L. 151       610  LOAD_FAST                'sec_eng_key_sel'
              612  LOAD_CONST               0
              614  COMPARE_OP               ==
          616_618  POP_JUMP_IF_FALSE   724  'to 724'

 L. 152       620  LOAD_FAST                'sec_eng_key'
              622  LOAD_CONST               16
              624  LOAD_CONST               32
              626  BUILD_SLICE_2         2 
              628  BINARY_SUBSCR    
              630  LOAD_FAST                'efuse_data'
              632  LOAD_GLOBAL              keyslot2
              634  LOAD_GLOBAL              keyslot3
              636  BUILD_SLICE_2         2 
              638  STORE_SUBSCR     

 L. 153       640  LOAD_FAST                'sec_eng_key'
              642  LOAD_CONST               0
              644  LOAD_CONST               16
              646  BUILD_SLICE_2         2 
              648  BINARY_SUBSCR    
              650  LOAD_FAST                'efuse_data'
              652  LOAD_GLOBAL              keyslot3
              654  LOAD_GLOBAL              keyslot3_end
              656  BUILD_SLICE_2         2 
              658  STORE_SUBSCR     

 L. 154       660  LOAD_FAST                'mask_4bytes'
              662  LOAD_CONST               8
              664  BINARY_MULTIPLY  
              666  LOAD_FAST                'efuse_mask_data'
              668  LOAD_GLOBAL              keyslot2
              670  LOAD_GLOBAL              keyslot3_end
              672  BUILD_SLICE_2         2 
              674  STORE_SUBSCR     

 L. 155       676  LOAD_FAST                'rw_lock0'
              678  LOAD_CONST               1
              680  LOAD_GLOBAL              wr_lock_key_slot_2
              682  BINARY_LSHIFT    
              684  INPLACE_OR       
              686  STORE_FAST               'rw_lock0'

 L. 156       688  LOAD_FAST                'rw_lock0'
              690  LOAD_CONST               1
              692  LOAD_GLOBAL              wr_lock_key_slot_3
              694  BINARY_LSHIFT    
              696  INPLACE_OR       
              698  STORE_FAST               'rw_lock0'

 L. 157       700  LOAD_FAST                'rw_lock0'
              702  LOAD_CONST               1
              704  LOAD_GLOBAL              rd_lock_key_slot_2
              706  BINARY_LSHIFT    
              708  INPLACE_OR       
              710  STORE_FAST               'rw_lock0'

 L. 158       712  LOAD_FAST                'rw_lock0'
              714  LOAD_CONST               1
              716  LOAD_GLOBAL              rd_lock_key_slot_3
              718  BINARY_LSHIFT    
              720  INPLACE_OR       
              722  STORE_FAST               'rw_lock0'
            724_0  COME_FROM           616  '616'

 L. 159       724  LOAD_FAST                'sec_eng_key_sel'
              726  LOAD_CONST               1
              728  COMPARE_OP               ==
          730_732  POP_JUMP_IF_FALSE   854  'to 854'

 L. 160       734  LOAD_FAST                'sec_eng_key'
              736  LOAD_CONST               16
              738  LOAD_CONST               32
              740  BUILD_SLICE_2         2 
              742  BINARY_SUBSCR    
              744  LOAD_FAST                'efuse_data'
              746  LOAD_GLOBAL              keyslot3
              748  LOAD_GLOBAL              keyslot3_end
              750  BUILD_SLICE_2         2 
              752  STORE_SUBSCR     

 L. 161       754  LOAD_FAST                'sec_eng_key'
              756  LOAD_CONST               0
              758  LOAD_CONST               16
              760  BUILD_SLICE_2         2 
              762  BINARY_SUBSCR    
              764  LOAD_FAST                'efuse_data'
              766  LOAD_GLOBAL              keyslot4
              768  LOAD_GLOBAL              keyslot5
              770  BUILD_SLICE_2         2 
              772  STORE_SUBSCR     

 L. 162       774  LOAD_FAST                'mask_4bytes'
              776  LOAD_CONST               4
              778  BINARY_MULTIPLY  
              780  LOAD_FAST                'efuse_mask_data'
              782  LOAD_GLOBAL              keyslot3
              784  LOAD_GLOBAL              keyslot3_end
              786  BUILD_SLICE_2         2 
              788  STORE_SUBSCR     

 L. 163       790  LOAD_FAST                'mask_4bytes'
              792  LOAD_CONST               4
              794  BINARY_MULTIPLY  
              796  LOAD_FAST                'efuse_mask_data'
              798  LOAD_GLOBAL              keyslot4
              800  LOAD_GLOBAL              keyslot5
              802  BUILD_SLICE_2         2 
              804  STORE_SUBSCR     

 L. 164       806  LOAD_FAST                'rw_lock0'
              808  LOAD_CONST               1
              810  LOAD_GLOBAL              wr_lock_key_slot_3
              812  BINARY_LSHIFT    
              814  INPLACE_OR       
              816  STORE_FAST               'rw_lock0'

 L. 165       818  LOAD_FAST                'rw_lock1'
              820  LOAD_CONST               1
              822  LOAD_GLOBAL              wr_lock_key_slot_4
              824  BINARY_LSHIFT    
              826  INPLACE_OR       
              828  STORE_FAST               'rw_lock1'

 L. 166       830  LOAD_FAST                'rw_lock0'
              832  LOAD_CONST               1
              834  LOAD_GLOBAL              rd_lock_key_slot_3
              836  BINARY_LSHIFT    
              838  INPLACE_OR       
              840  STORE_FAST               'rw_lock0'

 L. 167       842  LOAD_FAST                'rw_lock1'
              844  LOAD_CONST               1
              846  LOAD_GLOBAL              rd_lock_key_slot_4
              848  BINARY_LSHIFT    
              850  INPLACE_OR       
              852  STORE_FAST               'rw_lock1'
            854_0  COME_FROM           730  '730'

 L. 168       854  LOAD_FAST                'sec_eng_key_sel'
              856  LOAD_CONST               2
              858  COMPARE_OP               ==
          860_862  POP_JUMP_IF_FALSE   968  'to 968'

 L. 169       864  LOAD_FAST                'sec_eng_key'
              866  LOAD_CONST               16
              868  LOAD_CONST               32
              870  BUILD_SLICE_2         2 
              872  BINARY_SUBSCR    
              874  LOAD_FAST                'efuse_data'
              876  LOAD_GLOBAL              keyslot4
              878  LOAD_GLOBAL              keyslot5
              880  BUILD_SLICE_2         2 
              882  STORE_SUBSCR     

 L. 170       884  LOAD_FAST                'sec_eng_key'
              886  LOAD_CONST               0
              888  LOAD_CONST               16
              890  BUILD_SLICE_2         2 
              892  BINARY_SUBSCR    
              894  LOAD_FAST                'efuse_data'
              896  LOAD_GLOBAL              keyslot2
              898  LOAD_GLOBAL              keyslot3
              900  BUILD_SLICE_2         2 
              902  STORE_SUBSCR     

 L. 171       904  LOAD_FAST                'mask_4bytes'
              906  LOAD_CONST               8
              908  BINARY_MULTIPLY  
              910  LOAD_FAST                'efuse_mask_data'
              912  LOAD_GLOBAL              keyslot3
              914  LOAD_GLOBAL              keyslot5
              916  BUILD_SLICE_2         2 
              918  STORE_SUBSCR     

 L. 172       920  LOAD_FAST                'rw_lock1'
              922  LOAD_CONST               1
              924  LOAD_GLOBAL              wr_lock_key_slot_4
              926  BINARY_LSHIFT    
              928  INPLACE_OR       
              930  STORE_FAST               'rw_lock1'

 L. 173       932  LOAD_FAST                'rw_lock0'
              934  LOAD_CONST               1
              936  LOAD_GLOBAL              wr_lock_key_slot_2
              938  BINARY_LSHIFT    
              940  INPLACE_OR       
              942  STORE_FAST               'rw_lock0'

 L. 174       944  LOAD_FAST                'rw_lock1'
              946  LOAD_CONST               1
              948  LOAD_GLOBAL              rd_lock_key_slot_4
              950  BINARY_LSHIFT    
              952  INPLACE_OR       
              954  STORE_FAST               'rw_lock1'

 L. 175       956  LOAD_FAST                'rw_lock0'
              958  LOAD_CONST               1
              960  LOAD_GLOBAL              rd_lock_key_slot_2
              962  BINARY_LSHIFT    
              964  INPLACE_OR       
              966  STORE_FAST               'rw_lock0'
            968_0  COME_FROM           860  '860'

 L. 176       968  LOAD_FAST                'sec_eng_key_sel'
              970  LOAD_CONST               3
              972  COMPARE_OP               ==
          974_976  POP_JUMP_IF_FALSE  1082  'to 1082'

 L. 177       978  LOAD_FAST                'sec_eng_key'
              980  LOAD_CONST               16
              982  LOAD_CONST               32
              984  BUILD_SLICE_2         2 
              986  BINARY_SUBSCR    
              988  LOAD_FAST                'efuse_data'
              990  LOAD_GLOBAL              keyslot4
              992  LOAD_GLOBAL              keyslot5
              994  BUILD_SLICE_2         2 
              996  STORE_SUBSCR     

 L. 178       998  LOAD_FAST                'sec_eng_key'
             1000  LOAD_CONST               0
             1002  LOAD_CONST               16
             1004  BUILD_SLICE_2         2 
             1006  BINARY_SUBSCR    
             1008  LOAD_FAST                'efuse_data'
             1010  LOAD_GLOBAL              keyslot2
             1012  LOAD_GLOBAL              keyslot3
             1014  BUILD_SLICE_2         2 
             1016  STORE_SUBSCR     

 L. 179      1018  LOAD_FAST                'mask_4bytes'
             1020  LOAD_CONST               8
             1022  BINARY_MULTIPLY  
             1024  LOAD_FAST                'efuse_mask_data'
             1026  LOAD_GLOBAL              keyslot3
             1028  LOAD_GLOBAL              keyslot5
             1030  BUILD_SLICE_2         2 
             1032  STORE_SUBSCR     

 L. 180      1034  LOAD_FAST                'rw_lock1'
             1036  LOAD_CONST               1
             1038  LOAD_GLOBAL              wr_lock_key_slot_4
             1040  BINARY_LSHIFT    
             1042  INPLACE_OR       
             1044  STORE_FAST               'rw_lock1'

 L. 181      1046  LOAD_FAST                'rw_lock0'
             1048  LOAD_CONST               1
             1050  LOAD_GLOBAL              wr_lock_key_slot_2
             1052  BINARY_LSHIFT    
             1054  INPLACE_OR       
             1056  STORE_FAST               'rw_lock0'

 L. 182      1058  LOAD_FAST                'rw_lock1'
             1060  LOAD_CONST               1
             1062  LOAD_GLOBAL              rd_lock_key_slot_4
             1064  BINARY_LSHIFT    
             1066  INPLACE_OR       
             1068  STORE_FAST               'rw_lock1'

 L. 183      1070  LOAD_FAST                'rw_lock0'
             1072  LOAD_CONST               1
             1074  LOAD_GLOBAL              rd_lock_key_slot_2
             1076  BINARY_LSHIFT    
             1078  INPLACE_OR       
             1080  STORE_FAST               'rw_lock0'
           1082_0  COME_FROM           974  '974'
           1082_1  COME_FROM           606  '606'

 L. 184      1082  LOAD_FAST                'flash_encryp_type'
             1084  LOAD_CONST               1
             1086  COMPARE_OP               ==
         1088_1090  POP_JUMP_IF_FALSE  1396  'to 1396'

 L. 185      1092  LOAD_FAST                'sec_eng_key_sel'
             1094  LOAD_CONST               0
             1096  COMPARE_OP               ==
         1098_1100  POP_JUMP_IF_FALSE  1162  'to 1162'

 L. 186      1102  LOAD_FAST                'sec_eng_key'
             1104  LOAD_CONST               0
             1106  LOAD_CONST               16
             1108  BUILD_SLICE_2         2 
             1110  BINARY_SUBSCR    
             1112  LOAD_FAST                'efuse_data'
             1114  LOAD_GLOBAL              keyslot5
             1116  LOAD_GLOBAL              keyslot6
             1118  BUILD_SLICE_2         2 
             1120  STORE_SUBSCR     

 L. 187      1122  LOAD_FAST                'mask_4bytes'
             1124  LOAD_CONST               4
             1126  BINARY_MULTIPLY  
             1128  LOAD_FAST                'efuse_mask_data'
             1130  LOAD_GLOBAL              keyslot5
             1132  LOAD_GLOBAL              keyslot6
             1134  BUILD_SLICE_2         2 
             1136  STORE_SUBSCR     

 L. 188      1138  LOAD_FAST                'rw_lock1'
             1140  LOAD_CONST               1
             1142  LOAD_GLOBAL              wr_lock_key_slot_5
             1144  BINARY_LSHIFT    
             1146  INPLACE_OR       
             1148  STORE_FAST               'rw_lock1'

 L. 189      1150  LOAD_FAST                'rw_lock1'
             1152  LOAD_CONST               1
             1154  LOAD_GLOBAL              rd_lock_key_slot_5
             1156  BINARY_LSHIFT    
             1158  INPLACE_OR       
             1160  STORE_FAST               'rw_lock1'
           1162_0  COME_FROM          1098  '1098'

 L. 190      1162  LOAD_FAST                'sec_eng_key_sel'
             1164  LOAD_CONST               1
             1166  COMPARE_OP               ==
         1168_1170  POP_JUMP_IF_FALSE  1232  'to 1232'

 L. 191      1172  LOAD_FAST                'sec_eng_key'
             1174  LOAD_CONST               0
             1176  LOAD_CONST               16
             1178  BUILD_SLICE_2         2 
             1180  BINARY_SUBSCR    
             1182  LOAD_FAST                'efuse_data'
             1184  LOAD_GLOBAL              keyslot4
             1186  LOAD_GLOBAL              keyslot5
             1188  BUILD_SLICE_2         2 
             1190  STORE_SUBSCR     

 L. 192      1192  LOAD_FAST                'mask_4bytes'
             1194  LOAD_CONST               4
             1196  BINARY_MULTIPLY  
             1198  LOAD_FAST                'efuse_mask_data'
             1200  LOAD_GLOBAL              keyslot4
             1202  LOAD_GLOBAL              keyslot5
             1204  BUILD_SLICE_2         2 
             1206  STORE_SUBSCR     

 L. 193      1208  LOAD_FAST                'rw_lock1'
             1210  LOAD_CONST               1
             1212  LOAD_GLOBAL              wr_lock_key_slot_4
             1214  BINARY_LSHIFT    
             1216  INPLACE_OR       
             1218  STORE_FAST               'rw_lock1'

 L. 194      1220  LOAD_FAST                'rw_lock1'
             1222  LOAD_CONST               1
             1224  LOAD_GLOBAL              rd_lock_key_slot_4
             1226  BINARY_LSHIFT    
             1228  INPLACE_OR       
             1230  STORE_FAST               'rw_lock1'
           1232_0  COME_FROM          1168  '1168'

 L. 195      1232  LOAD_FAST                'sec_eng_key_sel'
             1234  LOAD_CONST               2
             1236  COMPARE_OP               ==
         1238_1240  POP_JUMP_IF_FALSE  1314  'to 1314'

 L. 196      1242  LOAD_FAST                'flash_key'
             1244  LOAD_CONST               None
             1246  COMPARE_OP               is-not
         1248_1250  POP_JUMP_IF_FALSE  1254  'to 1254'

 L. 198      1252  JUMP_FORWARD       1314  'to 1314'
           1254_0  COME_FROM          1248  '1248'

 L. 200      1254  LOAD_FAST                'sec_eng_key'
             1256  LOAD_CONST               0
             1258  LOAD_CONST               16
             1260  BUILD_SLICE_2         2 
             1262  BINARY_SUBSCR    
             1264  LOAD_FAST                'efuse_data'
             1266  LOAD_GLOBAL              keyslot3
             1268  LOAD_GLOBAL              keyslot3_end
             1270  BUILD_SLICE_2         2 
             1272  STORE_SUBSCR     

 L. 201      1274  LOAD_FAST                'mask_4bytes'
             1276  LOAD_CONST               4
             1278  BINARY_MULTIPLY  
             1280  LOAD_FAST                'efuse_mask_data'
             1282  LOAD_GLOBAL              keyslot3
             1284  LOAD_GLOBAL              keyslot3_end
             1286  BUILD_SLICE_2         2 
             1288  STORE_SUBSCR     

 L. 202      1290  LOAD_FAST                'rw_lock0'
             1292  LOAD_CONST               1
             1294  LOAD_GLOBAL              wr_lock_key_slot_3
             1296  BINARY_LSHIFT    
             1298  INPLACE_OR       
             1300  STORE_FAST               'rw_lock0'

 L. 203      1302  LOAD_FAST                'rw_lock0'
             1304  LOAD_CONST               1
             1306  LOAD_GLOBAL              rd_lock_key_slot_3
             1308  BINARY_LSHIFT    
             1310  INPLACE_OR       
             1312  STORE_FAST               'rw_lock0'
           1314_0  COME_FROM          1252  '1252'
           1314_1  COME_FROM          1238  '1238'

 L. 204      1314  LOAD_FAST                'sec_eng_key_sel'
             1316  LOAD_CONST               3
             1318  COMPARE_OP               ==
         1320_1322  POP_JUMP_IF_FALSE  1396  'to 1396'

 L. 205      1324  LOAD_FAST                'flash_key'
             1326  LOAD_CONST               None
             1328  COMPARE_OP               is-not
         1330_1332  POP_JUMP_IF_FALSE  1336  'to 1336'

 L. 207      1334  JUMP_FORWARD       1396  'to 1396'
           1336_0  COME_FROM          1330  '1330'

 L. 209      1336  LOAD_FAST                'sec_eng_key'
             1338  LOAD_CONST               0
             1340  LOAD_CONST               16
             1342  BUILD_SLICE_2         2 
             1344  BINARY_SUBSCR    
             1346  LOAD_FAST                'efuse_data'
             1348  LOAD_GLOBAL              keyslot2
             1350  LOAD_GLOBAL              keyslot3
             1352  BUILD_SLICE_2         2 
             1354  STORE_SUBSCR     

 L. 210      1356  LOAD_FAST                'mask_4bytes'
             1358  LOAD_CONST               4
             1360  BINARY_MULTIPLY  
             1362  LOAD_FAST                'efuse_mask_data'
             1364  LOAD_GLOBAL              keyslot2
             1366  LOAD_GLOBAL              keyslot3
             1368  BUILD_SLICE_2         2 
             1370  STORE_SUBSCR     

 L. 211      1372  LOAD_FAST                'rw_lock0'
             1374  LOAD_CONST               1
             1376  LOAD_GLOBAL              wr_lock_key_slot_2
             1378  BINARY_LSHIFT    
             1380  INPLACE_OR       
             1382  STORE_FAST               'rw_lock0'

 L. 212      1384  LOAD_FAST                'rw_lock0'
             1386  LOAD_CONST               1
             1388  LOAD_GLOBAL              rd_lock_key_slot_2
             1390  BINARY_LSHIFT    
             1392  INPLACE_OR       
             1394  STORE_FAST               'rw_lock0'
           1396_0  COME_FROM          1334  '1334'
           1396_1  COME_FROM          1320  '1320'
           1396_2  COME_FROM          1088  '1088'

 L. 213      1396  LOAD_FAST                'flash_encryp_type'
             1398  LOAD_CONST               2
             1400  COMPARE_OP               ==
         1402_1404  POP_JUMP_IF_TRUE   1446  'to 1446'

 L. 214      1406  LOAD_FAST                'flash_encryp_type'
             1408  LOAD_CONST               3
             1410  COMPARE_OP               ==
         1412_1414  POP_JUMP_IF_TRUE   1446  'to 1446'

 L. 215      1416  LOAD_FAST                'flash_encryp_type'
             1418  LOAD_CONST               4
             1420  COMPARE_OP               ==
         1422_1424  POP_JUMP_IF_TRUE   1446  'to 1446'

 L. 216      1426  LOAD_FAST                'flash_encryp_type'
             1428  LOAD_CONST               5
             1430  COMPARE_OP               ==
         1432_1434  POP_JUMP_IF_TRUE   1446  'to 1446'

 L. 217      1436  LOAD_FAST                'flash_encryp_type'
             1438  LOAD_CONST               6
             1440  COMPARE_OP               ==
         1442_1444  POP_JUMP_IF_FALSE  1930  'to 1930'
           1446_0  COME_FROM          1432  '1432'
           1446_1  COME_FROM          1422  '1422'
           1446_2  COME_FROM          1412  '1412'
           1446_3  COME_FROM          1402  '1402'

 L. 218      1446  LOAD_FAST                'sec_eng_key_sel'
             1448  LOAD_CONST               0
             1450  COMPARE_OP               ==
         1452_1454  POP_JUMP_IF_FALSE  1576  'to 1576'

 L. 219      1456  LOAD_FAST                'sec_eng_key'
             1458  LOAD_CONST               16
             1460  LOAD_CONST               32
             1462  BUILD_SLICE_2         2 
             1464  BINARY_SUBSCR    
             1466  LOAD_FAST                'efuse_data'
             1468  LOAD_GLOBAL              keyslot6
             1470  LOAD_GLOBAL              keyslot7
             1472  BUILD_SLICE_2         2 
             1474  STORE_SUBSCR     

 L. 220      1476  LOAD_FAST                'sec_eng_key'
             1478  LOAD_CONST               0
             1480  LOAD_CONST               16
             1482  BUILD_SLICE_2         2 
             1484  BINARY_SUBSCR    
             1486  LOAD_FAST                'efuse_data'
             1488  LOAD_GLOBAL              keyslot10
             1490  LOAD_GLOBAL              keyslot10_end
             1492  BUILD_SLICE_2         2 
             1494  STORE_SUBSCR     

 L. 221      1496  LOAD_FAST                'mask_4bytes'
             1498  LOAD_CONST               4
             1500  BINARY_MULTIPLY  
             1502  LOAD_FAST                'efuse_mask_data'
             1504  LOAD_GLOBAL              keyslot6
             1506  LOAD_GLOBAL              keyslot7
             1508  BUILD_SLICE_2         2 
             1510  STORE_SUBSCR     

 L. 222      1512  LOAD_FAST                'mask_4bytes'
             1514  LOAD_CONST               4
             1516  BINARY_MULTIPLY  
             1518  LOAD_FAST                'efuse_mask_data'
             1520  LOAD_GLOBAL              keyslot10
             1522  LOAD_GLOBAL              keyslot10_end
             1524  BUILD_SLICE_2         2 
             1526  STORE_SUBSCR     

 L. 223      1528  LOAD_FAST                'rw_lock1'
             1530  LOAD_CONST               1
             1532  LOAD_GLOBAL              wr_lock_key_slot_6
             1534  BINARY_LSHIFT    
             1536  INPLACE_OR       
             1538  STORE_FAST               'rw_lock1'

 L. 224      1540  LOAD_FAST                'rw_lock1'
             1542  LOAD_CONST               1
             1544  LOAD_GLOBAL              wr_lock_key_slot_10
             1546  BINARY_LSHIFT    
             1548  INPLACE_OR       
             1550  STORE_FAST               'rw_lock1'

 L. 225      1552  LOAD_FAST                'rw_lock1'
             1554  LOAD_CONST               1
             1556  LOAD_GLOBAL              rd_lock_key_slot_6
             1558  BINARY_LSHIFT    
             1560  INPLACE_OR       
             1562  STORE_FAST               'rw_lock1'

 L. 226      1564  LOAD_FAST                'rw_lock1'
             1566  LOAD_CONST               1
             1568  LOAD_GLOBAL              rd_lock_key_slot_10
             1570  BINARY_LSHIFT    
             1572  INPLACE_OR       
             1574  STORE_FAST               'rw_lock1'
           1576_0  COME_FROM          1452  '1452'

 L. 227      1576  LOAD_FAST                'sec_eng_key_sel'
             1578  LOAD_CONST               1
             1580  COMPARE_OP               ==
         1582_1584  POP_JUMP_IF_FALSE  1706  'to 1706'

 L. 228      1586  LOAD_FAST                'sec_eng_key'
             1588  LOAD_CONST               16
             1590  LOAD_CONST               32
             1592  BUILD_SLICE_2         2 
             1594  BINARY_SUBSCR    
             1596  LOAD_FAST                'efuse_data'
             1598  LOAD_GLOBAL              keyslot10
             1600  LOAD_GLOBAL              keyslot10_end
             1602  BUILD_SLICE_2         2 
             1604  STORE_SUBSCR     

 L. 229      1606  LOAD_FAST                'sec_eng_key'
             1608  LOAD_CONST               0
             1610  LOAD_CONST               16
             1612  BUILD_SLICE_2         2 
             1614  BINARY_SUBSCR    
             1616  LOAD_FAST                'efuse_data'
             1618  LOAD_GLOBAL              keyslot6
             1620  LOAD_GLOBAL              keyslot7
             1622  BUILD_SLICE_2         2 
             1624  STORE_SUBSCR     

 L. 230      1626  LOAD_FAST                'mask_4bytes'
             1628  LOAD_CONST               4
             1630  BINARY_MULTIPLY  
             1632  LOAD_FAST                'efuse_mask_data'
             1634  LOAD_GLOBAL              keyslot6
             1636  LOAD_GLOBAL              keyslot7
             1638  BUILD_SLICE_2         2 
             1640  STORE_SUBSCR     

 L. 231      1642  LOAD_FAST                'mask_4bytes'
             1644  LOAD_CONST               4
             1646  BINARY_MULTIPLY  
             1648  LOAD_FAST                'efuse_mask_data'
             1650  LOAD_GLOBAL              keyslot10
             1652  LOAD_GLOBAL              keyslot10_end
             1654  BUILD_SLICE_2         2 
             1656  STORE_SUBSCR     

 L. 232      1658  LOAD_FAST                'rw_lock1'
             1660  LOAD_CONST               1
             1662  LOAD_GLOBAL              wr_lock_key_slot_6
             1664  BINARY_LSHIFT    
             1666  INPLACE_OR       
             1668  STORE_FAST               'rw_lock1'

 L. 233      1670  LOAD_FAST                'rw_lock1'
             1672  LOAD_CONST               1
             1674  LOAD_GLOBAL              wr_lock_key_slot_10
             1676  BINARY_LSHIFT    
             1678  INPLACE_OR       
             1680  STORE_FAST               'rw_lock1'

 L. 234      1682  LOAD_FAST                'rw_lock1'
             1684  LOAD_CONST               1
             1686  LOAD_GLOBAL              rd_lock_key_slot_6
             1688  BINARY_LSHIFT    
             1690  INPLACE_OR       
             1692  STORE_FAST               'rw_lock1'

 L. 235      1694  LOAD_FAST                'rw_lock1'
             1696  LOAD_CONST               1
             1698  LOAD_GLOBAL              rd_lock_key_slot_10
             1700  BINARY_LSHIFT    
             1702  INPLACE_OR       
             1704  STORE_FAST               'rw_lock1'
           1706_0  COME_FROM          1582  '1582'

 L. 236      1706  LOAD_FAST                'sec_eng_key_sel'
             1708  LOAD_CONST               2
             1710  COMPARE_OP               ==
         1712_1714  POP_JUMP_IF_FALSE  1832  'to 1832'

 L. 237      1716  LOAD_FAST                'flash_key'
             1718  LOAD_CONST               None
             1720  COMPARE_OP               is-not
         1722_1724  POP_JUMP_IF_FALSE  1728  'to 1728'

 L. 239      1726  JUMP_FORWARD       1832  'to 1832'
           1728_0  COME_FROM          1722  '1722'

 L. 241      1728  LOAD_FAST                'sec_eng_key'
             1730  LOAD_CONST               16
             1732  LOAD_CONST               32
             1734  BUILD_SLICE_2         2 
             1736  BINARY_SUBSCR    
             1738  LOAD_FAST                'efuse_data'
             1740  LOAD_GLOBAL              keyslot2
             1742  LOAD_GLOBAL              keyslot3
             1744  BUILD_SLICE_2         2 
             1746  STORE_SUBSCR     

 L. 242      1748  LOAD_FAST                'sec_eng_key'
             1750  LOAD_CONST               0
             1752  LOAD_CONST               16
             1754  BUILD_SLICE_2         2 
             1756  BINARY_SUBSCR    
             1758  LOAD_FAST                'efuse_data'
             1760  LOAD_GLOBAL              keyslot3
             1762  LOAD_GLOBAL              keyslot3_end
             1764  BUILD_SLICE_2         2 
             1766  STORE_SUBSCR     

 L. 243      1768  LOAD_FAST                'mask_4bytes'
             1770  LOAD_CONST               8
             1772  BINARY_MULTIPLY  
             1774  LOAD_FAST                'efuse_mask_data'
             1776  LOAD_GLOBAL              keyslot2
             1778  LOAD_GLOBAL              keyslot3_end
             1780  BUILD_SLICE_2         2 
             1782  STORE_SUBSCR     

 L. 244      1784  LOAD_FAST                'rw_lock0'
             1786  LOAD_CONST               1
             1788  LOAD_GLOBAL              wr_lock_key_slot_2
             1790  BINARY_LSHIFT    
             1792  INPLACE_OR       
             1794  STORE_FAST               'rw_lock0'

 L. 245      1796  LOAD_FAST                'rw_lock0'
             1798  LOAD_CONST               1
             1800  LOAD_GLOBAL              rd_lock_key_slot_2
             1802  BINARY_LSHIFT    
             1804  INPLACE_OR       
             1806  STORE_FAST               'rw_lock0'

 L. 246      1808  LOAD_FAST                'rw_lock0'
             1810  LOAD_CONST               1
             1812  LOAD_GLOBAL              wr_lock_key_slot_3
             1814  BINARY_LSHIFT    
             1816  INPLACE_OR       
             1818  STORE_FAST               'rw_lock0'

 L. 247      1820  LOAD_FAST                'rw_lock0'
             1822  LOAD_CONST               1
             1824  LOAD_GLOBAL              rd_lock_key_slot_3
             1826  BINARY_LSHIFT    
             1828  INPLACE_OR       
             1830  STORE_FAST               'rw_lock0'
           1832_0  COME_FROM          1726  '1726'
           1832_1  COME_FROM          1712  '1712'

 L. 248      1832  LOAD_FAST                'sec_eng_key_sel'
             1834  LOAD_CONST               3
             1836  COMPARE_OP               ==
         1838_1840  POP_JUMP_IF_FALSE  1930  'to 1930'

 L. 249      1842  LOAD_FAST                'flash_key'
             1844  LOAD_CONST               None
             1846  COMPARE_OP               is-not
         1848_1850  POP_JUMP_IF_FALSE  1854  'to 1854'

 L. 251      1852  JUMP_FORWARD       1930  'to 1930'
           1854_0  COME_FROM          1848  '1848'

 L. 253      1854  LOAD_FAST                'sec_eng_key'
             1856  LOAD_FAST                'efuse_data'
             1858  LOAD_GLOBAL              keyslot2
             1860  LOAD_GLOBAL              keyslot3_end
             1862  BUILD_SLICE_2         2 
             1864  STORE_SUBSCR     

 L. 254      1866  LOAD_FAST                'mask_4bytes'
             1868  LOAD_CONST               8
             1870  BINARY_MULTIPLY  
             1872  LOAD_FAST                'efuse_mask_data'
             1874  LOAD_GLOBAL              keyslot2
             1876  LOAD_GLOBAL              keyslot3_end
             1878  BUILD_SLICE_2         2 
             1880  STORE_SUBSCR     

 L. 255      1882  LOAD_FAST                'rw_lock0'
             1884  LOAD_CONST               1
             1886  LOAD_GLOBAL              wr_lock_key_slot_2
             1888  BINARY_LSHIFT    
             1890  INPLACE_OR       
             1892  STORE_FAST               'rw_lock0'

 L. 256      1894  LOAD_FAST                'rw_lock0'
             1896  LOAD_CONST               1
             1898  LOAD_GLOBAL              rd_lock_key_slot_2
             1900  BINARY_LSHIFT    
             1902  INPLACE_OR       
             1904  STORE_FAST               'rw_lock0'

 L. 257      1906  LOAD_FAST                'rw_lock0'
             1908  LOAD_CONST               1
             1910  LOAD_GLOBAL              wr_lock_key_slot_3
             1912  BINARY_LSHIFT    
             1914  INPLACE_OR       
             1916  STORE_FAST               'rw_lock0'

 L. 258      1918  LOAD_FAST                'rw_lock0'
             1920  LOAD_CONST               1
             1922  LOAD_GLOBAL              rd_lock_key_slot_3
             1924  BINARY_LSHIFT    
             1926  INPLACE_OR       
             1928  STORE_FAST               'rw_lock0'
           1930_0  COME_FROM          1852  '1852'
           1930_1  COME_FROM          1838  '1838'
           1930_2  COME_FROM          1442  '1442'
           1930_3  COME_FROM           596  '596'

 L. 260      1930  LOAD_GLOBAL              bytearray_data_merge
             1932  LOAD_FAST                'efuse_data'
             1934  LOAD_CONST               124
             1936  LOAD_CONST               128
             1938  BUILD_SLICE_2         2 
             1940  BINARY_SUBSCR    

 L. 261      1942  LOAD_GLOBAL              bflb_utils
             1944  LOAD_METHOD              int_to_4bytearray_l
             1946  LOAD_FAST                'rw_lock0'
             1948  CALL_METHOD_1         1  '1 positional argument'
             1950  LOAD_CONST               4
             1952  CALL_FUNCTION_3       3  '3 positional arguments'
             1954  LOAD_FAST                'efuse_data'
             1956  LOAD_CONST               124
             1958  LOAD_CONST               128
             1960  BUILD_SLICE_2         2 
             1962  STORE_SUBSCR     

 L. 262      1964  LOAD_GLOBAL              bytearray_data_merge
             1966  LOAD_FAST                'efuse_mask_data'
             1968  LOAD_CONST               124
             1970  LOAD_CONST               128
             1972  BUILD_SLICE_2         2 
             1974  BINARY_SUBSCR    

 L. 263      1976  LOAD_GLOBAL              bflb_utils
             1978  LOAD_METHOD              int_to_4bytearray_l
             1980  LOAD_FAST                'rw_lock0'
             1982  CALL_METHOD_1         1  '1 positional argument'
             1984  LOAD_CONST               4
             1986  CALL_FUNCTION_3       3  '3 positional arguments'
             1988  LOAD_FAST                'efuse_mask_data'
             1990  LOAD_CONST               124
             1992  LOAD_CONST               128
             1994  BUILD_SLICE_2         2 
             1996  STORE_SUBSCR     

 L. 264      1998  LOAD_GLOBAL              bytearray_data_merge
             2000  LOAD_FAST                'efuse_data'
             2002  LOAD_CONST               252
             2004  LOAD_CONST               256
             2006  BUILD_SLICE_2         2 
             2008  BINARY_SUBSCR    

 L. 265      2010  LOAD_GLOBAL              bflb_utils
             2012  LOAD_METHOD              int_to_4bytearray_l
             2014  LOAD_FAST                'rw_lock1'
             2016  CALL_METHOD_1         1  '1 positional argument'
             2018  LOAD_CONST               4
             2020  CALL_FUNCTION_3       3  '3 positional arguments'
             2022  LOAD_FAST                'efuse_data'
             2024  LOAD_CONST               252
             2026  LOAD_CONST               256
             2028  BUILD_SLICE_2         2 
             2030  STORE_SUBSCR     

 L. 266      2032  LOAD_GLOBAL              bytearray_data_merge
             2034  LOAD_FAST                'efuse_mask_data'
             2036  LOAD_CONST               252
             2038  LOAD_CONST               256
             2040  BUILD_SLICE_2         2 
             2042  BINARY_SUBSCR    

 L. 267      2044  LOAD_GLOBAL              bflb_utils
             2046  LOAD_METHOD              int_to_4bytearray_l
             2048  LOAD_FAST                'rw_lock1'
             2050  CALL_METHOD_1         1  '1 positional argument'
             2052  LOAD_CONST               4
             2054  CALL_FUNCTION_3       3  '3 positional arguments'
             2056  LOAD_FAST                'efuse_mask_data'
             2058  LOAD_CONST               252
             2060  LOAD_CONST               256
             2062  BUILD_SLICE_2         2 
             2064  STORE_SUBSCR     

 L. 269      2066  LOAD_FAST                'security'
             2068  LOAD_CONST               True
             2070  COMPARE_OP               is
         2072_2074  POP_JUMP_IF_FALSE  2124  'to 2124'

 L. 270      2076  LOAD_GLOBAL              bflb_utils
             2078  LOAD_METHOD              printf
             2080  LOAD_STR                 'Encrypt efuse data'
             2082  CALL_METHOD_1         1  '1 positional argument'
             2084  POP_TOP          

 L. 271      2086  LOAD_GLOBAL              bflb_utils
             2088  LOAD_METHOD              get_security_key
             2090  CALL_METHOD_0         0  '0 positional arguments'
             2092  UNPACK_SEQUENCE_2     2 
             2094  STORE_FAST               'security_key'
             2096  STORE_FAST               'security_iv'

 L. 272      2098  LOAD_GLOBAL              img_create_encrypt_data
             2100  LOAD_FAST                'efuse_data'
             2102  LOAD_FAST                'security_key'
             2104  LOAD_FAST                'security_iv'
             2106  LOAD_CONST               0
             2108  CALL_FUNCTION_4       4  '4 positional arguments'
             2110  STORE_FAST               'efuse_data'

 L. 273      2112  LOAD_GLOBAL              bytearray
             2114  LOAD_CONST               4096
             2116  CALL_FUNCTION_1       1  '1 positional argument'
             2118  LOAD_FAST                'efuse_data'
             2120  BINARY_ADD       
             2122  STORE_FAST               'efuse_data'
           2124_0  COME_FROM          2072  '2072'

 L. 274      2124  LOAD_GLOBAL              open
             2126  LOAD_FAST                'cfg'
             2128  LOAD_METHOD              get
             2130  LOAD_STR                 'Img_Group0_Cfg'
             2132  LOAD_STR                 'efuse_file'
             2134  CALL_METHOD_2         2  '2 positional arguments'
             2136  LOAD_STR                 'wb+'
             2138  CALL_FUNCTION_2       2  '2 positional arguments'
             2140  STORE_FAST               'fp'

 L. 275      2142  LOAD_FAST                'fp'
             2144  LOAD_METHOD              write
             2146  LOAD_FAST                'efuse_data'
             2148  CALL_METHOD_1         1  '1 positional argument'
             2150  POP_TOP          

 L. 276      2152  LOAD_FAST                'fp'
             2154  LOAD_METHOD              close
             2156  CALL_METHOD_0         0  '0 positional arguments'
             2158  POP_TOP          

 L. 277      2160  LOAD_GLOBAL              open
             2162  LOAD_FAST                'cfg'
             2164  LOAD_METHOD              get
             2166  LOAD_STR                 'Img_Group0_Cfg'
             2168  LOAD_STR                 'efuse_mask_file'
             2170  CALL_METHOD_2         2  '2 positional arguments'
             2172  LOAD_STR                 'wb+'
             2174  CALL_FUNCTION_2       2  '2 positional arguments'
             2176  STORE_FAST               'fp'

 L. 278      2178  LOAD_FAST                'fp'
             2180  LOAD_METHOD              write
             2182  LOAD_FAST                'efuse_mask_data'
             2184  CALL_METHOD_1         1  '1 positional argument'
             2186  POP_TOP          

 L. 279      2188  LOAD_FAST                'fp'
             2190  LOAD_METHOD              close
             2192  CALL_METHOD_0         0  '0 positional arguments'
             2194  POP_TOP          

Parse error at or near `CALL_METHOD_0' instruction at offset 2192


def img_create_get_sign_encrypt_info(bootheader_data):
    sign = bootheader_data[bootcfg_start] & 3
    encrypt = bootheader_data[bootcfg_start] >> 2 & 3
    key_sel = bootheader_data[bootcfg_start] >> 4 & 3
    xts_mode = bootheader_data[bootcfg_start] >> 6 & 1
    return (sign, encrypt, key_sel, xts_mode)


def img_create_get_img_start_addr(bootheader_data):
    bootentry = []
    bootentry.append(bflb_utils.bytearray_to_int(bflb_utils.bytearray_reverse(bootheader_data[bootcpucfg_start + bootcpucfg_length * bootcpucfg_m0_index_number + 16:bootcpucfg_start + bootcpucfg_length * bootcpucfg_m0_index_number + 16 + 4])))
    return bootentry


def img_create_flash_default_data(length):
    datas = bytearray(length)
    for i in range(length):
        datas[i] = 255

    return datas


def img_get_file_data(files):
    datas = []
    for file in files:
        if file == 'UNUSED':
            datas.append(bytearray(0))
            continue
        with open(file, 'rb') as (fp):
            data = fp.read()
        datas.append(data)

    return datas


def img_get_largest_addr(addrs, files):
    min = 67108863
    maxlen = 0
    datalen = 0
    for i in range(len(addrs)):
        if files[i] == 'UNUSED':
            continue
        addr = addrs[i] & 67108863
        if addr >= maxlen:
            maxlen = addr
            datalen = os.path.getsize(files[i])
        if addr <= min:
            min = addr

    if maxlen == 0:
        if datalen == 0:
            return (0, 0)
    return (
     maxlen + datalen - min, min)


def img_get_one_group_img(d_addrs, d_files):
    whole_img_len, min = img_get_largest_addr(d_addrs, d_files)
    whole_img_len &= 67108863
    whole_img_data = img_create_flash_default_data(whole_img_len)
    filedatas = img_get_file_data(d_files)
    for i in range(len(d_addrs)):
        if d_files[i] == 'UNUSED':
            continue
        start_addr = d_addrs[i]
        start_addr &= 67108863
        start_addr -= min
        whole_img_data[start_addr:start_addr + len(filedatas[i])] = filedatas[i]

    return whole_img_data


def img_create_get_hash_ignore(bootheader_data):
    return bootheader_data[bootcfg_start + 2] >> 1 & 1


def img_create_get_crc_ignore(bootheader_data):
    return bootheader_data[bootcfg_start + 2] & 1


def img_create_update_bootheader_if(bootheader_data, hash, seg_cnt):
    bootheader_data[bootcfg_start + 12:bootcfg_start + 12 + 4] = bflb_utils.int_to_4bytearray_l(seg_cnt)
    sign = bootheader_data[bootcfg_start] & 3
    encrypt = bootheader_data[bootcfg_start] >> 2 & 3
    key_sel = bootheader_data[bootcfg_start] >> 4 & 3
    xts_mode = bootheader_data[bootcfg_start] >> 6 & 1
    if bootheader_data[bootcfg_start + 2] >> 1 & 1 == 1 and sign == 0:
        bflb_utils.printf('Hash ignored')
    else:
        bootheader_data[bootcfg_start + 16:bootcfg_start + 16 + 32] = hash
    if bootheader_data[bootcfg_start + 2] & 1 == 1:
        bflb_utils.printf('Header crc ignored')
    else:
        hd_crcarray = bflb_utils.get_crc32_bytearray(bootheader_data[custom_cfg_len:header_len - 4])
        bootheader_data[header_len - 4:header_len] = hd_crcarray
        bflb_utils.printf('Header crc: ', binascii.hexlify(hd_crcarray))
    return bootheader_data


def img_create_update_custom_bootheader(bootheader_data, seg_cnt, hash, signature, pk_data, aesiv_data):
    bootheader_data[20:24] = bflb_utils.int_to_4bytearray_l(seg_cnt)
    if hash != bytearray(0):
        bootheader_data[28:60] = hash
    if signature != bytearray(0):
        bootheader_data[60:124] = signature[4:68]
    if pk_data != bytearray(0):
        bootheader_data[124:188] = pk_data[0:64]
    if aesiv_data != bytearray(0):
        bootheader_data[188:204] = aesiv_data[0:16]
    bootheader_data[4:8] = bflb_utils.get_crc32_bytearray(bootheader_data[8:custom_cfg_len - 4])
    return bootheader_data[0:header_len]


def img_create_update_bootheader(bootheader_data, hash, seg_cnt, flashcfg_table_addr, flashcfg_table_len):
    bootheader_data[flashcfg_table_start:flashcfg_table_start + 4] = bflb_utils.int_to_4bytearray_l(flashcfg_table_addr)
    bootheader_data[flashcfg_table_start + 4:flashcfg_table_start + 8] = bflb_utils.int_to_4bytearray_l(flashcfg_table_len)
    bootheader_data[bootcfg_start + 12:bootcfg_start + 12 + 4] = bflb_utils.int_to_4bytearray_l(seg_cnt)
    sign, encrypt, key_sel, xts_mode = img_create_get_sign_encrypt_info(bootheader_data)
    if img_create_get_hash_ignore(bootheader_data) == 1 and sign == 0:
        bflb_utils.printf('Hash ignored')
    else:
        bootheader_data[bootcfg_start + 16:bootcfg_start + 16 + 32] = hash
    if img_create_get_crc_ignore(bootheader_data) == 1:
        bflb_utils.printf('Header crc ignored')
    else:
        hd_crcarray = bflb_utils.get_crc32_bytearray(bootheader_data[custom_cfg_len:header_len - 4])
        bootheader_data[header_len - 4:header_len] = hd_crcarray
        bflb_utils.printf('Header crc: ', binascii.hexlify(hd_crcarray))
    return bootheader_data[0:header_len]


def img_create_update_segheader(segheader, segdatalen, segdatacrc):
    segheader[4:8] = segdatalen
    segheader[8:12] = segdatacrc
    return segheader


def reverse_str_data_unit_number(str_data_unit_number):
    """
    high position low data
    data unit number:00000280
    storage format:  80020000
    """
    reverse_str = ''
    if len(str_data_unit_number) == 8:
        str_part1 = str_data_unit_number[0:2]
        str_part2 = str_data_unit_number[2:4]
        str_part3 = str_data_unit_number[4:6]
        str_part4 = str_data_unit_number[6:8]
        reverse_str = str_part4 + str_part3 + str_part2 + str_part1
    return reverse_str


def reverse_iv(need_reverse_iv_bytearray):
    temp_reverse_iv_bytearray = binascii.hexlify(need_reverse_iv_bytearray).decode()
    if temp_reverse_iv_bytearray[24:32] != '00000000':
        bflb_utils.printf('The lower 4 bytes of IV should be set 0, if set IV is less than 16 bytes, make up 0 for the low 4 bytes of IV ')
        sys.exit()
    reverse_iv_bytearray = '00000000' + temp_reverse_iv_bytearray[0:24]
    return reverse_iv_bytearray


def img_create_encrypt_data_xts(data_bytearray, key_bytearray, iv_bytearray, encrypt):
    counter = binascii.hexlify(iv_bytearray[4:16]).decode()
    data_unit_number = 0
    key = (
     key_bytearray[0:16], key_bytearray[16:32])
    if encrypt == 2 or encrypt == 3:
        key = (
         key_bytearray, key_bytearray)
    cipher = AES_XTS.new(key, AES_XTS.MODE_XTS)
    total_len = len(data_bytearray)
    ciphertext = bytearray(0)
    deal_len = 0
    while deal_len < total_len:
        data_unit_number = str(hex(data_unit_number)).replace('0x', '')
        data_unit_number_to_str = str(data_unit_number)
        right_justify_str = data_unit_number_to_str.rjust(8, '0')
        reverse_data_unit_number_str = reverse_str_data_unit_number(right_justify_str)
        tweak = reverse_data_unit_number_str + counter
        tweak = bflb_utils.hexstr_to_bytearray('0' * (32 - len(tweak)) + tweak)
        if 32 + deal_len <= total_len:
            cur_block = data_bytearray[0 + deal_len:32 + deal_len]
            ciphertext += cipher.encrypt(cur_block, tweak)
        else:
            cur_block = data_bytearray[0 + deal_len:16 + deal_len] + bytearray(16)
            ciphertext += cipher.encrypt(cur_block, tweak)[0:16]
        deal_len += 32
        data_unit_number = int(data_unit_number, 16)
        data_unit_number += 1

    return ciphertext


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
        offset = bootcfg_start
        sign_pos = 0
        encrypt_type_pos = 2
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
                    encrypt_key = bflb_utils.hexstr_to_bytearray(cfg.get('Img_Group0_Cfg', 'aes_key_org'))
                    encrypt_iv = bflb_utils.hexstr_to_bytearray(cfg.get('Img_Group0_Cfg', 'aes_iv'))
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
                if sign != 0:
                    newval = newval | 1 << sign_pos
                    data_tohash += load_helper_bin_body_encrypt
                    publickey_file = cfg.get('Img_Group0_Cfg', 'publickey_file')
                    privatekey_file_uecc = cfg.get('Img_Group0_Cfg', 'privatekey_file_uecc')
                    pk_data, pk_hash, signature = img_create_sign_data(data_tohash, privatekey_file_uecc, publickey_file)
                    pk_data = pk_data + bflb_utils.get_crc32_bytearray(pk_data)
                data[offset:offset + 4] = bflb_utils.int_to_4bytearray_l(newval)
                load_helper_bin_header = data
                load_helper_bin_encrypt = load_helper_bin_header + pk_data + signature + aesiv_data + load_helper_bin_body_encrypt
                hashfun = hashlib.sha256()
                hashfun.update(load_helper_bin_body_encrypt)
                hash = bflb_utils.hexstr_to_bytearray(hashfun.hexdigest())
                load_helper_bin_data = bytearray(load_helper_bin_encrypt)
                load_helper_bin_encrypt = img_create_update_bootheader_if(load_helper_bin_data, hash, 1)
        return (
         True, load_helper_bin_encrypt)
    return (False, None)


def img_creat_process(group_type, flash_img, cfg, security=False):
    encrypt_blk_size = 16
    padding = bytearray(encrypt_blk_size)
    data_tohash = bytearray(0)
    cfg_section = ''
    img_update_efuse_fun = img_update_efuse_group0
    cfg_section = 'Img_Group0_Cfg'
    segheader_file = []
    if flash_img == 0:
        for files in cfg.get(cfg_section, 'segheader_file').split(' '):
            segheader_file.append(str(files))

    segdata_file = []
    for files in cfg.get(cfg_section, 'segdata_file').split('|'):
        if files:
            segdata_file.append(str(files))

    boot_header_file = cfg.get(cfg_section, 'boot_header_file')
    bootheader_data = img_create_read_file_append_crc(boot_header_file, 0)
    encrypt = 0
    sign, encrypt, key_sel, xts_mode = img_create_get_sign_encrypt_info(bootheader_data)
    boot_entry = img_create_get_img_start_addr(bootheader_data)
    aesiv_data = bytearray(0)
    pk_data = bytearray(0)
    publickey_file = ''
    privatekey_file_uecc = ''
    if sign != 0:
        bflb_utils.printf('Image need sign')
        publickey_file = cfg.get(cfg_section, 'publickey_file')
        privatekey_file_uecc = cfg.get(cfg_section, 'privatekey_file_uecc')
    else:
        if encrypt != 0:
            bflb_utils.printf('Image need encrypt ', encrypt)
            if xts_mode == 1:
                bflb_utils.printf('Enable xts mode')
            encrypt_key_org = bflb_utils.hexstr_to_bytearray(cfg.get(cfg_section, 'aes_key_org'))
            if encrypt == 1:
                if xts_mode == 1:
                    encrypt_key = encrypt_key_org[0:32]
                else:
                    encrypt_key = encrypt_key_org[0:16]
            elif encrypt == 2:
                if xts_mode == 1:
                    encrypt_key = encrypt_key_org[0:32]
                else:
                    encrypt_key = encrypt_key_org[0:32]
            else:
                if encrypt == 3:
                    if xts_mode == 1:
                        encrypt_key = encrypt_key_org[0:24]
                    else:
                        encrypt_key = encrypt_key_org[0:24]
                bflb_utils.printf('Key= ', binascii.hexlify(encrypt_key))
                iv_value = cfg.get(cfg_section, 'aes_iv')
                if xts_mode == 1:
                    iv_value = iv_value[24:32] + iv_value[:24]
                encrypt_iv = bflb_utils.hexstr_to_bytearray(iv_value)
                iv_crcarray = bflb_utils.get_crc32_bytearray(encrypt_iv)
                aesiv_data = encrypt_iv + iv_crcarray
        seg_cnt = len(segheader_file)
        segdata_cnt = len(segdata_file)
        if flash_img == 0:
            if seg_cnt != segdata_cnt:
                bflb_utils.printf('Segheader count and segdata count not match')
                return ('FAIL', data_tohash)
            data_toencrypt = bytearray(0)
            if flash_img == 0:
                i = 0
                seg_header_list = []
                seg_data_list = []
                while i < seg_cnt:
                    seg_data = bytearray(0)
                    if segdata_file[i] != 'UNUSED':
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
                cnt = 0
                while i < seg_cnt:
                    if seg_header_list[i][4:8] != bytearray(4):
                        data_toencrypt += seg_header_list[i]
                        data_toencrypt += seg_data_list[i]
                        cnt += 1
                    i += 1

                seg_cnt = cnt
            else:
                seg_data = img_get_one_group_img(boot_entry, segdata_file)
                padding_size = 0
                if len(seg_data) % encrypt_blk_size != 0:
                    padding_size = encrypt_blk_size - len(seg_data) % encrypt_blk_size
                    seg_data += padding[0:padding_size]
                data_toencrypt += seg_data
                seg_cnt = len(data_toencrypt)
            if encrypt != 0:
                unencrypt_mfg_data = bytearray(0)
                if seg_cnt >= 8192:
                    if data_toencrypt[4096:4100] == bytearray('0mfg'.encode('utf-8')):
                        unencrypt_mfg_data = data_toencrypt[4096:8192]
                if xts_mode != 0:
                    data_toencrypt = img_create_encrypt_data_xts(data_toencrypt, encrypt_key, encrypt_iv, encrypt)
        else:
            data_toencrypt = img_create_encrypt_data(data_toencrypt, encrypt_key, encrypt_iv, flash_img)
    if unencrypt_mfg_data != bytearray(0):
        data_toencrypt = data_toencrypt[0:4096] + unencrypt_mfg_data + data_toencrypt[8192:]
    else:
        fw_data = bytearray(0)
        data_tohash += data_toencrypt
        fw_data = data_toencrypt
        hash = img_create_sha256_data(data_tohash)
        bflb_utils.printf('Image hash is ', binascii.hexlify(hash))
        signature = bytearray(0)
        pk_hash = None
        if sign == 1:
            pk_data, pk_hash, signature = img_create_sign_data(data_tohash, privatekey_file_uecc, publickey_file)
            pk_data = pk_data + bflb_utils.get_crc32_bytearray(pk_data)
        else:
            flashCfgAddr = len(bootheader_data + pk_data + signature + aesiv_data)
            flashCfgListLen = 0
            flashCfgList = bytearray(0)
            flashCfgTable = bytearray(0)
            if flash_img == 1:
                if bootheader_data[233:234] == b'\xff':
                    flashCfgList, flashCfgTable, flashCfgListLen = create_flashcfg_table(flashCfgAddr)
                bootheader_data = img_create_update_custom_bootheader(bootheader_data, seg_cnt, hash, signature, pk_data, aesiv_data)
            bootheader_data = img_create_update_bootheader(bootheader_data, hash, seg_cnt, flashCfgAddr, flashCfgListLen)
            if flash_img == 1:
                bflb_utils.printf('Write flash img')
                bootinfo_file_name = cfg.get(cfg_section, 'bootinfo_file')
                fp = open(bootinfo_file_name, 'wb+')
                bootinfo = bootheader_data + pk_data + signature + aesiv_data + flashCfgList + flashCfgTable
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
                    flash_encrypt_type = 0
                    if encrypt == 1:
                        flash_encrypt_type = 1
                    if encrypt == 2:
                        flash_encrypt_type = 3
                    if encrypt == 3:
                        flash_encrypt_type = 2
                    if xts_mode == 1:
                        flash_encrypt_type += 3
                    img_update_efuse_fun(cfg, sign, pk_hash, flash_encrypt_type, encrypt_key + bytearray(32 - len(encrypt_key)), key_sel, None, security)
                else:
                    img_update_efuse_fun(cfg, sign, pk_hash, encrypt, None, key_sel, None, security)
            else:
                bflb_utils.printf('Write if img')
                whole_img_file_name = cfg.get(cfg_section, 'whole_img_file')
                fp = open(whole_img_file_name, 'wb+')
                img_data = bootheader_data + pk_data + signature + aesiv_data + fw_data
                fp.write(img_data)
                fp.close()
                if encrypt != 0:
                    if_encrypt_type = 0
                    if encrypt == 1:
                        if_encrypt_type = 1
                    if encrypt == 2:
                        if_encrypt_type = 3
                    if encrypt == 3:
                        if_encrypt_type = 2
                    if xts_mode == 1:
                        if_encrypt_type += 3
                    img_update_efuse_fun(cfg, sign, pk_hash, if_encrypt_type, None, key_sel, encrypt_key + bytearray(32 - len(encrypt_key)), security)
                else:
                    img_update_efuse_fun(cfg, sign, pk_hash, 0, None, key_sel, bytearray(32), security)
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
        group_type = 'all'
        img_type = 'media'
        signer = 'none'
        security = False
        data_tohash = bytearray(0)
        try:
            if args.image:
                img_type = args.image
            if args.group:
                group_type = args.group
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
        ret0 = ret1 = 'OK'
        if group_type == 'group0' or group_type == 'all':
            ret0, data_tohash0 = img_creat_process('group0', flash_img, cfg, security)
        else:
            img_creat_process('', flash_img, cfg, security)
    if ret0 != 'OK':
        bflb_utils.printf('Fail to create group0 images!')
        return False
    if ret1 != 'OK':
        bflb_utils.printf('Fail to create group1 images!')
        return False
    return True


def create_sp_media_image(config, cpu_type=None, security=False):
    bflb_utils.printf('========= sp image create =========')
    cfg = BFConfigParser()
    cfg.read(config)
    img_creat_process('group0', 1, cfg, security)


if __name__ == '__main__':
    data_bytearray = codecs.decode('42464E500100000046434647040101036699FF039F00B7E904EF0001C72052D8060232000B010B013B01BB006B01EB02EB02025000010001010002010101AB01053500000131000038FF20FF77030240770302F02C01B004B0040500FFFF030036C3DD9E5043464704040001010105000101050000010101A612AC86000144650020000000000000503100007A6345494BCABEC7307FD8F8396729EB67DDC8C63B7AD69B797B08564E982A8701000000000000000000000000000000000000D80000000000010000000000000000000000200100000001D80000000000010000000000000000000000200200000002580000000000010000000000000000000000200300000003580000000000010000D0C57503C09E750300200400000004580000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000935F92BB', 'hex')
    key_bytearray = codecs.decode('fffefdfcfbfaf9f8f7f6f5f4f3f2f1f0000102030405060708090a0b0c0d0e0f', 'hex')
    need_reverse_iv_bytearray = codecs.decode('01000000000000000000000000000000', 'hex')
    iv_bytearray = codecs.decode(reverse_iv(need_reverse_iv_bytearray), 'hex')
    img_create_encrypt_data_xts(data_bytearray, key_bytearray, iv_bytearray, 0)