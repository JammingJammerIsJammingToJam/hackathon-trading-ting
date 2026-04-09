from nme import NME_Decode_File, NME_Encode_File
import os

"""
Stocks:
    Apple, Banana, Cherry, Dragonfruit, and Elderflower

User is stored as:
Username/Cash/Stock1/Stock2/Stock3/Stock4/Stock5/
    0     1     2      3      4      5      6
NME slashnum = 7

"""
class User:
    def __init__(self):
        self.user_file  = []
        self.stocks = [None, None, 'Apple', 'Banana', 'Cherry', 'Dragonfruit', 'Elderflower']
    
    def Import_From_NME(self):
        if not os.path.isfile('users.nme'):
            with open('users.nme', 'w') as file_contents:
                file_contents.write(str(7) + '\n')
        self.user_file = NME_Decode_File('users.nme')
        for i, user in enumerate(self.user_file):
            self.user_file[i] = [user[0]] + [int(num) for num in user[1:]]

    def Export_To_NME(self):
        NME_Encode_File('users.nme', self.user_file)

    def Create_User(self, username):
        if not any(user[0] == username for user in self.user_file):
            self.user_file.append([username, 0, 0, 0, 0, 0, 0])
    
    def Enough_Cash(self, username, change):
        if len(self.user_file) == 0:
            raise ValueError('user_file is empty????????????????')

        if change >= 0:
            return True
        else:
            for i, user in enumerate(self.user_file):
                if user[0] == username:
                    return (self.user_file[i][1] + change) >= 0

    def Enough_Stock(self, username, stock, change):
        if len(self.user_file) == 0:
            raise ValueError('user_file is empty????????????????')

        if change >= 0:
            return True
        else:
            for i, user in enumerate(self.user_file):
                if user[0] == username:
                    stock_x = self.stocks.index(stock)
                    return (self.user_file[i][stock_x] + change) >= 0
        
    def Modify_User_Cash(self, username, change):
        if len(self.user_file) == 0:
            raise ValueError('user_file is empty????????????????')

        for i, user in enumerate(self.user_file):
            if user[0] == username:
                if (self.user_file[i][1] + change) >= 0:
                    self.user_file[i][1] += change

    def Modify_User_Stock(self, username, stock, change):
        if len(self.user_file) == 0:
            raise ValueError('user_file is empty????????????????')

        for i, user in enumerate(self.user_file):
            if user[0] == username:
                stock_x = self.stocks.index(stock)
                if (self.user_file[i][stock_x] + change) >= 0:
                    self.user_file[i][stock_x] += change

    

