from nme import NME_Decode_File, NME_Encode_File
import os

"""
User is stored as:
Username/Cash/Stock1/Stock2/Stock3/Stock4/Stock5/
    0     1     2      3      4      5      6
NME slashnum = 7

"""
class User:
    def __init__(self):
        self.user_file  = []
    
    def Import_From_NME(self):
        if os.path.isfile('users.nme'):
            self.user_file = NME_Decode_File('users.nme')
        else:
            with open('users.nme', 'w') as file_contents:
                file_contents.write(str(7) + '\n')
            self.Import_From_NME()

k = User()
k.Import_From_NME()
print(k.user_file)
