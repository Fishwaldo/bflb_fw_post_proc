# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
# [GCC 9.4.0]
# Embedded file name: libs/bl60x/efuse_create_do.py
import os, sys
from libs import bflb_utils
from libs import bflb_efuse_boothd_create
from libs.bflb_utils import verify_hex_num, str_endian_switch
ef_sf_aes_mode_list = [
 'None', 'AES128', 'AES192', 'AES256']

def create_key_data_do--- This code section failed: ---

 L.  14         0  LOAD_STR                 ''
                2  STORE_FAST               'tips'

 L.  15         4  LOAD_GLOBAL              bflb_utils
                6  LOAD_METHOD              printf
                8  LOAD_STR                 'Create_key_data'
               10  CALL_METHOD_1         1  '1 positional argument'
               12  POP_TOP          

 L.  16        14  LOAD_GLOBAL              open
               16  LOAD_FAST                'cfg_file'
               18  LOAD_STR                 'w+'
               20  CALL_FUNCTION_2       2  '2 positional arguments'
               22  STORE_FAST               'fp'

 L.  17        24  LOAD_FAST                'fp'
               26  LOAD_METHOD              write
               28  LOAD_STR                 '[EFUSE_CFG]\n'
               30  CALL_METHOD_1         1  '1 positional argument'
               32  POP_TOP          

 L.  18        34  LOAD_GLOBAL              ef_sf_aes_mode_list
               36  LOAD_METHOD              index
               38  LOAD_FAST                'values'
               40  LOAD_STR                 'ef_sf_aes_mode'
               42  BINARY_SUBSCR    
               44  CALL_METHOD_1         1  '1 positional argument'
               46  STORE_FAST               'aes_mode'

 L.  19        48  LOAD_FAST                'tips'
               50  LOAD_STR                 'AES Mode:'
               52  LOAD_FAST                'values'
               54  LOAD_STR                 'ef_sf_aes_mode'
               56  BINARY_SUBSCR    
               58  BINARY_ADD       
               60  LOAD_STR                 '\r\n'
               62  BINARY_ADD       
               64  INPLACE_ADD      
               66  STORE_FAST               'tips'

 L.  20        68  LOAD_GLOBAL              bflb_utils
               70  LOAD_METHOD              printf
               72  LOAD_GLOBAL              ef_sf_aes_mode_list
               74  LOAD_FAST                'aes_mode'
               76  BINARY_SUBSCR    
               78  CALL_METHOD_1         1  '1 positional argument'
               80  POP_TOP          

 L.  22        82  LOAD_GLOBAL              len
               84  LOAD_FAST                'values'
               86  LOAD_STR                 'cpu0_pk_simple'
               88  BINARY_SUBSCR    
               90  CALL_FUNCTION_1       1  '1 positional argument'
               92  LOAD_CONST               64
               94  COMPARE_OP               ==
            96_98  POP_JUMP_IF_FALSE  1696  'to 1696'

 L.  23       100  LOAD_GLOBAL              len
              102  LOAD_FAST                'values'
              104  LOAD_STR                 'cpu1_pk_simple'
              106  BINARY_SUBSCR    
              108  CALL_FUNCTION_1       1  '1 positional argument'
              110  LOAD_CONST               64
              112  COMPARE_OP               ==
          114_116  POP_JUMP_IF_FALSE  1696  'to 1696'

 L.  24       118  LOAD_GLOBAL              verify_hex_num
              120  LOAD_FAST                'values'
              122  LOAD_STR                 'cpu0_pk_simple'
              124  BINARY_SUBSCR    
              126  CALL_FUNCTION_1       1  '1 positional argument'
              128  LOAD_CONST               True
              130  COMPARE_OP               is
          132_134  POP_JUMP_IF_FALSE  1696  'to 1696'

 L.  25       136  LOAD_GLOBAL              verify_hex_num
              138  LOAD_FAST                'values'
              140  LOAD_STR                 'cpu1_pk_simple'
              142  BINARY_SUBSCR    
              144  CALL_FUNCTION_1       1  '1 positional argument'
              146  LOAD_CONST               True
              148  COMPARE_OP               is
          150_152  POP_JUMP_IF_FALSE  1696  'to 1696'

 L.  27       154  LOAD_FAST                'fp'
              156  LOAD_METHOD              write
              158  LOAD_STR                 'ef_key_slot_0_w0 = 0x'
              160  LOAD_GLOBAL              str_endian_switch
              162  LOAD_FAST                'values'
              164  LOAD_STR                 'cpu0_pk_simple'
              166  BINARY_SUBSCR    
              168  LOAD_CONST               0
              170  LOAD_CONST               8
              172  BUILD_SLICE_2         2 
              174  BINARY_SUBSCR    
              176  CALL_FUNCTION_1       1  '1 positional argument'
              178  BINARY_ADD       
              180  LOAD_STR                 '\n'
              182  BINARY_ADD       
              184  CALL_METHOD_1         1  '1 positional argument'
              186  POP_TOP          

 L.  28       188  LOAD_FAST                'fp'
              190  LOAD_METHOD              write
              192  LOAD_STR                 'ef_key_slot_0_w1 = 0x'
              194  LOAD_GLOBAL              str_endian_switch
              196  LOAD_FAST                'values'
              198  LOAD_STR                 'cpu0_pk_simple'
              200  BINARY_SUBSCR    
              202  LOAD_CONST               8
              204  LOAD_CONST               16
              206  BUILD_SLICE_2         2 
              208  BINARY_SUBSCR    
              210  CALL_FUNCTION_1       1  '1 positional argument'
              212  BINARY_ADD       

 L.  29       214  LOAD_STR                 '\n'
              216  BINARY_ADD       
              218  CALL_METHOD_1         1  '1 positional argument'
              220  POP_TOP          

 L.  30       222  LOAD_FAST                'fp'
              224  LOAD_METHOD              write
              226  LOAD_STR                 'ef_key_slot_0_w2 = 0x'
              228  LOAD_GLOBAL              str_endian_switch
              230  LOAD_FAST                'values'
              232  LOAD_STR                 'cpu0_pk_simple'
              234  BINARY_SUBSCR    
              236  LOAD_CONST               16
              238  LOAD_CONST               24
              240  BUILD_SLICE_2         2 
              242  BINARY_SUBSCR    
              244  CALL_FUNCTION_1       1  '1 positional argument'
              246  BINARY_ADD       

 L.  31       248  LOAD_STR                 '\n'
              250  BINARY_ADD       
              252  CALL_METHOD_1         1  '1 positional argument'
              254  POP_TOP          

 L.  32       256  LOAD_FAST                'fp'
              258  LOAD_METHOD              write
              260  LOAD_STR                 'ef_key_slot_0_w3 = 0x'
              262  LOAD_GLOBAL              str_endian_switch
              264  LOAD_FAST                'values'
              266  LOAD_STR                 'cpu0_pk_simple'
              268  BINARY_SUBSCR    
              270  LOAD_CONST               24
              272  LOAD_CONST               32
              274  BUILD_SLICE_2         2 
              276  BINARY_SUBSCR    
              278  CALL_FUNCTION_1       1  '1 positional argument'
              280  BINARY_ADD       

 L.  33       282  LOAD_STR                 '\n'
              284  BINARY_ADD       
              286  CALL_METHOD_1         1  '1 positional argument'
              288  POP_TOP          

 L.  34       290  LOAD_FAST                'fp'
              292  LOAD_METHOD              write
              294  LOAD_STR                 'ef_key_slot_1_w0 = 0x'
              296  LOAD_GLOBAL              str_endian_switch
              298  LOAD_FAST                'values'
              300  LOAD_STR                 'cpu0_pk_simple'
              302  BINARY_SUBSCR    
              304  LOAD_CONST               32
              306  LOAD_CONST               40
              308  BUILD_SLICE_2         2 
              310  BINARY_SUBSCR    
              312  CALL_FUNCTION_1       1  '1 positional argument'
              314  BINARY_ADD       

 L.  35       316  LOAD_STR                 '\n'
              318  BINARY_ADD       
              320  CALL_METHOD_1         1  '1 positional argument'
              322  POP_TOP          

 L.  36       324  LOAD_FAST                'fp'
              326  LOAD_METHOD              write
              328  LOAD_STR                 'ef_key_slot_1_w1 = 0x'
              330  LOAD_GLOBAL              str_endian_switch
              332  LOAD_FAST                'values'
              334  LOAD_STR                 'cpu0_pk_simple'
              336  BINARY_SUBSCR    
              338  LOAD_CONST               40
              340  LOAD_CONST               48
              342  BUILD_SLICE_2         2 
              344  BINARY_SUBSCR    
              346  CALL_FUNCTION_1       1  '1 positional argument'
              348  BINARY_ADD       

 L.  37       350  LOAD_STR                 '\n'
              352  BINARY_ADD       
              354  CALL_METHOD_1         1  '1 positional argument'
              356  POP_TOP          

 L.  38       358  LOAD_FAST                'fp'
              360  LOAD_METHOD              write
              362  LOAD_STR                 'ef_key_slot_1_w2 = 0x'
              364  LOAD_GLOBAL              str_endian_switch
              366  LOAD_FAST                'values'
              368  LOAD_STR                 'cpu0_pk_simple'
              370  BINARY_SUBSCR    
              372  LOAD_CONST               48
              374  LOAD_CONST               56
              376  BUILD_SLICE_2         2 
              378  BINARY_SUBSCR    
              380  CALL_FUNCTION_1       1  '1 positional argument'
              382  BINARY_ADD       

 L.  39       384  LOAD_STR                 '\n'
              386  BINARY_ADD       
              388  CALL_METHOD_1         1  '1 positional argument'
              390  POP_TOP          

 L.  40       392  LOAD_FAST                'fp'
              394  LOAD_METHOD              write
              396  LOAD_STR                 'ef_key_slot_1_w3 = 0x'
              398  LOAD_GLOBAL              str_endian_switch
              400  LOAD_FAST                'values'
              402  LOAD_STR                 'cpu0_pk_simple'
              404  BINARY_SUBSCR    
              406  LOAD_CONST               56
              408  LOAD_CONST               64
              410  BUILD_SLICE_2         2 
              412  BINARY_SUBSCR    
              414  CALL_FUNCTION_1       1  '1 positional argument'
              416  BINARY_ADD       

 L.  41       418  LOAD_STR                 '\n'
              420  BINARY_ADD       
              422  CALL_METHOD_1         1  '1 positional argument'
              424  POP_TOP          

 L.  42       426  LOAD_FAST                'values'
              428  LOAD_STR                 'cpu0_pk_wp_enable'
              430  BINARY_SUBSCR    
              432  LOAD_CONST               True
              434  COMPARE_OP               is
          436_438  POP_JUMP_IF_FALSE   462  'to 462'

 L.  43       440  LOAD_FAST                'fp'
              442  LOAD_METHOD              write
              444  LOAD_STR                 'wr_lock_key_slot_0 = 1\n'
              446  CALL_METHOD_1         1  '1 positional argument'
              448  POP_TOP          

 L.  44       450  LOAD_FAST                'fp'
              452  LOAD_METHOD              write
              454  LOAD_STR                 'wr_lock_key_slot_1 = 1\n'
              456  CALL_METHOD_1         1  '1 positional argument'
              458  POP_TOP          
              460  JUMP_FORWARD        482  'to 482'
            462_0  COME_FROM           436  '436'

 L.  46       462  LOAD_FAST                'fp'
              464  LOAD_METHOD              write
              466  LOAD_STR                 'wr_lock_key_slot_0 = 0\n'
              468  CALL_METHOD_1         1  '1 positional argument'
              470  POP_TOP          

 L.  47       472  LOAD_FAST                'fp'
              474  LOAD_METHOD              write
              476  LOAD_STR                 'wr_lock_key_slot_1 = 0\n'
              478  CALL_METHOD_1         1  '1 positional argument'
              480  POP_TOP          
            482_0  COME_FROM           460  '460'

 L.  48       482  LOAD_FAST                'tips'
              484  LOAD_STR                 'CPU0 public key hash\r\n'
              486  INPLACE_ADD      
              488  STORE_FAST               'tips'

 L.  50       490  LOAD_FAST                'fp'
              492  LOAD_METHOD              write
              494  LOAD_STR                 'ef_key_slot_5_w0 = 0x'
              496  LOAD_GLOBAL              str_endian_switch
              498  LOAD_FAST                'values'
              500  LOAD_STR                 'cpu1_pk_simple'
              502  BINARY_SUBSCR    
              504  LOAD_CONST               0
              506  LOAD_CONST               8
              508  BUILD_SLICE_2         2 
              510  BINARY_SUBSCR    
              512  CALL_FUNCTION_1       1  '1 positional argument'
              514  BINARY_ADD       
              516  LOAD_STR                 '\n'
              518  BINARY_ADD       
              520  CALL_METHOD_1         1  '1 positional argument'
              522  POP_TOP          

 L.  51       524  LOAD_FAST                'fp'
              526  LOAD_METHOD              write
              528  LOAD_STR                 'ef_key_slot_5_w1 = 0x'
              530  LOAD_GLOBAL              str_endian_switch
              532  LOAD_FAST                'values'
              534  LOAD_STR                 'cpu1_pk_simple'
              536  BINARY_SUBSCR    
              538  LOAD_CONST               8
              540  LOAD_CONST               16
              542  BUILD_SLICE_2         2 
              544  BINARY_SUBSCR    
              546  CALL_FUNCTION_1       1  '1 positional argument'
              548  BINARY_ADD       

 L.  52       550  LOAD_STR                 '\n'
              552  BINARY_ADD       
              554  CALL_METHOD_1         1  '1 positional argument'
              556  POP_TOP          

 L.  53       558  LOAD_FAST                'fp'
              560  LOAD_METHOD              write
              562  LOAD_STR                 'ef_key_slot_5_w2 = 0x'
              564  LOAD_GLOBAL              str_endian_switch
              566  LOAD_FAST                'values'
              568  LOAD_STR                 'cpu1_pk_simple'
              570  BINARY_SUBSCR    
              572  LOAD_CONST               16
              574  LOAD_CONST               24
              576  BUILD_SLICE_2         2 
              578  BINARY_SUBSCR    
              580  CALL_FUNCTION_1       1  '1 positional argument'
              582  BINARY_ADD       

 L.  54       584  LOAD_STR                 '\n'
              586  BINARY_ADD       
              588  CALL_METHOD_1         1  '1 positional argument'
              590  POP_TOP          

 L.  55       592  LOAD_FAST                'fp'
              594  LOAD_METHOD              write
              596  LOAD_STR                 'ef_key_slot_5_w3 = 0x'
              598  LOAD_GLOBAL              str_endian_switch
              600  LOAD_FAST                'values'
              602  LOAD_STR                 'cpu1_pk_simple'
              604  BINARY_SUBSCR    
              606  LOAD_CONST               24
              608  LOAD_CONST               32
              610  BUILD_SLICE_2         2 
              612  BINARY_SUBSCR    
              614  CALL_FUNCTION_1       1  '1 positional argument'
              616  BINARY_ADD       

 L.  56       618  LOAD_STR                 '\n'
              620  BINARY_ADD       
              622  CALL_METHOD_1         1  '1 positional argument'
              624  POP_TOP          

 L.  57       626  LOAD_FAST                'fp'
              628  LOAD_METHOD              write
              630  LOAD_STR                 'ef_key_slot_6_w0 = 0x'
              632  LOAD_GLOBAL              str_endian_switch
              634  LOAD_FAST                'values'
              636  LOAD_STR                 'cpu1_pk_simple'
              638  BINARY_SUBSCR    
              640  LOAD_CONST               32
              642  LOAD_CONST               40
              644  BUILD_SLICE_2         2 
              646  BINARY_SUBSCR    
              648  CALL_FUNCTION_1       1  '1 positional argument'
              650  BINARY_ADD       

 L.  58       652  LOAD_STR                 '\n'
              654  BINARY_ADD       
              656  CALL_METHOD_1         1  '1 positional argument'
              658  POP_TOP          

 L.  59       660  LOAD_FAST                'fp'
              662  LOAD_METHOD              write
              664  LOAD_STR                 'ef_key_slot_6_w1 = 0x'
              666  LOAD_GLOBAL              str_endian_switch
              668  LOAD_FAST                'values'
              670  LOAD_STR                 'cpu1_pk_simple'
              672  BINARY_SUBSCR    
              674  LOAD_CONST               40
              676  LOAD_CONST               48
              678  BUILD_SLICE_2         2 
              680  BINARY_SUBSCR    
              682  CALL_FUNCTION_1       1  '1 positional argument'
              684  BINARY_ADD       

 L.  60       686  LOAD_STR                 '\n'
              688  BINARY_ADD       
              690  CALL_METHOD_1         1  '1 positional argument'
              692  POP_TOP          

 L.  61       694  LOAD_FAST                'fp'
              696  LOAD_METHOD              write
              698  LOAD_STR                 'ef_key_slot_6_w2 = 0x'
              700  LOAD_GLOBAL              str_endian_switch
              702  LOAD_FAST                'values'
              704  LOAD_STR                 'cpu1_pk_simple'
              706  BINARY_SUBSCR    
              708  LOAD_CONST               48
              710  LOAD_CONST               56
              712  BUILD_SLICE_2         2 
              714  BINARY_SUBSCR    
              716  CALL_FUNCTION_1       1  '1 positional argument'
              718  BINARY_ADD       

 L.  62       720  LOAD_STR                 '\n'
              722  BINARY_ADD       
              724  CALL_METHOD_1         1  '1 positional argument'
              726  POP_TOP          

 L.  63       728  LOAD_FAST                'fp'
              730  LOAD_METHOD              write
              732  LOAD_STR                 'ef_key_slot_6_w3 = 0x'
              734  LOAD_GLOBAL              str_endian_switch
              736  LOAD_FAST                'values'
              738  LOAD_STR                 'cpu1_pk_simple'
              740  BINARY_SUBSCR    
              742  LOAD_CONST               56
              744  LOAD_CONST               64
              746  BUILD_SLICE_2         2 
              748  BINARY_SUBSCR    
              750  CALL_FUNCTION_1       1  '1 positional argument'
              752  BINARY_ADD       

 L.  64       754  LOAD_STR                 '\n'
              756  BINARY_ADD       
              758  CALL_METHOD_1         1  '1 positional argument'
              760  POP_TOP          

 L.  65       762  LOAD_FAST                'values'
              764  LOAD_STR                 'cpu1_pk_wp_enable'
              766  BINARY_SUBSCR    
              768  LOAD_CONST               True
              770  COMPARE_OP               is
          772_774  POP_JUMP_IF_FALSE   798  'to 798'

 L.  66       776  LOAD_FAST                'fp'
              778  LOAD_METHOD              write
              780  LOAD_STR                 'wr_lock_key_slot_5 = 1\n'
              782  CALL_METHOD_1         1  '1 positional argument'
              784  POP_TOP          

 L.  67       786  LOAD_FAST                'fp'
              788  LOAD_METHOD              write
              790  LOAD_STR                 'wr_lock_key_slot_6 = 1\n'
              792  CALL_METHOD_1         1  '1 positional argument'
              794  POP_TOP          
              796  JUMP_FORWARD        818  'to 818'
            798_0  COME_FROM           772  '772'

 L.  69       798  LOAD_FAST                'fp'
              800  LOAD_METHOD              write
              802  LOAD_STR                 'wr_lock_key_slot_5 = 0\n'
              804  CALL_METHOD_1         1  '1 positional argument'
              806  POP_TOP          

 L.  70       808  LOAD_FAST                'fp'
              810  LOAD_METHOD              write
              812  LOAD_STR                 'wr_lock_key_slot_6 = 0\n'
              814  CALL_METHOD_1         1  '1 positional argument'
              816  POP_TOP          
            818_0  COME_FROM           796  '796'

 L.  71       818  LOAD_FAST                'tips'
              820  LOAD_STR                 'CPU1 public key hash\r\n'
              822  INPLACE_ADD      
              824  STORE_FAST               'tips'

 L.  73       826  LOAD_FAST                'aes_mode'
              828  LOAD_CONST               0
              830  COMPARE_OP               !=
          832_834  POP_JUMP_IF_FALSE  1610  'to 1610'

 L.  74       836  LOAD_GLOBAL              len
              838  LOAD_FAST                'values'
              840  LOAD_STR                 'cpu0_aes_key_simple'
              842  BINARY_SUBSCR    
              844  CALL_FUNCTION_1       1  '1 positional argument'
              846  LOAD_CONST               32
              848  COMPARE_OP               >=
          850_852  POP_JUMP_IF_FALSE  1594  'to 1594'

 L.  75       854  LOAD_GLOBAL              len
              856  LOAD_FAST                'values'
              858  LOAD_STR                 'cpu1_aes_key_simple'
              860  BINARY_SUBSCR    
              862  CALL_FUNCTION_1       1  '1 positional argument'
              864  LOAD_CONST               32
              866  COMPARE_OP               >=
          868_870  POP_JUMP_IF_FALSE  1594  'to 1594'

 L.  76       872  LOAD_GLOBAL              len
              874  LOAD_FAST                'values'
              876  LOAD_STR                 'common_aes_key_simple'
              878  BINARY_SUBSCR    
              880  CALL_FUNCTION_1       1  '1 positional argument'
              882  LOAD_CONST               32
              884  COMPARE_OP               >=
          886_888  POP_JUMP_IF_FALSE  1594  'to 1594'

 L.  77       890  LOAD_GLOBAL              verify_hex_num
              892  LOAD_FAST                'values'
              894  LOAD_STR                 'cpu0_aes_key_simple'
              896  BINARY_SUBSCR    
              898  CALL_FUNCTION_1       1  '1 positional argument'
              900  LOAD_CONST               True
              902  COMPARE_OP               is
          904_906  POP_JUMP_IF_FALSE  1594  'to 1594'

 L.  78       908  LOAD_GLOBAL              verify_hex_num
              910  LOAD_FAST                'values'
              912  LOAD_STR                 'cpu1_aes_key_simple'
              914  BINARY_SUBSCR    
              916  CALL_FUNCTION_1       1  '1 positional argument'
              918  LOAD_CONST               True
              920  COMPARE_OP               is
          922_924  POP_JUMP_IF_FALSE  1594  'to 1594'

 L.  79       926  LOAD_GLOBAL              verify_hex_num
              928  LOAD_FAST                'values'
              930  LOAD_STR                 'common_aes_key_simple'
              932  BINARY_SUBSCR    
              934  CALL_FUNCTION_1       1  '1 positional argument'
              936  LOAD_CONST               True
              938  COMPARE_OP               is
          940_942  POP_JUMP_IF_FALSE  1594  'to 1594'

 L.  80       944  LOAD_FAST                'fp'
              946  LOAD_METHOD              write

 L.  81       948  LOAD_STR                 'ef_key_slot_2_w0 = 0x'
              950  LOAD_GLOBAL              str_endian_switch
              952  LOAD_FAST                'values'
              954  LOAD_STR                 'cpu0_aes_key_simple'
              956  BINARY_SUBSCR    
              958  LOAD_CONST               0
              960  LOAD_CONST               8
              962  BUILD_SLICE_2         2 
              964  BINARY_SUBSCR    
              966  CALL_FUNCTION_1       1  '1 positional argument'
              968  BINARY_ADD       
              970  LOAD_STR                 '\n'
              972  BINARY_ADD       
              974  CALL_METHOD_1         1  '1 positional argument'
              976  POP_TOP          

 L.  82       978  LOAD_FAST                'fp'
              980  LOAD_METHOD              write

 L.  83       982  LOAD_STR                 'ef_key_slot_2_w1 = 0x'
              984  LOAD_GLOBAL              str_endian_switch
              986  LOAD_FAST                'values'
              988  LOAD_STR                 'cpu0_aes_key_simple'
              990  BINARY_SUBSCR    
              992  LOAD_CONST               8
              994  LOAD_CONST               16
              996  BUILD_SLICE_2         2 
              998  BINARY_SUBSCR    
             1000  CALL_FUNCTION_1       1  '1 positional argument'
             1002  BINARY_ADD       
             1004  LOAD_STR                 '\n'
             1006  BINARY_ADD       
             1008  CALL_METHOD_1         1  '1 positional argument'
             1010  POP_TOP          

 L.  84      1012  LOAD_FAST                'fp'
             1014  LOAD_METHOD              write

 L.  85      1016  LOAD_STR                 'ef_key_slot_2_w2 = 0x'
             1018  LOAD_GLOBAL              str_endian_switch
             1020  LOAD_FAST                'values'
             1022  LOAD_STR                 'cpu0_aes_key_simple'
             1024  BINARY_SUBSCR    
             1026  LOAD_CONST               16
             1028  LOAD_CONST               24
             1030  BUILD_SLICE_2         2 
             1032  BINARY_SUBSCR    
             1034  CALL_FUNCTION_1       1  '1 positional argument'
             1036  BINARY_ADD       
             1038  LOAD_STR                 '\n'
             1040  BINARY_ADD       
             1042  CALL_METHOD_1         1  '1 positional argument'
             1044  POP_TOP          

 L.  86      1046  LOAD_FAST                'fp'
             1048  LOAD_METHOD              write

 L.  87      1050  LOAD_STR                 'ef_key_slot_2_w3 = 0x'
             1052  LOAD_GLOBAL              str_endian_switch
             1054  LOAD_FAST                'values'
             1056  LOAD_STR                 'cpu0_aes_key_simple'
             1058  BINARY_SUBSCR    
             1060  LOAD_CONST               24
             1062  LOAD_CONST               32
             1064  BUILD_SLICE_2         2 
             1066  BINARY_SUBSCR    
             1068  CALL_FUNCTION_1       1  '1 positional argument'
             1070  BINARY_ADD       
             1072  LOAD_STR                 '\n'
             1074  BINARY_ADD       
             1076  CALL_METHOD_1         1  '1 positional argument'
             1078  POP_TOP          

 L.  88      1080  LOAD_FAST                'values'
             1082  LOAD_STR                 'cpu0_aes_key_wp_enable'
             1084  BINARY_SUBSCR    
             1086  LOAD_CONST               True
             1088  COMPARE_OP               is
         1090_1092  POP_JUMP_IF_FALSE  1106  'to 1106'

 L.  89      1094  LOAD_FAST                'fp'
             1096  LOAD_METHOD              write
             1098  LOAD_STR                 'wr_lock_key_slot_2 = 1\n'
             1100  CALL_METHOD_1         1  '1 positional argument'
             1102  POP_TOP          
             1104  JUMP_FORWARD       1116  'to 1116'
           1106_0  COME_FROM          1090  '1090'

 L.  91      1106  LOAD_FAST                'fp'
             1108  LOAD_METHOD              write
             1110  LOAD_STR                 'wr_lock_key_slot_2 = 0\n'
             1112  CALL_METHOD_1         1  '1 positional argument'
             1114  POP_TOP          
           1116_0  COME_FROM          1104  '1104'

 L.  92      1116  LOAD_FAST                'values'
             1118  LOAD_STR                 'cpu0_aes_key_rp_enable'
             1120  BINARY_SUBSCR    
             1122  LOAD_CONST               True
             1124  COMPARE_OP               is
         1126_1128  POP_JUMP_IF_FALSE  1142  'to 1142'

 L.  93      1130  LOAD_FAST                'fp'
             1132  LOAD_METHOD              write
             1134  LOAD_STR                 'rd_lock_key_slot_2 = 1\n'
             1136  CALL_METHOD_1         1  '1 positional argument'
             1138  POP_TOP          
             1140  JUMP_FORWARD       1152  'to 1152'
           1142_0  COME_FROM          1126  '1126'

 L.  95      1142  LOAD_FAST                'fp'
             1144  LOAD_METHOD              write
             1146  LOAD_STR                 'rd_lock_key_slot_2 = 0\n'
             1148  CALL_METHOD_1         1  '1 positional argument'
             1150  POP_TOP          
           1152_0  COME_FROM          1140  '1140'

 L.  96      1152  LOAD_FAST                'tips'
             1154  LOAD_STR                 'CPU0 AES key\r\n'
             1156  INPLACE_ADD      
             1158  STORE_FAST               'tips'

 L.  97      1160  LOAD_FAST                'fp'
             1162  LOAD_METHOD              write

 L.  98      1164  LOAD_STR                 'ef_key_slot_7_w0 = 0x'
             1166  LOAD_GLOBAL              str_endian_switch
             1168  LOAD_FAST                'values'
             1170  LOAD_STR                 'cpu1_aes_key_simple'
             1172  BINARY_SUBSCR    
             1174  LOAD_CONST               0
             1176  LOAD_CONST               8
             1178  BUILD_SLICE_2         2 
             1180  BINARY_SUBSCR    
             1182  CALL_FUNCTION_1       1  '1 positional argument'
             1184  BINARY_ADD       
             1186  LOAD_STR                 '\n'
             1188  BINARY_ADD       
             1190  CALL_METHOD_1         1  '1 positional argument'
             1192  POP_TOP          

 L.  99      1194  LOAD_FAST                'fp'
             1196  LOAD_METHOD              write

 L. 100      1198  LOAD_STR                 'ef_key_slot_7_w1 = 0x'
             1200  LOAD_GLOBAL              str_endian_switch
             1202  LOAD_FAST                'values'
             1204  LOAD_STR                 'cpu1_aes_key_simple'
             1206  BINARY_SUBSCR    
             1208  LOAD_CONST               8
             1210  LOAD_CONST               16
             1212  BUILD_SLICE_2         2 
             1214  BINARY_SUBSCR    
             1216  CALL_FUNCTION_1       1  '1 positional argument'
             1218  BINARY_ADD       
             1220  LOAD_STR                 '\n'
             1222  BINARY_ADD       
             1224  CALL_METHOD_1         1  '1 positional argument'
             1226  POP_TOP          

 L. 101      1228  LOAD_FAST                'fp'
             1230  LOAD_METHOD              write

 L. 102      1232  LOAD_STR                 'ef_key_slot_7_w2 = 0x'
             1234  LOAD_GLOBAL              str_endian_switch
             1236  LOAD_FAST                'values'
             1238  LOAD_STR                 'cpu1_aes_key_simple'
             1240  BINARY_SUBSCR    
             1242  LOAD_CONST               16
             1244  LOAD_CONST               24
             1246  BUILD_SLICE_2         2 
             1248  BINARY_SUBSCR    
             1250  CALL_FUNCTION_1       1  '1 positional argument'
             1252  BINARY_ADD       
             1254  LOAD_STR                 '\n'
             1256  BINARY_ADD       
             1258  CALL_METHOD_1         1  '1 positional argument'
             1260  POP_TOP          

 L. 103      1262  LOAD_FAST                'fp'
             1264  LOAD_METHOD              write

 L. 104      1266  LOAD_STR                 'ef_key_slot_7_w3 = 0x'
             1268  LOAD_GLOBAL              str_endian_switch
             1270  LOAD_FAST                'values'
             1272  LOAD_STR                 'cpu1_aes_key_simple'
             1274  BINARY_SUBSCR    
             1276  LOAD_CONST               24
             1278  LOAD_CONST               32
             1280  BUILD_SLICE_2         2 
             1282  BINARY_SUBSCR    
             1284  CALL_FUNCTION_1       1  '1 positional argument'
             1286  BINARY_ADD       
             1288  LOAD_STR                 '\n'
             1290  BINARY_ADD       
             1292  CALL_METHOD_1         1  '1 positional argument'
             1294  POP_TOP          

 L. 105      1296  LOAD_FAST                'values'
             1298  LOAD_STR                 'cpu1_aes_key_wp_enable'
             1300  BINARY_SUBSCR    
             1302  LOAD_CONST               True
             1304  COMPARE_OP               is
         1306_1308  POP_JUMP_IF_FALSE  1322  'to 1322'

 L. 106      1310  LOAD_FAST                'fp'
             1312  LOAD_METHOD              write
             1314  LOAD_STR                 'wr_lock_key_slot_7 = 1\n'
             1316  CALL_METHOD_1         1  '1 positional argument'
             1318  POP_TOP          
             1320  JUMP_FORWARD       1332  'to 1332'
           1322_0  COME_FROM          1306  '1306'

 L. 108      1322  LOAD_FAST                'fp'
             1324  LOAD_METHOD              write
             1326  LOAD_STR                 'wr_lock_key_slot_7 = 0\n'
             1328  CALL_METHOD_1         1  '1 positional argument'
             1330  POP_TOP          
           1332_0  COME_FROM          1320  '1320'

 L. 109      1332  LOAD_FAST                'values'
             1334  LOAD_STR                 'cpu1_aes_key_rp_enable'
             1336  BINARY_SUBSCR    
             1338  LOAD_CONST               True
             1340  COMPARE_OP               is
         1342_1344  POP_JUMP_IF_FALSE  1358  'to 1358'

 L. 110      1346  LOAD_FAST                'fp'
             1348  LOAD_METHOD              write
             1350  LOAD_STR                 'rd_lock_key_slot_7 = 1\n'
             1352  CALL_METHOD_1         1  '1 positional argument'
             1354  POP_TOP          
             1356  JUMP_FORWARD       1368  'to 1368'
           1358_0  COME_FROM          1342  '1342'

 L. 112      1358  LOAD_FAST                'fp'
             1360  LOAD_METHOD              write
             1362  LOAD_STR                 'rd_lock_key_slot_7 = 0\n'
             1364  CALL_METHOD_1         1  '1 positional argument'
             1366  POP_TOP          
           1368_0  COME_FROM          1356  '1356'

 L. 113      1368  LOAD_FAST                'tips'
             1370  LOAD_STR                 'CPU1 AES key\r\n'
             1372  INPLACE_ADD      
             1374  STORE_FAST               'tips'

 L. 114      1376  LOAD_FAST                'fp'
             1378  LOAD_METHOD              write

 L. 115      1380  LOAD_STR                 'ef_key_slot_10_w0 = 0x'
             1382  LOAD_GLOBAL              str_endian_switch
             1384  LOAD_FAST                'values'
             1386  LOAD_STR                 'common_aes_key_simple'
             1388  BINARY_SUBSCR    
             1390  LOAD_CONST               0
             1392  LOAD_CONST               8
             1394  BUILD_SLICE_2         2 
             1396  BINARY_SUBSCR    
             1398  CALL_FUNCTION_1       1  '1 positional argument'
             1400  BINARY_ADD       
             1402  LOAD_STR                 '\n'
             1404  BINARY_ADD       
             1406  CALL_METHOD_1         1  '1 positional argument'
             1408  POP_TOP          

 L. 116      1410  LOAD_FAST                'fp'
             1412  LOAD_METHOD              write

 L. 117      1414  LOAD_STR                 'ef_key_slot_10_w1 = 0x'
             1416  LOAD_GLOBAL              str_endian_switch
             1418  LOAD_FAST                'values'
             1420  LOAD_STR                 'common_aes_key_simple'
             1422  BINARY_SUBSCR    
             1424  LOAD_CONST               8
             1426  LOAD_CONST               16
             1428  BUILD_SLICE_2         2 
             1430  BINARY_SUBSCR    
             1432  CALL_FUNCTION_1       1  '1 positional argument'
             1434  BINARY_ADD       
             1436  LOAD_STR                 '\n'
             1438  BINARY_ADD       
             1440  CALL_METHOD_1         1  '1 positional argument'
             1442  POP_TOP          

 L. 118      1444  LOAD_FAST                'fp'
             1446  LOAD_METHOD              write

 L. 119      1448  LOAD_STR                 'ef_key_slot_10_w2 = 0x'
             1450  LOAD_GLOBAL              str_endian_switch
             1452  LOAD_FAST                'values'
             1454  LOAD_STR                 'common_aes_key_simple'
             1456  BINARY_SUBSCR    
             1458  LOAD_CONST               16
             1460  LOAD_CONST               24
             1462  BUILD_SLICE_2         2 
             1464  BINARY_SUBSCR    
             1466  CALL_FUNCTION_1       1  '1 positional argument'
             1468  BINARY_ADD       
             1470  LOAD_STR                 '\n'
             1472  BINARY_ADD       
             1474  CALL_METHOD_1         1  '1 positional argument'
             1476  POP_TOP          

 L. 120      1478  LOAD_FAST                'fp'
             1480  LOAD_METHOD              write

 L. 121      1482  LOAD_STR                 'ef_key_slot_10_w3 = 0x'
             1484  LOAD_GLOBAL              str_endian_switch
             1486  LOAD_FAST                'values'
             1488  LOAD_STR                 'common_aes_key_simple'
             1490  BINARY_SUBSCR    
             1492  LOAD_CONST               24
             1494  LOAD_CONST               32
             1496  BUILD_SLICE_2         2 
             1498  BINARY_SUBSCR    
             1500  CALL_FUNCTION_1       1  '1 positional argument'
             1502  BINARY_ADD       
             1504  LOAD_STR                 '\n'
             1506  BINARY_ADD       
             1508  CALL_METHOD_1         1  '1 positional argument'
             1510  POP_TOP          

 L. 122      1512  LOAD_FAST                'values'
             1514  LOAD_STR                 'common_aes_key_wp_enable'
             1516  BINARY_SUBSCR    
             1518  LOAD_CONST               True
             1520  COMPARE_OP               is
         1522_1524  POP_JUMP_IF_FALSE  1538  'to 1538'

 L. 123      1526  LOAD_FAST                'fp'
             1528  LOAD_METHOD              write
             1530  LOAD_STR                 'wr_lock_key_slot_10 = 1\n'
             1532  CALL_METHOD_1         1  '1 positional argument'
             1534  POP_TOP          
             1536  JUMP_FORWARD       1548  'to 1548'
           1538_0  COME_FROM          1522  '1522'

 L. 125      1538  LOAD_FAST                'fp'
             1540  LOAD_METHOD              write
             1542  LOAD_STR                 'wr_lock_key_slot_10 = 0\n'
             1544  CALL_METHOD_1         1  '1 positional argument'
             1546  POP_TOP          
           1548_0  COME_FROM          1536  '1536'

 L. 126      1548  LOAD_FAST                'values'
             1550  LOAD_STR                 'common_aes_key_rp_enable'
             1552  BINARY_SUBSCR    
             1554  LOAD_CONST               True
             1556  COMPARE_OP               is
         1558_1560  POP_JUMP_IF_FALSE  1574  'to 1574'

 L. 127      1562  LOAD_FAST                'fp'
             1564  LOAD_METHOD              write
             1566  LOAD_STR                 'rd_lock_key_slot_10 = 1\n'
             1568  CALL_METHOD_1         1  '1 positional argument'
             1570  POP_TOP          
             1572  JUMP_FORWARD       1584  'to 1584'
           1574_0  COME_FROM          1558  '1558'

 L. 129      1574  LOAD_FAST                'fp'
             1576  LOAD_METHOD              write
             1578  LOAD_STR                 'rd_lock_key_slot_10 = 0\n'
             1580  CALL_METHOD_1         1  '1 positional argument'
             1582  POP_TOP          
           1584_0  COME_FROM          1572  '1572'

 L. 130      1584  LOAD_FAST                'tips'
             1586  LOAD_STR                 'Common AES key\r\n'
             1588  INPLACE_ADD      
             1590  STORE_FAST               'tips'
             1592  JUMP_FORWARD       1608  'to 1608'
           1594_0  COME_FROM           940  '940'
           1594_1  COME_FROM           922  '922'
           1594_2  COME_FROM           904  '904'
           1594_3  COME_FROM           886  '886'
           1594_4  COME_FROM           868  '868'
           1594_5  COME_FROM           850  '850'

 L. 132      1594  LOAD_GLOBAL              bflb_utils
             1596  LOAD_METHOD              printf
             1598  LOAD_STR                 'Error: Please check AES key data and len'
             1600  CALL_METHOD_1         1  '1 positional argument'
             1602  POP_TOP          

 L. 133      1604  LOAD_STR                 'Error: Please check AES key data and len'
             1606  RETURN_VALUE     
           1608_0  COME_FROM          1592  '1592'
             1608  JUMP_FORWARD       1694  'to 1694'
           1610_0  COME_FROM           832  '832'

 L. 135      1610  LOAD_FAST                'values'
             1612  LOAD_STR                 'cpu0_aes_key_simple'
             1614  BINARY_SUBSCR    
             1616  LOAD_STR                 ''
             1618  COMPARE_OP               !=
         1620_1622  POP_JUMP_IF_FALSE  1638  'to 1638'

 L. 136      1624  LOAD_GLOBAL              bflb_utils
             1626  LOAD_METHOD              printf
             1628  LOAD_STR                 'Error: AES mode is None, no need to fill in CPU0 AES key'
             1630  CALL_METHOD_1         1  '1 positional argument'
             1632  POP_TOP          

 L. 137      1634  LOAD_STR                 'Error: AES mode is None, no need to fill in CPU0 AES key'
             1636  RETURN_VALUE     
           1638_0  COME_FROM          1620  '1620'

 L. 138      1638  LOAD_FAST                'values'
             1640  LOAD_STR                 'cpu1_aes_key_simple'
             1642  BINARY_SUBSCR    
             1644  LOAD_STR                 ''
             1646  COMPARE_OP               !=
         1648_1650  POP_JUMP_IF_FALSE  1666  'to 1666'

 L. 139      1652  LOAD_GLOBAL              bflb_utils
             1654  LOAD_METHOD              printf
             1656  LOAD_STR                 'Error: AES mode is None, no need to fill in CPU1 AES key'
             1658  CALL_METHOD_1         1  '1 positional argument'
             1660  POP_TOP          

 L. 140      1662  LOAD_STR                 'Error: AES mode is None, no need to fill in CPU1 AES key'
             1664  RETURN_VALUE     
           1666_0  COME_FROM          1648  '1648'

 L. 141      1666  LOAD_FAST                'values'
             1668  LOAD_STR                 'common_aes_key_simple'
             1670  BINARY_SUBSCR    
             1672  LOAD_STR                 ''
             1674  COMPARE_OP               !=
         1676_1678  POP_JUMP_IF_FALSE  1710  'to 1710'

 L. 142      1680  LOAD_GLOBAL              bflb_utils
             1682  LOAD_METHOD              printf
             1684  LOAD_STR                 'Error: AES mode is None, no need to fill in Common AES key'
             1686  CALL_METHOD_1         1  '1 positional argument'
             1688  POP_TOP          

 L. 143      1690  LOAD_STR                 'Error: AES mode is None, no need to fill in Common AES key'
             1692  RETURN_VALUE     
           1694_0  COME_FROM          1608  '1608'
             1694  JUMP_FORWARD       1710  'to 1710'
           1696_0  COME_FROM           150  '150'
           1696_1  COME_FROM           132  '132'
           1696_2  COME_FROM           114  '114'
           1696_3  COME_FROM            96  '96'

 L. 145      1696  LOAD_GLOBAL              bflb_utils
             1698  LOAD_METHOD              printf
             1700  LOAD_STR                 'Error: Please check public key hash data and len'
             1702  CALL_METHOD_1         1  '1 positional argument'
             1704  POP_TOP          

 L. 146      1706  LOAD_STR                 'Error: Please check public key hash data and len'
             1708  RETURN_VALUE     
           1710_0  COME_FROM          1694  '1694'
           1710_1  COME_FROM          1676  '1676'

 L. 147      1710  LOAD_FAST                'aes_mode'
             1712  LOAD_CONST               1
             1714  COMPARE_OP               ==
         1716_1718  POP_JUMP_IF_FALSE  1820  'to 1820'

 L. 148      1720  LOAD_GLOBAL              len
             1722  LOAD_FAST                'values'
             1724  LOAD_STR                 'cpu0_aes_key_simple'
             1726  BINARY_SUBSCR    
             1728  CALL_FUNCTION_1       1  '1 positional argument'
             1730  LOAD_CONST               32
             1732  COMPARE_OP               !=
         1734_1736  POP_JUMP_IF_FALSE  1752  'to 1752'

 L. 149      1738  LOAD_GLOBAL              bflb_utils
             1740  LOAD_METHOD              printf
             1742  LOAD_STR                 'Error: Please check CPU0 AES key len'
             1744  CALL_METHOD_1         1  '1 positional argument'
             1746  POP_TOP          

 L. 150      1748  LOAD_STR                 'Error: Please check CPU0 AES key len'
             1750  RETURN_VALUE     
           1752_0  COME_FROM          1734  '1734'

 L. 151      1752  LOAD_GLOBAL              len
             1754  LOAD_FAST                'values'
             1756  LOAD_STR                 'cpu1_aes_key_simple'
             1758  BINARY_SUBSCR    
             1760  CALL_FUNCTION_1       1  '1 positional argument'
             1762  LOAD_CONST               32
             1764  COMPARE_OP               !=
         1766_1768  POP_JUMP_IF_FALSE  1784  'to 1784'

 L. 152      1770  LOAD_GLOBAL              bflb_utils
             1772  LOAD_METHOD              printf
             1774  LOAD_STR                 'Error: Please check CPU1 AES key len'
             1776  CALL_METHOD_1         1  '1 positional argument'
             1778  POP_TOP          

 L. 153      1780  LOAD_STR                 'Error: Please check CPU1 AES key len'
             1782  RETURN_VALUE     
           1784_0  COME_FROM          1766  '1766'

 L. 154      1784  LOAD_GLOBAL              len
             1786  LOAD_FAST                'values'
             1788  LOAD_STR                 'common_aes_key_simple'
             1790  BINARY_SUBSCR    
             1792  CALL_FUNCTION_1       1  '1 positional argument'
             1794  LOAD_CONST               32
             1796  COMPARE_OP               !=
         1798_1800  POP_JUMP_IF_FALSE  3092  'to 3092'

 L. 155      1802  LOAD_GLOBAL              bflb_utils
             1804  LOAD_METHOD              printf
             1806  LOAD_STR                 'Error: Please check Common AES key len'
             1808  CALL_METHOD_1         1  '1 positional argument'
             1810  POP_TOP          

 L. 156      1812  LOAD_STR                 'Error: Please check Common AES key len'
             1814  RETURN_VALUE     
         1816_1818  JUMP_FORWARD       3092  'to 3092'
           1820_0  COME_FROM          1716  '1716'

 L. 157      1820  LOAD_FAST                'aes_mode'
             1822  LOAD_CONST               2
             1824  COMPARE_OP               ==
         1826_1828  POP_JUMP_IF_FALSE  2356  'to 2356'

 L. 158      1830  LOAD_GLOBAL              len
             1832  LOAD_FAST                'values'
             1834  LOAD_STR                 'cpu0_aes_key_simple'
             1836  BINARY_SUBSCR    
             1838  CALL_FUNCTION_1       1  '1 positional argument'
             1840  LOAD_CONST               48
             1842  COMPARE_OP               ==
         1844_1846  POP_JUMP_IF_FALSE  1990  'to 1990'

 L. 159      1848  LOAD_FAST                'fp'
             1850  LOAD_METHOD              write

 L. 160      1852  LOAD_STR                 'ef_key_slot_3_w0 = 0x'
             1854  LOAD_GLOBAL              str_endian_switch
             1856  LOAD_FAST                'values'
             1858  LOAD_STR                 'cpu0_aes_key_simple'
             1860  BINARY_SUBSCR    
             1862  LOAD_CONST               32
             1864  LOAD_CONST               40
             1866  BUILD_SLICE_2         2 
             1868  BINARY_SUBSCR    
             1870  CALL_FUNCTION_1       1  '1 positional argument'
             1872  BINARY_ADD       
             1874  LOAD_STR                 '\n'
             1876  BINARY_ADD       
             1878  CALL_METHOD_1         1  '1 positional argument'
             1880  POP_TOP          

 L. 161      1882  LOAD_FAST                'fp'
             1884  LOAD_METHOD              write

 L. 162      1886  LOAD_STR                 'ef_key_slot_3_w1 = 0x'
             1888  LOAD_GLOBAL              str_endian_switch
             1890  LOAD_FAST                'values'
             1892  LOAD_STR                 'cpu0_aes_key_simple'
             1894  BINARY_SUBSCR    
             1896  LOAD_CONST               40
             1898  LOAD_CONST               48
             1900  BUILD_SLICE_2         2 
             1902  BINARY_SUBSCR    
             1904  CALL_FUNCTION_1       1  '1 positional argument'
             1906  BINARY_ADD       
             1908  LOAD_STR                 '\n'
             1910  BINARY_ADD       
             1912  CALL_METHOD_1         1  '1 positional argument'
             1914  POP_TOP          

 L. 163      1916  LOAD_FAST                'values'
             1918  LOAD_STR                 'cpu0_aes_key_wp_enable'
             1920  BINARY_SUBSCR    
             1922  LOAD_CONST               True
             1924  COMPARE_OP               is
         1926_1928  POP_JUMP_IF_FALSE  1942  'to 1942'

 L. 164      1930  LOAD_FAST                'fp'
             1932  LOAD_METHOD              write
             1934  LOAD_STR                 'wr_lock_key_slot_3 = 1\n'
             1936  CALL_METHOD_1         1  '1 positional argument'
             1938  POP_TOP          
             1940  JUMP_FORWARD       1952  'to 1952'
           1942_0  COME_FROM          1926  '1926'

 L. 166      1942  LOAD_FAST                'fp'
             1944  LOAD_METHOD              write
             1946  LOAD_STR                 'wr_lock_key_slot_3 = 0\n'
             1948  CALL_METHOD_1         1  '1 positional argument'
             1950  POP_TOP          
           1952_0  COME_FROM          1940  '1940'

 L. 167      1952  LOAD_FAST                'values'
             1954  LOAD_STR                 'cpu0_aes_key_rp_enable'
             1956  BINARY_SUBSCR    
             1958  LOAD_CONST               True
             1960  COMPARE_OP               is
         1962_1964  POP_JUMP_IF_FALSE  1978  'to 1978'

 L. 168      1966  LOAD_FAST                'fp'
             1968  LOAD_METHOD              write
             1970  LOAD_STR                 'rd_lock_key_slot_3 = 1\n'
             1972  CALL_METHOD_1         1  '1 positional argument'
             1974  POP_TOP          
             1976  JUMP_FORWARD       1988  'to 1988'
           1978_0  COME_FROM          1962  '1962'

 L. 170      1978  LOAD_FAST                'fp'
             1980  LOAD_METHOD              write
             1982  LOAD_STR                 'rd_lock_key_slot_3 = 0\n'
             1984  CALL_METHOD_1         1  '1 positional argument'
             1986  POP_TOP          
           1988_0  COME_FROM          1976  '1976'
             1988  JUMP_FORWARD       2004  'to 2004'
           1990_0  COME_FROM          1844  '1844'

 L. 172      1990  LOAD_GLOBAL              bflb_utils
             1992  LOAD_METHOD              printf
             1994  LOAD_STR                 'Error: Please check CPU0 AES key len'
             1996  CALL_METHOD_1         1  '1 positional argument'
             1998  POP_TOP          

 L. 173      2000  LOAD_STR                 'Error: Please check CPU0 AES key len'
             2002  RETURN_VALUE     
           2004_0  COME_FROM          1988  '1988'

 L. 174      2004  LOAD_GLOBAL              len
             2006  LOAD_FAST                'values'
             2008  LOAD_STR                 'cpu1_aes_key_simple'
             2010  BINARY_SUBSCR    
             2012  CALL_FUNCTION_1       1  '1 positional argument'
             2014  LOAD_CONST               48
             2016  COMPARE_OP               ==
         2018_2020  POP_JUMP_IF_FALSE  2164  'to 2164'

 L. 175      2022  LOAD_FAST                'fp'
             2024  LOAD_METHOD              write

 L. 176      2026  LOAD_STR                 'ef_key_slot_8_w0 = 0x'
             2028  LOAD_GLOBAL              str_endian_switch
             2030  LOAD_FAST                'values'
             2032  LOAD_STR                 'cpu1_aes_key_simple'
             2034  BINARY_SUBSCR    
             2036  LOAD_CONST               32
             2038  LOAD_CONST               40
             2040  BUILD_SLICE_2         2 
             2042  BINARY_SUBSCR    
             2044  CALL_FUNCTION_1       1  '1 positional argument'
             2046  BINARY_ADD       
             2048  LOAD_STR                 '\n'
             2050  BINARY_ADD       
             2052  CALL_METHOD_1         1  '1 positional argument'
             2054  POP_TOP          

 L. 177      2056  LOAD_FAST                'fp'
             2058  LOAD_METHOD              write

 L. 178      2060  LOAD_STR                 'ef_key_slot_8_w1 = 0x'
             2062  LOAD_GLOBAL              str_endian_switch
             2064  LOAD_FAST                'values'
             2066  LOAD_STR                 'cpu1_aes_key_simple'
             2068  BINARY_SUBSCR    
             2070  LOAD_CONST               40
             2072  LOAD_CONST               48
             2074  BUILD_SLICE_2         2 
             2076  BINARY_SUBSCR    
             2078  CALL_FUNCTION_1       1  '1 positional argument'
             2080  BINARY_ADD       
             2082  LOAD_STR                 '\n'
             2084  BINARY_ADD       
             2086  CALL_METHOD_1         1  '1 positional argument'
             2088  POP_TOP          

 L. 179      2090  LOAD_FAST                'values'
             2092  LOAD_STR                 'cpu1_aes_key_wp_enable'
             2094  BINARY_SUBSCR    
             2096  LOAD_CONST               True
             2098  COMPARE_OP               is
         2100_2102  POP_JUMP_IF_FALSE  2116  'to 2116'

 L. 180      2104  LOAD_FAST                'fp'
             2106  LOAD_METHOD              write
             2108  LOAD_STR                 'wr_lock_key_slot_8 = 1\n'
             2110  CALL_METHOD_1         1  '1 positional argument'
             2112  POP_TOP          
             2114  JUMP_FORWARD       2126  'to 2126'
           2116_0  COME_FROM          2100  '2100'

 L. 182      2116  LOAD_FAST                'fp'
             2118  LOAD_METHOD              write
             2120  LOAD_STR                 'wr_lock_key_slot_8 = 0\n'
             2122  CALL_METHOD_1         1  '1 positional argument'
             2124  POP_TOP          
           2126_0  COME_FROM          2114  '2114'

 L. 183      2126  LOAD_FAST                'values'
             2128  LOAD_STR                 'cpu1_aes_key_rp_enable'
             2130  BINARY_SUBSCR    
             2132  LOAD_CONST               True
             2134  COMPARE_OP               is
         2136_2138  POP_JUMP_IF_FALSE  2152  'to 2152'

 L. 184      2140  LOAD_FAST                'fp'
             2142  LOAD_METHOD              write
             2144  LOAD_STR                 'rd_lock_key_slot_8 = 1\n'
             2146  CALL_METHOD_1         1  '1 positional argument'
             2148  POP_TOP          
             2150  JUMP_FORWARD       2162  'to 2162'
           2152_0  COME_FROM          2136  '2136'

 L. 186      2152  LOAD_FAST                'fp'
             2154  LOAD_METHOD              write
             2156  LOAD_STR                 'rd_lock_key_slot_8 = 0\n'
             2158  CALL_METHOD_1         1  '1 positional argument'
             2160  POP_TOP          
           2162_0  COME_FROM          2150  '2150'
             2162  JUMP_FORWARD       2178  'to 2178'
           2164_0  COME_FROM          2018  '2018'

 L. 188      2164  LOAD_GLOBAL              bflb_utils
             2166  LOAD_METHOD              printf
             2168  LOAD_STR                 'Error: Please check CPU1 AES key len'
             2170  CALL_METHOD_1         1  '1 positional argument'
             2172  POP_TOP          

 L. 189      2174  LOAD_STR                 'Error: Please check CPU1 AES key len'
             2176  RETURN_VALUE     
           2178_0  COME_FROM          2162  '2162'

 L. 190      2178  LOAD_GLOBAL              len
             2180  LOAD_FAST                'values'
             2182  LOAD_STR                 'common_aes_key_simple'
             2184  BINARY_SUBSCR    
             2186  CALL_FUNCTION_1       1  '1 positional argument'
             2188  LOAD_CONST               48
             2190  COMPARE_OP               ==
         2192_2194  POP_JUMP_IF_FALSE  2338  'to 2338'

 L. 191      2196  LOAD_FAST                'fp'
             2198  LOAD_METHOD              write

 L. 192      2200  LOAD_STR                 'ef_key_slot_11_w0 = 0x'
             2202  LOAD_GLOBAL              str_endian_switch
             2204  LOAD_FAST                'values'
             2206  LOAD_STR                 'common_aes_key_simple'
             2208  BINARY_SUBSCR    
             2210  LOAD_CONST               32
             2212  LOAD_CONST               40
             2214  BUILD_SLICE_2         2 
             2216  BINARY_SUBSCR    
             2218  CALL_FUNCTION_1       1  '1 positional argument'
             2220  BINARY_ADD       
             2222  LOAD_STR                 '\n'
             2224  BINARY_ADD       
             2226  CALL_METHOD_1         1  '1 positional argument'
             2228  POP_TOP          

 L. 193      2230  LOAD_FAST                'fp'
             2232  LOAD_METHOD              write

 L. 194      2234  LOAD_STR                 'ef_key_slot_11_w1 = 0x'
             2236  LOAD_GLOBAL              str_endian_switch
             2238  LOAD_FAST                'values'
             2240  LOAD_STR                 'common_aes_key_simple'
             2242  BINARY_SUBSCR    
             2244  LOAD_CONST               40
             2246  LOAD_CONST               48
             2248  BUILD_SLICE_2         2 
             2250  BINARY_SUBSCR    
             2252  CALL_FUNCTION_1       1  '1 positional argument'
             2254  BINARY_ADD       
             2256  LOAD_STR                 '\n'
             2258  BINARY_ADD       
             2260  CALL_METHOD_1         1  '1 positional argument'
             2262  POP_TOP          

 L. 195      2264  LOAD_FAST                'values'
             2266  LOAD_STR                 'common_aes_key_wp_enable'
             2268  BINARY_SUBSCR    
             2270  LOAD_CONST               True
             2272  COMPARE_OP               is
         2274_2276  POP_JUMP_IF_FALSE  2290  'to 2290'

 L. 196      2278  LOAD_FAST                'fp'
             2280  LOAD_METHOD              write
             2282  LOAD_STR                 'wr_lock_key_slot_11 = 1\n'
             2284  CALL_METHOD_1         1  '1 positional argument'
             2286  POP_TOP          
             2288  JUMP_FORWARD       2300  'to 2300'
           2290_0  COME_FROM          2274  '2274'

 L. 198      2290  LOAD_FAST                'fp'
             2292  LOAD_METHOD              write
             2294  LOAD_STR                 'wr_lock_key_slot_11 = 0\n'
             2296  CALL_METHOD_1         1  '1 positional argument'
             2298  POP_TOP          
           2300_0  COME_FROM          2288  '2288'

 L. 199      2300  LOAD_FAST                'values'
             2302  LOAD_STR                 'common_aes_key_rp_enable'
             2304  BINARY_SUBSCR    
             2306  LOAD_CONST               True
             2308  COMPARE_OP               is
         2310_2312  POP_JUMP_IF_FALSE  2326  'to 2326'

 L. 200      2314  LOAD_FAST                'fp'
             2316  LOAD_METHOD              write
             2318  LOAD_STR                 'rd_lock_key_slot_11 = 1\n'
             2320  CALL_METHOD_1         1  '1 positional argument'
             2322  POP_TOP          
             2324  JUMP_FORWARD       2336  'to 2336'
           2326_0  COME_FROM          2310  '2310'

 L. 202      2326  LOAD_FAST                'fp'
             2328  LOAD_METHOD              write
             2330  LOAD_STR                 'rd_lock_key_slot_11 = 0\n'
             2332  CALL_METHOD_1         1  '1 positional argument'
             2334  POP_TOP          
           2336_0  COME_FROM          2324  '2324'
             2336  JUMP_FORWARD       3092  'to 3092'
           2338_0  COME_FROM          2192  '2192'

 L. 204      2338  LOAD_GLOBAL              bflb_utils
             2340  LOAD_METHOD              printf
             2342  LOAD_STR                 'Error: Please check Common AES key len'
             2344  CALL_METHOD_1         1  '1 positional argument'
             2346  POP_TOP          

 L. 205      2348  LOAD_STR                 'Error: Please check Common AES key len'
             2350  RETURN_VALUE     
         2352_2354  JUMP_FORWARD       3092  'to 3092'
           2356_0  COME_FROM          1826  '1826'

 L. 206      2356  LOAD_FAST                'aes_mode'
             2358  LOAD_CONST               3
             2360  COMPARE_OP               ==
         2362_2364  POP_JUMP_IF_FALSE  3092  'to 3092'

 L. 207      2366  LOAD_GLOBAL              len
             2368  LOAD_FAST                'values'
             2370  LOAD_STR                 'cpu0_aes_key_simple'
             2372  BINARY_SUBSCR    
             2374  CALL_FUNCTION_1       1  '1 positional argument'
             2376  LOAD_CONST               64
             2378  COMPARE_OP               ==
         2380_2382  POP_JUMP_IF_FALSE  2594  'to 2594'

 L. 208      2384  LOAD_FAST                'fp'
             2386  LOAD_METHOD              write

 L. 209      2388  LOAD_STR                 'ef_key_slot_3_w0 = 0x'
             2390  LOAD_GLOBAL              str_endian_switch
             2392  LOAD_FAST                'values'
             2394  LOAD_STR                 'cpu0_aes_key_simple'
             2396  BINARY_SUBSCR    
             2398  LOAD_CONST               32
             2400  LOAD_CONST               40
             2402  BUILD_SLICE_2         2 
             2404  BINARY_SUBSCR    
             2406  CALL_FUNCTION_1       1  '1 positional argument'
             2408  BINARY_ADD       
             2410  LOAD_STR                 '\n'
             2412  BINARY_ADD       
             2414  CALL_METHOD_1         1  '1 positional argument'
             2416  POP_TOP          

 L. 210      2418  LOAD_FAST                'fp'
             2420  LOAD_METHOD              write

 L. 211      2422  LOAD_STR                 'ef_key_slot_3_w1 = 0x'
             2424  LOAD_GLOBAL              str_endian_switch
             2426  LOAD_FAST                'values'
             2428  LOAD_STR                 'cpu0_aes_key_simple'
             2430  BINARY_SUBSCR    
             2432  LOAD_CONST               40
             2434  LOAD_CONST               48
             2436  BUILD_SLICE_2         2 
             2438  BINARY_SUBSCR    
             2440  CALL_FUNCTION_1       1  '1 positional argument'
             2442  BINARY_ADD       
             2444  LOAD_STR                 '\n'
             2446  BINARY_ADD       
             2448  CALL_METHOD_1         1  '1 positional argument'
             2450  POP_TOP          

 L. 212      2452  LOAD_FAST                'fp'
             2454  LOAD_METHOD              write

 L. 213      2456  LOAD_STR                 'ef_key_slot_3_w2 = 0x'
             2458  LOAD_GLOBAL              str_endian_switch
             2460  LOAD_FAST                'values'
             2462  LOAD_STR                 'cpu0_aes_key_simple'
             2464  BINARY_SUBSCR    
             2466  LOAD_CONST               48
             2468  LOAD_CONST               56
             2470  BUILD_SLICE_2         2 
             2472  BINARY_SUBSCR    
             2474  CALL_FUNCTION_1       1  '1 positional argument'
             2476  BINARY_ADD       
             2478  LOAD_STR                 '\n'
             2480  BINARY_ADD       
             2482  CALL_METHOD_1         1  '1 positional argument'
             2484  POP_TOP          

 L. 214      2486  LOAD_FAST                'fp'
             2488  LOAD_METHOD              write

 L. 215      2490  LOAD_STR                 'ef_key_slot_3_w3 = 0x'
             2492  LOAD_GLOBAL              str_endian_switch
             2494  LOAD_FAST                'values'
             2496  LOAD_STR                 'cpu0_aes_key_simple'
             2498  BINARY_SUBSCR    
             2500  LOAD_CONST               56
             2502  LOAD_CONST               64
             2504  BUILD_SLICE_2         2 
             2506  BINARY_SUBSCR    
             2508  CALL_FUNCTION_1       1  '1 positional argument'
             2510  BINARY_ADD       
             2512  LOAD_STR                 '\n'
             2514  BINARY_ADD       
             2516  CALL_METHOD_1         1  '1 positional argument'
             2518  POP_TOP          

 L. 216      2520  LOAD_FAST                'values'
             2522  LOAD_STR                 'cpu0_aes_key_wp_enable'
             2524  BINARY_SUBSCR    
             2526  LOAD_CONST               True
             2528  COMPARE_OP               is
         2530_2532  POP_JUMP_IF_FALSE  2546  'to 2546'

 L. 217      2534  LOAD_FAST                'fp'
             2536  LOAD_METHOD              write
             2538  LOAD_STR                 'wr_lock_key_slot_3 = 1\n'
             2540  CALL_METHOD_1         1  '1 positional argument'
             2542  POP_TOP          
             2544  JUMP_FORWARD       2556  'to 2556'
           2546_0  COME_FROM          2530  '2530'

 L. 219      2546  LOAD_FAST                'fp'
             2548  LOAD_METHOD              write
             2550  LOAD_STR                 'wr_lock_key_slot_3 = 0\n'
             2552  CALL_METHOD_1         1  '1 positional argument'
             2554  POP_TOP          
           2556_0  COME_FROM          2544  '2544'

 L. 220      2556  LOAD_FAST                'values'
             2558  LOAD_STR                 'cpu0_aes_key_rp_enable'
             2560  BINARY_SUBSCR    
             2562  LOAD_CONST               True
             2564  COMPARE_OP               is
         2566_2568  POP_JUMP_IF_FALSE  2582  'to 2582'

 L. 221      2570  LOAD_FAST                'fp'
             2572  LOAD_METHOD              write
             2574  LOAD_STR                 'rd_lock_key_slot_3 = 1\n'
             2576  CALL_METHOD_1         1  '1 positional argument'
             2578  POP_TOP          
             2580  JUMP_FORWARD       2592  'to 2592'
           2582_0  COME_FROM          2566  '2566'

 L. 223      2582  LOAD_FAST                'fp'
             2584  LOAD_METHOD              write
             2586  LOAD_STR                 'rd_lock_key_slot_3 = 0\n'
             2588  CALL_METHOD_1         1  '1 positional argument'
             2590  POP_TOP          
           2592_0  COME_FROM          2580  '2580'
             2592  JUMP_FORWARD       2608  'to 2608'
           2594_0  COME_FROM          2380  '2380'

 L. 225      2594  LOAD_GLOBAL              bflb_utils
             2596  LOAD_METHOD              printf
             2598  LOAD_STR                 'Error: Please check CPU0 AES key len'
             2600  CALL_METHOD_1         1  '1 positional argument'
             2602  POP_TOP          

 L. 226      2604  LOAD_STR                 'Error: Please check CPU0 AES key len'
             2606  RETURN_VALUE     
           2608_0  COME_FROM          2592  '2592'

 L. 227      2608  LOAD_GLOBAL              len
             2610  LOAD_FAST                'values'
             2612  LOAD_STR                 'cpu1_aes_key_simple'
             2614  BINARY_SUBSCR    
             2616  CALL_FUNCTION_1       1  '1 positional argument'
             2618  LOAD_CONST               64
             2620  COMPARE_OP               ==
         2622_2624  POP_JUMP_IF_FALSE  2836  'to 2836'

 L. 228      2626  LOAD_FAST                'fp'
             2628  LOAD_METHOD              write

 L. 229      2630  LOAD_STR                 'ef_key_slot_8_w0 = 0x'
             2632  LOAD_GLOBAL              str_endian_switch
             2634  LOAD_FAST                'values'
             2636  LOAD_STR                 'cpu1_aes_key_simple'
             2638  BINARY_SUBSCR    
             2640  LOAD_CONST               32
             2642  LOAD_CONST               40
             2644  BUILD_SLICE_2         2 
             2646  BINARY_SUBSCR    
             2648  CALL_FUNCTION_1       1  '1 positional argument'
             2650  BINARY_ADD       
             2652  LOAD_STR                 '\n'
             2654  BINARY_ADD       
             2656  CALL_METHOD_1         1  '1 positional argument'
             2658  POP_TOP          

 L. 230      2660  LOAD_FAST                'fp'
             2662  LOAD_METHOD              write

 L. 231      2664  LOAD_STR                 'ef_key_slot_8_w1 = 0x'
             2666  LOAD_GLOBAL              str_endian_switch
             2668  LOAD_FAST                'values'
             2670  LOAD_STR                 'cpu1_aes_key_simple'
             2672  BINARY_SUBSCR    
             2674  LOAD_CONST               40
             2676  LOAD_CONST               48
             2678  BUILD_SLICE_2         2 
             2680  BINARY_SUBSCR    
             2682  CALL_FUNCTION_1       1  '1 positional argument'
             2684  BINARY_ADD       
             2686  LOAD_STR                 '\n'
             2688  BINARY_ADD       
             2690  CALL_METHOD_1         1  '1 positional argument'
             2692  POP_TOP          

 L. 232      2694  LOAD_FAST                'fp'
             2696  LOAD_METHOD              write

 L. 233      2698  LOAD_STR                 'ef_key_slot_8_w2 = 0x'
             2700  LOAD_GLOBAL              str_endian_switch
             2702  LOAD_FAST                'values'
             2704  LOAD_STR                 'cpu1_aes_key_simple'
             2706  BINARY_SUBSCR    
             2708  LOAD_CONST               48
             2710  LOAD_CONST               56
             2712  BUILD_SLICE_2         2 
             2714  BINARY_SUBSCR    
             2716  CALL_FUNCTION_1       1  '1 positional argument'
             2718  BINARY_ADD       
             2720  LOAD_STR                 '\n'
             2722  BINARY_ADD       
             2724  CALL_METHOD_1         1  '1 positional argument'
             2726  POP_TOP          

 L. 234      2728  LOAD_FAST                'fp'
             2730  LOAD_METHOD              write

 L. 235      2732  LOAD_STR                 'ef_key_slot_8_w3 = 0x'
             2734  LOAD_GLOBAL              str_endian_switch
             2736  LOAD_FAST                'values'
             2738  LOAD_STR                 'cpu1_aes_key_simple'
             2740  BINARY_SUBSCR    
             2742  LOAD_CONST               56
             2744  LOAD_CONST               64
             2746  BUILD_SLICE_2         2 
             2748  BINARY_SUBSCR    
             2750  CALL_FUNCTION_1       1  '1 positional argument'
             2752  BINARY_ADD       
             2754  LOAD_STR                 '\n'
             2756  BINARY_ADD       
             2758  CALL_METHOD_1         1  '1 positional argument'
             2760  POP_TOP          

 L. 236      2762  LOAD_FAST                'values'
             2764  LOAD_STR                 'cpu1_aes_key_wp_enable'
             2766  BINARY_SUBSCR    
             2768  LOAD_CONST               True
             2770  COMPARE_OP               is
         2772_2774  POP_JUMP_IF_FALSE  2788  'to 2788'

 L. 237      2776  LOAD_FAST                'fp'
             2778  LOAD_METHOD              write
             2780  LOAD_STR                 'wr_lock_key_slot_8 = 1\n'
             2782  CALL_METHOD_1         1  '1 positional argument'
             2784  POP_TOP          
             2786  JUMP_FORWARD       2798  'to 2798'
           2788_0  COME_FROM          2772  '2772'

 L. 239      2788  LOAD_FAST                'fp'
             2790  LOAD_METHOD              write
             2792  LOAD_STR                 'wr_lock_key_slot_8 = 0\n'
             2794  CALL_METHOD_1         1  '1 positional argument'
             2796  POP_TOP          
           2798_0  COME_FROM          2786  '2786'

 L. 240      2798  LOAD_FAST                'values'
             2800  LOAD_STR                 'cpu1_aes_key_rp_enable'
             2802  BINARY_SUBSCR    
             2804  LOAD_CONST               True
             2806  COMPARE_OP               is
         2808_2810  POP_JUMP_IF_FALSE  2824  'to 2824'

 L. 241      2812  LOAD_FAST                'fp'
             2814  LOAD_METHOD              write
             2816  LOAD_STR                 'rd_lock_key_slot_8 = 1\n'
             2818  CALL_METHOD_1         1  '1 positional argument'
             2820  POP_TOP          
             2822  JUMP_FORWARD       2834  'to 2834'
           2824_0  COME_FROM          2808  '2808'

 L. 243      2824  LOAD_FAST                'fp'
             2826  LOAD_METHOD              write
             2828  LOAD_STR                 'rd_lock_key_slot_8 = 0\n'
             2830  CALL_METHOD_1         1  '1 positional argument'
             2832  POP_TOP          
           2834_0  COME_FROM          2822  '2822'
             2834  JUMP_FORWARD       2850  'to 2850'
           2836_0  COME_FROM          2622  '2622'

 L. 245      2836  LOAD_GLOBAL              bflb_utils
             2838  LOAD_METHOD              printf
             2840  LOAD_STR                 'Error: Please check CPU1 AES key len'
             2842  CALL_METHOD_1         1  '1 positional argument'
             2844  POP_TOP          

 L. 246      2846  LOAD_STR                 'Error: Please check CPU1 AES key len'
             2848  RETURN_VALUE     
           2850_0  COME_FROM          2834  '2834'

 L. 247      2850  LOAD_GLOBAL              len
             2852  LOAD_FAST                'values'
             2854  LOAD_STR                 'common_aes_key_simple'
             2856  BINARY_SUBSCR    
             2858  CALL_FUNCTION_1       1  '1 positional argument'
             2860  LOAD_CONST               64
             2862  COMPARE_OP               ==
         2864_2866  POP_JUMP_IF_FALSE  3078  'to 3078'

 L. 248      2868  LOAD_FAST                'fp'
             2870  LOAD_METHOD              write

 L. 249      2872  LOAD_STR                 'ef_key_slot_11_w0 = 0x'
             2874  LOAD_GLOBAL              str_endian_switch
             2876  LOAD_FAST                'values'
             2878  LOAD_STR                 'common_aes_key_simple'
             2880  BINARY_SUBSCR    
             2882  LOAD_CONST               32
             2884  LOAD_CONST               40
             2886  BUILD_SLICE_2         2 
             2888  BINARY_SUBSCR    
             2890  CALL_FUNCTION_1       1  '1 positional argument'
             2892  BINARY_ADD       
             2894  LOAD_STR                 '\n'
             2896  BINARY_ADD       
             2898  CALL_METHOD_1         1  '1 positional argument'
             2900  POP_TOP          

 L. 250      2902  LOAD_FAST                'fp'
             2904  LOAD_METHOD              write

 L. 251      2906  LOAD_STR                 'ef_key_slot_11_w1 = 0x'
             2908  LOAD_GLOBAL              str_endian_switch
             2910  LOAD_FAST                'values'
             2912  LOAD_STR                 'common_aes_key_simple'
             2914  BINARY_SUBSCR    
             2916  LOAD_CONST               40
             2918  LOAD_CONST               48
             2920  BUILD_SLICE_2         2 
             2922  BINARY_SUBSCR    
             2924  CALL_FUNCTION_1       1  '1 positional argument'
             2926  BINARY_ADD       
             2928  LOAD_STR                 '\n'
             2930  BINARY_ADD       
             2932  CALL_METHOD_1         1  '1 positional argument'
             2934  POP_TOP          

 L. 252      2936  LOAD_FAST                'fp'
             2938  LOAD_METHOD              write

 L. 253      2940  LOAD_STR                 'ef_key_slot_11_w2 = 0x'
             2942  LOAD_GLOBAL              str_endian_switch
             2944  LOAD_FAST                'values'
             2946  LOAD_STR                 'common_aes_key_simple'
             2948  BINARY_SUBSCR    
             2950  LOAD_CONST               48
             2952  LOAD_CONST               56
             2954  BUILD_SLICE_2         2 
             2956  BINARY_SUBSCR    
             2958  CALL_FUNCTION_1       1  '1 positional argument'
             2960  BINARY_ADD       
             2962  LOAD_STR                 '\n'
             2964  BINARY_ADD       
             2966  CALL_METHOD_1         1  '1 positional argument'
             2968  POP_TOP          

 L. 254      2970  LOAD_FAST                'fp'
             2972  LOAD_METHOD              write

 L. 255      2974  LOAD_STR                 'ef_key_slot_11_w3 = 0x'
             2976  LOAD_GLOBAL              str_endian_switch
             2978  LOAD_FAST                'values'
             2980  LOAD_STR                 'common_aes_key_simple'
             2982  BINARY_SUBSCR    
             2984  LOAD_CONST               56
             2986  LOAD_CONST               64
             2988  BUILD_SLICE_2         2 
             2990  BINARY_SUBSCR    
             2992  CALL_FUNCTION_1       1  '1 positional argument'
             2994  BINARY_ADD       
             2996  LOAD_STR                 '\n'
             2998  BINARY_ADD       
             3000  CALL_METHOD_1         1  '1 positional argument'
             3002  POP_TOP          

 L. 256      3004  LOAD_FAST                'values'
             3006  LOAD_STR                 'common_aes_key_wp_enable'
             3008  BINARY_SUBSCR    
             3010  LOAD_CONST               True
             3012  COMPARE_OP               is
         3014_3016  POP_JUMP_IF_FALSE  3030  'to 3030'

 L. 257      3018  LOAD_FAST                'fp'
             3020  LOAD_METHOD              write
             3022  LOAD_STR                 'wr_lock_key_slot_11 = 1\n'
             3024  CALL_METHOD_1         1  '1 positional argument'
             3026  POP_TOP          
             3028  JUMP_FORWARD       3040  'to 3040'
           3030_0  COME_FROM          3014  '3014'

 L. 259      3030  LOAD_FAST                'fp'
             3032  LOAD_METHOD              write
             3034  LOAD_STR                 'wr_lock_key_slot_11 = 0\n'
             3036  CALL_METHOD_1         1  '1 positional argument'
             3038  POP_TOP          
           3040_0  COME_FROM          3028  '3028'

 L. 260      3040  LOAD_FAST                'values'
             3042  LOAD_STR                 'common_aes_key_rp_enable'
             3044  BINARY_SUBSCR    
             3046  LOAD_CONST               True
             3048  COMPARE_OP               is
         3050_3052  POP_JUMP_IF_FALSE  3066  'to 3066'

 L. 261      3054  LOAD_FAST                'fp'
             3056  LOAD_METHOD              write
             3058  LOAD_STR                 'rd_lock_key_slot_11 = 1\n'
             3060  CALL_METHOD_1         1  '1 positional argument'
             3062  POP_TOP          
             3064  JUMP_FORWARD       3076  'to 3076'
           3066_0  COME_FROM          3050  '3050'

 L. 263      3066  LOAD_FAST                'fp'
             3068  LOAD_METHOD              write
             3070  LOAD_STR                 'rd_lock_key_slot_11 = 0\n'
             3072  CALL_METHOD_1         1  '1 positional argument'
           3074_0  COME_FROM          2336  '2336'
             3074  POP_TOP          
           3076_0  COME_FROM          3064  '3064'
             3076  JUMP_FORWARD       3092  'to 3092'
           3078_0  COME_FROM          2864  '2864'

 L. 265      3078  LOAD_GLOBAL              bflb_utils
             3080  LOAD_METHOD              printf
             3082  LOAD_STR                 'Error: Please check Common AES key len'
             3084  CALL_METHOD_1         1  '1 positional argument'
             3086  POP_TOP          

 L. 266      3088  LOAD_STR                 'Error: Please check Common AES key len'
             3090  RETURN_VALUE     
           3092_0  COME_FROM          3076  '3076'
           3092_1  COME_FROM          2362  '2362'
           3092_2  COME_FROM          2352  '2352'
           3092_3  COME_FROM          1816  '1816'
           3092_4  COME_FROM          1798  '1798'

 L. 268      3092  LOAD_GLOBAL              bflb_utils
             3094  LOAD_METHOD              printf
             3096  LOAD_STR                 'Following will be burned:\r\n'
             3098  LOAD_FAST                'tips'
             3100  BINARY_ADD       
             3102  CALL_METHOD_1         1  '1 positional argument'
             3104  POP_TOP          

 L. 269      3106  LOAD_FAST                'fp'
             3108  LOAD_METHOD              close
             3110  CALL_METHOD_0         0  '0 positional arguments'
             3112  POP_TOP          

 L. 270      3114  LOAD_GLOBAL              bflb_efuse_boothd_create
             3116  LOAD_METHOD              efuse_create_process
             3118  LOAD_FAST                'chip_name'
             3120  LOAD_FAST                'chip_type'
             3122  LOAD_FAST                'cfg_file'
             3124  LOAD_FAST                'efuse_data'
             3126  CALL_METHOD_4         4  '4 positional arguments'
             3128  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 3074_0