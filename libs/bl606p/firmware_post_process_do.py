# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
# [GCC 9.4.0]
# Embedded file name: libs/bl606p/firmware_post_process_do.py
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
                2  LOAD_CONST               256
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  STORE_FAST               'efuse_data'

 L.  83         8  LOAD_GLOBAL              bytearray
               10  LOAD_CONST               256
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
               74  POP_JUMP_IF_FALSE   108  'to 108'

 L.  94        76  LOAD_FAST                'efuse_data'
               78  LOAD_CONST               93
               80  DUP_TOP_TWO      
               82  BINARY_SUBSCR    
               84  LOAD_FAST                'sign'
               86  INPLACE_OR       
               88  ROT_THREE        
               90  STORE_SUBSCR     

 L.  95        92  LOAD_FAST                'efuse_mask_data'
               94  LOAD_CONST               93
               96  DUP_TOP_TWO      
               98  BINARY_SUBSCR    
              100  LOAD_CONST               255
              102  INPLACE_OR       
              104  ROT_THREE        
              106  STORE_SUBSCR     
            108_0  COME_FROM            74  '74'

 L.  97       108  LOAD_FAST                'flash_encryp_type'
              110  LOAD_CONST               0
              112  COMPARE_OP               >
              114  POP_JUMP_IF_FALSE   132  'to 132'

 L.  98       116  LOAD_FAST                'efuse_data'
              118  LOAD_CONST               0
              120  DUP_TOP_TWO      
              122  BINARY_SUBSCR    
              124  LOAD_CONST               48
              126  INPLACE_OR       
              128  ROT_THREE        
              130  STORE_SUBSCR     
            132_0  COME_FROM           114  '114'

 L.  99       132  LOAD_FAST                'efuse_mask_data'
              134  LOAD_CONST               0
              136  DUP_TOP_TWO      
              138  BINARY_SUBSCR    
              140  LOAD_CONST               255
              142  INPLACE_OR       
              144  ROT_THREE        
              146  STORE_SUBSCR     

 L. 100       148  LOAD_CONST               0
              150  STORE_FAST               'rw_lock0'

 L. 101       152  LOAD_CONST               0
              154  STORE_FAST               'rw_lock1'

 L. 102       156  LOAD_FAST                'pk_hash'
              158  LOAD_CONST               None
              160  COMPARE_OP               is-not
              162  POP_JUMP_IF_FALSE   216  'to 216'

 L. 103       164  LOAD_FAST                'pk_hash'
              166  LOAD_FAST                'efuse_data'
              168  LOAD_GLOBAL              keyslot0
              170  LOAD_GLOBAL              keyslot2
              172  BUILD_SLICE_2         2 
              174  STORE_SUBSCR     

 L. 104       176  LOAD_FAST                'mask_4bytes'
              178  LOAD_CONST               8
              180  BINARY_MULTIPLY  
              182  LOAD_FAST                'efuse_mask_data'
              184  LOAD_GLOBAL              keyslot0
              186  LOAD_GLOBAL              keyslot2
              188  BUILD_SLICE_2         2 
              190  STORE_SUBSCR     

 L. 105       192  LOAD_FAST                'rw_lock0'
              194  LOAD_CONST               1
              196  LOAD_GLOBAL              wr_lock_key_slot_0
              198  BINARY_LSHIFT    
              200  INPLACE_OR       
              202  STORE_FAST               'rw_lock0'

 L. 106       204  LOAD_FAST                'rw_lock0'
              206  LOAD_CONST               1
              208  LOAD_GLOBAL              wr_lock_key_slot_1
              210  BINARY_LSHIFT    
              212  INPLACE_OR       
              214  STORE_FAST               'rw_lock0'
            216_0  COME_FROM           162  '162'

 L. 107       216  LOAD_FAST                'flash_key'
              218  LOAD_CONST               None
              220  COMPARE_OP               is-not
          222_224  POP_JUMP_IF_FALSE   508  'to 508'

 L. 108       226  LOAD_FAST                'flash_encryp_type'
              228  LOAD_CONST               1
              230  COMPARE_OP               ==
          232_234  POP_JUMP_IF_FALSE   274  'to 274'

 L. 110       236  LOAD_FAST                'flash_key'
              238  LOAD_CONST               0
              240  LOAD_CONST               16
              242  BUILD_SLICE_2         2 
              244  BINARY_SUBSCR    
              246  LOAD_FAST                'efuse_data'
              248  LOAD_GLOBAL              keyslot2
              250  LOAD_GLOBAL              keyslot3
              252  BUILD_SLICE_2         2 
              254  STORE_SUBSCR     

 L. 111       256  LOAD_FAST                'mask_4bytes'
              258  LOAD_CONST               4
              260  BINARY_MULTIPLY  
              262  LOAD_FAST                'efuse_mask_data'
              264  LOAD_GLOBAL              keyslot2
              266  LOAD_GLOBAL              keyslot3
              268  BUILD_SLICE_2         2 
              270  STORE_SUBSCR     
              272  JUMP_FORWARD        484  'to 484'
            274_0  COME_FROM           232  '232'

 L. 112       274  LOAD_FAST                'flash_encryp_type'
              276  LOAD_CONST               2
              278  COMPARE_OP               ==
          280_282  POP_JUMP_IF_FALSE   338  'to 338'

 L. 114       284  LOAD_FAST                'flash_key'
              286  LOAD_FAST                'efuse_data'
              288  LOAD_GLOBAL              keyslot2
              290  LOAD_GLOBAL              keyslot3_end
              292  BUILD_SLICE_2         2 
              294  STORE_SUBSCR     

 L. 115       296  LOAD_FAST                'mask_4bytes'
              298  LOAD_CONST               8
              300  BINARY_MULTIPLY  
              302  LOAD_FAST                'efuse_mask_data'
              304  LOAD_GLOBAL              keyslot2
              306  LOAD_GLOBAL              keyslot3_end
              308  BUILD_SLICE_2         2 
              310  STORE_SUBSCR     

 L. 116       312  LOAD_FAST                'rw_lock0'
              314  LOAD_CONST               1
              316  LOAD_GLOBAL              wr_lock_key_slot_3
              318  BINARY_LSHIFT    
              320  INPLACE_OR       
              322  STORE_FAST               'rw_lock0'

 L. 117       324  LOAD_FAST                'rw_lock0'
              326  LOAD_CONST               1
              328  LOAD_GLOBAL              rd_lock_key_slot_3
              330  BINARY_LSHIFT    
              332  INPLACE_OR       
              334  STORE_FAST               'rw_lock0'
              336  JUMP_FORWARD        484  'to 484'
            338_0  COME_FROM           280  '280'

 L. 118       338  LOAD_FAST                'flash_encryp_type'
              340  LOAD_CONST               3
              342  COMPARE_OP               ==
          344_346  POP_JUMP_IF_FALSE   402  'to 402'

 L. 120       348  LOAD_FAST                'flash_key'
              350  LOAD_FAST                'efuse_data'
              352  LOAD_GLOBAL              keyslot2
              354  LOAD_GLOBAL              keyslot3_end
              356  BUILD_SLICE_2         2 
              358  STORE_SUBSCR     

 L. 121       360  LOAD_FAST                'mask_4bytes'
              362  LOAD_CONST               8
              364  BINARY_MULTIPLY  
              366  LOAD_FAST                'efuse_mask_data'
              368  LOAD_GLOBAL              keyslot2
              370  LOAD_GLOBAL              keyslot3_end
              372  BUILD_SLICE_2         2 
              374  STORE_SUBSCR     

 L. 122       376  LOAD_FAST                'rw_lock0'
              378  LOAD_CONST               1
              380  LOAD_GLOBAL              wr_lock_key_slot_3
              382  BINARY_LSHIFT    
              384  INPLACE_OR       
              386  STORE_FAST               'rw_lock0'

 L. 123       388  LOAD_FAST                'rw_lock0'
              390  LOAD_CONST               1
              392  LOAD_GLOBAL              rd_lock_key_slot_3
              394  BINARY_LSHIFT    
              396  INPLACE_OR       
              398  STORE_FAST               'rw_lock0'
              400  JUMP_FORWARD        484  'to 484'
            402_0  COME_FROM           344  '344'

 L. 124       402  LOAD_FAST                'flash_encryp_type'
              404  LOAD_CONST               4
              406  COMPARE_OP               ==
          408_410  POP_JUMP_IF_TRUE    432  'to 432'

 L. 125       412  LOAD_FAST                'flash_encryp_type'
              414  LOAD_CONST               5
              416  COMPARE_OP               ==
          418_420  POP_JUMP_IF_TRUE    432  'to 432'

 L. 126       422  LOAD_FAST                'flash_encryp_type'
              424  LOAD_CONST               6
              426  COMPARE_OP               ==
          428_430  POP_JUMP_IF_FALSE   484  'to 484'
            432_0  COME_FROM           418  '418'
            432_1  COME_FROM           408  '408'

 L. 128       432  LOAD_FAST                'flash_key'
              434  LOAD_FAST                'efuse_data'
              436  LOAD_GLOBAL              keyslot2
              438  LOAD_GLOBAL              keyslot3_end
              440  BUILD_SLICE_2         2 
              442  STORE_SUBSCR     

 L. 129       444  LOAD_FAST                'mask_4bytes'
              446  LOAD_CONST               8
              448  BINARY_MULTIPLY  
              450  LOAD_FAST                'efuse_mask_data'
              452  LOAD_GLOBAL              keyslot2
              454  LOAD_GLOBAL              keyslot3_end
              456  BUILD_SLICE_2         2 
              458  STORE_SUBSCR     

 L. 130       460  LOAD_FAST                'rw_lock0'
              462  LOAD_CONST               1
              464  LOAD_GLOBAL              wr_lock_key_slot_3
              466  BINARY_LSHIFT    
              468  INPLACE_OR       
              470  STORE_FAST               'rw_lock0'

 L. 131       472  LOAD_FAST                'rw_lock0'
              474  LOAD_CONST               1
              476  LOAD_GLOBAL              rd_lock_key_slot_3
              478  BINARY_LSHIFT    
              480  INPLACE_OR       
              482  STORE_FAST               'rw_lock0'
            484_0  COME_FROM           428  '428'
            484_1  COME_FROM           400  '400'
            484_2  COME_FROM           336  '336'
            484_3  COME_FROM           272  '272'

 L. 133       484  LOAD_FAST                'rw_lock0'
              486  LOAD_CONST               1
              488  LOAD_GLOBAL              wr_lock_key_slot_2
              490  BINARY_LSHIFT    
              492  INPLACE_OR       
              494  STORE_FAST               'rw_lock0'

 L. 134       496  LOAD_FAST                'rw_lock0'
              498  LOAD_CONST               1
              500  LOAD_GLOBAL              rd_lock_key_slot_2
              502  BINARY_LSHIFT    
              504  INPLACE_OR       
              506  STORE_FAST               'rw_lock0'
            508_0  COME_FROM           222  '222'

 L. 136       508  LOAD_FAST                'sec_eng_key'
              510  LOAD_CONST               None
              512  COMPARE_OP               is-not
          514_516  POP_JUMP_IF_FALSE  1848  'to 1848'

 L. 137       518  LOAD_FAST                'flash_encryp_type'
              520  LOAD_CONST               0
              522  COMPARE_OP               ==
          524_526  POP_JUMP_IF_FALSE  1000  'to 1000'

 L. 138       528  LOAD_FAST                'sec_eng_key_sel'
              530  LOAD_CONST               0
              532  COMPARE_OP               ==
          534_536  POP_JUMP_IF_FALSE   642  'to 642'

 L. 139       538  LOAD_FAST                'sec_eng_key'
              540  LOAD_CONST               16
              542  LOAD_CONST               32
              544  BUILD_SLICE_2         2 
              546  BINARY_SUBSCR    
              548  LOAD_FAST                'efuse_data'
              550  LOAD_GLOBAL              keyslot2
              552  LOAD_GLOBAL              keyslot3
              554  BUILD_SLICE_2         2 
              556  STORE_SUBSCR     

 L. 140       558  LOAD_FAST                'sec_eng_key'
              560  LOAD_CONST               0
              562  LOAD_CONST               16
              564  BUILD_SLICE_2         2 
              566  BINARY_SUBSCR    
              568  LOAD_FAST                'efuse_data'
              570  LOAD_GLOBAL              keyslot3
              572  LOAD_GLOBAL              keyslot3_end
              574  BUILD_SLICE_2         2 
              576  STORE_SUBSCR     

 L. 141       578  LOAD_FAST                'mask_4bytes'
              580  LOAD_CONST               8
              582  BINARY_MULTIPLY  
              584  LOAD_FAST                'efuse_mask_data'
              586  LOAD_GLOBAL              keyslot2
              588  LOAD_GLOBAL              keyslot3_end
              590  BUILD_SLICE_2         2 
              592  STORE_SUBSCR     

 L. 142       594  LOAD_FAST                'rw_lock0'
              596  LOAD_CONST               1
              598  LOAD_GLOBAL              wr_lock_key_slot_2
              600  BINARY_LSHIFT    
              602  INPLACE_OR       
              604  STORE_FAST               'rw_lock0'

 L. 143       606  LOAD_FAST                'rw_lock0'
              608  LOAD_CONST               1
              610  LOAD_GLOBAL              wr_lock_key_slot_3
              612  BINARY_LSHIFT    
              614  INPLACE_OR       
              616  STORE_FAST               'rw_lock0'

 L. 144       618  LOAD_FAST                'rw_lock0'
              620  LOAD_CONST               1
              622  LOAD_GLOBAL              rd_lock_key_slot_2
              624  BINARY_LSHIFT    
              626  INPLACE_OR       
              628  STORE_FAST               'rw_lock0'

 L. 145       630  LOAD_FAST                'rw_lock0'
              632  LOAD_CONST               1
              634  LOAD_GLOBAL              rd_lock_key_slot_3
              636  BINARY_LSHIFT    
              638  INPLACE_OR       
              640  STORE_FAST               'rw_lock0'
            642_0  COME_FROM           534  '534'

 L. 146       642  LOAD_FAST                'sec_eng_key_sel'
              644  LOAD_CONST               1
              646  COMPARE_OP               ==
          648_650  POP_JUMP_IF_FALSE   772  'to 772'

 L. 147       652  LOAD_FAST                'sec_eng_key'
              654  LOAD_CONST               16
              656  LOAD_CONST               32
              658  BUILD_SLICE_2         2 
              660  BINARY_SUBSCR    
              662  LOAD_FAST                'efuse_data'
              664  LOAD_GLOBAL              keyslot3
              666  LOAD_GLOBAL              keyslot3_end
              668  BUILD_SLICE_2         2 
              670  STORE_SUBSCR     

 L. 148       672  LOAD_FAST                'sec_eng_key'
              674  LOAD_CONST               0
              676  LOAD_CONST               16
              678  BUILD_SLICE_2         2 
              680  BINARY_SUBSCR    
              682  LOAD_FAST                'efuse_data'
              684  LOAD_GLOBAL              keyslot4
              686  LOAD_GLOBAL              keyslot5
              688  BUILD_SLICE_2         2 
              690  STORE_SUBSCR     

 L. 149       692  LOAD_FAST                'mask_4bytes'
              694  LOAD_CONST               4
              696  BINARY_MULTIPLY  
              698  LOAD_FAST                'efuse_mask_data'
              700  LOAD_GLOBAL              keyslot3
              702  LOAD_GLOBAL              keyslot3_end
              704  BUILD_SLICE_2         2 
              706  STORE_SUBSCR     

 L. 150       708  LOAD_FAST                'mask_4bytes'
              710  LOAD_CONST               4
              712  BINARY_MULTIPLY  
              714  LOAD_FAST                'efuse_mask_data'
              716  LOAD_GLOBAL              keyslot4
              718  LOAD_GLOBAL              keyslot5
              720  BUILD_SLICE_2         2 
              722  STORE_SUBSCR     

 L. 151       724  LOAD_FAST                'rw_lock0'
              726  LOAD_CONST               1
              728  LOAD_GLOBAL              wr_lock_key_slot_3
              730  BINARY_LSHIFT    
              732  INPLACE_OR       
              734  STORE_FAST               'rw_lock0'

 L. 152       736  LOAD_FAST                'rw_lock1'
              738  LOAD_CONST               1
              740  LOAD_GLOBAL              wr_lock_key_slot_4
              742  BINARY_LSHIFT    
              744  INPLACE_OR       
              746  STORE_FAST               'rw_lock1'

 L. 153       748  LOAD_FAST                'rw_lock0'
              750  LOAD_CONST               1
              752  LOAD_GLOBAL              rd_lock_key_slot_3
              754  BINARY_LSHIFT    
              756  INPLACE_OR       
              758  STORE_FAST               'rw_lock0'

 L. 154       760  LOAD_FAST                'rw_lock1'
              762  LOAD_CONST               1
              764  LOAD_GLOBAL              rd_lock_key_slot_4
              766  BINARY_LSHIFT    
              768  INPLACE_OR       
              770  STORE_FAST               'rw_lock1'
            772_0  COME_FROM           648  '648'

 L. 155       772  LOAD_FAST                'sec_eng_key_sel'
              774  LOAD_CONST               2
              776  COMPARE_OP               ==
          778_780  POP_JUMP_IF_FALSE   886  'to 886'

 L. 156       782  LOAD_FAST                'sec_eng_key'
              784  LOAD_CONST               16
              786  LOAD_CONST               32
              788  BUILD_SLICE_2         2 
              790  BINARY_SUBSCR    
              792  LOAD_FAST                'efuse_data'
              794  LOAD_GLOBAL              keyslot4
              796  LOAD_GLOBAL              keyslot5
              798  BUILD_SLICE_2         2 
              800  STORE_SUBSCR     

 L. 157       802  LOAD_FAST                'sec_eng_key'
              804  LOAD_CONST               0
              806  LOAD_CONST               16
              808  BUILD_SLICE_2         2 
              810  BINARY_SUBSCR    
              812  LOAD_FAST                'efuse_data'
              814  LOAD_GLOBAL              keyslot2
              816  LOAD_GLOBAL              keyslot3
              818  BUILD_SLICE_2         2 
              820  STORE_SUBSCR     

 L. 158       822  LOAD_FAST                'mask_4bytes'
              824  LOAD_CONST               8
              826  BINARY_MULTIPLY  
              828  LOAD_FAST                'efuse_mask_data'
              830  LOAD_GLOBAL              keyslot3
              832  LOAD_GLOBAL              keyslot5
              834  BUILD_SLICE_2         2 
              836  STORE_SUBSCR     

 L. 159       838  LOAD_FAST                'rw_lock1'
              840  LOAD_CONST               1
              842  LOAD_GLOBAL              wr_lock_key_slot_4
              844  BINARY_LSHIFT    
              846  INPLACE_OR       
              848  STORE_FAST               'rw_lock1'

 L. 160       850  LOAD_FAST                'rw_lock0'
              852  LOAD_CONST               1
              854  LOAD_GLOBAL              wr_lock_key_slot_2
              856  BINARY_LSHIFT    
              858  INPLACE_OR       
              860  STORE_FAST               'rw_lock0'

 L. 161       862  LOAD_FAST                'rw_lock1'
              864  LOAD_CONST               1
              866  LOAD_GLOBAL              rd_lock_key_slot_4
              868  BINARY_LSHIFT    
              870  INPLACE_OR       
              872  STORE_FAST               'rw_lock1'

 L. 162       874  LOAD_FAST                'rw_lock0'
              876  LOAD_CONST               1
              878  LOAD_GLOBAL              rd_lock_key_slot_2
              880  BINARY_LSHIFT    
              882  INPLACE_OR       
              884  STORE_FAST               'rw_lock0'
            886_0  COME_FROM           778  '778'

 L. 163       886  LOAD_FAST                'sec_eng_key_sel'
              888  LOAD_CONST               3
              890  COMPARE_OP               ==
          892_894  POP_JUMP_IF_FALSE  1000  'to 1000'

 L. 164       896  LOAD_FAST                'sec_eng_key'
              898  LOAD_CONST               16
              900  LOAD_CONST               32
              902  BUILD_SLICE_2         2 
              904  BINARY_SUBSCR    
              906  LOAD_FAST                'efuse_data'
              908  LOAD_GLOBAL              keyslot4
              910  LOAD_GLOBAL              keyslot5
              912  BUILD_SLICE_2         2 
              914  STORE_SUBSCR     

 L. 165       916  LOAD_FAST                'sec_eng_key'
              918  LOAD_CONST               0
              920  LOAD_CONST               16
              922  BUILD_SLICE_2         2 
              924  BINARY_SUBSCR    
              926  LOAD_FAST                'efuse_data'
              928  LOAD_GLOBAL              keyslot2
              930  LOAD_GLOBAL              keyslot3
              932  BUILD_SLICE_2         2 
              934  STORE_SUBSCR     

 L. 166       936  LOAD_FAST                'mask_4bytes'
              938  LOAD_CONST               8
              940  BINARY_MULTIPLY  
              942  LOAD_FAST                'efuse_mask_data'
              944  LOAD_GLOBAL              keyslot3
              946  LOAD_GLOBAL              keyslot5
              948  BUILD_SLICE_2         2 
              950  STORE_SUBSCR     

 L. 167       952  LOAD_FAST                'rw_lock1'
              954  LOAD_CONST               1
              956  LOAD_GLOBAL              wr_lock_key_slot_4
              958  BINARY_LSHIFT    
              960  INPLACE_OR       
              962  STORE_FAST               'rw_lock1'

 L. 168       964  LOAD_FAST                'rw_lock0'
              966  LOAD_CONST               1
              968  LOAD_GLOBAL              wr_lock_key_slot_2
              970  BINARY_LSHIFT    
              972  INPLACE_OR       
              974  STORE_FAST               'rw_lock0'

 L. 169       976  LOAD_FAST                'rw_lock1'
              978  LOAD_CONST               1
              980  LOAD_GLOBAL              rd_lock_key_slot_4
              982  BINARY_LSHIFT    
              984  INPLACE_OR       
              986  STORE_FAST               'rw_lock1'

 L. 170       988  LOAD_FAST                'rw_lock0'
              990  LOAD_CONST               1
              992  LOAD_GLOBAL              rd_lock_key_slot_2
              994  BINARY_LSHIFT    
              996  INPLACE_OR       
              998  STORE_FAST               'rw_lock0'
           1000_0  COME_FROM           892  '892'
           1000_1  COME_FROM           524  '524'

 L. 171      1000  LOAD_FAST                'flash_encryp_type'
             1002  LOAD_CONST               1
             1004  COMPARE_OP               ==
         1006_1008  POP_JUMP_IF_FALSE  1314  'to 1314'

 L. 172      1010  LOAD_FAST                'sec_eng_key_sel'
             1012  LOAD_CONST               0
             1014  COMPARE_OP               ==
         1016_1018  POP_JUMP_IF_FALSE  1080  'to 1080'

 L. 173      1020  LOAD_FAST                'sec_eng_key'
             1022  LOAD_CONST               0
             1024  LOAD_CONST               16
             1026  BUILD_SLICE_2         2 
             1028  BINARY_SUBSCR    
             1030  LOAD_FAST                'efuse_data'
             1032  LOAD_GLOBAL              keyslot5
             1034  LOAD_GLOBAL              keyslot6
             1036  BUILD_SLICE_2         2 
             1038  STORE_SUBSCR     

 L. 174      1040  LOAD_FAST                'mask_4bytes'
             1042  LOAD_CONST               4
             1044  BINARY_MULTIPLY  
             1046  LOAD_FAST                'efuse_mask_data'
             1048  LOAD_GLOBAL              keyslot5
             1050  LOAD_GLOBAL              keyslot6
             1052  BUILD_SLICE_2         2 
             1054  STORE_SUBSCR     

 L. 175      1056  LOAD_FAST                'rw_lock1'
             1058  LOAD_CONST               1
             1060  LOAD_GLOBAL              wr_lock_key_slot_5
             1062  BINARY_LSHIFT    
             1064  INPLACE_OR       
             1066  STORE_FAST               'rw_lock1'

 L. 176      1068  LOAD_FAST                'rw_lock1'
             1070  LOAD_CONST               1
             1072  LOAD_GLOBAL              rd_lock_key_slot_5
             1074  BINARY_LSHIFT    
             1076  INPLACE_OR       
             1078  STORE_FAST               'rw_lock1'
           1080_0  COME_FROM          1016  '1016'

 L. 177      1080  LOAD_FAST                'sec_eng_key_sel'
             1082  LOAD_CONST               1
             1084  COMPARE_OP               ==
         1086_1088  POP_JUMP_IF_FALSE  1150  'to 1150'

 L. 178      1090  LOAD_FAST                'sec_eng_key'
             1092  LOAD_CONST               0
             1094  LOAD_CONST               16
             1096  BUILD_SLICE_2         2 
             1098  BINARY_SUBSCR    
             1100  LOAD_FAST                'efuse_data'
             1102  LOAD_GLOBAL              keyslot4
             1104  LOAD_GLOBAL              keyslot5
             1106  BUILD_SLICE_2         2 
             1108  STORE_SUBSCR     

 L. 179      1110  LOAD_FAST                'mask_4bytes'
             1112  LOAD_CONST               4
             1114  BINARY_MULTIPLY  
             1116  LOAD_FAST                'efuse_mask_data'
             1118  LOAD_GLOBAL              keyslot4
             1120  LOAD_GLOBAL              keyslot5
             1122  BUILD_SLICE_2         2 
             1124  STORE_SUBSCR     

 L. 180      1126  LOAD_FAST                'rw_lock1'
             1128  LOAD_CONST               1
             1130  LOAD_GLOBAL              wr_lock_key_slot_4
             1132  BINARY_LSHIFT    
             1134  INPLACE_OR       
             1136  STORE_FAST               'rw_lock1'

 L. 181      1138  LOAD_FAST                'rw_lock1'
             1140  LOAD_CONST               1
             1142  LOAD_GLOBAL              rd_lock_key_slot_4
             1144  BINARY_LSHIFT    
             1146  INPLACE_OR       
             1148  STORE_FAST               'rw_lock1'
           1150_0  COME_FROM          1086  '1086'

 L. 182      1150  LOAD_FAST                'sec_eng_key_sel'
             1152  LOAD_CONST               2
             1154  COMPARE_OP               ==
         1156_1158  POP_JUMP_IF_FALSE  1232  'to 1232'

 L. 183      1160  LOAD_FAST                'flash_key'
             1162  LOAD_CONST               None
             1164  COMPARE_OP               is-not
         1166_1168  POP_JUMP_IF_FALSE  1172  'to 1172'

 L. 185      1170  JUMP_FORWARD       1232  'to 1232'
           1172_0  COME_FROM          1166  '1166'

 L. 187      1172  LOAD_FAST                'sec_eng_key'
             1174  LOAD_CONST               0
             1176  LOAD_CONST               16
             1178  BUILD_SLICE_2         2 
             1180  BINARY_SUBSCR    
             1182  LOAD_FAST                'efuse_data'
             1184  LOAD_GLOBAL              keyslot3
             1186  LOAD_GLOBAL              keyslot3_end
             1188  BUILD_SLICE_2         2 
             1190  STORE_SUBSCR     

 L. 188      1192  LOAD_FAST                'mask_4bytes'
             1194  LOAD_CONST               4
             1196  BINARY_MULTIPLY  
             1198  LOAD_FAST                'efuse_mask_data'
             1200  LOAD_GLOBAL              keyslot3
             1202  LOAD_GLOBAL              keyslot3_end
             1204  BUILD_SLICE_2         2 
             1206  STORE_SUBSCR     

 L. 189      1208  LOAD_FAST                'rw_lock0'
             1210  LOAD_CONST               1
             1212  LOAD_GLOBAL              wr_lock_key_slot_3
             1214  BINARY_LSHIFT    
             1216  INPLACE_OR       
             1218  STORE_FAST               'rw_lock0'

 L. 190      1220  LOAD_FAST                'rw_lock0'
             1222  LOAD_CONST               1
             1224  LOAD_GLOBAL              rd_lock_key_slot_3
             1226  BINARY_LSHIFT    
             1228  INPLACE_OR       
             1230  STORE_FAST               'rw_lock0'
           1232_0  COME_FROM          1170  '1170'
           1232_1  COME_FROM          1156  '1156'

 L. 191      1232  LOAD_FAST                'sec_eng_key_sel'
             1234  LOAD_CONST               3
             1236  COMPARE_OP               ==
         1238_1240  POP_JUMP_IF_FALSE  1314  'to 1314'

 L. 192      1242  LOAD_FAST                'flash_key'
             1244  LOAD_CONST               None
             1246  COMPARE_OP               is-not
         1248_1250  POP_JUMP_IF_FALSE  1254  'to 1254'

 L. 194      1252  JUMP_FORWARD       1314  'to 1314'
           1254_0  COME_FROM          1248  '1248'

 L. 196      1254  LOAD_FAST                'sec_eng_key'
             1256  LOAD_CONST               0
             1258  LOAD_CONST               16
             1260  BUILD_SLICE_2         2 
             1262  BINARY_SUBSCR    
             1264  LOAD_FAST                'efuse_data'
             1266  LOAD_GLOBAL              keyslot2
             1268  LOAD_GLOBAL              keyslot3
             1270  BUILD_SLICE_2         2 
             1272  STORE_SUBSCR     

 L. 197      1274  LOAD_FAST                'mask_4bytes'
             1276  LOAD_CONST               4
             1278  BINARY_MULTIPLY  
             1280  LOAD_FAST                'efuse_mask_data'
             1282  LOAD_GLOBAL              keyslot2
             1284  LOAD_GLOBAL              keyslot3
             1286  BUILD_SLICE_2         2 
             1288  STORE_SUBSCR     

 L. 198      1290  LOAD_FAST                'rw_lock0'
             1292  LOAD_CONST               1
             1294  LOAD_GLOBAL              wr_lock_key_slot_2
             1296  BINARY_LSHIFT    
             1298  INPLACE_OR       
             1300  STORE_FAST               'rw_lock0'

 L. 199      1302  LOAD_FAST                'rw_lock0'
             1304  LOAD_CONST               1
             1306  LOAD_GLOBAL              rd_lock_key_slot_2
             1308  BINARY_LSHIFT    
             1310  INPLACE_OR       
             1312  STORE_FAST               'rw_lock0'
           1314_0  COME_FROM          1252  '1252'
           1314_1  COME_FROM          1238  '1238'
           1314_2  COME_FROM          1006  '1006'

 L. 200      1314  LOAD_FAST                'flash_encryp_type'
             1316  LOAD_CONST               2
             1318  COMPARE_OP               ==
         1320_1322  POP_JUMP_IF_TRUE   1364  'to 1364'

 L. 201      1324  LOAD_FAST                'flash_encryp_type'
             1326  LOAD_CONST               3
             1328  COMPARE_OP               ==
         1330_1332  POP_JUMP_IF_TRUE   1364  'to 1364'

 L. 202      1334  LOAD_FAST                'flash_encryp_type'
             1336  LOAD_CONST               4
             1338  COMPARE_OP               ==
         1340_1342  POP_JUMP_IF_TRUE   1364  'to 1364'

 L. 203      1344  LOAD_FAST                'flash_encryp_type'
             1346  LOAD_CONST               5
             1348  COMPARE_OP               ==
         1350_1352  POP_JUMP_IF_TRUE   1364  'to 1364'

 L. 204      1354  LOAD_FAST                'flash_encryp_type'
             1356  LOAD_CONST               6
             1358  COMPARE_OP               ==
         1360_1362  POP_JUMP_IF_FALSE  1848  'to 1848'
           1364_0  COME_FROM          1350  '1350'
           1364_1  COME_FROM          1340  '1340'
           1364_2  COME_FROM          1330  '1330'
           1364_3  COME_FROM          1320  '1320'

 L. 205      1364  LOAD_FAST                'sec_eng_key_sel'
             1366  LOAD_CONST               0
             1368  COMPARE_OP               ==
         1370_1372  POP_JUMP_IF_FALSE  1494  'to 1494'

 L. 206      1374  LOAD_FAST                'sec_eng_key'
             1376  LOAD_CONST               16
             1378  LOAD_CONST               32
             1380  BUILD_SLICE_2         2 
             1382  BINARY_SUBSCR    
             1384  LOAD_FAST                'efuse_data'
             1386  LOAD_GLOBAL              keyslot6
             1388  LOAD_GLOBAL              keyslot7
             1390  BUILD_SLICE_2         2 
             1392  STORE_SUBSCR     

 L. 207      1394  LOAD_FAST                'sec_eng_key'
             1396  LOAD_CONST               0
             1398  LOAD_CONST               16
             1400  BUILD_SLICE_2         2 
             1402  BINARY_SUBSCR    
             1404  LOAD_FAST                'efuse_data'
             1406  LOAD_GLOBAL              keyslot10
             1408  LOAD_GLOBAL              keyslot10_end
             1410  BUILD_SLICE_2         2 
             1412  STORE_SUBSCR     

 L. 208      1414  LOAD_FAST                'mask_4bytes'
             1416  LOAD_CONST               4
             1418  BINARY_MULTIPLY  
             1420  LOAD_FAST                'efuse_mask_data'
             1422  LOAD_GLOBAL              keyslot6
             1424  LOAD_GLOBAL              keyslot7
             1426  BUILD_SLICE_2         2 
             1428  STORE_SUBSCR     

 L. 209      1430  LOAD_FAST                'mask_4bytes'
             1432  LOAD_CONST               4
             1434  BINARY_MULTIPLY  
             1436  LOAD_FAST                'efuse_mask_data'
             1438  LOAD_GLOBAL              keyslot10
             1440  LOAD_GLOBAL              keyslot10_end
             1442  BUILD_SLICE_2         2 
             1444  STORE_SUBSCR     

 L. 210      1446  LOAD_FAST                'rw_lock1'
             1448  LOAD_CONST               1
             1450  LOAD_GLOBAL              wr_lock_key_slot_6
             1452  BINARY_LSHIFT    
             1454  INPLACE_OR       
             1456  STORE_FAST               'rw_lock1'

 L. 211      1458  LOAD_FAST                'rw_lock1'
             1460  LOAD_CONST               1
             1462  LOAD_GLOBAL              wr_lock_key_slot_10
             1464  BINARY_LSHIFT    
             1466  INPLACE_OR       
             1468  STORE_FAST               'rw_lock1'

 L. 212      1470  LOAD_FAST                'rw_lock1'
             1472  LOAD_CONST               1
             1474  LOAD_GLOBAL              rd_lock_key_slot_6
             1476  BINARY_LSHIFT    
             1478  INPLACE_OR       
             1480  STORE_FAST               'rw_lock1'

 L. 213      1482  LOAD_FAST                'rw_lock1'
             1484  LOAD_CONST               1
             1486  LOAD_GLOBAL              rd_lock_key_slot_10
             1488  BINARY_LSHIFT    
             1490  INPLACE_OR       
             1492  STORE_FAST               'rw_lock1'
           1494_0  COME_FROM          1370  '1370'

 L. 214      1494  LOAD_FAST                'sec_eng_key_sel'
             1496  LOAD_CONST               1
             1498  COMPARE_OP               ==
         1500_1502  POP_JUMP_IF_FALSE  1624  'to 1624'

 L. 215      1504  LOAD_FAST                'sec_eng_key'
             1506  LOAD_CONST               16
             1508  LOAD_CONST               32
             1510  BUILD_SLICE_2         2 
             1512  BINARY_SUBSCR    
             1514  LOAD_FAST                'efuse_data'
             1516  LOAD_GLOBAL              keyslot10
             1518  LOAD_GLOBAL              keyslot10_end
             1520  BUILD_SLICE_2         2 
             1522  STORE_SUBSCR     

 L. 216      1524  LOAD_FAST                'sec_eng_key'
             1526  LOAD_CONST               0
             1528  LOAD_CONST               16
             1530  BUILD_SLICE_2         2 
             1532  BINARY_SUBSCR    
             1534  LOAD_FAST                'efuse_data'
             1536  LOAD_GLOBAL              keyslot6
             1538  LOAD_GLOBAL              keyslot7
             1540  BUILD_SLICE_2         2 
             1542  STORE_SUBSCR     

 L. 217      1544  LOAD_FAST                'mask_4bytes'
             1546  LOAD_CONST               4
             1548  BINARY_MULTIPLY  
             1550  LOAD_FAST                'efuse_mask_data'
             1552  LOAD_GLOBAL              keyslot6
             1554  LOAD_GLOBAL              keyslot7
             1556  BUILD_SLICE_2         2 
             1558  STORE_SUBSCR     

 L. 218      1560  LOAD_FAST                'mask_4bytes'
             1562  LOAD_CONST               4
             1564  BINARY_MULTIPLY  
             1566  LOAD_FAST                'efuse_mask_data'
             1568  LOAD_GLOBAL              keyslot10
             1570  LOAD_GLOBAL              keyslot10_end
             1572  BUILD_SLICE_2         2 
             1574  STORE_SUBSCR     

 L. 219      1576  LOAD_FAST                'rw_lock1'
             1578  LOAD_CONST               1
             1580  LOAD_GLOBAL              wr_lock_key_slot_6
             1582  BINARY_LSHIFT    
             1584  INPLACE_OR       
             1586  STORE_FAST               'rw_lock1'

 L. 220      1588  LOAD_FAST                'rw_lock1'
             1590  LOAD_CONST               1
             1592  LOAD_GLOBAL              wr_lock_key_slot_10
             1594  BINARY_LSHIFT    
             1596  INPLACE_OR       
             1598  STORE_FAST               'rw_lock1'

 L. 221      1600  LOAD_FAST                'rw_lock1'
             1602  LOAD_CONST               1
             1604  LOAD_GLOBAL              rd_lock_key_slot_6
             1606  BINARY_LSHIFT    
             1608  INPLACE_OR       
             1610  STORE_FAST               'rw_lock1'

 L. 222      1612  LOAD_FAST                'rw_lock1'
             1614  LOAD_CONST               1
             1616  LOAD_GLOBAL              rd_lock_key_slot_10
             1618  BINARY_LSHIFT    
             1620  INPLACE_OR       
             1622  STORE_FAST               'rw_lock1'
           1624_0  COME_FROM          1500  '1500'

 L. 223      1624  LOAD_FAST                'sec_eng_key_sel'
             1626  LOAD_CONST               2
             1628  COMPARE_OP               ==
         1630_1632  POP_JUMP_IF_FALSE  1750  'to 1750'

 L. 224      1634  LOAD_FAST                'flash_key'
             1636  LOAD_CONST               None
             1638  COMPARE_OP               is-not
         1640_1642  POP_JUMP_IF_FALSE  1646  'to 1646'

 L. 226      1644  JUMP_FORWARD       1750  'to 1750'
           1646_0  COME_FROM          1640  '1640'

 L. 228      1646  LOAD_FAST                'sec_eng_key'
             1648  LOAD_CONST               16
             1650  LOAD_CONST               32
             1652  BUILD_SLICE_2         2 
             1654  BINARY_SUBSCR    
             1656  LOAD_FAST                'efuse_data'
             1658  LOAD_GLOBAL              keyslot2
             1660  LOAD_GLOBAL              keyslot3
             1662  BUILD_SLICE_2         2 
             1664  STORE_SUBSCR     

 L. 229      1666  LOAD_FAST                'sec_eng_key'
             1668  LOAD_CONST               0
             1670  LOAD_CONST               16
             1672  BUILD_SLICE_2         2 
             1674  BINARY_SUBSCR    
             1676  LOAD_FAST                'efuse_data'
             1678  LOAD_GLOBAL              keyslot3
             1680  LOAD_GLOBAL              keyslot3_end
             1682  BUILD_SLICE_2         2 
             1684  STORE_SUBSCR     

 L. 230      1686  LOAD_FAST                'mask_4bytes'
             1688  LOAD_CONST               8
             1690  BINARY_MULTIPLY  
             1692  LOAD_FAST                'efuse_mask_data'
             1694  LOAD_GLOBAL              keyslot2
             1696  LOAD_GLOBAL              keyslot3_end
             1698  BUILD_SLICE_2         2 
             1700  STORE_SUBSCR     

 L. 231      1702  LOAD_FAST                'rw_lock0'
             1704  LOAD_CONST               1
             1706  LOAD_GLOBAL              wr_lock_key_slot_2
             1708  BINARY_LSHIFT    
             1710  INPLACE_OR       
             1712  STORE_FAST               'rw_lock0'

 L. 232      1714  LOAD_FAST                'rw_lock0'
             1716  LOAD_CONST               1
             1718  LOAD_GLOBAL              rd_lock_key_slot_2
             1720  BINARY_LSHIFT    
             1722  INPLACE_OR       
             1724  STORE_FAST               'rw_lock0'

 L. 233      1726  LOAD_FAST                'rw_lock0'
             1728  LOAD_CONST               1
             1730  LOAD_GLOBAL              wr_lock_key_slot_3
             1732  BINARY_LSHIFT    
             1734  INPLACE_OR       
             1736  STORE_FAST               'rw_lock0'

 L. 234      1738  LOAD_FAST                'rw_lock0'
             1740  LOAD_CONST               1
             1742  LOAD_GLOBAL              rd_lock_key_slot_3
             1744  BINARY_LSHIFT    
             1746  INPLACE_OR       
             1748  STORE_FAST               'rw_lock0'
           1750_0  COME_FROM          1644  '1644'
           1750_1  COME_FROM          1630  '1630'

 L. 235      1750  LOAD_FAST                'sec_eng_key_sel'
             1752  LOAD_CONST               3
             1754  COMPARE_OP               ==
         1756_1758  POP_JUMP_IF_FALSE  1848  'to 1848'

 L. 236      1760  LOAD_FAST                'flash_key'
             1762  LOAD_CONST               None
             1764  COMPARE_OP               is-not
         1766_1768  POP_JUMP_IF_FALSE  1772  'to 1772'

 L. 238      1770  JUMP_FORWARD       1848  'to 1848'
           1772_0  COME_FROM          1766  '1766'

 L. 240      1772  LOAD_FAST                'sec_eng_key'
             1774  LOAD_FAST                'efuse_data'
             1776  LOAD_GLOBAL              keyslot2
             1778  LOAD_GLOBAL              keyslot3_end
             1780  BUILD_SLICE_2         2 
             1782  STORE_SUBSCR     

 L. 241      1784  LOAD_FAST                'mask_4bytes'
             1786  LOAD_CONST               8
             1788  BINARY_MULTIPLY  
             1790  LOAD_FAST                'efuse_mask_data'
             1792  LOAD_GLOBAL              keyslot2
             1794  LOAD_GLOBAL              keyslot3_end
             1796  BUILD_SLICE_2         2 
             1798  STORE_SUBSCR     

 L. 242      1800  LOAD_FAST                'rw_lock0'
             1802  LOAD_CONST               1
             1804  LOAD_GLOBAL              wr_lock_key_slot_2
             1806  BINARY_LSHIFT    
             1808  INPLACE_OR       
             1810  STORE_FAST               'rw_lock0'

 L. 243      1812  LOAD_FAST                'rw_lock0'
             1814  LOAD_CONST               1
             1816  LOAD_GLOBAL              rd_lock_key_slot_2
             1818  BINARY_LSHIFT    
             1820  INPLACE_OR       
             1822  STORE_FAST               'rw_lock0'

 L. 244      1824  LOAD_FAST                'rw_lock0'
             1826  LOAD_CONST               1
             1828  LOAD_GLOBAL              wr_lock_key_slot_3
             1830  BINARY_LSHIFT    
             1832  INPLACE_OR       
             1834  STORE_FAST               'rw_lock0'

 L. 245      1836  LOAD_FAST                'rw_lock0'
             1838  LOAD_CONST               1
             1840  LOAD_GLOBAL              rd_lock_key_slot_3
             1842  BINARY_LSHIFT    
             1844  INPLACE_OR       
             1846  STORE_FAST               'rw_lock0'
           1848_0  COME_FROM          1770  '1770'
           1848_1  COME_FROM          1756  '1756'
           1848_2  COME_FROM          1360  '1360'
           1848_3  COME_FROM           514  '514'

 L. 247      1848  LOAD_GLOBAL              bytearray_data_merge
             1850  LOAD_FAST                'efuse_data'
             1852  LOAD_CONST               124
             1854  LOAD_CONST               128
             1856  BUILD_SLICE_2         2 
             1858  BINARY_SUBSCR    

 L. 248      1860  LOAD_GLOBAL              bflb_utils
             1862  LOAD_METHOD              int_to_4bytearray_l
             1864  LOAD_FAST                'rw_lock0'
             1866  CALL_METHOD_1         1  '1 positional argument'
             1868  LOAD_CONST               4
             1870  CALL_FUNCTION_3       3  '3 positional arguments'
             1872  LOAD_FAST                'efuse_data'
             1874  LOAD_CONST               124
             1876  LOAD_CONST               128
             1878  BUILD_SLICE_2         2 
             1880  STORE_SUBSCR     

 L. 249      1882  LOAD_GLOBAL              bytearray_data_merge
             1884  LOAD_FAST                'efuse_mask_data'
             1886  LOAD_CONST               124
             1888  LOAD_CONST               128
             1890  BUILD_SLICE_2         2 
             1892  BINARY_SUBSCR    

 L. 250      1894  LOAD_GLOBAL              bflb_utils
             1896  LOAD_METHOD              int_to_4bytearray_l
             1898  LOAD_FAST                'rw_lock0'
             1900  CALL_METHOD_1         1  '1 positional argument'
             1902  LOAD_CONST               4
             1904  CALL_FUNCTION_3       3  '3 positional arguments'
             1906  LOAD_FAST                'efuse_mask_data'
             1908  LOAD_CONST               124
             1910  LOAD_CONST               128
             1912  BUILD_SLICE_2         2 
             1914  STORE_SUBSCR     

 L. 251      1916  LOAD_GLOBAL              bytearray_data_merge
             1918  LOAD_FAST                'efuse_data'
             1920  LOAD_CONST               252
             1922  LOAD_CONST               256
             1924  BUILD_SLICE_2         2 
             1926  BINARY_SUBSCR    

 L. 252      1928  LOAD_GLOBAL              bflb_utils
             1930  LOAD_METHOD              int_to_4bytearray_l
             1932  LOAD_FAST                'rw_lock1'
             1934  CALL_METHOD_1         1  '1 positional argument'
             1936  LOAD_CONST               4
             1938  CALL_FUNCTION_3       3  '3 positional arguments'
             1940  LOAD_FAST                'efuse_data'
             1942  LOAD_CONST               252
             1944  LOAD_CONST               256
             1946  BUILD_SLICE_2         2 
             1948  STORE_SUBSCR     

 L. 253      1950  LOAD_GLOBAL              bytearray_data_merge
             1952  LOAD_FAST                'efuse_mask_data'
             1954  LOAD_CONST               252
             1956  LOAD_CONST               256
             1958  BUILD_SLICE_2         2 
             1960  BINARY_SUBSCR    

 L. 254      1962  LOAD_GLOBAL              bflb_utils
             1964  LOAD_METHOD              int_to_4bytearray_l
             1966  LOAD_FAST                'rw_lock1'
             1968  CALL_METHOD_1         1  '1 positional argument'
             1970  LOAD_CONST               4
             1972  CALL_FUNCTION_3       3  '3 positional arguments'
             1974  LOAD_FAST                'efuse_mask_data'
             1976  LOAD_CONST               252
             1978  LOAD_CONST               256
             1980  BUILD_SLICE_2         2 
             1982  STORE_SUBSCR     

 L. 256      1984  LOAD_FAST                'security'
             1986  LOAD_CONST               True
             1988  COMPARE_OP               is
         1990_1992  POP_JUMP_IF_FALSE  2080  'to 2080'

 L. 257      1994  LOAD_GLOBAL              open
             1996  LOAD_GLOBAL              os
             1998  LOAD_ATTR                path
             2000  LOAD_METHOD              join
             2002  LOAD_FAST                'cfg'
             2004  LOAD_STR                 'efusedata_raw.bin'
             2006  CALL_METHOD_2         2  '2 positional arguments'
             2008  LOAD_STR                 'wb+'
             2010  CALL_FUNCTION_2       2  '2 positional arguments'
             2012  STORE_FAST               'fp'

 L. 258      2014  LOAD_FAST                'fp'
             2016  LOAD_METHOD              write
             2018  LOAD_FAST                'efuse_data'
             2020  CALL_METHOD_1         1  '1 positional argument'
             2022  POP_TOP          

 L. 259      2024  LOAD_FAST                'fp'
             2026  LOAD_METHOD              close
             2028  CALL_METHOD_0         0  '0 positional arguments'
             2030  POP_TOP          

 L. 260      2032  LOAD_GLOBAL              bflb_utils
             2034  LOAD_METHOD              printf
             2036  LOAD_STR                 'Encrypt efuse data'
             2038  CALL_METHOD_1         1  '1 positional argument'
             2040  POP_TOP          

 L. 261      2042  LOAD_GLOBAL              bflb_utils
             2044  LOAD_METHOD              get_security_key
             2046  CALL_METHOD_0         0  '0 positional arguments'
             2048  UNPACK_SEQUENCE_2     2 
             2050  STORE_FAST               'security_key'
             2052  STORE_FAST               'security_iv'

 L. 262      2054  LOAD_GLOBAL              img_create_encrypt_data
             2056  LOAD_FAST                'efuse_data'
             2058  LOAD_FAST                'security_key'
             2060  LOAD_FAST                'security_iv'
             2062  LOAD_CONST               0
             2064  CALL_FUNCTION_4       4  '4 positional arguments'
             2066  STORE_FAST               'efuse_data'

 L. 263      2068  LOAD_GLOBAL              bytearray
             2070  LOAD_CONST               4096
             2072  CALL_FUNCTION_1       1  '1 positional argument'
             2074  LOAD_FAST                'efuse_data'
             2076  BINARY_ADD       
             2078  STORE_FAST               'efuse_data'
           2080_0  COME_FROM          1990  '1990'

 L. 264      2080  LOAD_GLOBAL              open
             2082  LOAD_GLOBAL              os
             2084  LOAD_ATTR                path
             2086  LOAD_METHOD              join
             2088  LOAD_FAST                'cfg'
             2090  LOAD_STR                 'efusedata.bin'
             2092  CALL_METHOD_2         2  '2 positional arguments'
             2094  LOAD_STR                 'wb+'
             2096  CALL_FUNCTION_2       2  '2 positional arguments'
             2098  STORE_FAST               'fp'

 L. 265      2100  LOAD_FAST                'fp'
             2102  LOAD_METHOD              write
             2104  LOAD_FAST                'efuse_data'
             2106  CALL_METHOD_1         1  '1 positional argument'
             2108  POP_TOP          

 L. 266      2110  LOAD_FAST                'fp'
             2112  LOAD_METHOD              close
             2114  CALL_METHOD_0         0  '0 positional arguments'
             2116  POP_TOP          

 L. 267      2118  LOAD_GLOBAL              open
             2120  LOAD_GLOBAL              os
             2122  LOAD_ATTR                path
             2124  LOAD_METHOD              join
             2126  LOAD_FAST                'cfg'
             2128  LOAD_STR                 'efusedata_mask.bin'
             2130  CALL_METHOD_2         2  '2 positional arguments'
             2132  LOAD_STR                 'wb+'
             2134  CALL_FUNCTION_2       2  '2 positional arguments'
             2136  STORE_FAST               'fp'

 L. 268      2138  LOAD_FAST                'fp'
             2140  LOAD_METHOD              write
             2142  LOAD_FAST                'efuse_mask_data'
             2144  CALL_METHOD_1         1  '1 positional argument'
             2146  POP_TOP          

 L. 269      2148  LOAD_FAST                'fp'
             2150  LOAD_METHOD              close
             2152  CALL_METHOD_0         0  '0 positional arguments'
             2154  POP_TOP          

Parse error at or near `CALL_METHOD_0' instruction at offset 2152


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
    bootcfg_start = 128
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
                pk_sig_len = len(pk_data + pk_data + signature + signature)
                boot_data[352:352 + pk_sig_len] = pk_data + pk_data + signature + signature
                boot_data[352 + pk_sig_len:352 + pk_sig_len + len(aesiv_data)] = aesiv_data
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
    crcarray = bflb_utils.get_crc32_bytearray(image_data[clockcfg_start + 4:clockcfg_start + 24])
    image_data[clockcfg_start + 24:clockcfg_start + 24 + 4] = crcarray
    bflb_utils.printf('Clock config crc: ', binascii.hexlify(crcarray))
    return image_data


def firmware_post_proc_update_bootheader_crc(image_data):
    crcarray = bflb_utils.get_crc32_bytearray(image_data[0:348])
    image_data[348:352] = crcarray
    bflb_utils.printf('Bootheader config crc: ', binascii.hexlify(crcarray))
    return image_data


def firmware_post_proc_get_hash_ignore(image_data):
    bootcfg_start = 128
    return image_data[bootcfg_start + 2] >> 1 & 1


def firmware_post_proc_enable_hash_cfg(image_data):
    bootcfg_start = 128
    image_data[bootcfg_start + 2] &= -3
    return image_data


def firmware_post_proc_get_image_offset(image_data):
    cpucfg_start = 132
    return image_data[cpucfg_start + 0] + (image_data[cpucfg_start + 1] << 8) + (image_data[cpucfg_start + 2] << 16) + (image_data[cpucfg_start + 3] << 24)


def firmware_post_proc_update_hash(image_data, force_update, args, hash):
    image_offset = firmware_post_proc_get_image_offset(image_data)
    bflb_utils.printf('Image Offset:' + hex(image_offset))
    bootcfg_start = 128
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