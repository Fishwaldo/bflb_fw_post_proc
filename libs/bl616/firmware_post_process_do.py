# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
# [GCC 9.4.0]
# Embedded file name: libs/bl616/firmware_post_process_do.py
import os, sys, hashlib, binascii, codecs, ecdsa
from CryptoPlus.Cipher import AES as AES_XTS
from libs import bflb_utils
from libs.bflb_utils import img_create_sha256_data, img_create_encrypt_data
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


def img_update_efuse_data--- This code section failed: ---

 L.  82         0  LOAD_GLOBAL              bytearray
                2  LOAD_CONST               512
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  STORE_FAST               'efuse_data'

 L.  83         8  LOAD_GLOBAL              bytearray
               10  LOAD_CONST               512
               12  CALL_FUNCTION_1       1  '1 positional argument'
               14  STORE_FAST               'efuse_mask_data'

 L.  85        16  LOAD_GLOBAL              bytearray
               18  LOAD_METHOD              fromhex
               20  LOAD_STR                 'FFFFFFFF'
               22  CALL_METHOD_1         1  '1 positional argument'
               24  STORE_FAST               'mask_4bytes'

 L.  88        26  LOAD_FAST                'flash_encryp_type'
               28  LOAD_CONST               3
               30  COMPARE_OP               >=
               32  POP_JUMP_IF_FALSE    52  'to 52'

 L.  89        34  LOAD_FAST                'efuse_data'
               36  LOAD_CONST               0
               38  DUP_TOP_TWO      
               40  BINARY_SUBSCR    
               42  LOAD_CONST               3
               44  INPLACE_OR       
               46  ROT_THREE        
               48  STORE_SUBSCR     
               50  JUMP_FORWARD         68  'to 68'
             52_0  COME_FROM            32  '32'

 L.  91        52  LOAD_FAST                'efuse_data'
               54  LOAD_CONST               0
               56  DUP_TOP_TWO      
               58  BINARY_SUBSCR    
               60  LOAD_FAST                'flash_encryp_type'
               62  INPLACE_OR       
               64  ROT_THREE        
               66  STORE_SUBSCR     
             68_0  COME_FROM            50  '50'

 L.  93        68  LOAD_FAST                'sign'
               70  LOAD_CONST               0
               72  COMPARE_OP               >
               74  POP_JUMP_IF_FALSE   112  'to 112'

 L.  94        76  LOAD_FAST                'efuse_data'
               78  LOAD_CONST               92
               80  DUP_TOP_TWO      
               82  BINARY_SUBSCR    
               84  LOAD_FAST                'sign'
               86  LOAD_CONST               7
               88  BINARY_LSHIFT    
               90  INPLACE_OR       
               92  ROT_THREE        
               94  STORE_SUBSCR     

 L.  95        96  LOAD_FAST                'efuse_mask_data'
               98  LOAD_CONST               92
              100  DUP_TOP_TWO      
              102  BINARY_SUBSCR    
              104  LOAD_CONST               255
              106  INPLACE_OR       
              108  ROT_THREE        
              110  STORE_SUBSCR     
            112_0  COME_FROM            74  '74'

 L.  97       112  LOAD_FAST                'flash_encryp_type'
              114  LOAD_CONST               0
              116  COMPARE_OP               >
              118  POP_JUMP_IF_FALSE   136  'to 136'

 L.  98       120  LOAD_FAST                'efuse_data'
              122  LOAD_CONST               0
              124  DUP_TOP_TWO      
              126  BINARY_SUBSCR    
              128  LOAD_CONST               48
              130  INPLACE_OR       
              132  ROT_THREE        
              134  STORE_SUBSCR     
            136_0  COME_FROM           118  '118'

 L.  99       136  LOAD_FAST                'efuse_mask_data'
              138  LOAD_CONST               0
              140  DUP_TOP_TWO      
              142  BINARY_SUBSCR    
              144  LOAD_CONST               255
              146  INPLACE_OR       
              148  ROT_THREE        
              150  STORE_SUBSCR     

 L. 100       152  LOAD_CONST               0
              154  STORE_FAST               'rw_lock0'

 L. 101       156  LOAD_CONST               0
              158  STORE_FAST               'rw_lock1'

 L. 102       160  LOAD_FAST                'pk_hash'
              162  LOAD_CONST               None
              164  COMPARE_OP               is-not
              166  POP_JUMP_IF_FALSE   220  'to 220'

 L. 103       168  LOAD_FAST                'pk_hash'
              170  LOAD_FAST                'efuse_data'
              172  LOAD_GLOBAL              keyslot0
              174  LOAD_GLOBAL              keyslot2
              176  BUILD_SLICE_2         2 
              178  STORE_SUBSCR     

 L. 104       180  LOAD_FAST                'mask_4bytes'
              182  LOAD_CONST               8
              184  BINARY_MULTIPLY  
              186  LOAD_FAST                'efuse_mask_data'
              188  LOAD_GLOBAL              keyslot0
              190  LOAD_GLOBAL              keyslot2
              192  BUILD_SLICE_2         2 
              194  STORE_SUBSCR     

 L. 105       196  LOAD_FAST                'rw_lock0'
              198  LOAD_CONST               1
              200  LOAD_GLOBAL              wr_lock_key_slot_0
              202  BINARY_LSHIFT    
              204  INPLACE_OR       
              206  STORE_FAST               'rw_lock0'

 L. 106       208  LOAD_FAST                'rw_lock0'
              210  LOAD_CONST               1
              212  LOAD_GLOBAL              wr_lock_key_slot_1
              214  BINARY_LSHIFT    
              216  INPLACE_OR       
              218  STORE_FAST               'rw_lock0'
            220_0  COME_FROM           166  '166'

 L. 107       220  LOAD_FAST                'flash_key'
              222  LOAD_CONST               None
              224  COMPARE_OP               is-not
          226_228  POP_JUMP_IF_FALSE   512  'to 512'

 L. 108       230  LOAD_FAST                'flash_encryp_type'
              232  LOAD_CONST               1
              234  COMPARE_OP               ==
          236_238  POP_JUMP_IF_FALSE   278  'to 278'

 L. 110       240  LOAD_FAST                'flash_key'
              242  LOAD_CONST               0
              244  LOAD_CONST               16
              246  BUILD_SLICE_2         2 
              248  BINARY_SUBSCR    
              250  LOAD_FAST                'efuse_data'
              252  LOAD_GLOBAL              keyslot2
              254  LOAD_GLOBAL              keyslot3
              256  BUILD_SLICE_2         2 
              258  STORE_SUBSCR     

 L. 111       260  LOAD_FAST                'mask_4bytes'
              262  LOAD_CONST               4
              264  BINARY_MULTIPLY  
              266  LOAD_FAST                'efuse_mask_data'
              268  LOAD_GLOBAL              keyslot2
              270  LOAD_GLOBAL              keyslot3
              272  BUILD_SLICE_2         2 
              274  STORE_SUBSCR     
              276  JUMP_FORWARD        488  'to 488'
            278_0  COME_FROM           236  '236'

 L. 112       278  LOAD_FAST                'flash_encryp_type'
              280  LOAD_CONST               2
              282  COMPARE_OP               ==
          284_286  POP_JUMP_IF_FALSE   342  'to 342'

 L. 114       288  LOAD_FAST                'flash_key'
              290  LOAD_FAST                'efuse_data'
              292  LOAD_GLOBAL              keyslot2
              294  LOAD_GLOBAL              keyslot3_end
              296  BUILD_SLICE_2         2 
              298  STORE_SUBSCR     

 L. 115       300  LOAD_FAST                'mask_4bytes'
              302  LOAD_CONST               8
              304  BINARY_MULTIPLY  
              306  LOAD_FAST                'efuse_mask_data'
              308  LOAD_GLOBAL              keyslot2
              310  LOAD_GLOBAL              keyslot3_end
              312  BUILD_SLICE_2         2 
              314  STORE_SUBSCR     

 L. 116       316  LOAD_FAST                'rw_lock0'
              318  LOAD_CONST               1
              320  LOAD_GLOBAL              wr_lock_key_slot_3
              322  BINARY_LSHIFT    
              324  INPLACE_OR       
              326  STORE_FAST               'rw_lock0'

 L. 117       328  LOAD_FAST                'rw_lock0'
              330  LOAD_CONST               1
              332  LOAD_GLOBAL              rd_lock_key_slot_3
              334  BINARY_LSHIFT    
              336  INPLACE_OR       
              338  STORE_FAST               'rw_lock0'
              340  JUMP_FORWARD        488  'to 488'
            342_0  COME_FROM           284  '284'

 L. 118       342  LOAD_FAST                'flash_encryp_type'
              344  LOAD_CONST               3
              346  COMPARE_OP               ==
          348_350  POP_JUMP_IF_FALSE   406  'to 406'

 L. 120       352  LOAD_FAST                'flash_key'
              354  LOAD_FAST                'efuse_data'
              356  LOAD_GLOBAL              keyslot2
              358  LOAD_GLOBAL              keyslot3_end
              360  BUILD_SLICE_2         2 
              362  STORE_SUBSCR     

 L. 121       364  LOAD_FAST                'mask_4bytes'
              366  LOAD_CONST               8
              368  BINARY_MULTIPLY  
              370  LOAD_FAST                'efuse_mask_data'
              372  LOAD_GLOBAL              keyslot2
              374  LOAD_GLOBAL              keyslot3_end
              376  BUILD_SLICE_2         2 
              378  STORE_SUBSCR     

 L. 122       380  LOAD_FAST                'rw_lock0'
              382  LOAD_CONST               1
              384  LOAD_GLOBAL              wr_lock_key_slot_3
              386  BINARY_LSHIFT    
              388  INPLACE_OR       
              390  STORE_FAST               'rw_lock0'

 L. 123       392  LOAD_FAST                'rw_lock0'
              394  LOAD_CONST               1
              396  LOAD_GLOBAL              rd_lock_key_slot_3
              398  BINARY_LSHIFT    
              400  INPLACE_OR       
              402  STORE_FAST               'rw_lock0'
              404  JUMP_FORWARD        488  'to 488'
            406_0  COME_FROM           348  '348'

 L. 124       406  LOAD_FAST                'flash_encryp_type'
              408  LOAD_CONST               4
              410  COMPARE_OP               ==
          412_414  POP_JUMP_IF_TRUE    436  'to 436'

 L. 125       416  LOAD_FAST                'flash_encryp_type'
              418  LOAD_CONST               5
              420  COMPARE_OP               ==
          422_424  POP_JUMP_IF_TRUE    436  'to 436'

 L. 126       426  LOAD_FAST                'flash_encryp_type'
              428  LOAD_CONST               6
              430  COMPARE_OP               ==
          432_434  POP_JUMP_IF_FALSE   488  'to 488'
            436_0  COME_FROM           422  '422'
            436_1  COME_FROM           412  '412'

 L. 128       436  LOAD_FAST                'flash_key'
              438  LOAD_FAST                'efuse_data'
              440  LOAD_GLOBAL              keyslot2
              442  LOAD_GLOBAL              keyslot3_end
              444  BUILD_SLICE_2         2 
              446  STORE_SUBSCR     

 L. 129       448  LOAD_FAST                'mask_4bytes'
              450  LOAD_CONST               8
              452  BINARY_MULTIPLY  
              454  LOAD_FAST                'efuse_mask_data'
              456  LOAD_GLOBAL              keyslot2
              458  LOAD_GLOBAL              keyslot3_end
              460  BUILD_SLICE_2         2 
              462  STORE_SUBSCR     

 L. 130       464  LOAD_FAST                'rw_lock0'
              466  LOAD_CONST               1
              468  LOAD_GLOBAL              wr_lock_key_slot_3
              470  BINARY_LSHIFT    
              472  INPLACE_OR       
              474  STORE_FAST               'rw_lock0'

 L. 131       476  LOAD_FAST                'rw_lock0'
              478  LOAD_CONST               1
              480  LOAD_GLOBAL              rd_lock_key_slot_3
              482  BINARY_LSHIFT    
              484  INPLACE_OR       
              486  STORE_FAST               'rw_lock0'
            488_0  COME_FROM           432  '432'
            488_1  COME_FROM           404  '404'
            488_2  COME_FROM           340  '340'
            488_3  COME_FROM           276  '276'

 L. 133       488  LOAD_FAST                'rw_lock0'
              490  LOAD_CONST               1
              492  LOAD_GLOBAL              wr_lock_key_slot_2
              494  BINARY_LSHIFT    
              496  INPLACE_OR       
              498  STORE_FAST               'rw_lock0'

 L. 134       500  LOAD_FAST                'rw_lock0'
              502  LOAD_CONST               1
              504  LOAD_GLOBAL              rd_lock_key_slot_2
              506  BINARY_LSHIFT    
              508  INPLACE_OR       
              510  STORE_FAST               'rw_lock0'
            512_0  COME_FROM           226  '226'

 L. 136       512  LOAD_FAST                'sec_eng_key'
              514  LOAD_CONST               None
              516  COMPARE_OP               is-not
          518_520  POP_JUMP_IF_FALSE  1852  'to 1852'

 L. 137       522  LOAD_FAST                'flash_encryp_type'
              524  LOAD_CONST               0
              526  COMPARE_OP               ==
          528_530  POP_JUMP_IF_FALSE  1004  'to 1004'

 L. 138       532  LOAD_FAST                'sec_eng_key_sel'
              534  LOAD_CONST               0
              536  COMPARE_OP               ==
          538_540  POP_JUMP_IF_FALSE   646  'to 646'

 L. 139       542  LOAD_FAST                'sec_eng_key'
              544  LOAD_CONST               16
              546  LOAD_CONST               32
              548  BUILD_SLICE_2         2 
              550  BINARY_SUBSCR    
              552  LOAD_FAST                'efuse_data'
              554  LOAD_GLOBAL              keyslot2
              556  LOAD_GLOBAL              keyslot3
              558  BUILD_SLICE_2         2 
              560  STORE_SUBSCR     

 L. 140       562  LOAD_FAST                'sec_eng_key'
              564  LOAD_CONST               0
              566  LOAD_CONST               16
              568  BUILD_SLICE_2         2 
              570  BINARY_SUBSCR    
              572  LOAD_FAST                'efuse_data'
              574  LOAD_GLOBAL              keyslot3
              576  LOAD_GLOBAL              keyslot3_end
              578  BUILD_SLICE_2         2 
              580  STORE_SUBSCR     

 L. 141       582  LOAD_FAST                'mask_4bytes'
              584  LOAD_CONST               8
              586  BINARY_MULTIPLY  
              588  LOAD_FAST                'efuse_mask_data'
              590  LOAD_GLOBAL              keyslot2
              592  LOAD_GLOBAL              keyslot3_end
              594  BUILD_SLICE_2         2 
              596  STORE_SUBSCR     

 L. 142       598  LOAD_FAST                'rw_lock0'
              600  LOAD_CONST               1
              602  LOAD_GLOBAL              wr_lock_key_slot_2
              604  BINARY_LSHIFT    
              606  INPLACE_OR       
              608  STORE_FAST               'rw_lock0'

 L. 143       610  LOAD_FAST                'rw_lock0'
              612  LOAD_CONST               1
              614  LOAD_GLOBAL              wr_lock_key_slot_3
              616  BINARY_LSHIFT    
              618  INPLACE_OR       
              620  STORE_FAST               'rw_lock0'

 L. 144       622  LOAD_FAST                'rw_lock0'
              624  LOAD_CONST               1
              626  LOAD_GLOBAL              rd_lock_key_slot_2
              628  BINARY_LSHIFT    
              630  INPLACE_OR       
              632  STORE_FAST               'rw_lock0'

 L. 145       634  LOAD_FAST                'rw_lock0'
              636  LOAD_CONST               1
              638  LOAD_GLOBAL              rd_lock_key_slot_3
              640  BINARY_LSHIFT    
              642  INPLACE_OR       
              644  STORE_FAST               'rw_lock0'
            646_0  COME_FROM           538  '538'

 L. 146       646  LOAD_FAST                'sec_eng_key_sel'
              648  LOAD_CONST               1
              650  COMPARE_OP               ==
          652_654  POP_JUMP_IF_FALSE   776  'to 776'

 L. 147       656  LOAD_FAST                'sec_eng_key'
              658  LOAD_CONST               16
              660  LOAD_CONST               32
              662  BUILD_SLICE_2         2 
              664  BINARY_SUBSCR    
              666  LOAD_FAST                'efuse_data'
              668  LOAD_GLOBAL              keyslot3
              670  LOAD_GLOBAL              keyslot3_end
              672  BUILD_SLICE_2         2 
              674  STORE_SUBSCR     

 L. 148       676  LOAD_FAST                'sec_eng_key'
              678  LOAD_CONST               0
              680  LOAD_CONST               16
              682  BUILD_SLICE_2         2 
              684  BINARY_SUBSCR    
              686  LOAD_FAST                'efuse_data'
              688  LOAD_GLOBAL              keyslot4
              690  LOAD_GLOBAL              keyslot5
              692  BUILD_SLICE_2         2 
              694  STORE_SUBSCR     

 L. 149       696  LOAD_FAST                'mask_4bytes'
              698  LOAD_CONST               4
              700  BINARY_MULTIPLY  
              702  LOAD_FAST                'efuse_mask_data'
              704  LOAD_GLOBAL              keyslot3
              706  LOAD_GLOBAL              keyslot3_end
              708  BUILD_SLICE_2         2 
              710  STORE_SUBSCR     

 L. 150       712  LOAD_FAST                'mask_4bytes'
              714  LOAD_CONST               4
              716  BINARY_MULTIPLY  
              718  LOAD_FAST                'efuse_mask_data'
              720  LOAD_GLOBAL              keyslot4
              722  LOAD_GLOBAL              keyslot5
              724  BUILD_SLICE_2         2 
              726  STORE_SUBSCR     

 L. 151       728  LOAD_FAST                'rw_lock0'
              730  LOAD_CONST               1
              732  LOAD_GLOBAL              wr_lock_key_slot_3
              734  BINARY_LSHIFT    
              736  INPLACE_OR       
              738  STORE_FAST               'rw_lock0'

 L. 152       740  LOAD_FAST                'rw_lock1'
              742  LOAD_CONST               1
              744  LOAD_GLOBAL              wr_lock_key_slot_4
              746  BINARY_LSHIFT    
              748  INPLACE_OR       
              750  STORE_FAST               'rw_lock1'

 L. 153       752  LOAD_FAST                'rw_lock0'
              754  LOAD_CONST               1
              756  LOAD_GLOBAL              rd_lock_key_slot_3
              758  BINARY_LSHIFT    
              760  INPLACE_OR       
              762  STORE_FAST               'rw_lock0'

 L. 154       764  LOAD_FAST                'rw_lock1'
              766  LOAD_CONST               1
              768  LOAD_GLOBAL              rd_lock_key_slot_4
              770  BINARY_LSHIFT    
              772  INPLACE_OR       
              774  STORE_FAST               'rw_lock1'
            776_0  COME_FROM           652  '652'

 L. 155       776  LOAD_FAST                'sec_eng_key_sel'
              778  LOAD_CONST               2
              780  COMPARE_OP               ==
          782_784  POP_JUMP_IF_FALSE   890  'to 890'

 L. 156       786  LOAD_FAST                'sec_eng_key'
              788  LOAD_CONST               16
              790  LOAD_CONST               32
              792  BUILD_SLICE_2         2 
              794  BINARY_SUBSCR    
              796  LOAD_FAST                'efuse_data'
              798  LOAD_GLOBAL              keyslot4
              800  LOAD_GLOBAL              keyslot5
              802  BUILD_SLICE_2         2 
              804  STORE_SUBSCR     

 L. 157       806  LOAD_FAST                'sec_eng_key'
              808  LOAD_CONST               0
              810  LOAD_CONST               16
              812  BUILD_SLICE_2         2 
              814  BINARY_SUBSCR    
              816  LOAD_FAST                'efuse_data'
              818  LOAD_GLOBAL              keyslot2
              820  LOAD_GLOBAL              keyslot3
              822  BUILD_SLICE_2         2 
              824  STORE_SUBSCR     

 L. 158       826  LOAD_FAST                'mask_4bytes'
              828  LOAD_CONST               8
              830  BINARY_MULTIPLY  
              832  LOAD_FAST                'efuse_mask_data'
              834  LOAD_GLOBAL              keyslot3
              836  LOAD_GLOBAL              keyslot5
              838  BUILD_SLICE_2         2 
              840  STORE_SUBSCR     

 L. 159       842  LOAD_FAST                'rw_lock1'
              844  LOAD_CONST               1
              846  LOAD_GLOBAL              wr_lock_key_slot_4
              848  BINARY_LSHIFT    
              850  INPLACE_OR       
              852  STORE_FAST               'rw_lock1'

 L. 160       854  LOAD_FAST                'rw_lock0'
              856  LOAD_CONST               1
              858  LOAD_GLOBAL              wr_lock_key_slot_2
              860  BINARY_LSHIFT    
              862  INPLACE_OR       
              864  STORE_FAST               'rw_lock0'

 L. 161       866  LOAD_FAST                'rw_lock1'
              868  LOAD_CONST               1
              870  LOAD_GLOBAL              rd_lock_key_slot_4
              872  BINARY_LSHIFT    
              874  INPLACE_OR       
              876  STORE_FAST               'rw_lock1'

 L. 162       878  LOAD_FAST                'rw_lock0'
              880  LOAD_CONST               1
              882  LOAD_GLOBAL              rd_lock_key_slot_2
              884  BINARY_LSHIFT    
              886  INPLACE_OR       
              888  STORE_FAST               'rw_lock0'
            890_0  COME_FROM           782  '782'

 L. 163       890  LOAD_FAST                'sec_eng_key_sel'
              892  LOAD_CONST               3
              894  COMPARE_OP               ==
          896_898  POP_JUMP_IF_FALSE  1004  'to 1004'

 L. 164       900  LOAD_FAST                'sec_eng_key'
              902  LOAD_CONST               16
              904  LOAD_CONST               32
              906  BUILD_SLICE_2         2 
              908  BINARY_SUBSCR    
              910  LOAD_FAST                'efuse_data'
              912  LOAD_GLOBAL              keyslot4
              914  LOAD_GLOBAL              keyslot5
              916  BUILD_SLICE_2         2 
              918  STORE_SUBSCR     

 L. 165       920  LOAD_FAST                'sec_eng_key'
              922  LOAD_CONST               0
              924  LOAD_CONST               16
              926  BUILD_SLICE_2         2 
              928  BINARY_SUBSCR    
              930  LOAD_FAST                'efuse_data'
              932  LOAD_GLOBAL              keyslot2
              934  LOAD_GLOBAL              keyslot3
              936  BUILD_SLICE_2         2 
              938  STORE_SUBSCR     

 L. 166       940  LOAD_FAST                'mask_4bytes'
              942  LOAD_CONST               8
              944  BINARY_MULTIPLY  
              946  LOAD_FAST                'efuse_mask_data'
              948  LOAD_GLOBAL              keyslot3
              950  LOAD_GLOBAL              keyslot5
              952  BUILD_SLICE_2         2 
              954  STORE_SUBSCR     

 L. 167       956  LOAD_FAST                'rw_lock1'
              958  LOAD_CONST               1
              960  LOAD_GLOBAL              wr_lock_key_slot_4
              962  BINARY_LSHIFT    
              964  INPLACE_OR       
              966  STORE_FAST               'rw_lock1'

 L. 168       968  LOAD_FAST                'rw_lock0'
              970  LOAD_CONST               1
              972  LOAD_GLOBAL              wr_lock_key_slot_2
              974  BINARY_LSHIFT    
              976  INPLACE_OR       
              978  STORE_FAST               'rw_lock0'

 L. 169       980  LOAD_FAST                'rw_lock1'
              982  LOAD_CONST               1
              984  LOAD_GLOBAL              rd_lock_key_slot_4
              986  BINARY_LSHIFT    
              988  INPLACE_OR       
              990  STORE_FAST               'rw_lock1'

 L. 170       992  LOAD_FAST                'rw_lock0'
              994  LOAD_CONST               1
              996  LOAD_GLOBAL              rd_lock_key_slot_2
              998  BINARY_LSHIFT    
             1000  INPLACE_OR       
             1002  STORE_FAST               'rw_lock0'
           1004_0  COME_FROM           896  '896'
           1004_1  COME_FROM           528  '528'

 L. 171      1004  LOAD_FAST                'flash_encryp_type'
             1006  LOAD_CONST               1
             1008  COMPARE_OP               ==
         1010_1012  POP_JUMP_IF_FALSE  1318  'to 1318'

 L. 172      1014  LOAD_FAST                'sec_eng_key_sel'
             1016  LOAD_CONST               0
             1018  COMPARE_OP               ==
         1020_1022  POP_JUMP_IF_FALSE  1084  'to 1084'

 L. 173      1024  LOAD_FAST                'sec_eng_key'
             1026  LOAD_CONST               0
             1028  LOAD_CONST               16
             1030  BUILD_SLICE_2         2 
             1032  BINARY_SUBSCR    
             1034  LOAD_FAST                'efuse_data'
             1036  LOAD_GLOBAL              keyslot5
             1038  LOAD_GLOBAL              keyslot6
             1040  BUILD_SLICE_2         2 
             1042  STORE_SUBSCR     

 L. 174      1044  LOAD_FAST                'mask_4bytes'
             1046  LOAD_CONST               4
             1048  BINARY_MULTIPLY  
             1050  LOAD_FAST                'efuse_mask_data'
             1052  LOAD_GLOBAL              keyslot5
             1054  LOAD_GLOBAL              keyslot6
             1056  BUILD_SLICE_2         2 
             1058  STORE_SUBSCR     

 L. 175      1060  LOAD_FAST                'rw_lock1'
             1062  LOAD_CONST               1
             1064  LOAD_GLOBAL              wr_lock_key_slot_5
             1066  BINARY_LSHIFT    
             1068  INPLACE_OR       
             1070  STORE_FAST               'rw_lock1'

 L. 176      1072  LOAD_FAST                'rw_lock1'
             1074  LOAD_CONST               1
             1076  LOAD_GLOBAL              rd_lock_key_slot_5
             1078  BINARY_LSHIFT    
             1080  INPLACE_OR       
             1082  STORE_FAST               'rw_lock1'
           1084_0  COME_FROM          1020  '1020'

 L. 177      1084  LOAD_FAST                'sec_eng_key_sel'
             1086  LOAD_CONST               1
             1088  COMPARE_OP               ==
         1090_1092  POP_JUMP_IF_FALSE  1154  'to 1154'

 L. 178      1094  LOAD_FAST                'sec_eng_key'
             1096  LOAD_CONST               0
             1098  LOAD_CONST               16
             1100  BUILD_SLICE_2         2 
             1102  BINARY_SUBSCR    
             1104  LOAD_FAST                'efuse_data'
             1106  LOAD_GLOBAL              keyslot4
             1108  LOAD_GLOBAL              keyslot5
             1110  BUILD_SLICE_2         2 
             1112  STORE_SUBSCR     

 L. 179      1114  LOAD_FAST                'mask_4bytes'
             1116  LOAD_CONST               4
             1118  BINARY_MULTIPLY  
             1120  LOAD_FAST                'efuse_mask_data'
             1122  LOAD_GLOBAL              keyslot4
             1124  LOAD_GLOBAL              keyslot5
             1126  BUILD_SLICE_2         2 
             1128  STORE_SUBSCR     

 L. 180      1130  LOAD_FAST                'rw_lock1'
             1132  LOAD_CONST               1
             1134  LOAD_GLOBAL              wr_lock_key_slot_4
             1136  BINARY_LSHIFT    
             1138  INPLACE_OR       
             1140  STORE_FAST               'rw_lock1'

 L. 181      1142  LOAD_FAST                'rw_lock1'
             1144  LOAD_CONST               1
             1146  LOAD_GLOBAL              rd_lock_key_slot_4
             1148  BINARY_LSHIFT    
             1150  INPLACE_OR       
             1152  STORE_FAST               'rw_lock1'
           1154_0  COME_FROM          1090  '1090'

 L. 182      1154  LOAD_FAST                'sec_eng_key_sel'
             1156  LOAD_CONST               2
             1158  COMPARE_OP               ==
         1160_1162  POP_JUMP_IF_FALSE  1236  'to 1236'

 L. 183      1164  LOAD_FAST                'flash_key'
             1166  LOAD_CONST               None
             1168  COMPARE_OP               is-not
         1170_1172  POP_JUMP_IF_FALSE  1176  'to 1176'

 L. 185      1174  JUMP_FORWARD       1236  'to 1236'
           1176_0  COME_FROM          1170  '1170'

 L. 187      1176  LOAD_FAST                'sec_eng_key'
             1178  LOAD_CONST               0
             1180  LOAD_CONST               16
             1182  BUILD_SLICE_2         2 
             1184  BINARY_SUBSCR    
             1186  LOAD_FAST                'efuse_data'
             1188  LOAD_GLOBAL              keyslot3
             1190  LOAD_GLOBAL              keyslot3_end
             1192  BUILD_SLICE_2         2 
             1194  STORE_SUBSCR     

 L. 188      1196  LOAD_FAST                'mask_4bytes'
             1198  LOAD_CONST               4
             1200  BINARY_MULTIPLY  
             1202  LOAD_FAST                'efuse_mask_data'
             1204  LOAD_GLOBAL              keyslot3
             1206  LOAD_GLOBAL              keyslot3_end
             1208  BUILD_SLICE_2         2 
             1210  STORE_SUBSCR     

 L. 189      1212  LOAD_FAST                'rw_lock0'
             1214  LOAD_CONST               1
             1216  LOAD_GLOBAL              wr_lock_key_slot_3
             1218  BINARY_LSHIFT    
             1220  INPLACE_OR       
             1222  STORE_FAST               'rw_lock0'

 L. 190      1224  LOAD_FAST                'rw_lock0'
             1226  LOAD_CONST               1
             1228  LOAD_GLOBAL              rd_lock_key_slot_3
             1230  BINARY_LSHIFT    
             1232  INPLACE_OR       
             1234  STORE_FAST               'rw_lock0'
           1236_0  COME_FROM          1174  '1174'
           1236_1  COME_FROM          1160  '1160'

 L. 191      1236  LOAD_FAST                'sec_eng_key_sel'
             1238  LOAD_CONST               3
             1240  COMPARE_OP               ==
         1242_1244  POP_JUMP_IF_FALSE  1318  'to 1318'

 L. 192      1246  LOAD_FAST                'flash_key'
             1248  LOAD_CONST               None
             1250  COMPARE_OP               is-not
         1252_1254  POP_JUMP_IF_FALSE  1258  'to 1258'

 L. 194      1256  JUMP_FORWARD       1318  'to 1318'
           1258_0  COME_FROM          1252  '1252'

 L. 196      1258  LOAD_FAST                'sec_eng_key'
             1260  LOAD_CONST               0
             1262  LOAD_CONST               16
             1264  BUILD_SLICE_2         2 
             1266  BINARY_SUBSCR    
             1268  LOAD_FAST                'efuse_data'
             1270  LOAD_GLOBAL              keyslot2
             1272  LOAD_GLOBAL              keyslot3
             1274  BUILD_SLICE_2         2 
             1276  STORE_SUBSCR     

 L. 197      1278  LOAD_FAST                'mask_4bytes'
             1280  LOAD_CONST               4
             1282  BINARY_MULTIPLY  
             1284  LOAD_FAST                'efuse_mask_data'
             1286  LOAD_GLOBAL              keyslot2
             1288  LOAD_GLOBAL              keyslot3
             1290  BUILD_SLICE_2         2 
             1292  STORE_SUBSCR     

 L. 198      1294  LOAD_FAST                'rw_lock0'
             1296  LOAD_CONST               1
             1298  LOAD_GLOBAL              wr_lock_key_slot_2
             1300  BINARY_LSHIFT    
             1302  INPLACE_OR       
             1304  STORE_FAST               'rw_lock0'

 L. 199      1306  LOAD_FAST                'rw_lock0'
             1308  LOAD_CONST               1
             1310  LOAD_GLOBAL              rd_lock_key_slot_2
             1312  BINARY_LSHIFT    
             1314  INPLACE_OR       
             1316  STORE_FAST               'rw_lock0'
           1318_0  COME_FROM          1256  '1256'
           1318_1  COME_FROM          1242  '1242'
           1318_2  COME_FROM          1010  '1010'

 L. 200      1318  LOAD_FAST                'flash_encryp_type'
             1320  LOAD_CONST               2
             1322  COMPARE_OP               ==
         1324_1326  POP_JUMP_IF_TRUE   1368  'to 1368'

 L. 201      1328  LOAD_FAST                'flash_encryp_type'
             1330  LOAD_CONST               3
             1332  COMPARE_OP               ==
         1334_1336  POP_JUMP_IF_TRUE   1368  'to 1368'

 L. 202      1338  LOAD_FAST                'flash_encryp_type'
             1340  LOAD_CONST               4
             1342  COMPARE_OP               ==
         1344_1346  POP_JUMP_IF_TRUE   1368  'to 1368'

 L. 203      1348  LOAD_FAST                'flash_encryp_type'
             1350  LOAD_CONST               5
             1352  COMPARE_OP               ==
         1354_1356  POP_JUMP_IF_TRUE   1368  'to 1368'

 L. 204      1358  LOAD_FAST                'flash_encryp_type'
             1360  LOAD_CONST               6
             1362  COMPARE_OP               ==
         1364_1366  POP_JUMP_IF_FALSE  1852  'to 1852'
           1368_0  COME_FROM          1354  '1354'
           1368_1  COME_FROM          1344  '1344'
           1368_2  COME_FROM          1334  '1334'
           1368_3  COME_FROM          1324  '1324'

 L. 205      1368  LOAD_FAST                'sec_eng_key_sel'
             1370  LOAD_CONST               0
             1372  COMPARE_OP               ==
         1374_1376  POP_JUMP_IF_FALSE  1498  'to 1498'

 L. 206      1378  LOAD_FAST                'sec_eng_key'
             1380  LOAD_CONST               16
             1382  LOAD_CONST               32
             1384  BUILD_SLICE_2         2 
             1386  BINARY_SUBSCR    
             1388  LOAD_FAST                'efuse_data'
             1390  LOAD_GLOBAL              keyslot6
             1392  LOAD_GLOBAL              keyslot7
             1394  BUILD_SLICE_2         2 
             1396  STORE_SUBSCR     

 L. 207      1398  LOAD_FAST                'sec_eng_key'
             1400  LOAD_CONST               0
             1402  LOAD_CONST               16
             1404  BUILD_SLICE_2         2 
             1406  BINARY_SUBSCR    
             1408  LOAD_FAST                'efuse_data'
             1410  LOAD_GLOBAL              keyslot10
             1412  LOAD_GLOBAL              keyslot10_end
             1414  BUILD_SLICE_2         2 
             1416  STORE_SUBSCR     

 L. 208      1418  LOAD_FAST                'mask_4bytes'
             1420  LOAD_CONST               4
             1422  BINARY_MULTIPLY  
             1424  LOAD_FAST                'efuse_mask_data'
             1426  LOAD_GLOBAL              keyslot6
             1428  LOAD_GLOBAL              keyslot7
             1430  BUILD_SLICE_2         2 
             1432  STORE_SUBSCR     

 L. 209      1434  LOAD_FAST                'mask_4bytes'
             1436  LOAD_CONST               4
             1438  BINARY_MULTIPLY  
             1440  LOAD_FAST                'efuse_mask_data'
             1442  LOAD_GLOBAL              keyslot10
             1444  LOAD_GLOBAL              keyslot10_end
             1446  BUILD_SLICE_2         2 
             1448  STORE_SUBSCR     

 L. 210      1450  LOAD_FAST                'rw_lock1'
             1452  LOAD_CONST               1
             1454  LOAD_GLOBAL              wr_lock_key_slot_6
             1456  BINARY_LSHIFT    
             1458  INPLACE_OR       
             1460  STORE_FAST               'rw_lock1'

 L. 211      1462  LOAD_FAST                'rw_lock1'
             1464  LOAD_CONST               1
             1466  LOAD_GLOBAL              wr_lock_key_slot_10
             1468  BINARY_LSHIFT    
             1470  INPLACE_OR       
             1472  STORE_FAST               'rw_lock1'

 L. 212      1474  LOAD_FAST                'rw_lock1'
             1476  LOAD_CONST               1
             1478  LOAD_GLOBAL              rd_lock_key_slot_6
             1480  BINARY_LSHIFT    
             1482  INPLACE_OR       
             1484  STORE_FAST               'rw_lock1'

 L. 213      1486  LOAD_FAST                'rw_lock1'
             1488  LOAD_CONST               1
             1490  LOAD_GLOBAL              rd_lock_key_slot_10
             1492  BINARY_LSHIFT    
             1494  INPLACE_OR       
             1496  STORE_FAST               'rw_lock1'
           1498_0  COME_FROM          1374  '1374'

 L. 214      1498  LOAD_FAST                'sec_eng_key_sel'
             1500  LOAD_CONST               1
             1502  COMPARE_OP               ==
         1504_1506  POP_JUMP_IF_FALSE  1628  'to 1628'

 L. 215      1508  LOAD_FAST                'sec_eng_key'
             1510  LOAD_CONST               16
             1512  LOAD_CONST               32
             1514  BUILD_SLICE_2         2 
             1516  BINARY_SUBSCR    
             1518  LOAD_FAST                'efuse_data'
             1520  LOAD_GLOBAL              keyslot10
             1522  LOAD_GLOBAL              keyslot10_end
             1524  BUILD_SLICE_2         2 
             1526  STORE_SUBSCR     

 L. 216      1528  LOAD_FAST                'sec_eng_key'
             1530  LOAD_CONST               0
             1532  LOAD_CONST               16
             1534  BUILD_SLICE_2         2 
             1536  BINARY_SUBSCR    
             1538  LOAD_FAST                'efuse_data'
             1540  LOAD_GLOBAL              keyslot6
             1542  LOAD_GLOBAL              keyslot7
             1544  BUILD_SLICE_2         2 
             1546  STORE_SUBSCR     

 L. 217      1548  LOAD_FAST                'mask_4bytes'
             1550  LOAD_CONST               4
             1552  BINARY_MULTIPLY  
             1554  LOAD_FAST                'efuse_mask_data'
             1556  LOAD_GLOBAL              keyslot6
             1558  LOAD_GLOBAL              keyslot7
             1560  BUILD_SLICE_2         2 
             1562  STORE_SUBSCR     

 L. 218      1564  LOAD_FAST                'mask_4bytes'
             1566  LOAD_CONST               4
             1568  BINARY_MULTIPLY  
             1570  LOAD_FAST                'efuse_mask_data'
             1572  LOAD_GLOBAL              keyslot10
             1574  LOAD_GLOBAL              keyslot10_end
             1576  BUILD_SLICE_2         2 
             1578  STORE_SUBSCR     

 L. 219      1580  LOAD_FAST                'rw_lock1'
             1582  LOAD_CONST               1
             1584  LOAD_GLOBAL              wr_lock_key_slot_6
             1586  BINARY_LSHIFT    
             1588  INPLACE_OR       
             1590  STORE_FAST               'rw_lock1'

 L. 220      1592  LOAD_FAST                'rw_lock1'
             1594  LOAD_CONST               1
             1596  LOAD_GLOBAL              wr_lock_key_slot_10
             1598  BINARY_LSHIFT    
             1600  INPLACE_OR       
             1602  STORE_FAST               'rw_lock1'

 L. 221      1604  LOAD_FAST                'rw_lock1'
             1606  LOAD_CONST               1
             1608  LOAD_GLOBAL              rd_lock_key_slot_6
             1610  BINARY_LSHIFT    
             1612  INPLACE_OR       
             1614  STORE_FAST               'rw_lock1'

 L. 222      1616  LOAD_FAST                'rw_lock1'
             1618  LOAD_CONST               1
             1620  LOAD_GLOBAL              rd_lock_key_slot_10
             1622  BINARY_LSHIFT    
             1624  INPLACE_OR       
             1626  STORE_FAST               'rw_lock1'
           1628_0  COME_FROM          1504  '1504'

 L. 223      1628  LOAD_FAST                'sec_eng_key_sel'
             1630  LOAD_CONST               2
             1632  COMPARE_OP               ==
         1634_1636  POP_JUMP_IF_FALSE  1754  'to 1754'

 L. 224      1638  LOAD_FAST                'flash_key'
             1640  LOAD_CONST               None
             1642  COMPARE_OP               is-not
         1644_1646  POP_JUMP_IF_FALSE  1650  'to 1650'

 L. 226      1648  JUMP_FORWARD       1754  'to 1754'
           1650_0  COME_FROM          1644  '1644'

 L. 228      1650  LOAD_FAST                'sec_eng_key'
             1652  LOAD_CONST               16
             1654  LOAD_CONST               32
             1656  BUILD_SLICE_2         2 
             1658  BINARY_SUBSCR    
             1660  LOAD_FAST                'efuse_data'
             1662  LOAD_GLOBAL              keyslot2
             1664  LOAD_GLOBAL              keyslot3
             1666  BUILD_SLICE_2         2 
             1668  STORE_SUBSCR     

 L. 229      1670  LOAD_FAST                'sec_eng_key'
             1672  LOAD_CONST               0
             1674  LOAD_CONST               16
             1676  BUILD_SLICE_2         2 
             1678  BINARY_SUBSCR    
             1680  LOAD_FAST                'efuse_data'
             1682  LOAD_GLOBAL              keyslot3
             1684  LOAD_GLOBAL              keyslot3_end
             1686  BUILD_SLICE_2         2 
             1688  STORE_SUBSCR     

 L. 230      1690  LOAD_FAST                'mask_4bytes'
             1692  LOAD_CONST               8
             1694  BINARY_MULTIPLY  
             1696  LOAD_FAST                'efuse_mask_data'
             1698  LOAD_GLOBAL              keyslot2
             1700  LOAD_GLOBAL              keyslot3_end
             1702  BUILD_SLICE_2         2 
             1704  STORE_SUBSCR     

 L. 231      1706  LOAD_FAST                'rw_lock0'
             1708  LOAD_CONST               1
             1710  LOAD_GLOBAL              wr_lock_key_slot_2
             1712  BINARY_LSHIFT    
             1714  INPLACE_OR       
             1716  STORE_FAST               'rw_lock0'

 L. 232      1718  LOAD_FAST                'rw_lock0'
             1720  LOAD_CONST               1
             1722  LOAD_GLOBAL              rd_lock_key_slot_2
             1724  BINARY_LSHIFT    
             1726  INPLACE_OR       
             1728  STORE_FAST               'rw_lock0'

 L. 233      1730  LOAD_FAST                'rw_lock0'
             1732  LOAD_CONST               1
             1734  LOAD_GLOBAL              wr_lock_key_slot_3
             1736  BINARY_LSHIFT    
             1738  INPLACE_OR       
             1740  STORE_FAST               'rw_lock0'

 L. 234      1742  LOAD_FAST                'rw_lock0'
             1744  LOAD_CONST               1
             1746  LOAD_GLOBAL              rd_lock_key_slot_3
             1748  BINARY_LSHIFT    
             1750  INPLACE_OR       
             1752  STORE_FAST               'rw_lock0'
           1754_0  COME_FROM          1648  '1648'
           1754_1  COME_FROM          1634  '1634'

 L. 235      1754  LOAD_FAST                'sec_eng_key_sel'
             1756  LOAD_CONST               3
             1758  COMPARE_OP               ==
         1760_1762  POP_JUMP_IF_FALSE  1852  'to 1852'

 L. 236      1764  LOAD_FAST                'flash_key'
             1766  LOAD_CONST               None
             1768  COMPARE_OP               is-not
         1770_1772  POP_JUMP_IF_FALSE  1776  'to 1776'

 L. 238      1774  JUMP_FORWARD       1852  'to 1852'
           1776_0  COME_FROM          1770  '1770'

 L. 240      1776  LOAD_FAST                'sec_eng_key'
             1778  LOAD_FAST                'efuse_data'
             1780  LOAD_GLOBAL              keyslot2
             1782  LOAD_GLOBAL              keyslot3_end
             1784  BUILD_SLICE_2         2 
             1786  STORE_SUBSCR     

 L. 241      1788  LOAD_FAST                'mask_4bytes'
             1790  LOAD_CONST               8
             1792  BINARY_MULTIPLY  
             1794  LOAD_FAST                'efuse_mask_data'
             1796  LOAD_GLOBAL              keyslot2
             1798  LOAD_GLOBAL              keyslot3_end
             1800  BUILD_SLICE_2         2 
             1802  STORE_SUBSCR     

 L. 242      1804  LOAD_FAST                'rw_lock0'
             1806  LOAD_CONST               1
             1808  LOAD_GLOBAL              wr_lock_key_slot_2
             1810  BINARY_LSHIFT    
             1812  INPLACE_OR       
             1814  STORE_FAST               'rw_lock0'

 L. 243      1816  LOAD_FAST                'rw_lock0'
             1818  LOAD_CONST               1
             1820  LOAD_GLOBAL              rd_lock_key_slot_2
             1822  BINARY_LSHIFT    
             1824  INPLACE_OR       
             1826  STORE_FAST               'rw_lock0'

 L. 244      1828  LOAD_FAST                'rw_lock0'
             1830  LOAD_CONST               1
             1832  LOAD_GLOBAL              wr_lock_key_slot_3
             1834  BINARY_LSHIFT    
             1836  INPLACE_OR       
             1838  STORE_FAST               'rw_lock0'

 L. 245      1840  LOAD_FAST                'rw_lock0'
             1842  LOAD_CONST               1
             1844  LOAD_GLOBAL              rd_lock_key_slot_3
             1846  BINARY_LSHIFT    
             1848  INPLACE_OR       
             1850  STORE_FAST               'rw_lock0'
           1852_0  COME_FROM          1774  '1774'
           1852_1  COME_FROM          1760  '1760'
           1852_2  COME_FROM          1364  '1364'
           1852_3  COME_FROM           518  '518'

 L. 247      1852  LOAD_GLOBAL              bytearray_data_merge
             1854  LOAD_FAST                'efuse_data'
             1856  LOAD_CONST               124
             1858  LOAD_CONST               128
             1860  BUILD_SLICE_2         2 
             1862  BINARY_SUBSCR    

 L. 248      1864  LOAD_GLOBAL              bflb_utils
             1866  LOAD_METHOD              int_to_4bytearray_l
             1868  LOAD_FAST                'rw_lock0'
             1870  CALL_METHOD_1         1  '1 positional argument'
             1872  LOAD_CONST               4
             1874  CALL_FUNCTION_3       3  '3 positional arguments'
             1876  LOAD_FAST                'efuse_data'
             1878  LOAD_CONST               124
             1880  LOAD_CONST               128
             1882  BUILD_SLICE_2         2 
             1884  STORE_SUBSCR     

 L. 249      1886  LOAD_GLOBAL              bytearray_data_merge
             1888  LOAD_FAST                'efuse_mask_data'
             1890  LOAD_CONST               124
             1892  LOAD_CONST               128
             1894  BUILD_SLICE_2         2 
             1896  BINARY_SUBSCR    

 L. 250      1898  LOAD_GLOBAL              bflb_utils
             1900  LOAD_METHOD              int_to_4bytearray_l
             1902  LOAD_FAST                'rw_lock0'
             1904  CALL_METHOD_1         1  '1 positional argument'
             1906  LOAD_CONST               4
             1908  CALL_FUNCTION_3       3  '3 positional arguments'
             1910  LOAD_FAST                'efuse_mask_data'
             1912  LOAD_CONST               124
             1914  LOAD_CONST               128
             1916  BUILD_SLICE_2         2 
             1918  STORE_SUBSCR     

 L. 251      1920  LOAD_GLOBAL              bytearray_data_merge
             1922  LOAD_FAST                'efuse_data'
             1924  LOAD_CONST               252
             1926  LOAD_CONST               256
             1928  BUILD_SLICE_2         2 
             1930  BINARY_SUBSCR    

 L. 252      1932  LOAD_GLOBAL              bflb_utils
             1934  LOAD_METHOD              int_to_4bytearray_l
             1936  LOAD_FAST                'rw_lock1'
             1938  CALL_METHOD_1         1  '1 positional argument'
             1940  LOAD_CONST               4
             1942  CALL_FUNCTION_3       3  '3 positional arguments'
             1944  LOAD_FAST                'efuse_data'
             1946  LOAD_CONST               252
             1948  LOAD_CONST               256
             1950  BUILD_SLICE_2         2 
             1952  STORE_SUBSCR     

 L. 253      1954  LOAD_GLOBAL              bytearray_data_merge
             1956  LOAD_FAST                'efuse_mask_data'
             1958  LOAD_CONST               252
             1960  LOAD_CONST               256
             1962  BUILD_SLICE_2         2 
             1964  BINARY_SUBSCR    

 L. 254      1966  LOAD_GLOBAL              bflb_utils
             1968  LOAD_METHOD              int_to_4bytearray_l
             1970  LOAD_FAST                'rw_lock1'
             1972  CALL_METHOD_1         1  '1 positional argument'
             1974  LOAD_CONST               4
             1976  CALL_FUNCTION_3       3  '3 positional arguments'
             1978  LOAD_FAST                'efuse_mask_data'
             1980  LOAD_CONST               252
             1982  LOAD_CONST               256
             1984  BUILD_SLICE_2         2 
             1986  STORE_SUBSCR     

 L. 256      1988  LOAD_FAST                'security'
             1990  LOAD_CONST               True
             1992  COMPARE_OP               is
         1994_1996  POP_JUMP_IF_FALSE  2084  'to 2084'

 L. 257      1998  LOAD_GLOBAL              open
             2000  LOAD_GLOBAL              os
             2002  LOAD_ATTR                path
             2004  LOAD_METHOD              join
             2006  LOAD_FAST                'cfg'
             2008  LOAD_STR                 'efusedata_raw.bin'
             2010  CALL_METHOD_2         2  '2 positional arguments'
             2012  LOAD_STR                 'wb+'
             2014  CALL_FUNCTION_2       2  '2 positional arguments'
             2016  STORE_FAST               'fp'

 L. 258      2018  LOAD_FAST                'fp'
             2020  LOAD_METHOD              write
             2022  LOAD_FAST                'efuse_data'
             2024  CALL_METHOD_1         1  '1 positional argument'
             2026  POP_TOP          

 L. 259      2028  LOAD_FAST                'fp'
             2030  LOAD_METHOD              close
             2032  CALL_METHOD_0         0  '0 positional arguments'
             2034  POP_TOP          

 L. 260      2036  LOAD_GLOBAL              bflb_utils
             2038  LOAD_METHOD              printf
             2040  LOAD_STR                 'Encrypt efuse data'
             2042  CALL_METHOD_1         1  '1 positional argument'
             2044  POP_TOP          

 L. 261      2046  LOAD_GLOBAL              bflb_utils
             2048  LOAD_METHOD              get_security_key
             2050  CALL_METHOD_0         0  '0 positional arguments'
             2052  UNPACK_SEQUENCE_2     2 
             2054  STORE_FAST               'security_key'
             2056  STORE_FAST               'security_iv'

 L. 262      2058  LOAD_GLOBAL              img_create_encrypt_data
             2060  LOAD_FAST                'efuse_data'
             2062  LOAD_FAST                'security_key'
             2064  LOAD_FAST                'security_iv'
             2066  LOAD_CONST               0
             2068  CALL_FUNCTION_4       4  '4 positional arguments'
             2070  STORE_FAST               'efuse_data'

 L. 263      2072  LOAD_GLOBAL              bytearray
             2074  LOAD_CONST               4096
             2076  CALL_FUNCTION_1       1  '1 positional argument'
             2078  LOAD_FAST                'efuse_data'
             2080  BINARY_ADD       
             2082  STORE_FAST               'efuse_data'
           2084_0  COME_FROM          1994  '1994'

 L. 264      2084  LOAD_GLOBAL              open
             2086  LOAD_GLOBAL              os
             2088  LOAD_ATTR                path
             2090  LOAD_METHOD              join
             2092  LOAD_FAST                'cfg'
             2094  LOAD_STR                 'efusedata.bin'
             2096  CALL_METHOD_2         2  '2 positional arguments'
             2098  LOAD_STR                 'wb+'
             2100  CALL_FUNCTION_2       2  '2 positional arguments'
             2102  STORE_FAST               'fp'

 L. 265      2104  LOAD_FAST                'fp'
             2106  LOAD_METHOD              write
             2108  LOAD_FAST                'efuse_data'
             2110  CALL_METHOD_1         1  '1 positional argument'
             2112  POP_TOP          

 L. 266      2114  LOAD_FAST                'fp'
             2116  LOAD_METHOD              close
             2118  CALL_METHOD_0         0  '0 positional arguments'
             2120  POP_TOP          

 L. 267      2122  LOAD_GLOBAL              open
             2124  LOAD_GLOBAL              os
             2126  LOAD_ATTR                path
             2128  LOAD_METHOD              join
             2130  LOAD_FAST                'cfg'
             2132  LOAD_STR                 'efusedata_mask.bin'
             2134  CALL_METHOD_2         2  '2 positional arguments'
             2136  LOAD_STR                 'wb+'
             2138  CALL_FUNCTION_2       2  '2 positional arguments'
             2140  STORE_FAST               'fp'

 L. 268      2142  LOAD_FAST                'fp'
             2144  LOAD_METHOD              write
             2146  LOAD_FAST                'efuse_mask_data'
             2148  CALL_METHOD_1         1  '1 positional argument'
             2150  POP_TOP          

 L. 269      2152  LOAD_FAST                'fp'
             2154  LOAD_METHOD              close
             2156  CALL_METHOD_0         0  '0 positional arguments'
             2158  POP_TOP          

Parse error at or near `CALL_METHOD_0' instruction at offset 2156


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
    bootcfg_start = 120
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
            if len(aeskey_hexstr) != 64:
                bflb_utils.printf('[Error] Key len must be 32 when xts mode enabled!!!!')
                return (data_bytearray, None)
            bflb_utils.printf('Enable xts mode')
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
                boot_data[256:256 + len(pk_data + signature)] = pk_data + signature
                boot_data[256 + len(pk_data + signature):256 + len(pk_data + signature) + len(aesiv_data)] = aesiv_data
                filedir, ext = os.path.split(imgfile)
                flash_encrypt_type = firmware_post_get_flash_encrypt_type(encrypt, xts_mode)
                key_sel = 0
                security = True
                if encrypt != 0:
                    img_update_efuse_data(filedir, sign, pk_hash, flash_encrypt_type, encrypt_key + bytearray(32 - len(encrypt_key)), key_sel, None, security)
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
    crcarray = bflb_utils.get_crc32_bytearray(image_data[clockcfg_start + 4:clockcfg_start + 16])
    image_data[clockcfg_start + 16:clockcfg_start + 16 + 4] = crcarray
    bflb_utils.printf('Clock config crc: ', binascii.hexlify(crcarray))
    return image_data


def firmware_post_proc_update_bootheader_crc(image_data):
    crcarray = bflb_utils.get_crc32_bytearray(image_data[0:252])
    image_data[252:256] = crcarray
    bflb_utils.printf('Bootheader config crc: ', binascii.hexlify(crcarray))
    return image_data


def firmware_post_proc_get_hash_ignore(image_data):
    bootcfg_start = 120
    return image_data[bootcfg_start + 2] >> 1 & 1


def firmware_post_proc_enable_hash_cfg(image_data):
    bootcfg_start = 120
    image_data[bootcfg_start + 2] &= -3
    return image_data


def firmware_post_proc_get_image_offset(image_data):
    cpucfg_start = 120
    return image_data[cpucfg_start + 4] + (image_data[cpucfg_start + 5] << 8) + (image_data[cpucfg_start + 6] << 16) + (image_data[cpucfg_start + 7] << 24)


def firmware_post_proc_update_hash(image_data, force_update, args, hash):
    image_offset = firmware_post_proc_get_image_offset(image_data)
    bflb_utils.printf('Image Offset:' + hex(image_offset))
    bootcfg_start = 120
    image_data[bootcfg_start + 12:bootcfg_start + 12 + 4] = bflb_utils.int_to_4bytearray_l(len(image_data) - image_offset)
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