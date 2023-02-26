# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
# [GCC 9.4.0]
# Embedded file name: libs/bl628/img_create_do.py
import os, sys, hashlib, binascii, codecs, ecdsa
from CryptoPlus.Cipher import AES as AES_XTS
from libs import bflb_utils
from libs.bflb_utils import img_create_sha256_data, img_create_encrypt_data
from libs.bflb_configobj import BFConfigParser
from libs.bl628.flash_select_do import create_flashcfg_table
from libs.bl628.bootheader_cfg_keys import flashcfg_table_start_pos as flashcfg_table_start
from libs.bl628.bootheader_cfg_keys import bootcpucfg_start_pos as bootcpucfg_start
from libs.bl628.bootheader_cfg_keys import bootcpucfg_len as bootcpucfg_length
from libs.bl628.bootheader_cfg_keys import bootcpucfg_m0_index as bootcpucfg_m0_index_number
from libs.bl628.bootheader_cfg_keys import bootcpucfg_m1_index as bootcpucfg_m1_index_number
from libs.bl628.bootheader_cfg_keys import bootcfg_start_pos as bootcfg_start
from libs.bl628.bootheader_cfg_keys import bootheader_len as header_len
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
              150  POP_JUMP_IF_FALSE   184  'to 184'

 L. 107       152  LOAD_FAST                'efuse_data'
              154  LOAD_CONST               93
              156  DUP_TOP_TWO      
              158  BINARY_SUBSCR    
              160  LOAD_FAST                'sign'
              162  INPLACE_OR       
              164  ROT_THREE        
              166  STORE_SUBSCR     

 L. 108       168  LOAD_FAST                'efuse_mask_data'
              170  LOAD_CONST               93
              172  DUP_TOP_TWO      
              174  BINARY_SUBSCR    
              176  LOAD_CONST               255
              178  INPLACE_OR       
              180  ROT_THREE        
              182  STORE_SUBSCR     
            184_0  COME_FROM           150  '150'

 L. 110       184  LOAD_FAST                'flash_encryp_type'
              186  LOAD_CONST               0
              188  COMPARE_OP               >
              190  POP_JUMP_IF_FALSE   208  'to 208'

 L. 111       192  LOAD_FAST                'efuse_data'
              194  LOAD_CONST               0
              196  DUP_TOP_TWO      
              198  BINARY_SUBSCR    
              200  LOAD_CONST               48
              202  INPLACE_OR       
              204  ROT_THREE        
              206  STORE_SUBSCR     
            208_0  COME_FROM           190  '190'

 L. 112       208  LOAD_FAST                'efuse_mask_data'
              210  LOAD_CONST               0
              212  DUP_TOP_TWO      
              214  BINARY_SUBSCR    
              216  LOAD_CONST               255
              218  INPLACE_OR       
              220  ROT_THREE        
              222  STORE_SUBSCR     

 L. 113       224  LOAD_CONST               0
              226  STORE_FAST               'rw_lock0'

 L. 114       228  LOAD_CONST               0
              230  STORE_FAST               'rw_lock1'

 L. 115       232  LOAD_FAST                'pk_hash'
              234  LOAD_CONST               None
              236  COMPARE_OP               is-not
          238_240  POP_JUMP_IF_FALSE   294  'to 294'

 L. 116       242  LOAD_FAST                'pk_hash'
              244  LOAD_FAST                'efuse_data'
              246  LOAD_GLOBAL              keyslot0
              248  LOAD_GLOBAL              keyslot2
              250  BUILD_SLICE_2         2 
              252  STORE_SUBSCR     

 L. 117       254  LOAD_FAST                'mask_4bytes'
              256  LOAD_CONST               8
              258  BINARY_MULTIPLY  
              260  LOAD_FAST                'efuse_mask_data'
              262  LOAD_GLOBAL              keyslot0
              264  LOAD_GLOBAL              keyslot2
              266  BUILD_SLICE_2         2 
              268  STORE_SUBSCR     

 L. 118       270  LOAD_FAST                'rw_lock0'
              272  LOAD_CONST               1
              274  LOAD_GLOBAL              wr_lock_key_slot_0
              276  BINARY_LSHIFT    
              278  INPLACE_OR       
              280  STORE_FAST               'rw_lock0'

 L. 119       282  LOAD_FAST                'rw_lock0'
              284  LOAD_CONST               1
              286  LOAD_GLOBAL              wr_lock_key_slot_1
              288  BINARY_LSHIFT    
              290  INPLACE_OR       
              292  STORE_FAST               'rw_lock0'
            294_0  COME_FROM           238  '238'

 L. 120       294  LOAD_FAST                'flash_key'
              296  LOAD_CONST               None
              298  COMPARE_OP               is-not
          300_302  POP_JUMP_IF_FALSE   586  'to 586'

 L. 121       304  LOAD_FAST                'flash_encryp_type'
              306  LOAD_CONST               1
              308  COMPARE_OP               ==
          310_312  POP_JUMP_IF_FALSE   352  'to 352'

 L. 123       314  LOAD_FAST                'flash_key'
              316  LOAD_CONST               0
              318  LOAD_CONST               16
              320  BUILD_SLICE_2         2 
              322  BINARY_SUBSCR    
              324  LOAD_FAST                'efuse_data'
              326  LOAD_GLOBAL              keyslot2
              328  LOAD_GLOBAL              keyslot3
              330  BUILD_SLICE_2         2 
              332  STORE_SUBSCR     

 L. 124       334  LOAD_FAST                'mask_4bytes'
              336  LOAD_CONST               4
              338  BINARY_MULTIPLY  
              340  LOAD_FAST                'efuse_mask_data'
              342  LOAD_GLOBAL              keyslot2
              344  LOAD_GLOBAL              keyslot3
              346  BUILD_SLICE_2         2 
              348  STORE_SUBSCR     
              350  JUMP_FORWARD        562  'to 562'
            352_0  COME_FROM           310  '310'

 L. 125       352  LOAD_FAST                'flash_encryp_type'
              354  LOAD_CONST               2
              356  COMPARE_OP               ==
          358_360  POP_JUMP_IF_FALSE   416  'to 416'

 L. 127       362  LOAD_FAST                'flash_key'
              364  LOAD_FAST                'efuse_data'
              366  LOAD_GLOBAL              keyslot2
              368  LOAD_GLOBAL              keyslot3_end
              370  BUILD_SLICE_2         2 
              372  STORE_SUBSCR     

 L. 128       374  LOAD_FAST                'mask_4bytes'
              376  LOAD_CONST               8
              378  BINARY_MULTIPLY  
              380  LOAD_FAST                'efuse_mask_data'
              382  LOAD_GLOBAL              keyslot2
              384  LOAD_GLOBAL              keyslot3_end
              386  BUILD_SLICE_2         2 
              388  STORE_SUBSCR     

 L. 129       390  LOAD_FAST                'rw_lock0'
              392  LOAD_CONST               1
              394  LOAD_GLOBAL              wr_lock_key_slot_3
              396  BINARY_LSHIFT    
              398  INPLACE_OR       
              400  STORE_FAST               'rw_lock0'

 L. 130       402  LOAD_FAST                'rw_lock0'
              404  LOAD_CONST               1
              406  LOAD_GLOBAL              rd_lock_key_slot_3
              408  BINARY_LSHIFT    
              410  INPLACE_OR       
              412  STORE_FAST               'rw_lock0'
              414  JUMP_FORWARD        562  'to 562'
            416_0  COME_FROM           358  '358'

 L. 131       416  LOAD_FAST                'flash_encryp_type'
              418  LOAD_CONST               3
              420  COMPARE_OP               ==
          422_424  POP_JUMP_IF_FALSE   480  'to 480'

 L. 133       426  LOAD_FAST                'flash_key'
              428  LOAD_FAST                'efuse_data'
              430  LOAD_GLOBAL              keyslot2
              432  LOAD_GLOBAL              keyslot3_end
              434  BUILD_SLICE_2         2 
              436  STORE_SUBSCR     

 L. 134       438  LOAD_FAST                'mask_4bytes'
              440  LOAD_CONST               8
              442  BINARY_MULTIPLY  
              444  LOAD_FAST                'efuse_mask_data'
              446  LOAD_GLOBAL              keyslot2
              448  LOAD_GLOBAL              keyslot3_end
              450  BUILD_SLICE_2         2 
              452  STORE_SUBSCR     

 L. 135       454  LOAD_FAST                'rw_lock0'
              456  LOAD_CONST               1
              458  LOAD_GLOBAL              wr_lock_key_slot_3
              460  BINARY_LSHIFT    
              462  INPLACE_OR       
              464  STORE_FAST               'rw_lock0'

 L. 136       466  LOAD_FAST                'rw_lock0'
              468  LOAD_CONST               1
              470  LOAD_GLOBAL              rd_lock_key_slot_3
              472  BINARY_LSHIFT    
              474  INPLACE_OR       
              476  STORE_FAST               'rw_lock0'
              478  JUMP_FORWARD        562  'to 562'
            480_0  COME_FROM           422  '422'

 L. 137       480  LOAD_FAST                'flash_encryp_type'
              482  LOAD_CONST               4
              484  COMPARE_OP               ==
          486_488  POP_JUMP_IF_TRUE    510  'to 510'

 L. 138       490  LOAD_FAST                'flash_encryp_type'
              492  LOAD_CONST               5
              494  COMPARE_OP               ==
          496_498  POP_JUMP_IF_TRUE    510  'to 510'

 L. 139       500  LOAD_FAST                'flash_encryp_type'
              502  LOAD_CONST               6
              504  COMPARE_OP               ==
          506_508  POP_JUMP_IF_FALSE   562  'to 562'
            510_0  COME_FROM           496  '496'
            510_1  COME_FROM           486  '486'

 L. 141       510  LOAD_FAST                'flash_key'
              512  LOAD_FAST                'efuse_data'
              514  LOAD_GLOBAL              keyslot2
              516  LOAD_GLOBAL              keyslot3_end
              518  BUILD_SLICE_2         2 
              520  STORE_SUBSCR     

 L. 142       522  LOAD_FAST                'mask_4bytes'
              524  LOAD_CONST               8
              526  BINARY_MULTIPLY  
              528  LOAD_FAST                'efuse_mask_data'
              530  LOAD_GLOBAL              keyslot2
              532  LOAD_GLOBAL              keyslot3_end
              534  BUILD_SLICE_2         2 
              536  STORE_SUBSCR     

 L. 143       538  LOAD_FAST                'rw_lock0'
              540  LOAD_CONST               1
              542  LOAD_GLOBAL              wr_lock_key_slot_3
              544  BINARY_LSHIFT    
              546  INPLACE_OR       
              548  STORE_FAST               'rw_lock0'

 L. 144       550  LOAD_FAST                'rw_lock0'
              552  LOAD_CONST               1
              554  LOAD_GLOBAL              rd_lock_key_slot_3
              556  BINARY_LSHIFT    
              558  INPLACE_OR       
              560  STORE_FAST               'rw_lock0'
            562_0  COME_FROM           506  '506'
            562_1  COME_FROM           478  '478'
            562_2  COME_FROM           414  '414'
            562_3  COME_FROM           350  '350'

 L. 146       562  LOAD_FAST                'rw_lock0'
              564  LOAD_CONST               1
              566  LOAD_GLOBAL              wr_lock_key_slot_2
              568  BINARY_LSHIFT    
              570  INPLACE_OR       
              572  STORE_FAST               'rw_lock0'

 L. 147       574  LOAD_FAST                'rw_lock0'
              576  LOAD_CONST               1
              578  LOAD_GLOBAL              rd_lock_key_slot_2
              580  BINARY_LSHIFT    
              582  INPLACE_OR       
              584  STORE_FAST               'rw_lock0'
            586_0  COME_FROM           300  '300'

 L. 149       586  LOAD_FAST                'sec_eng_key'
              588  LOAD_CONST               None
              590  COMPARE_OP               is-not
          592_594  POP_JUMP_IF_FALSE  1926  'to 1926'

 L. 150       596  LOAD_FAST                'flash_encryp_type'
              598  LOAD_CONST               0
              600  COMPARE_OP               ==
          602_604  POP_JUMP_IF_FALSE  1078  'to 1078'

 L. 151       606  LOAD_FAST                'sec_eng_key_sel'
              608  LOAD_CONST               0
              610  COMPARE_OP               ==
          612_614  POP_JUMP_IF_FALSE   720  'to 720'

 L. 152       616  LOAD_FAST                'sec_eng_key'
              618  LOAD_CONST               16
              620  LOAD_CONST               32
              622  BUILD_SLICE_2         2 
              624  BINARY_SUBSCR    
              626  LOAD_FAST                'efuse_data'
              628  LOAD_GLOBAL              keyslot2
              630  LOAD_GLOBAL              keyslot3
              632  BUILD_SLICE_2         2 
              634  STORE_SUBSCR     

 L. 153       636  LOAD_FAST                'sec_eng_key'
              638  LOAD_CONST               0
              640  LOAD_CONST               16
              642  BUILD_SLICE_2         2 
              644  BINARY_SUBSCR    
              646  LOAD_FAST                'efuse_data'
              648  LOAD_GLOBAL              keyslot3
              650  LOAD_GLOBAL              keyslot3_end
              652  BUILD_SLICE_2         2 
              654  STORE_SUBSCR     

 L. 154       656  LOAD_FAST                'mask_4bytes'
              658  LOAD_CONST               8
              660  BINARY_MULTIPLY  
              662  LOAD_FAST                'efuse_mask_data'
              664  LOAD_GLOBAL              keyslot2
              666  LOAD_GLOBAL              keyslot3_end
              668  BUILD_SLICE_2         2 
              670  STORE_SUBSCR     

 L. 155       672  LOAD_FAST                'rw_lock0'
              674  LOAD_CONST               1
              676  LOAD_GLOBAL              wr_lock_key_slot_2
              678  BINARY_LSHIFT    
              680  INPLACE_OR       
              682  STORE_FAST               'rw_lock0'

 L. 156       684  LOAD_FAST                'rw_lock0'
              686  LOAD_CONST               1
              688  LOAD_GLOBAL              wr_lock_key_slot_3
              690  BINARY_LSHIFT    
              692  INPLACE_OR       
              694  STORE_FAST               'rw_lock0'

 L. 157       696  LOAD_FAST                'rw_lock0'
              698  LOAD_CONST               1
              700  LOAD_GLOBAL              rd_lock_key_slot_2
              702  BINARY_LSHIFT    
              704  INPLACE_OR       
              706  STORE_FAST               'rw_lock0'

 L. 158       708  LOAD_FAST                'rw_lock0'
              710  LOAD_CONST               1
              712  LOAD_GLOBAL              rd_lock_key_slot_3
              714  BINARY_LSHIFT    
              716  INPLACE_OR       
              718  STORE_FAST               'rw_lock0'
            720_0  COME_FROM           612  '612'

 L. 159       720  LOAD_FAST                'sec_eng_key_sel'
              722  LOAD_CONST               1
              724  COMPARE_OP               ==
          726_728  POP_JUMP_IF_FALSE   850  'to 850'

 L. 160       730  LOAD_FAST                'sec_eng_key'
              732  LOAD_CONST               16
              734  LOAD_CONST               32
              736  BUILD_SLICE_2         2 
              738  BINARY_SUBSCR    
              740  LOAD_FAST                'efuse_data'
              742  LOAD_GLOBAL              keyslot3
              744  LOAD_GLOBAL              keyslot3_end
              746  BUILD_SLICE_2         2 
              748  STORE_SUBSCR     

 L. 161       750  LOAD_FAST                'sec_eng_key'
              752  LOAD_CONST               0
              754  LOAD_CONST               16
              756  BUILD_SLICE_2         2 
              758  BINARY_SUBSCR    
              760  LOAD_FAST                'efuse_data'
              762  LOAD_GLOBAL              keyslot4
              764  LOAD_GLOBAL              keyslot5
              766  BUILD_SLICE_2         2 
              768  STORE_SUBSCR     

 L. 162       770  LOAD_FAST                'mask_4bytes'
              772  LOAD_CONST               4
              774  BINARY_MULTIPLY  
              776  LOAD_FAST                'efuse_mask_data'
              778  LOAD_GLOBAL              keyslot3
              780  LOAD_GLOBAL              keyslot3_end
              782  BUILD_SLICE_2         2 
              784  STORE_SUBSCR     

 L. 163       786  LOAD_FAST                'mask_4bytes'
              788  LOAD_CONST               4
              790  BINARY_MULTIPLY  
              792  LOAD_FAST                'efuse_mask_data'
              794  LOAD_GLOBAL              keyslot4
              796  LOAD_GLOBAL              keyslot5
              798  BUILD_SLICE_2         2 
              800  STORE_SUBSCR     

 L. 164       802  LOAD_FAST                'rw_lock0'
              804  LOAD_CONST               1
              806  LOAD_GLOBAL              wr_lock_key_slot_3
              808  BINARY_LSHIFT    
              810  INPLACE_OR       
              812  STORE_FAST               'rw_lock0'

 L. 165       814  LOAD_FAST                'rw_lock1'
              816  LOAD_CONST               1
              818  LOAD_GLOBAL              wr_lock_key_slot_4
              820  BINARY_LSHIFT    
              822  INPLACE_OR       
              824  STORE_FAST               'rw_lock1'

 L. 166       826  LOAD_FAST                'rw_lock0'
              828  LOAD_CONST               1
              830  LOAD_GLOBAL              rd_lock_key_slot_3
              832  BINARY_LSHIFT    
              834  INPLACE_OR       
              836  STORE_FAST               'rw_lock0'

 L. 167       838  LOAD_FAST                'rw_lock1'
              840  LOAD_CONST               1
              842  LOAD_GLOBAL              rd_lock_key_slot_4
              844  BINARY_LSHIFT    
              846  INPLACE_OR       
              848  STORE_FAST               'rw_lock1'
            850_0  COME_FROM           726  '726'

 L. 168       850  LOAD_FAST                'sec_eng_key_sel'
              852  LOAD_CONST               2
              854  COMPARE_OP               ==
          856_858  POP_JUMP_IF_FALSE   964  'to 964'

 L. 169       860  LOAD_FAST                'sec_eng_key'
              862  LOAD_CONST               16
              864  LOAD_CONST               32
              866  BUILD_SLICE_2         2 
              868  BINARY_SUBSCR    
              870  LOAD_FAST                'efuse_data'
              872  LOAD_GLOBAL              keyslot4
              874  LOAD_GLOBAL              keyslot5
              876  BUILD_SLICE_2         2 
              878  STORE_SUBSCR     

 L. 170       880  LOAD_FAST                'sec_eng_key'
              882  LOAD_CONST               0
              884  LOAD_CONST               16
              886  BUILD_SLICE_2         2 
              888  BINARY_SUBSCR    
              890  LOAD_FAST                'efuse_data'
              892  LOAD_GLOBAL              keyslot2
              894  LOAD_GLOBAL              keyslot3
              896  BUILD_SLICE_2         2 
              898  STORE_SUBSCR     

 L. 171       900  LOAD_FAST                'mask_4bytes'
              902  LOAD_CONST               8
              904  BINARY_MULTIPLY  
              906  LOAD_FAST                'efuse_mask_data'
              908  LOAD_GLOBAL              keyslot3
              910  LOAD_GLOBAL              keyslot5
              912  BUILD_SLICE_2         2 
              914  STORE_SUBSCR     

 L. 172       916  LOAD_FAST                'rw_lock1'
              918  LOAD_CONST               1
              920  LOAD_GLOBAL              wr_lock_key_slot_4
              922  BINARY_LSHIFT    
              924  INPLACE_OR       
              926  STORE_FAST               'rw_lock1'

 L. 173       928  LOAD_FAST                'rw_lock0'
              930  LOAD_CONST               1
              932  LOAD_GLOBAL              wr_lock_key_slot_2
              934  BINARY_LSHIFT    
              936  INPLACE_OR       
              938  STORE_FAST               'rw_lock0'

 L. 174       940  LOAD_FAST                'rw_lock1'
              942  LOAD_CONST               1
              944  LOAD_GLOBAL              rd_lock_key_slot_4
              946  BINARY_LSHIFT    
              948  INPLACE_OR       
              950  STORE_FAST               'rw_lock1'

 L. 175       952  LOAD_FAST                'rw_lock0'
              954  LOAD_CONST               1
              956  LOAD_GLOBAL              rd_lock_key_slot_2
              958  BINARY_LSHIFT    
              960  INPLACE_OR       
              962  STORE_FAST               'rw_lock0'
            964_0  COME_FROM           856  '856'

 L. 176       964  LOAD_FAST                'sec_eng_key_sel'
              966  LOAD_CONST               3
              968  COMPARE_OP               ==
          970_972  POP_JUMP_IF_FALSE  1078  'to 1078'

 L. 177       974  LOAD_FAST                'sec_eng_key'
              976  LOAD_CONST               16
              978  LOAD_CONST               32
              980  BUILD_SLICE_2         2 
              982  BINARY_SUBSCR    
              984  LOAD_FAST                'efuse_data'
              986  LOAD_GLOBAL              keyslot4
              988  LOAD_GLOBAL              keyslot5
              990  BUILD_SLICE_2         2 
              992  STORE_SUBSCR     

 L. 178       994  LOAD_FAST                'sec_eng_key'
              996  LOAD_CONST               0
              998  LOAD_CONST               16
             1000  BUILD_SLICE_2         2 
             1002  BINARY_SUBSCR    
             1004  LOAD_FAST                'efuse_data'
             1006  LOAD_GLOBAL              keyslot2
             1008  LOAD_GLOBAL              keyslot3
             1010  BUILD_SLICE_2         2 
             1012  STORE_SUBSCR     

 L. 179      1014  LOAD_FAST                'mask_4bytes'
             1016  LOAD_CONST               8
             1018  BINARY_MULTIPLY  
             1020  LOAD_FAST                'efuse_mask_data'
             1022  LOAD_GLOBAL              keyslot3
             1024  LOAD_GLOBAL              keyslot5
             1026  BUILD_SLICE_2         2 
             1028  STORE_SUBSCR     

 L. 180      1030  LOAD_FAST                'rw_lock1'
             1032  LOAD_CONST               1
             1034  LOAD_GLOBAL              wr_lock_key_slot_4
             1036  BINARY_LSHIFT    
             1038  INPLACE_OR       
             1040  STORE_FAST               'rw_lock1'

 L. 181      1042  LOAD_FAST                'rw_lock0'
             1044  LOAD_CONST               1
             1046  LOAD_GLOBAL              wr_lock_key_slot_2
             1048  BINARY_LSHIFT    
             1050  INPLACE_OR       
             1052  STORE_FAST               'rw_lock0'

 L. 182      1054  LOAD_FAST                'rw_lock1'
             1056  LOAD_CONST               1
             1058  LOAD_GLOBAL              rd_lock_key_slot_4
             1060  BINARY_LSHIFT    
             1062  INPLACE_OR       
             1064  STORE_FAST               'rw_lock1'

 L. 183      1066  LOAD_FAST                'rw_lock0'
             1068  LOAD_CONST               1
             1070  LOAD_GLOBAL              rd_lock_key_slot_2
             1072  BINARY_LSHIFT    
             1074  INPLACE_OR       
             1076  STORE_FAST               'rw_lock0'
           1078_0  COME_FROM           970  '970'
           1078_1  COME_FROM           602  '602'

 L. 184      1078  LOAD_FAST                'flash_encryp_type'
             1080  LOAD_CONST               1
             1082  COMPARE_OP               ==
         1084_1086  POP_JUMP_IF_FALSE  1392  'to 1392'

 L. 185      1088  LOAD_FAST                'sec_eng_key_sel'
             1090  LOAD_CONST               0
             1092  COMPARE_OP               ==
         1094_1096  POP_JUMP_IF_FALSE  1158  'to 1158'

 L. 186      1098  LOAD_FAST                'sec_eng_key'
             1100  LOAD_CONST               0
             1102  LOAD_CONST               16
             1104  BUILD_SLICE_2         2 
             1106  BINARY_SUBSCR    
             1108  LOAD_FAST                'efuse_data'
             1110  LOAD_GLOBAL              keyslot5
             1112  LOAD_GLOBAL              keyslot6
             1114  BUILD_SLICE_2         2 
             1116  STORE_SUBSCR     

 L. 187      1118  LOAD_FAST                'mask_4bytes'
             1120  LOAD_CONST               4
             1122  BINARY_MULTIPLY  
             1124  LOAD_FAST                'efuse_mask_data'
             1126  LOAD_GLOBAL              keyslot5
             1128  LOAD_GLOBAL              keyslot6
             1130  BUILD_SLICE_2         2 
             1132  STORE_SUBSCR     

 L. 188      1134  LOAD_FAST                'rw_lock1'
             1136  LOAD_CONST               1
             1138  LOAD_GLOBAL              wr_lock_key_slot_5
             1140  BINARY_LSHIFT    
             1142  INPLACE_OR       
             1144  STORE_FAST               'rw_lock1'

 L. 189      1146  LOAD_FAST                'rw_lock1'
             1148  LOAD_CONST               1
             1150  LOAD_GLOBAL              rd_lock_key_slot_5
             1152  BINARY_LSHIFT    
             1154  INPLACE_OR       
             1156  STORE_FAST               'rw_lock1'
           1158_0  COME_FROM          1094  '1094'

 L. 190      1158  LOAD_FAST                'sec_eng_key_sel'
             1160  LOAD_CONST               1
             1162  COMPARE_OP               ==
         1164_1166  POP_JUMP_IF_FALSE  1228  'to 1228'

 L. 191      1168  LOAD_FAST                'sec_eng_key'
             1170  LOAD_CONST               0
             1172  LOAD_CONST               16
             1174  BUILD_SLICE_2         2 
             1176  BINARY_SUBSCR    
             1178  LOAD_FAST                'efuse_data'
             1180  LOAD_GLOBAL              keyslot4
             1182  LOAD_GLOBAL              keyslot5
             1184  BUILD_SLICE_2         2 
             1186  STORE_SUBSCR     

 L. 192      1188  LOAD_FAST                'mask_4bytes'
             1190  LOAD_CONST               4
             1192  BINARY_MULTIPLY  
             1194  LOAD_FAST                'efuse_mask_data'
             1196  LOAD_GLOBAL              keyslot4
             1198  LOAD_GLOBAL              keyslot5
             1200  BUILD_SLICE_2         2 
             1202  STORE_SUBSCR     

 L. 193      1204  LOAD_FAST                'rw_lock1'
             1206  LOAD_CONST               1
             1208  LOAD_GLOBAL              wr_lock_key_slot_4
             1210  BINARY_LSHIFT    
             1212  INPLACE_OR       
             1214  STORE_FAST               'rw_lock1'

 L. 194      1216  LOAD_FAST                'rw_lock1'
             1218  LOAD_CONST               1
             1220  LOAD_GLOBAL              rd_lock_key_slot_4
             1222  BINARY_LSHIFT    
             1224  INPLACE_OR       
             1226  STORE_FAST               'rw_lock1'
           1228_0  COME_FROM          1164  '1164'

 L. 195      1228  LOAD_FAST                'sec_eng_key_sel'
             1230  LOAD_CONST               2
             1232  COMPARE_OP               ==
         1234_1236  POP_JUMP_IF_FALSE  1310  'to 1310'

 L. 196      1238  LOAD_FAST                'flash_key'
             1240  LOAD_CONST               None
             1242  COMPARE_OP               is-not
         1244_1246  POP_JUMP_IF_FALSE  1250  'to 1250'

 L. 198      1248  JUMP_FORWARD       1310  'to 1310'
           1250_0  COME_FROM          1244  '1244'

 L. 200      1250  LOAD_FAST                'sec_eng_key'
             1252  LOAD_CONST               0
             1254  LOAD_CONST               16
             1256  BUILD_SLICE_2         2 
             1258  BINARY_SUBSCR    
             1260  LOAD_FAST                'efuse_data'
             1262  LOAD_GLOBAL              keyslot3
             1264  LOAD_GLOBAL              keyslot3_end
             1266  BUILD_SLICE_2         2 
             1268  STORE_SUBSCR     

 L. 201      1270  LOAD_FAST                'mask_4bytes'
             1272  LOAD_CONST               4
             1274  BINARY_MULTIPLY  
             1276  LOAD_FAST                'efuse_mask_data'
             1278  LOAD_GLOBAL              keyslot3
             1280  LOAD_GLOBAL              keyslot3_end
             1282  BUILD_SLICE_2         2 
             1284  STORE_SUBSCR     

 L. 202      1286  LOAD_FAST                'rw_lock0'
             1288  LOAD_CONST               1
             1290  LOAD_GLOBAL              wr_lock_key_slot_3
             1292  BINARY_LSHIFT    
             1294  INPLACE_OR       
             1296  STORE_FAST               'rw_lock0'

 L. 203      1298  LOAD_FAST                'rw_lock0'
             1300  LOAD_CONST               1
             1302  LOAD_GLOBAL              rd_lock_key_slot_3
             1304  BINARY_LSHIFT    
             1306  INPLACE_OR       
             1308  STORE_FAST               'rw_lock0'
           1310_0  COME_FROM          1248  '1248'
           1310_1  COME_FROM          1234  '1234'

 L. 204      1310  LOAD_FAST                'sec_eng_key_sel'
             1312  LOAD_CONST               3
             1314  COMPARE_OP               ==
         1316_1318  POP_JUMP_IF_FALSE  1392  'to 1392'

 L. 205      1320  LOAD_FAST                'flash_key'
             1322  LOAD_CONST               None
             1324  COMPARE_OP               is-not
         1326_1328  POP_JUMP_IF_FALSE  1332  'to 1332'

 L. 207      1330  JUMP_FORWARD       1392  'to 1392'
           1332_0  COME_FROM          1326  '1326'

 L. 209      1332  LOAD_FAST                'sec_eng_key'
             1334  LOAD_CONST               0
             1336  LOAD_CONST               16
             1338  BUILD_SLICE_2         2 
             1340  BINARY_SUBSCR    
             1342  LOAD_FAST                'efuse_data'
             1344  LOAD_GLOBAL              keyslot2
             1346  LOAD_GLOBAL              keyslot3
             1348  BUILD_SLICE_2         2 
             1350  STORE_SUBSCR     

 L. 210      1352  LOAD_FAST                'mask_4bytes'
             1354  LOAD_CONST               4
             1356  BINARY_MULTIPLY  
             1358  LOAD_FAST                'efuse_mask_data'
             1360  LOAD_GLOBAL              keyslot2
             1362  LOAD_GLOBAL              keyslot3
             1364  BUILD_SLICE_2         2 
             1366  STORE_SUBSCR     

 L. 211      1368  LOAD_FAST                'rw_lock0'
             1370  LOAD_CONST               1
             1372  LOAD_GLOBAL              wr_lock_key_slot_2
             1374  BINARY_LSHIFT    
             1376  INPLACE_OR       
             1378  STORE_FAST               'rw_lock0'

 L. 212      1380  LOAD_FAST                'rw_lock0'
             1382  LOAD_CONST               1
             1384  LOAD_GLOBAL              rd_lock_key_slot_2
             1386  BINARY_LSHIFT    
             1388  INPLACE_OR       
             1390  STORE_FAST               'rw_lock0'
           1392_0  COME_FROM          1330  '1330'
           1392_1  COME_FROM          1316  '1316'
           1392_2  COME_FROM          1084  '1084'

 L. 213      1392  LOAD_FAST                'flash_encryp_type'
             1394  LOAD_CONST               2
             1396  COMPARE_OP               ==
         1398_1400  POP_JUMP_IF_TRUE   1442  'to 1442'

 L. 214      1402  LOAD_FAST                'flash_encryp_type'
             1404  LOAD_CONST               3
             1406  COMPARE_OP               ==
         1408_1410  POP_JUMP_IF_TRUE   1442  'to 1442'

 L. 215      1412  LOAD_FAST                'flash_encryp_type'
             1414  LOAD_CONST               4
             1416  COMPARE_OP               ==
         1418_1420  POP_JUMP_IF_TRUE   1442  'to 1442'

 L. 216      1422  LOAD_FAST                'flash_encryp_type'
             1424  LOAD_CONST               5
             1426  COMPARE_OP               ==
         1428_1430  POP_JUMP_IF_TRUE   1442  'to 1442'

 L. 217      1432  LOAD_FAST                'flash_encryp_type'
             1434  LOAD_CONST               6
             1436  COMPARE_OP               ==
         1438_1440  POP_JUMP_IF_FALSE  1926  'to 1926'
           1442_0  COME_FROM          1428  '1428'
           1442_1  COME_FROM          1418  '1418'
           1442_2  COME_FROM          1408  '1408'
           1442_3  COME_FROM          1398  '1398'

 L. 218      1442  LOAD_FAST                'sec_eng_key_sel'
             1444  LOAD_CONST               0
             1446  COMPARE_OP               ==
         1448_1450  POP_JUMP_IF_FALSE  1572  'to 1572'

 L. 219      1452  LOAD_FAST                'sec_eng_key'
             1454  LOAD_CONST               16
             1456  LOAD_CONST               32
             1458  BUILD_SLICE_2         2 
             1460  BINARY_SUBSCR    
             1462  LOAD_FAST                'efuse_data'
             1464  LOAD_GLOBAL              keyslot6
             1466  LOAD_GLOBAL              keyslot7
             1468  BUILD_SLICE_2         2 
             1470  STORE_SUBSCR     

 L. 220      1472  LOAD_FAST                'sec_eng_key'
             1474  LOAD_CONST               0
             1476  LOAD_CONST               16
             1478  BUILD_SLICE_2         2 
             1480  BINARY_SUBSCR    
             1482  LOAD_FAST                'efuse_data'
             1484  LOAD_GLOBAL              keyslot10
             1486  LOAD_GLOBAL              keyslot10_end
             1488  BUILD_SLICE_2         2 
             1490  STORE_SUBSCR     

 L. 221      1492  LOAD_FAST                'mask_4bytes'
             1494  LOAD_CONST               4
             1496  BINARY_MULTIPLY  
             1498  LOAD_FAST                'efuse_mask_data'
             1500  LOAD_GLOBAL              keyslot6
             1502  LOAD_GLOBAL              keyslot7
             1504  BUILD_SLICE_2         2 
             1506  STORE_SUBSCR     

 L. 222      1508  LOAD_FAST                'mask_4bytes'
             1510  LOAD_CONST               4
             1512  BINARY_MULTIPLY  
             1514  LOAD_FAST                'efuse_mask_data'
             1516  LOAD_GLOBAL              keyslot10
             1518  LOAD_GLOBAL              keyslot10_end
             1520  BUILD_SLICE_2         2 
             1522  STORE_SUBSCR     

 L. 223      1524  LOAD_FAST                'rw_lock1'
             1526  LOAD_CONST               1
             1528  LOAD_GLOBAL              wr_lock_key_slot_6
             1530  BINARY_LSHIFT    
             1532  INPLACE_OR       
             1534  STORE_FAST               'rw_lock1'

 L. 224      1536  LOAD_FAST                'rw_lock1'
             1538  LOAD_CONST               1
             1540  LOAD_GLOBAL              wr_lock_key_slot_10
             1542  BINARY_LSHIFT    
             1544  INPLACE_OR       
             1546  STORE_FAST               'rw_lock1'

 L. 225      1548  LOAD_FAST                'rw_lock1'
             1550  LOAD_CONST               1
             1552  LOAD_GLOBAL              rd_lock_key_slot_6
             1554  BINARY_LSHIFT    
             1556  INPLACE_OR       
             1558  STORE_FAST               'rw_lock1'

 L. 226      1560  LOAD_FAST                'rw_lock1'
             1562  LOAD_CONST               1
             1564  LOAD_GLOBAL              rd_lock_key_slot_10
             1566  BINARY_LSHIFT    
             1568  INPLACE_OR       
             1570  STORE_FAST               'rw_lock1'
           1572_0  COME_FROM          1448  '1448'

 L. 227      1572  LOAD_FAST                'sec_eng_key_sel'
             1574  LOAD_CONST               1
             1576  COMPARE_OP               ==
         1578_1580  POP_JUMP_IF_FALSE  1702  'to 1702'

 L. 228      1582  LOAD_FAST                'sec_eng_key'
             1584  LOAD_CONST               16
             1586  LOAD_CONST               32
             1588  BUILD_SLICE_2         2 
             1590  BINARY_SUBSCR    
             1592  LOAD_FAST                'efuse_data'
             1594  LOAD_GLOBAL              keyslot10
             1596  LOAD_GLOBAL              keyslot10_end
             1598  BUILD_SLICE_2         2 
             1600  STORE_SUBSCR     

 L. 229      1602  LOAD_FAST                'sec_eng_key'
             1604  LOAD_CONST               0
             1606  LOAD_CONST               16
             1608  BUILD_SLICE_2         2 
             1610  BINARY_SUBSCR    
             1612  LOAD_FAST                'efuse_data'
             1614  LOAD_GLOBAL              keyslot6
             1616  LOAD_GLOBAL              keyslot7
             1618  BUILD_SLICE_2         2 
             1620  STORE_SUBSCR     

 L. 230      1622  LOAD_FAST                'mask_4bytes'
             1624  LOAD_CONST               4
             1626  BINARY_MULTIPLY  
             1628  LOAD_FAST                'efuse_mask_data'
             1630  LOAD_GLOBAL              keyslot6
             1632  LOAD_GLOBAL              keyslot7
             1634  BUILD_SLICE_2         2 
             1636  STORE_SUBSCR     

 L. 231      1638  LOAD_FAST                'mask_4bytes'
             1640  LOAD_CONST               4
             1642  BINARY_MULTIPLY  
             1644  LOAD_FAST                'efuse_mask_data'
             1646  LOAD_GLOBAL              keyslot10
             1648  LOAD_GLOBAL              keyslot10_end
             1650  BUILD_SLICE_2         2 
             1652  STORE_SUBSCR     

 L. 232      1654  LOAD_FAST                'rw_lock1'
             1656  LOAD_CONST               1
             1658  LOAD_GLOBAL              wr_lock_key_slot_6
             1660  BINARY_LSHIFT    
             1662  INPLACE_OR       
             1664  STORE_FAST               'rw_lock1'

 L. 233      1666  LOAD_FAST                'rw_lock1'
             1668  LOAD_CONST               1
             1670  LOAD_GLOBAL              wr_lock_key_slot_10
             1672  BINARY_LSHIFT    
             1674  INPLACE_OR       
             1676  STORE_FAST               'rw_lock1'

 L. 234      1678  LOAD_FAST                'rw_lock1'
             1680  LOAD_CONST               1
             1682  LOAD_GLOBAL              rd_lock_key_slot_6
             1684  BINARY_LSHIFT    
             1686  INPLACE_OR       
             1688  STORE_FAST               'rw_lock1'

 L. 235      1690  LOAD_FAST                'rw_lock1'
             1692  LOAD_CONST               1
             1694  LOAD_GLOBAL              rd_lock_key_slot_10
             1696  BINARY_LSHIFT    
             1698  INPLACE_OR       
             1700  STORE_FAST               'rw_lock1'
           1702_0  COME_FROM          1578  '1578'

 L. 236      1702  LOAD_FAST                'sec_eng_key_sel'
             1704  LOAD_CONST               2
             1706  COMPARE_OP               ==
         1708_1710  POP_JUMP_IF_FALSE  1828  'to 1828'

 L. 237      1712  LOAD_FAST                'flash_key'
             1714  LOAD_CONST               None
             1716  COMPARE_OP               is-not
         1718_1720  POP_JUMP_IF_FALSE  1724  'to 1724'

 L. 239      1722  JUMP_FORWARD       1828  'to 1828'
           1724_0  COME_FROM          1718  '1718'

 L. 241      1724  LOAD_FAST                'sec_eng_key'
             1726  LOAD_CONST               16
             1728  LOAD_CONST               32
             1730  BUILD_SLICE_2         2 
             1732  BINARY_SUBSCR    
             1734  LOAD_FAST                'efuse_data'
             1736  LOAD_GLOBAL              keyslot2
             1738  LOAD_GLOBAL              keyslot3
             1740  BUILD_SLICE_2         2 
             1742  STORE_SUBSCR     

 L. 242      1744  LOAD_FAST                'sec_eng_key'
             1746  LOAD_CONST               0
             1748  LOAD_CONST               16
             1750  BUILD_SLICE_2         2 
             1752  BINARY_SUBSCR    
             1754  LOAD_FAST                'efuse_data'
             1756  LOAD_GLOBAL              keyslot3
             1758  LOAD_GLOBAL              keyslot3_end
             1760  BUILD_SLICE_2         2 
             1762  STORE_SUBSCR     

 L. 243      1764  LOAD_FAST                'mask_4bytes'
             1766  LOAD_CONST               8
             1768  BINARY_MULTIPLY  
             1770  LOAD_FAST                'efuse_mask_data'
             1772  LOAD_GLOBAL              keyslot2
             1774  LOAD_GLOBAL              keyslot3_end
             1776  BUILD_SLICE_2         2 
             1778  STORE_SUBSCR     

 L. 244      1780  LOAD_FAST                'rw_lock0'
             1782  LOAD_CONST               1
             1784  LOAD_GLOBAL              wr_lock_key_slot_2
             1786  BINARY_LSHIFT    
             1788  INPLACE_OR       
             1790  STORE_FAST               'rw_lock0'

 L. 245      1792  LOAD_FAST                'rw_lock0'
             1794  LOAD_CONST               1
             1796  LOAD_GLOBAL              rd_lock_key_slot_2
             1798  BINARY_LSHIFT    
             1800  INPLACE_OR       
             1802  STORE_FAST               'rw_lock0'

 L. 246      1804  LOAD_FAST                'rw_lock0'
             1806  LOAD_CONST               1
             1808  LOAD_GLOBAL              wr_lock_key_slot_3
             1810  BINARY_LSHIFT    
             1812  INPLACE_OR       
             1814  STORE_FAST               'rw_lock0'

 L. 247      1816  LOAD_FAST                'rw_lock0'
             1818  LOAD_CONST               1
             1820  LOAD_GLOBAL              rd_lock_key_slot_3
             1822  BINARY_LSHIFT    
             1824  INPLACE_OR       
             1826  STORE_FAST               'rw_lock0'
           1828_0  COME_FROM          1722  '1722'
           1828_1  COME_FROM          1708  '1708'

 L. 248      1828  LOAD_FAST                'sec_eng_key_sel'
             1830  LOAD_CONST               3
             1832  COMPARE_OP               ==
         1834_1836  POP_JUMP_IF_FALSE  1926  'to 1926'

 L. 249      1838  LOAD_FAST                'flash_key'
             1840  LOAD_CONST               None
             1842  COMPARE_OP               is-not
         1844_1846  POP_JUMP_IF_FALSE  1850  'to 1850'

 L. 251      1848  JUMP_FORWARD       1926  'to 1926'
           1850_0  COME_FROM          1844  '1844'

 L. 253      1850  LOAD_FAST                'sec_eng_key'
             1852  LOAD_FAST                'efuse_data'
             1854  LOAD_GLOBAL              keyslot2
             1856  LOAD_GLOBAL              keyslot3_end
             1858  BUILD_SLICE_2         2 
             1860  STORE_SUBSCR     

 L. 254      1862  LOAD_FAST                'mask_4bytes'
             1864  LOAD_CONST               8
             1866  BINARY_MULTIPLY  
             1868  LOAD_FAST                'efuse_mask_data'
             1870  LOAD_GLOBAL              keyslot2
             1872  LOAD_GLOBAL              keyslot3_end
             1874  BUILD_SLICE_2         2 
             1876  STORE_SUBSCR     

 L. 255      1878  LOAD_FAST                'rw_lock0'
             1880  LOAD_CONST               1
             1882  LOAD_GLOBAL              wr_lock_key_slot_2
             1884  BINARY_LSHIFT    
             1886  INPLACE_OR       
             1888  STORE_FAST               'rw_lock0'

 L. 256      1890  LOAD_FAST                'rw_lock0'
             1892  LOAD_CONST               1
             1894  LOAD_GLOBAL              rd_lock_key_slot_2
             1896  BINARY_LSHIFT    
             1898  INPLACE_OR       
             1900  STORE_FAST               'rw_lock0'

 L. 257      1902  LOAD_FAST                'rw_lock0'
             1904  LOAD_CONST               1
             1906  LOAD_GLOBAL              wr_lock_key_slot_3
             1908  BINARY_LSHIFT    
             1910  INPLACE_OR       
             1912  STORE_FAST               'rw_lock0'

 L. 258      1914  LOAD_FAST                'rw_lock0'
             1916  LOAD_CONST               1
             1918  LOAD_GLOBAL              rd_lock_key_slot_3
             1920  BINARY_LSHIFT    
             1922  INPLACE_OR       
             1924  STORE_FAST               'rw_lock0'
           1926_0  COME_FROM          1848  '1848'
           1926_1  COME_FROM          1834  '1834'
           1926_2  COME_FROM          1438  '1438'
           1926_3  COME_FROM           592  '592'

 L. 260      1926  LOAD_GLOBAL              bytearray_data_merge
             1928  LOAD_FAST                'efuse_data'
             1930  LOAD_CONST               124
             1932  LOAD_CONST               128
             1934  BUILD_SLICE_2         2 
             1936  BINARY_SUBSCR    

 L. 261      1938  LOAD_GLOBAL              bflb_utils
             1940  LOAD_METHOD              int_to_4bytearray_l
             1942  LOAD_FAST                'rw_lock0'
             1944  CALL_METHOD_1         1  '1 positional argument'
             1946  LOAD_CONST               4
             1948  CALL_FUNCTION_3       3  '3 positional arguments'
             1950  LOAD_FAST                'efuse_data'
             1952  LOAD_CONST               124
             1954  LOAD_CONST               128
             1956  BUILD_SLICE_2         2 
             1958  STORE_SUBSCR     

 L. 262      1960  LOAD_GLOBAL              bytearray_data_merge
             1962  LOAD_FAST                'efuse_mask_data'
             1964  LOAD_CONST               124
             1966  LOAD_CONST               128
             1968  BUILD_SLICE_2         2 
             1970  BINARY_SUBSCR    

 L. 263      1972  LOAD_GLOBAL              bflb_utils
             1974  LOAD_METHOD              int_to_4bytearray_l
             1976  LOAD_FAST                'rw_lock0'
             1978  CALL_METHOD_1         1  '1 positional argument'
             1980  LOAD_CONST               4
             1982  CALL_FUNCTION_3       3  '3 positional arguments'
             1984  LOAD_FAST                'efuse_mask_data'
             1986  LOAD_CONST               124
             1988  LOAD_CONST               128
             1990  BUILD_SLICE_2         2 
             1992  STORE_SUBSCR     

 L. 264      1994  LOAD_GLOBAL              bytearray_data_merge
             1996  LOAD_FAST                'efuse_data'
             1998  LOAD_CONST               252
             2000  LOAD_CONST               256
             2002  BUILD_SLICE_2         2 
             2004  BINARY_SUBSCR    

 L. 265      2006  LOAD_GLOBAL              bflb_utils
             2008  LOAD_METHOD              int_to_4bytearray_l
             2010  LOAD_FAST                'rw_lock1'
             2012  CALL_METHOD_1         1  '1 positional argument'
             2014  LOAD_CONST               4
             2016  CALL_FUNCTION_3       3  '3 positional arguments'
             2018  LOAD_FAST                'efuse_data'
             2020  LOAD_CONST               252
             2022  LOAD_CONST               256
             2024  BUILD_SLICE_2         2 
             2026  STORE_SUBSCR     

 L. 266      2028  LOAD_GLOBAL              bytearray_data_merge
             2030  LOAD_FAST                'efuse_mask_data'
             2032  LOAD_CONST               252
             2034  LOAD_CONST               256
             2036  BUILD_SLICE_2         2 
             2038  BINARY_SUBSCR    

 L. 267      2040  LOAD_GLOBAL              bflb_utils
             2042  LOAD_METHOD              int_to_4bytearray_l
             2044  LOAD_FAST                'rw_lock1'
             2046  CALL_METHOD_1         1  '1 positional argument'
             2048  LOAD_CONST               4
             2050  CALL_FUNCTION_3       3  '3 positional arguments'
             2052  LOAD_FAST                'efuse_mask_data'
             2054  LOAD_CONST               252
             2056  LOAD_CONST               256
             2058  BUILD_SLICE_2         2 
             2060  STORE_SUBSCR     

 L. 269      2062  LOAD_FAST                'security'
             2064  LOAD_CONST               True
             2066  COMPARE_OP               is
         2068_2070  POP_JUMP_IF_FALSE  2120  'to 2120'

 L. 270      2072  LOAD_GLOBAL              bflb_utils
             2074  LOAD_METHOD              printf
             2076  LOAD_STR                 'Encrypt efuse data'
             2078  CALL_METHOD_1         1  '1 positional argument'
             2080  POP_TOP          

 L. 271      2082  LOAD_GLOBAL              bflb_utils
             2084  LOAD_METHOD              get_security_key
             2086  CALL_METHOD_0         0  '0 positional arguments'
             2088  UNPACK_SEQUENCE_2     2 
             2090  STORE_FAST               'security_key'
             2092  STORE_FAST               'security_iv'

 L. 272      2094  LOAD_GLOBAL              img_create_encrypt_data
             2096  LOAD_FAST                'efuse_data'
             2098  LOAD_FAST                'security_key'
             2100  LOAD_FAST                'security_iv'
             2102  LOAD_CONST               0
             2104  CALL_FUNCTION_4       4  '4 positional arguments'
             2106  STORE_FAST               'efuse_data'

 L. 273      2108  LOAD_GLOBAL              bytearray
             2110  LOAD_CONST               4096
             2112  CALL_FUNCTION_1       1  '1 positional argument'
             2114  LOAD_FAST                'efuse_data'
             2116  BINARY_ADD       
             2118  STORE_FAST               'efuse_data'
           2120_0  COME_FROM          2068  '2068'

 L. 274      2120  LOAD_GLOBAL              open
             2122  LOAD_FAST                'cfg'
             2124  LOAD_METHOD              get
             2126  LOAD_STR                 'Img_Group0_Cfg'
             2128  LOAD_STR                 'efuse_file'
             2130  CALL_METHOD_2         2  '2 positional arguments'
             2132  LOAD_STR                 'wb+'
             2134  CALL_FUNCTION_2       2  '2 positional arguments'
             2136  STORE_FAST               'fp'

 L. 275      2138  LOAD_FAST                'fp'
             2140  LOAD_METHOD              write
             2142  LOAD_FAST                'efuse_data'
             2144  CALL_METHOD_1         1  '1 positional argument'
             2146  POP_TOP          

 L. 276      2148  LOAD_FAST                'fp'
             2150  LOAD_METHOD              close
             2152  CALL_METHOD_0         0  '0 positional arguments'
             2154  POP_TOP          

 L. 277      2156  LOAD_GLOBAL              open
             2158  LOAD_FAST                'cfg'
             2160  LOAD_METHOD              get
             2162  LOAD_STR                 'Img_Group0_Cfg'
             2164  LOAD_STR                 'efuse_mask_file'
             2166  CALL_METHOD_2         2  '2 positional arguments'
             2168  LOAD_STR                 'wb+'
             2170  CALL_FUNCTION_2       2  '2 positional arguments'
             2172  STORE_FAST               'fp'

 L. 278      2174  LOAD_FAST                'fp'
             2176  LOAD_METHOD              write
             2178  LOAD_FAST                'efuse_mask_data'
             2180  CALL_METHOD_1         1  '1 positional argument'
             2182  POP_TOP          

 L. 279      2184  LOAD_FAST                'fp'
             2186  LOAD_METHOD              close
             2188  CALL_METHOD_0         0  '0 positional arguments'
             2190  POP_TOP          

Parse error at or near `CALL_METHOD_0' instruction at offset 2188


def img_update_efuse_group1--- This code section failed: ---

 L. 290         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'cfg'
                4  LOAD_METHOD              get
                6  LOAD_STR                 'Img_Group1_Cfg'
                8  LOAD_STR                 'efuse_file'
               10  CALL_METHOD_2         2  '2 positional arguments'
               12  LOAD_STR                 'rb'
               14  CALL_FUNCTION_2       2  '2 positional arguments'
               16  STORE_FAST               'fp'

 L. 291        18  LOAD_GLOBAL              bytearray
               20  LOAD_FAST                'fp'
               22  LOAD_METHOD              read
               24  CALL_METHOD_0         0  '0 positional arguments'
               26  CALL_FUNCTION_1       1  '1 positional argument'
               28  LOAD_GLOBAL              bytearray
               30  LOAD_CONST               0
               32  CALL_FUNCTION_1       1  '1 positional argument'
               34  BINARY_ADD       
               36  STORE_FAST               'efuse_data'

 L. 292        38  LOAD_FAST                'fp'
               40  LOAD_METHOD              close
               42  CALL_METHOD_0         0  '0 positional arguments'
               44  POP_TOP          

 L. 293        46  LOAD_GLOBAL              open
               48  LOAD_FAST                'cfg'
               50  LOAD_METHOD              get
               52  LOAD_STR                 'Img_Group1_Cfg'
               54  LOAD_STR                 'efuse_mask_file'
               56  CALL_METHOD_2         2  '2 positional arguments'
               58  LOAD_STR                 'rb'
               60  CALL_FUNCTION_2       2  '2 positional arguments'
               62  STORE_FAST               'fp'

 L. 294        64  LOAD_GLOBAL              bytearray
               66  LOAD_FAST                'fp'
               68  LOAD_METHOD              read
               70  CALL_METHOD_0         0  '0 positional arguments'
               72  CALL_FUNCTION_1       1  '1 positional argument'
               74  LOAD_GLOBAL              bytearray
               76  LOAD_CONST               0
               78  CALL_FUNCTION_1       1  '1 positional argument'
               80  BINARY_ADD       
               82  STORE_FAST               'efuse_mask_data'

 L. 295        84  LOAD_FAST                'fp'
               86  LOAD_METHOD              close
               88  CALL_METHOD_0         0  '0 positional arguments'
               90  POP_TOP          

 L. 297        92  LOAD_GLOBAL              bytearray
               94  LOAD_METHOD              fromhex
               96  LOAD_STR                 'FFFFFFFF'
               98  CALL_METHOD_1         1  '1 positional argument'
              100  STORE_FAST               'mask_4bytes'

 L. 300       102  LOAD_FAST                'flash_encryp_type'
              104  LOAD_CONST               3
              106  COMPARE_OP               >=
              108  POP_JUMP_IF_FALSE   128  'to 128'

 L. 301       110  LOAD_FAST                'efuse_data'
              112  LOAD_CONST               0
              114  DUP_TOP_TWO      
              116  BINARY_SUBSCR    
              118  LOAD_CONST               3
              120  INPLACE_OR       
              122  ROT_THREE        
              124  STORE_SUBSCR     
              126  JUMP_FORWARD        144  'to 144'
            128_0  COME_FROM           108  '108'

 L. 303       128  LOAD_FAST                'efuse_data'
              130  LOAD_CONST               0
              132  DUP_TOP_TWO      
              134  BINARY_SUBSCR    
              136  LOAD_FAST                'flash_encryp_type'
              138  INPLACE_OR       
              140  ROT_THREE        
              142  STORE_SUBSCR     
            144_0  COME_FROM           126  '126'

 L. 305       144  LOAD_FAST                'sign'
              146  LOAD_CONST               0
              148  COMPARE_OP               >
              150  POP_JUMP_IF_FALSE   184  'to 184'

 L. 306       152  LOAD_FAST                'efuse_data'
              154  LOAD_CONST               93
              156  DUP_TOP_TWO      
              158  BINARY_SUBSCR    
              160  LOAD_FAST                'sign'
              162  INPLACE_OR       
              164  ROT_THREE        
              166  STORE_SUBSCR     

 L. 307       168  LOAD_FAST                'efuse_mask_data'
              170  LOAD_CONST               93
              172  DUP_TOP_TWO      
              174  BINARY_SUBSCR    
              176  LOAD_CONST               255
              178  INPLACE_OR       
              180  ROT_THREE        
              182  STORE_SUBSCR     
            184_0  COME_FROM           150  '150'

 L. 309       184  LOAD_FAST                'flash_encryp_type'
              186  LOAD_CONST               0
              188  COMPARE_OP               >
              190  POP_JUMP_IF_FALSE   208  'to 208'

 L. 310       192  LOAD_FAST                'efuse_data'
              194  LOAD_CONST               0
              196  DUP_TOP_TWO      
              198  BINARY_SUBSCR    
              200  LOAD_CONST               48
              202  INPLACE_OR       
              204  ROT_THREE        
              206  STORE_SUBSCR     
            208_0  COME_FROM           190  '190'

 L. 311       208  LOAD_FAST                'efuse_mask_data'
              210  LOAD_CONST               0
              212  DUP_TOP_TWO      
              214  BINARY_SUBSCR    
              216  LOAD_CONST               255
              218  INPLACE_OR       
              220  ROT_THREE        
              222  STORE_SUBSCR     

 L. 312       224  LOAD_CONST               0
              226  STORE_FAST               'rw_lock0'

 L. 313       228  LOAD_CONST               0
              230  STORE_FAST               'rw_lock1'

 L. 314       232  LOAD_FAST                'pk_hash'
              234  LOAD_CONST               None
              236  COMPARE_OP               is-not
          238_240  POP_JUMP_IF_FALSE   294  'to 294'

 L. 315       242  LOAD_FAST                'pk_hash'
              244  LOAD_FAST                'efuse_data'
              246  LOAD_GLOBAL              keyslot8
              248  LOAD_GLOBAL              keyslot10
              250  BUILD_SLICE_2         2 
              252  STORE_SUBSCR     

 L. 316       254  LOAD_FAST                'mask_4bytes'
              256  LOAD_CONST               8
              258  BINARY_MULTIPLY  
              260  LOAD_FAST                'efuse_mask_data'
              262  LOAD_GLOBAL              keyslot8
              264  LOAD_GLOBAL              keyslot10
              266  BUILD_SLICE_2         2 
              268  STORE_SUBSCR     

 L. 317       270  LOAD_FAST                'rw_lock1'
              272  LOAD_CONST               1
              274  LOAD_GLOBAL              wr_lock_key_slot_8
              276  BINARY_LSHIFT    
              278  INPLACE_OR       
              280  STORE_FAST               'rw_lock1'

 L. 318       282  LOAD_FAST                'rw_lock1'
              284  LOAD_CONST               1
              286  LOAD_GLOBAL              wr_lock_key_slot_9
              288  BINARY_LSHIFT    
              290  INPLACE_OR       
              292  STORE_FAST               'rw_lock1'
            294_0  COME_FROM           238  '238'

 L. 319       294  LOAD_FAST                'flash_key'
              296  LOAD_CONST               None
              298  COMPARE_OP               is-not
          300_302  POP_JUMP_IF_FALSE   660  'to 660'

 L. 320       304  LOAD_FAST                'flash_encryp_type'
              306  LOAD_CONST               1
              308  COMPARE_OP               ==
          310_312  POP_JUMP_IF_FALSE   378  'to 378'

 L. 322       314  LOAD_FAST                'flash_key'
              316  LOAD_CONST               0
              318  LOAD_CONST               16
              320  BUILD_SLICE_2         2 
              322  BINARY_SUBSCR    
              324  LOAD_FAST                'efuse_data'
              326  LOAD_GLOBAL              keyslot3
              328  LOAD_GLOBAL              keyslot3_end
              330  BUILD_SLICE_2         2 
              332  STORE_SUBSCR     

 L. 323       334  LOAD_FAST                'mask_4bytes'
              336  LOAD_CONST               4
              338  BINARY_MULTIPLY  
              340  LOAD_FAST                'efuse_mask_data'
              342  LOAD_GLOBAL              keyslot3
              344  LOAD_GLOBAL              keyslot3_end
              346  BUILD_SLICE_2         2 
              348  STORE_SUBSCR     

 L. 324       350  LOAD_FAST                'rw_lock0'
              352  LOAD_CONST               1
              354  LOAD_GLOBAL              wr_lock_key_slot_3
              356  BINARY_LSHIFT    
              358  INPLACE_OR       
              360  STORE_FAST               'rw_lock0'

 L. 325       362  LOAD_FAST                'rw_lock0'
              364  LOAD_CONST               1
              366  LOAD_GLOBAL              rd_lock_key_slot_3
              368  BINARY_LSHIFT    
              370  INPLACE_OR       
              372  STORE_FAST               'rw_lock0'
          374_376  JUMP_FORWARD        660  'to 660'
            378_0  COME_FROM           310  '310'

 L. 326       378  LOAD_FAST                'flash_encryp_type'
              380  LOAD_CONST               2
              382  COMPARE_OP               ==
          384_386  POP_JUMP_IF_FALSE   466  'to 466'

 L. 328       388  LOAD_FAST                'flash_key'
              390  LOAD_FAST                'efuse_data'
              392  LOAD_GLOBAL              keyslot4
              394  LOAD_GLOBAL              keyslot6
              396  BUILD_SLICE_2         2 
              398  STORE_SUBSCR     

 L. 329       400  LOAD_FAST                'mask_4bytes'
              402  LOAD_CONST               8
              404  BINARY_MULTIPLY  
              406  LOAD_FAST                'efuse_mask_data'
              408  LOAD_GLOBAL              keyslot4
              410  LOAD_GLOBAL              keyslot6
              412  BUILD_SLICE_2         2 
              414  STORE_SUBSCR     

 L. 330       416  LOAD_FAST                'rw_lock1'
              418  LOAD_CONST               1
              420  LOAD_GLOBAL              wr_lock_key_slot_4
              422  BINARY_LSHIFT    
              424  INPLACE_OR       
              426  STORE_FAST               'rw_lock1'

 L. 331       428  LOAD_FAST                'rw_lock1'
              430  LOAD_CONST               1
              432  LOAD_GLOBAL              wr_lock_key_slot_5
              434  BINARY_LSHIFT    
              436  INPLACE_OR       
              438  STORE_FAST               'rw_lock1'

 L. 332       440  LOAD_FAST                'rw_lock1'
              442  LOAD_CONST               1
              444  LOAD_GLOBAL              rd_lock_key_slot_4
              446  BINARY_LSHIFT    
              448  INPLACE_OR       
              450  STORE_FAST               'rw_lock1'

 L. 333       452  LOAD_FAST                'rw_lock1'
              454  LOAD_CONST               1
              456  LOAD_GLOBAL              rd_lock_key_slot_5
              458  BINARY_LSHIFT    
              460  INPLACE_OR       
              462  STORE_FAST               'rw_lock1'
              464  JUMP_FORWARD        660  'to 660'
            466_0  COME_FROM           384  '384'

 L. 334       466  LOAD_FAST                'flash_encryp_type'
              468  LOAD_CONST               3
              470  COMPARE_OP               ==
          472_474  POP_JUMP_IF_FALSE   554  'to 554'

 L. 336       476  LOAD_FAST                'flash_key'
              478  LOAD_FAST                'efuse_data'
              480  LOAD_GLOBAL              keyslot4
              482  LOAD_GLOBAL              keyslot6
              484  BUILD_SLICE_2         2 
              486  STORE_SUBSCR     

 L. 337       488  LOAD_FAST                'mask_4bytes'
              490  LOAD_CONST               8
              492  BINARY_MULTIPLY  
              494  LOAD_FAST                'efuse_mask_data'
              496  LOAD_GLOBAL              keyslot4
              498  LOAD_GLOBAL              keyslot6
              500  BUILD_SLICE_2         2 
              502  STORE_SUBSCR     

 L. 338       504  LOAD_FAST                'rw_lock1'
              506  LOAD_CONST               1
              508  LOAD_GLOBAL              wr_lock_key_slot_4
              510  BINARY_LSHIFT    
              512  INPLACE_OR       
              514  STORE_FAST               'rw_lock1'

 L. 339       516  LOAD_FAST                'rw_lock1'
              518  LOAD_CONST               1
              520  LOAD_GLOBAL              wr_lock_key_slot_5
              522  BINARY_LSHIFT    
              524  INPLACE_OR       
              526  STORE_FAST               'rw_lock1'

 L. 340       528  LOAD_FAST                'rw_lock1'
              530  LOAD_CONST               1
              532  LOAD_GLOBAL              rd_lock_key_slot_4
              534  BINARY_LSHIFT    
              536  INPLACE_OR       
              538  STORE_FAST               'rw_lock1'

 L. 341       540  LOAD_FAST                'rw_lock1'
              542  LOAD_CONST               1
              544  LOAD_GLOBAL              rd_lock_key_slot_5
              546  BINARY_LSHIFT    
              548  INPLACE_OR       
              550  STORE_FAST               'rw_lock1'
              552  JUMP_FORWARD        660  'to 660'
            554_0  COME_FROM           472  '472'

 L. 342       554  LOAD_FAST                'flash_encryp_type'
              556  LOAD_CONST               4
              558  COMPARE_OP               ==
          560_562  POP_JUMP_IF_TRUE    584  'to 584'

 L. 343       564  LOAD_FAST                'flash_encryp_type'
              566  LOAD_CONST               5
              568  COMPARE_OP               ==
          570_572  POP_JUMP_IF_TRUE    584  'to 584'

 L. 344       574  LOAD_FAST                'flash_encryp_type'
              576  LOAD_CONST               6
              578  COMPARE_OP               ==
          580_582  POP_JUMP_IF_FALSE   660  'to 660'
            584_0  COME_FROM           570  '570'
            584_1  COME_FROM           560  '560'

 L. 346       584  LOAD_FAST                'flash_key'
              586  LOAD_FAST                'efuse_data'
              588  LOAD_GLOBAL              keyslot4
              590  LOAD_GLOBAL              keyslot6
              592  BUILD_SLICE_2         2 
              594  STORE_SUBSCR     

 L. 347       596  LOAD_FAST                'mask_4bytes'
              598  LOAD_CONST               8
              600  BINARY_MULTIPLY  
              602  LOAD_FAST                'efuse_mask_data'
              604  LOAD_GLOBAL              keyslot4
              606  LOAD_GLOBAL              keyslot6
              608  BUILD_SLICE_2         2 
              610  STORE_SUBSCR     

 L. 348       612  LOAD_FAST                'rw_lock1'
              614  LOAD_CONST               1
              616  LOAD_GLOBAL              wr_lock_key_slot_4
              618  BINARY_LSHIFT    
              620  INPLACE_OR       
              622  STORE_FAST               'rw_lock1'

 L. 349       624  LOAD_FAST                'rw_lock1'
              626  LOAD_CONST               1
              628  LOAD_GLOBAL              wr_lock_key_slot_5
              630  BINARY_LSHIFT    
              632  INPLACE_OR       
              634  STORE_FAST               'rw_lock1'

 L. 350       636  LOAD_FAST                'rw_lock1'
              638  LOAD_CONST               1
              640  LOAD_GLOBAL              rd_lock_key_slot_4
              642  BINARY_LSHIFT    
              644  INPLACE_OR       
              646  STORE_FAST               'rw_lock1'

 L. 351       648  LOAD_FAST                'rw_lock1'
              650  LOAD_CONST               1
              652  LOAD_GLOBAL              rd_lock_key_slot_5
              654  BINARY_LSHIFT    
              656  INPLACE_OR       
              658  STORE_FAST               'rw_lock1'
            660_0  COME_FROM           580  '580'
            660_1  COME_FROM           552  '552'
            660_2  COME_FROM           464  '464'
            660_3  COME_FROM           374  '374'
            660_4  COME_FROM           300  '300'

 L. 353       660  LOAD_FAST                'sec_eng_key'
              662  LOAD_CONST               None
              664  COMPARE_OP               is-not
          666_668  POP_JUMP_IF_FALSE  2016  'to 2016'

 L. 354       670  LOAD_FAST                'flash_encryp_type'
              672  LOAD_CONST               0
              674  COMPARE_OP               ==
          676_678  POP_JUMP_IF_FALSE  1168  'to 1168'

 L. 355       680  LOAD_FAST                'sec_eng_key_sel'
              682  LOAD_CONST               0
              684  COMPARE_OP               ==
          686_688  POP_JUMP_IF_FALSE   794  'to 794'

 L. 356       690  LOAD_FAST                'sec_eng_key'
              692  LOAD_CONST               16
              694  LOAD_CONST               32
              696  BUILD_SLICE_2         2 
              698  BINARY_SUBSCR    
              700  LOAD_FAST                'efuse_data'
              702  LOAD_GLOBAL              keyslot5
              704  LOAD_GLOBAL              keyslot6
              706  BUILD_SLICE_2         2 
              708  STORE_SUBSCR     

 L. 357       710  LOAD_FAST                'sec_eng_key'
              712  LOAD_CONST               0
              714  LOAD_CONST               16
              716  BUILD_SLICE_2         2 
              718  BINARY_SUBSCR    
              720  LOAD_FAST                'efuse_data'
              722  LOAD_GLOBAL              keyslot6
              724  LOAD_GLOBAL              keyslot7
              726  BUILD_SLICE_2         2 
              728  STORE_SUBSCR     

 L. 358       730  LOAD_FAST                'mask_4bytes'
              732  LOAD_CONST               8
              734  BINARY_MULTIPLY  
              736  LOAD_FAST                'efuse_mask_data'
              738  LOAD_GLOBAL              keyslot5
              740  LOAD_GLOBAL              keyslot7
              742  BUILD_SLICE_2         2 
              744  STORE_SUBSCR     

 L. 359       746  LOAD_FAST                'rw_lock1'
              748  LOAD_CONST               1
              750  LOAD_GLOBAL              wr_lock_key_slot_5
              752  BINARY_LSHIFT    
              754  INPLACE_OR       
              756  STORE_FAST               'rw_lock1'

 L. 360       758  LOAD_FAST                'rw_lock1'
              760  LOAD_CONST               1
              762  LOAD_GLOBAL              wr_lock_key_slot_6
              764  BINARY_LSHIFT    
              766  INPLACE_OR       
              768  STORE_FAST               'rw_lock1'

 L. 361       770  LOAD_FAST                'rw_lock1'
              772  LOAD_CONST               1
              774  LOAD_GLOBAL              rd_lock_key_slot_5
              776  BINARY_LSHIFT    
              778  INPLACE_OR       
              780  STORE_FAST               'rw_lock1'

 L. 362       782  LOAD_FAST                'rw_lock1'
              784  LOAD_CONST               1
              786  LOAD_GLOBAL              rd_lock_key_slot_6
              788  BINARY_LSHIFT    
              790  INPLACE_OR       
              792  STORE_FAST               'rw_lock1'
            794_0  COME_FROM           686  '686'

 L. 363       794  LOAD_FAST                'sec_eng_key_sel'
              796  LOAD_CONST               1
              798  COMPARE_OP               ==
          800_802  POP_JUMP_IF_FALSE   908  'to 908'

 L. 364       804  LOAD_FAST                'sec_eng_key'
              806  LOAD_CONST               16
              808  LOAD_CONST               32
              810  BUILD_SLICE_2         2 
              812  BINARY_SUBSCR    
              814  LOAD_FAST                'efuse_data'
              816  LOAD_GLOBAL              keyslot6
              818  LOAD_GLOBAL              keyslot7
              820  BUILD_SLICE_2         2 
              822  STORE_SUBSCR     

 L. 365       824  LOAD_FAST                'sec_eng_key'
              826  LOAD_CONST               0
              828  LOAD_CONST               16
              830  BUILD_SLICE_2         2 
              832  BINARY_SUBSCR    
              834  LOAD_FAST                'efuse_data'
              836  LOAD_GLOBAL              keyslot7
              838  LOAD_GLOBAL              keyslot8
              840  BUILD_SLICE_2         2 
              842  STORE_SUBSCR     

 L. 366       844  LOAD_FAST                'mask_4bytes'
              846  LOAD_CONST               8
              848  BINARY_MULTIPLY  
              850  LOAD_FAST                'efuse_mask_data'
              852  LOAD_GLOBAL              keyslot6
              854  LOAD_GLOBAL              keyslot8
              856  BUILD_SLICE_2         2 
              858  STORE_SUBSCR     

 L. 367       860  LOAD_FAST                'rw_lock1'
              862  LOAD_CONST               1
              864  LOAD_GLOBAL              wr_lock_key_slot_6
              866  BINARY_LSHIFT    
              868  INPLACE_OR       
              870  STORE_FAST               'rw_lock1'

 L. 368       872  LOAD_FAST                'rw_lock1'
              874  LOAD_CONST               1
              876  LOAD_GLOBAL              wr_lock_key_slot_7
              878  BINARY_LSHIFT    
              880  INPLACE_OR       
              882  STORE_FAST               'rw_lock1'

 L. 369       884  LOAD_FAST                'rw_lock1'
              886  LOAD_CONST               1
              888  LOAD_GLOBAL              rd_lock_key_slot_6
              890  BINARY_LSHIFT    
              892  INPLACE_OR       
              894  STORE_FAST               'rw_lock1'

 L. 370       896  LOAD_FAST                'rw_lock1'
              898  LOAD_CONST               1
              900  LOAD_GLOBAL              rd_lock_key_slot_7
              902  BINARY_LSHIFT    
              904  INPLACE_OR       
              906  STORE_FAST               'rw_lock1'
            908_0  COME_FROM           800  '800'

 L. 371       908  LOAD_FAST                'sec_eng_key_sel'
              910  LOAD_CONST               2
              912  COMPARE_OP               ==
          914_916  POP_JUMP_IF_FALSE  1038  'to 1038'

 L. 372       918  LOAD_FAST                'sec_eng_key'
              920  LOAD_CONST               16
              922  LOAD_CONST               32
              924  BUILD_SLICE_2         2 
              926  BINARY_SUBSCR    
              928  LOAD_FAST                'efuse_data'
              930  LOAD_GLOBAL              keyslot7
              932  LOAD_GLOBAL              keyslot8
              934  BUILD_SLICE_2         2 
              936  STORE_SUBSCR     

 L. 373       938  LOAD_FAST                'sec_eng_key'
              940  LOAD_CONST               0
              942  LOAD_CONST               16
              944  BUILD_SLICE_2         2 
              946  BINARY_SUBSCR    
              948  LOAD_FAST                'efuse_data'
              950  LOAD_GLOBAL              keyslot5
              952  LOAD_GLOBAL              keyslot6
              954  BUILD_SLICE_2         2 
              956  STORE_SUBSCR     

 L. 374       958  LOAD_FAST                'mask_4bytes'
              960  LOAD_CONST               4
              962  BINARY_MULTIPLY  
              964  LOAD_FAST                'efuse_mask_data'
              966  LOAD_GLOBAL              keyslot7
              968  LOAD_GLOBAL              keyslot8
              970  BUILD_SLICE_2         2 
              972  STORE_SUBSCR     

 L. 375       974  LOAD_FAST                'mask_4bytes'
              976  LOAD_CONST               4
              978  BINARY_MULTIPLY  
              980  LOAD_FAST                'efuse_mask_data'
              982  LOAD_GLOBAL              keyslot5
              984  LOAD_GLOBAL              keyslot6
              986  BUILD_SLICE_2         2 
              988  STORE_SUBSCR     

 L. 376       990  LOAD_FAST                'rw_lock1'
              992  LOAD_CONST               1
              994  LOAD_GLOBAL              wr_lock_key_slot_7
              996  BINARY_LSHIFT    
              998  INPLACE_OR       
             1000  STORE_FAST               'rw_lock1'

 L. 377      1002  LOAD_FAST                'rw_lock1'
             1004  LOAD_CONST               1
             1006  LOAD_GLOBAL              wr_lock_key_slot_5
             1008  BINARY_LSHIFT    
             1010  INPLACE_OR       
             1012  STORE_FAST               'rw_lock1'

 L. 378      1014  LOAD_FAST                'rw_lock1'
             1016  LOAD_CONST               1
             1018  LOAD_GLOBAL              rd_lock_key_slot_7
             1020  BINARY_LSHIFT    
             1022  INPLACE_OR       
             1024  STORE_FAST               'rw_lock1'

 L. 379      1026  LOAD_FAST                'rw_lock1'
             1028  LOAD_CONST               1
             1030  LOAD_GLOBAL              rd_lock_key_slot_5
             1032  BINARY_LSHIFT    
             1034  INPLACE_OR       
             1036  STORE_FAST               'rw_lock1'
           1038_0  COME_FROM           914  '914'

 L. 380      1038  LOAD_FAST                'sec_eng_key_sel'
             1040  LOAD_CONST               3
             1042  COMPARE_OP               ==
         1044_1046  POP_JUMP_IF_FALSE  1168  'to 1168'

 L. 381      1048  LOAD_FAST                'sec_eng_key'
             1050  LOAD_CONST               16
             1052  LOAD_CONST               32
             1054  BUILD_SLICE_2         2 
             1056  BINARY_SUBSCR    
             1058  LOAD_FAST                'efuse_data'
             1060  LOAD_GLOBAL              keyslot7
             1062  LOAD_GLOBAL              keyslot8
             1064  BUILD_SLICE_2         2 
             1066  STORE_SUBSCR     

 L. 382      1068  LOAD_FAST                'sec_eng_key'
             1070  LOAD_CONST               0
             1072  LOAD_CONST               16
             1074  BUILD_SLICE_2         2 
             1076  BINARY_SUBSCR    
             1078  LOAD_FAST                'efuse_data'
             1080  LOAD_GLOBAL              keyslot5
             1082  LOAD_GLOBAL              keyslot6
             1084  BUILD_SLICE_2         2 
             1086  STORE_SUBSCR     

 L. 383      1088  LOAD_FAST                'mask_4bytes'
             1090  LOAD_CONST               4
             1092  BINARY_MULTIPLY  
             1094  LOAD_FAST                'efuse_mask_data'
             1096  LOAD_GLOBAL              keyslot7
             1098  LOAD_GLOBAL              keyslot8
             1100  BUILD_SLICE_2         2 
             1102  STORE_SUBSCR     

 L. 384      1104  LOAD_FAST                'mask_4bytes'
             1106  LOAD_CONST               4
             1108  BINARY_MULTIPLY  
             1110  LOAD_FAST                'efuse_mask_data'
             1112  LOAD_GLOBAL              keyslot5
             1114  LOAD_GLOBAL              keyslot6
             1116  BUILD_SLICE_2         2 
             1118  STORE_SUBSCR     

 L. 385      1120  LOAD_FAST                'rw_lock1'
             1122  LOAD_CONST               1
             1124  LOAD_GLOBAL              wr_lock_key_slot_7
             1126  BINARY_LSHIFT    
             1128  INPLACE_OR       
             1130  STORE_FAST               'rw_lock1'

 L. 386      1132  LOAD_FAST                'rw_lock1'
             1134  LOAD_CONST               1
             1136  LOAD_GLOBAL              wr_lock_key_slot_5
             1138  BINARY_LSHIFT    
             1140  INPLACE_OR       
             1142  STORE_FAST               'rw_lock1'

 L. 387      1144  LOAD_FAST                'rw_lock1'
             1146  LOAD_CONST               1
             1148  LOAD_GLOBAL              rd_lock_key_slot_7
             1150  BINARY_LSHIFT    
             1152  INPLACE_OR       
             1154  STORE_FAST               'rw_lock1'

 L. 388      1156  LOAD_FAST                'rw_lock1'
             1158  LOAD_CONST               1
             1160  LOAD_GLOBAL              rd_lock_key_slot_5
             1162  BINARY_LSHIFT    
             1164  INPLACE_OR       
             1166  STORE_FAST               'rw_lock1'
           1168_0  COME_FROM          1044  '1044'
           1168_1  COME_FROM           676  '676'

 L. 389      1168  LOAD_FAST                'flash_encryp_type'
             1170  LOAD_CONST               1
             1172  COMPARE_OP               ==
         1174_1176  POP_JUMP_IF_FALSE  1482  'to 1482'

 L. 390      1178  LOAD_FAST                'sec_eng_key_sel'
             1180  LOAD_CONST               0
             1182  COMPARE_OP               ==
         1184_1186  POP_JUMP_IF_FALSE  1248  'to 1248'

 L. 391      1188  LOAD_FAST                'sec_eng_key'
             1190  LOAD_CONST               0
             1192  LOAD_CONST               16
             1194  BUILD_SLICE_2         2 
             1196  BINARY_SUBSCR    
             1198  LOAD_FAST                'efuse_data'
             1200  LOAD_GLOBAL              keyslot7
             1202  LOAD_GLOBAL              keyslot8
             1204  BUILD_SLICE_2         2 
             1206  STORE_SUBSCR     

 L. 392      1208  LOAD_FAST                'mask_4bytes'
             1210  LOAD_CONST               4
             1212  BINARY_MULTIPLY  
             1214  LOAD_FAST                'efuse_mask_data'
             1216  LOAD_GLOBAL              keyslot7
             1218  LOAD_GLOBAL              keyslot8
             1220  BUILD_SLICE_2         2 
             1222  STORE_SUBSCR     

 L. 393      1224  LOAD_FAST                'rw_lock1'
             1226  LOAD_CONST               1
             1228  LOAD_GLOBAL              wr_lock_key_slot_7
             1230  BINARY_LSHIFT    
             1232  INPLACE_OR       
             1234  STORE_FAST               'rw_lock1'

 L. 394      1236  LOAD_FAST                'rw_lock1'
             1238  LOAD_CONST               1
             1240  LOAD_GLOBAL              rd_lock_key_slot_7
             1242  BINARY_LSHIFT    
             1244  INPLACE_OR       
             1246  STORE_FAST               'rw_lock1'
           1248_0  COME_FROM          1184  '1184'

 L. 395      1248  LOAD_FAST                'sec_eng_key_sel'
             1250  LOAD_CONST               1
             1252  COMPARE_OP               ==
         1254_1256  POP_JUMP_IF_FALSE  1318  'to 1318'

 L. 396      1258  LOAD_FAST                'sec_eng_key'
             1260  LOAD_CONST               0
             1262  LOAD_CONST               16
             1264  BUILD_SLICE_2         2 
             1266  BINARY_SUBSCR    
             1268  LOAD_FAST                'efuse_data'
             1270  LOAD_GLOBAL              keyslot6
             1272  LOAD_GLOBAL              keyslot7
             1274  BUILD_SLICE_2         2 
             1276  STORE_SUBSCR     

 L. 397      1278  LOAD_FAST                'mask_4bytes'
             1280  LOAD_CONST               4
             1282  BINARY_MULTIPLY  
             1284  LOAD_FAST                'efuse_mask_data'
             1286  LOAD_GLOBAL              keyslot6
             1288  LOAD_GLOBAL              keyslot7
             1290  BUILD_SLICE_2         2 
             1292  STORE_SUBSCR     

 L. 398      1294  LOAD_FAST                'rw_lock1'
             1296  LOAD_CONST               1
             1298  LOAD_GLOBAL              wr_lock_key_slot_6
             1300  BINARY_LSHIFT    
             1302  INPLACE_OR       
             1304  STORE_FAST               'rw_lock1'

 L. 399      1306  LOAD_FAST                'rw_lock1'
             1308  LOAD_CONST               1
             1310  LOAD_GLOBAL              rd_lock_key_slot_6
             1312  BINARY_LSHIFT    
             1314  INPLACE_OR       
             1316  STORE_FAST               'rw_lock1'
           1318_0  COME_FROM          1254  '1254'

 L. 400      1318  LOAD_FAST                'sec_eng_key_sel'
             1320  LOAD_CONST               2
             1322  COMPARE_OP               ==
         1324_1326  POP_JUMP_IF_FALSE  1400  'to 1400'

 L. 401      1328  LOAD_FAST                'flash_key'
             1330  LOAD_CONST               None
             1332  COMPARE_OP               is-not
         1334_1336  POP_JUMP_IF_FALSE  1340  'to 1340'

 L. 403      1338  JUMP_FORWARD       1400  'to 1400'
           1340_0  COME_FROM          1334  '1334'

 L. 405      1340  LOAD_FAST                'sec_eng_key'
             1342  LOAD_CONST               0
             1344  LOAD_CONST               16
             1346  BUILD_SLICE_2         2 
             1348  BINARY_SUBSCR    
             1350  LOAD_FAST                'efuse_data'
             1352  LOAD_GLOBAL              keyslot3
             1354  LOAD_GLOBAL              keyslot3_end
             1356  BUILD_SLICE_2         2 
             1358  STORE_SUBSCR     

 L. 406      1360  LOAD_FAST                'mask_4bytes'
             1362  LOAD_CONST               4
             1364  BINARY_MULTIPLY  
             1366  LOAD_FAST                'efuse_mask_data'
             1368  LOAD_GLOBAL              keyslot3
             1370  LOAD_GLOBAL              keyslot3_end
             1372  BUILD_SLICE_2         2 
             1374  STORE_SUBSCR     

 L. 407      1376  LOAD_FAST                'rw_lock0'
             1378  LOAD_CONST               1
             1380  LOAD_GLOBAL              wr_lock_key_slot_3
             1382  BINARY_LSHIFT    
             1384  INPLACE_OR       
             1386  STORE_FAST               'rw_lock0'

 L. 408      1388  LOAD_FAST                'rw_lock0'
             1390  LOAD_CONST               1
             1392  LOAD_GLOBAL              rd_lock_key_slot_3
             1394  BINARY_LSHIFT    
             1396  INPLACE_OR       
             1398  STORE_FAST               'rw_lock0'
           1400_0  COME_FROM          1338  '1338'
           1400_1  COME_FROM          1324  '1324'

 L. 409      1400  LOAD_FAST                'sec_eng_key_sel'
             1402  LOAD_CONST               3
             1404  COMPARE_OP               ==
         1406_1408  POP_JUMP_IF_FALSE  1482  'to 1482'

 L. 410      1410  LOAD_FAST                'flash_key'
             1412  LOAD_CONST               None
             1414  COMPARE_OP               is-not
         1416_1418  POP_JUMP_IF_FALSE  1422  'to 1422'

 L. 412      1420  JUMP_FORWARD       1482  'to 1482'
           1422_0  COME_FROM          1416  '1416'

 L. 414      1422  LOAD_FAST                'sec_eng_key'
             1424  LOAD_CONST               0
             1426  LOAD_CONST               16
             1428  BUILD_SLICE_2         2 
             1430  BINARY_SUBSCR    
             1432  LOAD_FAST                'efuse_data'
             1434  LOAD_GLOBAL              keyslot2
             1436  LOAD_GLOBAL              keyslot3
             1438  BUILD_SLICE_2         2 
             1440  STORE_SUBSCR     

 L. 415      1442  LOAD_FAST                'mask_4bytes'
             1444  LOAD_CONST               4
             1446  BINARY_MULTIPLY  
             1448  LOAD_FAST                'efuse_mask_data'
             1450  LOAD_GLOBAL              keyslot2
             1452  LOAD_GLOBAL              keyslot3
             1454  BUILD_SLICE_2         2 
             1456  STORE_SUBSCR     

 L. 416      1458  LOAD_FAST                'rw_lock0'
             1460  LOAD_CONST               1
             1462  LOAD_GLOBAL              wr_lock_key_slot_2
             1464  BINARY_LSHIFT    
             1466  INPLACE_OR       
             1468  STORE_FAST               'rw_lock0'

 L. 417      1470  LOAD_FAST                'rw_lock0'
             1472  LOAD_CONST               1
             1474  LOAD_GLOBAL              rd_lock_key_slot_2
             1476  BINARY_LSHIFT    
             1478  INPLACE_OR       
             1480  STORE_FAST               'rw_lock0'
           1482_0  COME_FROM          1420  '1420'
           1482_1  COME_FROM          1406  '1406'
           1482_2  COME_FROM          1174  '1174'

 L. 418      1482  LOAD_FAST                'flash_encryp_type'
             1484  LOAD_CONST               2
             1486  COMPARE_OP               ==
         1488_1490  POP_JUMP_IF_TRUE   1532  'to 1532'

 L. 419      1492  LOAD_FAST                'flash_encryp_type'
             1494  LOAD_CONST               3
             1496  COMPARE_OP               ==
         1498_1500  POP_JUMP_IF_TRUE   1532  'to 1532'

 L. 420      1502  LOAD_FAST                'flash_encryp_type'
             1504  LOAD_CONST               4
             1506  COMPARE_OP               ==
         1508_1510  POP_JUMP_IF_TRUE   1532  'to 1532'

 L. 421      1512  LOAD_FAST                'flash_encryp_type'
             1514  LOAD_CONST               5
             1516  COMPARE_OP               ==
         1518_1520  POP_JUMP_IF_TRUE   1532  'to 1532'

 L. 422      1522  LOAD_FAST                'flash_encryp_type'
             1524  LOAD_CONST               6
             1526  COMPARE_OP               ==
         1528_1530  POP_JUMP_IF_FALSE  2016  'to 2016'
           1532_0  COME_FROM          1518  '1518'
           1532_1  COME_FROM          1508  '1508'
           1532_2  COME_FROM          1498  '1498'
           1532_3  COME_FROM          1488  '1488'

 L. 423      1532  LOAD_FAST                'sec_eng_key_sel'
             1534  LOAD_CONST               0
             1536  COMPARE_OP               ==
         1538_1540  POP_JUMP_IF_FALSE  1662  'to 1662'

 L. 424      1542  LOAD_FAST                'sec_eng_key'
             1544  LOAD_CONST               16
             1546  LOAD_CONST               32
             1548  BUILD_SLICE_2         2 
             1550  BINARY_SUBSCR    
             1552  LOAD_FAST                'efuse_data'
             1554  LOAD_GLOBAL              keyslot7
             1556  LOAD_GLOBAL              keyslot8
             1558  BUILD_SLICE_2         2 
             1560  STORE_SUBSCR     

 L. 425      1562  LOAD_FAST                'sec_eng_key'
             1564  LOAD_CONST               0
             1566  LOAD_CONST               16
             1568  BUILD_SLICE_2         2 
             1570  BINARY_SUBSCR    
             1572  LOAD_FAST                'efuse_data'
             1574  LOAD_GLOBAL              keyslot11
             1576  LOAD_GLOBAL              keyslot11_end
             1578  BUILD_SLICE_2         2 
             1580  STORE_SUBSCR     

 L. 426      1582  LOAD_FAST                'mask_4bytes'
             1584  LOAD_CONST               4
             1586  BINARY_MULTIPLY  
             1588  LOAD_FAST                'efuse_mask_data'
             1590  LOAD_GLOBAL              keyslot7
             1592  LOAD_GLOBAL              keyslot8
             1594  BUILD_SLICE_2         2 
             1596  STORE_SUBSCR     

 L. 427      1598  LOAD_FAST                'mask_4bytes'
             1600  LOAD_CONST               4
             1602  BINARY_MULTIPLY  
             1604  LOAD_FAST                'efuse_mask_data'
             1606  LOAD_GLOBAL              keyslot11
             1608  LOAD_GLOBAL              keyslot11_end
             1610  BUILD_SLICE_2         2 
             1612  STORE_SUBSCR     

 L. 428      1614  LOAD_FAST                'rw_lock1'
             1616  LOAD_CONST               1
             1618  LOAD_GLOBAL              wr_lock_key_slot_7
             1620  BINARY_LSHIFT    
             1622  INPLACE_OR       
             1624  STORE_FAST               'rw_lock1'

 L. 429      1626  LOAD_FAST                'rw_lock0'
             1628  LOAD_CONST               1
             1630  LOAD_GLOBAL              rd_lock_key_slot_11
             1632  BINARY_LSHIFT    
             1634  INPLACE_OR       
             1636  STORE_FAST               'rw_lock0'

 L. 430      1638  LOAD_FAST                'rw_lock1'
             1640  LOAD_CONST               1
             1642  LOAD_GLOBAL              wr_lock_key_slot_7
             1644  BINARY_LSHIFT    
             1646  INPLACE_OR       
             1648  STORE_FAST               'rw_lock1'

 L. 431      1650  LOAD_FAST                'rw_lock0'
             1652  LOAD_CONST               1
             1654  LOAD_GLOBAL              rd_lock_key_slot_11
             1656  BINARY_LSHIFT    
             1658  INPLACE_OR       
             1660  STORE_FAST               'rw_lock0'
           1662_0  COME_FROM          1538  '1538'

 L. 432      1662  LOAD_FAST                'sec_eng_key_sel'
             1664  LOAD_CONST               1
             1666  COMPARE_OP               ==
         1668_1670  POP_JUMP_IF_FALSE  1792  'to 1792'

 L. 433      1672  LOAD_FAST                'sec_eng_key'
             1674  LOAD_CONST               16
             1676  LOAD_CONST               32
             1678  BUILD_SLICE_2         2 
             1680  BINARY_SUBSCR    
             1682  LOAD_FAST                'efuse_data'
             1684  LOAD_GLOBAL              keyslot11
             1686  LOAD_GLOBAL              keyslot11_end
             1688  BUILD_SLICE_2         2 
             1690  STORE_SUBSCR     

 L. 434      1692  LOAD_FAST                'sec_eng_key'
             1694  LOAD_CONST               0
             1696  LOAD_CONST               16
             1698  BUILD_SLICE_2         2 
             1700  BINARY_SUBSCR    
             1702  LOAD_FAST                'efuse_data'
             1704  LOAD_GLOBAL              keyslot7
             1706  LOAD_GLOBAL              keyslot8
             1708  BUILD_SLICE_2         2 
             1710  STORE_SUBSCR     

 L. 435      1712  LOAD_FAST                'mask_4bytes'
             1714  LOAD_CONST               4
             1716  BINARY_MULTIPLY  
             1718  LOAD_FAST                'efuse_mask_data'
             1720  LOAD_GLOBAL              keyslot7
             1722  LOAD_GLOBAL              keyslot8
             1724  BUILD_SLICE_2         2 
             1726  STORE_SUBSCR     

 L. 436      1728  LOAD_FAST                'mask_4bytes'
             1730  LOAD_CONST               4
             1732  BINARY_MULTIPLY  
             1734  LOAD_FAST                'efuse_mask_data'
             1736  LOAD_GLOBAL              keyslot11
             1738  LOAD_GLOBAL              keyslot11_end
             1740  BUILD_SLICE_2         2 
             1742  STORE_SUBSCR     

 L. 437      1744  LOAD_FAST                'rw_lock1'
             1746  LOAD_CONST               1
             1748  LOAD_GLOBAL              wr_lock_key_slot_7
             1750  BINARY_LSHIFT    
             1752  INPLACE_OR       
             1754  STORE_FAST               'rw_lock1'

 L. 438      1756  LOAD_FAST                'rw_lock0'
             1758  LOAD_CONST               1
             1760  LOAD_GLOBAL              rd_lock_key_slot_11
             1762  BINARY_LSHIFT    
             1764  INPLACE_OR       
             1766  STORE_FAST               'rw_lock0'

 L. 439      1768  LOAD_FAST                'rw_lock1'
             1770  LOAD_CONST               1
             1772  LOAD_GLOBAL              wr_lock_key_slot_7
             1774  BINARY_LSHIFT    
             1776  INPLACE_OR       
             1778  STORE_FAST               'rw_lock1'

 L. 440      1780  LOAD_FAST                'rw_lock0'
             1782  LOAD_CONST               1
             1784  LOAD_GLOBAL              rd_lock_key_slot_11
             1786  BINARY_LSHIFT    
             1788  INPLACE_OR       
             1790  STORE_FAST               'rw_lock0'
           1792_0  COME_FROM          1668  '1668'

 L. 441      1792  LOAD_FAST                'sec_eng_key_sel'
             1794  LOAD_CONST               2
             1796  COMPARE_OP               ==
         1798_1800  POP_JUMP_IF_FALSE  1918  'to 1918'

 L. 442      1802  LOAD_FAST                'flash_key'
             1804  LOAD_CONST               None
             1806  COMPARE_OP               is-not
         1808_1810  POP_JUMP_IF_FALSE  1814  'to 1814'

 L. 444      1812  JUMP_FORWARD       1918  'to 1918'
           1814_0  COME_FROM          1808  '1808'

 L. 446      1814  LOAD_FAST                'sec_eng_key'
             1816  LOAD_CONST               16
             1818  LOAD_CONST               32
             1820  BUILD_SLICE_2         2 
             1822  BINARY_SUBSCR    
             1824  LOAD_FAST                'efuse_data'
             1826  LOAD_GLOBAL              keyslot4
             1828  LOAD_GLOBAL              keyslot5
             1830  BUILD_SLICE_2         2 
             1832  STORE_SUBSCR     

 L. 447      1834  LOAD_FAST                'sec_eng_key'
             1836  LOAD_CONST               0
             1838  LOAD_CONST               16
             1840  BUILD_SLICE_2         2 
             1842  BINARY_SUBSCR    
             1844  LOAD_FAST                'efuse_data'
             1846  LOAD_GLOBAL              keyslot5
             1848  LOAD_GLOBAL              keyslot6
             1850  BUILD_SLICE_2         2 
             1852  STORE_SUBSCR     

 L. 448      1854  LOAD_FAST                'mask_4bytes'
             1856  LOAD_CONST               8
             1858  BINARY_MULTIPLY  
             1860  LOAD_FAST                'efuse_mask_data'
             1862  LOAD_GLOBAL              keyslot4
             1864  LOAD_GLOBAL              keyslot6
             1866  BUILD_SLICE_2         2 
             1868  STORE_SUBSCR     

 L. 449      1870  LOAD_FAST                'rw_lock1'
             1872  LOAD_CONST               1
             1874  LOAD_GLOBAL              wr_lock_key_slot_4
             1876  BINARY_LSHIFT    
             1878  INPLACE_OR       
             1880  STORE_FAST               'rw_lock1'

 L. 450      1882  LOAD_FAST                'rw_lock1'
             1884  LOAD_CONST               1
             1886  LOAD_GLOBAL              wr_lock_key_slot_5
             1888  BINARY_LSHIFT    
             1890  INPLACE_OR       
             1892  STORE_FAST               'rw_lock1'

 L. 451      1894  LOAD_FAST                'rw_lock1'
             1896  LOAD_CONST               1
             1898  LOAD_GLOBAL              rd_lock_key_slot_4
             1900  BINARY_LSHIFT    
             1902  INPLACE_OR       
             1904  STORE_FAST               'rw_lock1'

 L. 452      1906  LOAD_FAST                'rw_lock1'
             1908  LOAD_CONST               1
             1910  LOAD_GLOBAL              rd_lock_key_slot_5
             1912  BINARY_LSHIFT    
             1914  INPLACE_OR       
             1916  STORE_FAST               'rw_lock1'
           1918_0  COME_FROM          1812  '1812'
           1918_1  COME_FROM          1798  '1798'

 L. 453      1918  LOAD_FAST                'sec_eng_key_sel'
             1920  LOAD_CONST               3
             1922  COMPARE_OP               ==
         1924_1926  POP_JUMP_IF_FALSE  2016  'to 2016'

 L. 454      1928  LOAD_FAST                'flash_key'
             1930  LOAD_CONST               None
             1932  COMPARE_OP               is-not
         1934_1936  POP_JUMP_IF_FALSE  1940  'to 1940'

 L. 456      1938  JUMP_FORWARD       2016  'to 2016'
           1940_0  COME_FROM          1934  '1934'

 L. 458      1940  LOAD_FAST                'sec_eng_key'
             1942  LOAD_FAST                'efuse_data'
             1944  LOAD_GLOBAL              keyslot4
             1946  LOAD_GLOBAL              keyslot6
             1948  BUILD_SLICE_2         2 
             1950  STORE_SUBSCR     

 L. 459      1952  LOAD_FAST                'mask_4bytes'
             1954  LOAD_CONST               8
             1956  BINARY_MULTIPLY  
             1958  LOAD_FAST                'efuse_mask_data'
             1960  LOAD_GLOBAL              keyslot4
             1962  LOAD_GLOBAL              keyslot6
             1964  BUILD_SLICE_2         2 
             1966  STORE_SUBSCR     

 L. 460      1968  LOAD_FAST                'rw_lock1'
             1970  LOAD_CONST               1
             1972  LOAD_GLOBAL              wr_lock_key_slot_4
             1974  BINARY_LSHIFT    
             1976  INPLACE_OR       
             1978  STORE_FAST               'rw_lock1'

 L. 461      1980  LOAD_FAST                'rw_lock1'
             1982  LOAD_CONST               1
             1984  LOAD_GLOBAL              wr_lock_key_slot_5
             1986  BINARY_LSHIFT    
             1988  INPLACE_OR       
             1990  STORE_FAST               'rw_lock1'

 L. 462      1992  LOAD_FAST                'rw_lock1'
             1994  LOAD_CONST               1
             1996  LOAD_GLOBAL              rd_lock_key_slot_4
             1998  BINARY_LSHIFT    
             2000  INPLACE_OR       
             2002  STORE_FAST               'rw_lock1'

 L. 463      2004  LOAD_FAST                'rw_lock1'
             2006  LOAD_CONST               1
             2008  LOAD_GLOBAL              rd_lock_key_slot_5
             2010  BINARY_LSHIFT    
             2012  INPLACE_OR       
             2014  STORE_FAST               'rw_lock1'
           2016_0  COME_FROM          1938  '1938'
           2016_1  COME_FROM          1924  '1924'
           2016_2  COME_FROM          1528  '1528'
           2016_3  COME_FROM           666  '666'

 L. 465      2016  LOAD_GLOBAL              bytearray_data_merge
             2018  LOAD_FAST                'efuse_data'
             2020  LOAD_CONST               124
             2022  LOAD_CONST               128
             2024  BUILD_SLICE_2         2 
             2026  BINARY_SUBSCR    

 L. 466      2028  LOAD_GLOBAL              bflb_utils
             2030  LOAD_METHOD              int_to_4bytearray_l
             2032  LOAD_FAST                'rw_lock0'
             2034  CALL_METHOD_1         1  '1 positional argument'
             2036  LOAD_CONST               4
             2038  CALL_FUNCTION_3       3  '3 positional arguments'
             2040  LOAD_FAST                'efuse_data'
             2042  LOAD_CONST               124
             2044  LOAD_CONST               128
             2046  BUILD_SLICE_2         2 
             2048  STORE_SUBSCR     

 L. 467      2050  LOAD_GLOBAL              bytearray_data_merge
             2052  LOAD_FAST                'efuse_mask_data'
             2054  LOAD_CONST               124
             2056  LOAD_CONST               128
             2058  BUILD_SLICE_2         2 
             2060  BINARY_SUBSCR    

 L. 468      2062  LOAD_GLOBAL              bflb_utils
             2064  LOAD_METHOD              int_to_4bytearray_l
             2066  LOAD_FAST                'rw_lock0'
             2068  CALL_METHOD_1         1  '1 positional argument'
             2070  LOAD_CONST               4
             2072  CALL_FUNCTION_3       3  '3 positional arguments'
             2074  LOAD_FAST                'efuse_mask_data'
             2076  LOAD_CONST               124
             2078  LOAD_CONST               128
             2080  BUILD_SLICE_2         2 
             2082  STORE_SUBSCR     

 L. 469      2084  LOAD_GLOBAL              bytearray_data_merge
             2086  LOAD_FAST                'efuse_data'
             2088  LOAD_CONST               252
             2090  LOAD_CONST               256
             2092  BUILD_SLICE_2         2 
             2094  BINARY_SUBSCR    

 L. 470      2096  LOAD_GLOBAL              bflb_utils
             2098  LOAD_METHOD              int_to_4bytearray_l
             2100  LOAD_FAST                'rw_lock1'
             2102  CALL_METHOD_1         1  '1 positional argument'
             2104  LOAD_CONST               4
             2106  CALL_FUNCTION_3       3  '3 positional arguments'
             2108  LOAD_FAST                'efuse_data'
             2110  LOAD_CONST               252
             2112  LOAD_CONST               256
             2114  BUILD_SLICE_2         2 
             2116  STORE_SUBSCR     

 L. 471      2118  LOAD_GLOBAL              bytearray_data_merge
             2120  LOAD_FAST                'efuse_mask_data'
             2122  LOAD_CONST               252
             2124  LOAD_CONST               256
             2126  BUILD_SLICE_2         2 
             2128  BINARY_SUBSCR    

 L. 472      2130  LOAD_GLOBAL              bflb_utils
             2132  LOAD_METHOD              int_to_4bytearray_l
             2134  LOAD_FAST                'rw_lock1'
             2136  CALL_METHOD_1         1  '1 positional argument'
             2138  LOAD_CONST               4
             2140  CALL_FUNCTION_3       3  '3 positional arguments'
             2142  LOAD_FAST                'efuse_mask_data'
             2144  LOAD_CONST               252
             2146  LOAD_CONST               256
             2148  BUILD_SLICE_2         2 
             2150  STORE_SUBSCR     

 L. 474      2152  LOAD_FAST                'security'
             2154  LOAD_CONST               True
             2156  COMPARE_OP               is
         2158_2160  POP_JUMP_IF_FALSE  2210  'to 2210'

 L. 475      2162  LOAD_GLOBAL              bflb_utils
             2164  LOAD_METHOD              printf
             2166  LOAD_STR                 'Encrypt efuse data'
             2168  CALL_METHOD_1         1  '1 positional argument'
             2170  POP_TOP          

 L. 476      2172  LOAD_GLOBAL              bflb_utils
             2174  LOAD_METHOD              get_security_key
             2176  CALL_METHOD_0         0  '0 positional arguments'
             2178  UNPACK_SEQUENCE_2     2 
             2180  STORE_FAST               'security_key'
             2182  STORE_FAST               'security_iv'

 L. 477      2184  LOAD_GLOBAL              img_create_encrypt_data
             2186  LOAD_FAST                'efuse_data'
             2188  LOAD_FAST                'security_key'
             2190  LOAD_FAST                'security_iv'
             2192  LOAD_CONST               0
             2194  CALL_FUNCTION_4       4  '4 positional arguments'
             2196  STORE_FAST               'efuse_data'

 L. 478      2198  LOAD_GLOBAL              bytearray
             2200  LOAD_CONST               4096
             2202  CALL_FUNCTION_1       1  '1 positional argument'
             2204  LOAD_FAST                'efuse_data'
             2206  BINARY_ADD       
             2208  STORE_FAST               'efuse_data'
           2210_0  COME_FROM          2158  '2158'

 L. 479      2210  LOAD_GLOBAL              open
             2212  LOAD_FAST                'cfg'
             2214  LOAD_METHOD              get
             2216  LOAD_STR                 'Img_Group1_Cfg'
             2218  LOAD_STR                 'efuse_file'
             2220  CALL_METHOD_2         2  '2 positional arguments'
             2222  LOAD_STR                 'wb+'
             2224  CALL_FUNCTION_2       2  '2 positional arguments'
             2226  STORE_FAST               'fp'

 L. 480      2228  LOAD_FAST                'fp'
             2230  LOAD_METHOD              write
             2232  LOAD_FAST                'efuse_data'
             2234  CALL_METHOD_1         1  '1 positional argument'
             2236  POP_TOP          

 L. 481      2238  LOAD_FAST                'fp'
             2240  LOAD_METHOD              close
             2242  CALL_METHOD_0         0  '0 positional arguments'
             2244  POP_TOP          

 L. 482      2246  LOAD_GLOBAL              open
             2248  LOAD_FAST                'cfg'
             2250  LOAD_METHOD              get
             2252  LOAD_STR                 'Img_Group1_Cfg'
             2254  LOAD_STR                 'efuse_mask_file'
             2256  CALL_METHOD_2         2  '2 positional arguments'
             2258  LOAD_STR                 'wb+'
             2260  CALL_FUNCTION_2       2  '2 positional arguments'
             2262  STORE_FAST               'fp'

 L. 483      2264  LOAD_FAST                'fp'
             2266  LOAD_METHOD              write
             2268  LOAD_FAST                'efuse_mask_data'
             2270  CALL_METHOD_1         1  '1 positional argument'
             2272  POP_TOP          

 L. 484      2274  LOAD_FAST                'fp'
             2276  LOAD_METHOD              close
             2278  CALL_METHOD_0         0  '0 positional arguments'
             2280  POP_TOP          

Parse error at or near `CALL_METHOD_0' instruction at offset 2278


def img_create_get_sign_encrypt_info(bootheader_data):
    sign = bootheader_data[bootcfg_start] & 3
    encrypt = bootheader_data[bootcfg_start] >> 2 & 3
    key_sel = bootheader_data[bootcfg_start] >> 4 & 3
    xts_mode = bootheader_data[bootcfg_start] >> 6 & 1
    return (sign, encrypt, key_sel, xts_mode)


def img_create_get_img_start_addr(bootheader_data):
    bootentry = []
    bootentry.append(bflb_utils.bytearray_to_int(bflb_utils.bytearray_reverse(bootheader_data[bootcpucfg_start + bootcpucfg_length * bootcpucfg_m0_index_number + 8:bootcpucfg_start + bootcpucfg_length * bootcpucfg_m0_index_number + 8 + 4])))
    bootentry.append(bflb_utils.bytearray_to_int(bflb_utils.bytearray_reverse(bootheader_data[bootcpucfg_start + bootcpucfg_length * bootcpucfg_m1_index_number + 8:bootcpucfg_start + bootcpucfg_length * bootcpucfg_m1_index_number + 8 + 4])))
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
        hd_crcarray = bflb_utils.get_crc32_bytearray(bootheader_data[0:header_len - 4])
        bootheader_data[header_len - 4:header_len] = hd_crcarray
        bflb_utils.printf('Header crc: ', binascii.hexlify(hd_crcarray))
    return bootheader_data


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
        hd_crcarray = bflb_utils.get_crc32_bytearray(bootheader_data[0:header_len - 4])
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
    if group_type == 'group0':
        img_update_efuse_fun = img_update_efuse_group0
        cfg_section = 'Img_Group0_Cfg'
    else:
        if group_type == 'group1':
            img_update_efuse_fun = img_update_efuse_group1
            cfg_section = 'Img_Group1_Cfg'
        else:
            bflb_utils.printf('group type wrong')
            return ('FAIL', data_tohash)
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
                data_tohash = data_tohash + aesiv_data
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
        flashCfgAddr = len(bootheader_data + pk_data + pk_data + signature + signature + aesiv_data)
        flashCfgListLen = 0
        flashCfgList = bytearray(0)
        flashCfgTable = bytearray(0)
        if flash_img == 1:
            if bootheader_data[25:26] == b'\xff':
                flashCfgList, flashCfgTable, flashCfgListLen = create_flashcfg_table(flashCfgAddr)
        bootheader_data = img_create_update_bootheader(bootheader_data, hash, seg_cnt, flashCfgAddr, flashCfgListLen)
        if flash_img == 1:
            bflb_utils.printf('Write flash img')
            bootinfo_file_name = cfg.get(cfg_section, 'bootinfo_file')
            fp = open(bootinfo_file_name, 'wb+')
            bootinfo = bootheader_data + pk_data + pk_data + signature + signature + aesiv_data + flashCfgList + flashCfgTable
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
            img_data = bootheader_data + pk_data + pk_data + signature + signature + aesiv_data + fw_data
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
        if group_type == 'group0':
            ret0, data_tohash0 = img_creat_process('group0', flash_img, cfg, security)
        else:
            if group_type == 'group1':
                ret1, data_tohash1 = img_creat_process('group1', flash_img, cfg, security)
            else:
                if group_type == 'all':
                    ret0, data_tohash0 = img_creat_process('group0', flash_img, cfg, False)
                    ret1, data_tohash1 = img_creat_process('group1', flash_img, cfg, security)
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
    if cpu_type == 'Group1':
        img_creat_process('group1', 1, cfg, security)
    else:
        img_creat_process('group0', 1, cfg, security)


if __name__ == '__main__':
    data_bytearray = codecs.decode('42464E500100000046434647040101036699FF039F00B7E904EF0001C72052D8060232000B010B013B01BB006B01EB02EB02025000010001010002010101AB01053500000131000038FF20FF77030240770302F02C01B004B0040500FFFF030036C3DD9E5043464704040001010105000101050000010101A612AC86000144650020000000000000503100007A6345494BCABEC7307FD8F8396729EB67DDC8C63B7AD69B797B08564E982A8701000000000000000000000000000000000000D80000000000010000000000000000000000200100000001D80000000000010000000000000000000000200200000002580000000000010000000000000000000000200300000003580000000000010000D0C57503C09E750300200400000004580000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000935F92BB', 'hex')
    key_bytearray = codecs.decode('fffefdfcfbfaf9f8f7f6f5f4f3f2f1f0000102030405060708090a0b0c0d0e0f', 'hex')
    need_reverse_iv_bytearray = codecs.decode('01000000000000000000000000000000', 'hex')
    iv_bytearray = codecs.decode(reverse_iv(need_reverse_iv_bytearray), 'hex')
    img_create_encrypt_data_xts(data_bytearray, key_bytearray, iv_bytearray, 0)