import math
import ast
import os
from users import User

def valid_input(question, max):
  while True:
    answer = input(question)
    try: #Checks if it is an integer
      answer = int(answer)
    except:
      print("Please enter a valid input")
      continue
    if answer < 0 or answer > max or answer - round(answer) != 0: #Checks whether the integer is correct
      print("Please enter a valid input")
      continue
    break
  return answer

class Stock:
  def __init__(self, name):
    self.buy_orders = []
    self.sell_orders = []
    self.name = name
    self.users = User()
    self.users.Import_From_NME()
    if os.path.exists(f'{name}.txt'): self.read_stock_from_file()
    else: self.write_stock_to_file()

  def read_stock_from_file(self):
    with open(f'{self.name}.txt', 'r') as text:
      k = text.readlines()
      self.buy_orders = ast.literal_eval(k[0])
      self.sell_orders = ast.literal_eval(k[1])
  
  def place_buy_order(self, user, amount, price):
    if not self.users.Is_User(user):
      print("User doesn't exist")
      return
    if self.users.Enough_Cash(user, 0-(amount * price)):
      if len(self.buy_orders) == 0:
        self.buy_orders.append([user, amount, price])
      else:
        j = 0
        for i, order in enumerate(self.buy_orders):
          if price >= order[2] and j != 1:
            self.buy_orders.insert(i, [user, amount, price])
            j = 1
        if j == 0: self.buy_orders.append([user, amount, price])
      self.write_stock_to_file()
      self.users.Modify_User_Cash(user, 0 - (amount * price))
      self.users.Export_To_NME()
      self.cross_check()
    else:
      print('Not enough cash')

  
  def place_sell_order(self, user, amount, price):
    if not self.users.Is_User(user):
      print("User doesn't exist")
      return
    if self.users.Enough_Stock(user, self.name, 0-amount):
      if len(self.sell_orders) == 0: 
        self.sell_orders.append([user, amount, price])
      else:
        j = 0
        for i, order in enumerate(self.sell_orders):
          if price <= order[2] and j != 1:
            self.sell_orders.insert(i, [user, amount, price])
            j = 1
        if j == 0: 
          self.sell_orders.append([user, amount, price])
      self.write_stock_to_file()
      self.users.Modify_User_Stock(user, self.name, 0 - amount)
      self.users.Export_To_NME()
      self.cross_check()
    else:
      print('Not enough stock')
  
  def market_buy(self, user, amount):
    if not self.users.Is_User(user):
      print("User doesn't exist")
      return
    while amount > 0:
      if len(self.sell_orders) == 0:
        print('No sell orders remaining')
        return
      price = self.sell_orders[0][2]
      change = self.sell_orders[0][1]
      if self.users.Enough_Cash(user, 0-(amount * price)):
        if amount >= change:
          self.place_buy_order(user, change, price)
          amount -= change
        else:
          self.place_buy_order(user, amount, price)
          break
      else:
        print('Not enough cash')
        return
      

  def market_sell(self, user, amount):
    if not self.users.Is_User(user):
      print("User doesn't exist")
      return
    if self.users.Enough_Stock(user, self.name, 0-amount):
      while amount > 0:
        if len(self.buy_orders) == 0:
          print('No buy orders remaining')
          return
        price = self.buy_orders[0][2]
        change = self.buy_orders[0][1]
        if amount >= change:
          self.place_sell_order(user, change, price)
          amount -= change
        else:
          self.place_sell_order(user, amount, price)
          break
    else:
      print('Not enough stock')

  def write_stock_to_file(self):
    with open(f'{self.name}.txt', 'w') as text:
      text.write(str(self.buy_orders) + '\n')
      text.write(str(self.sell_orders))

  def clear_stock(self):
    with open(f'{self.name}.txt', 'w') as text:
      text.write('[]' + '\n')
      text.write('[]')
    self.buy_orders = []
    self.sell_orders = []

  def cross_check(self):
    while True:
      if len(self.buy_orders) == 0 or len(self.sell_orders) == 0: break
      best_sell_price = self.sell_orders[0][2]
      best_buy_price = self.buy_orders[0][2]
      if best_sell_price <= best_buy_price:
        self.complete_transaction()
      else: 
        break
    self.write_stock_to_file()

  def complete_transaction(self):
    buyer = self.buy_orders[0][0]
    seller = self.sell_orders[0][0]
    buy_amount = self.buy_orders[0][1]
    sell_amount = self.sell_orders[0][1]
    buy_price = self.buy_orders[0][2]
    sell_price = self.sell_orders[0][2]
    total = 0
    if sell_amount > buy_amount:
      self.sell_orders[0][1] -= buy_amount
      self.buy_orders.pop(0)
      sold = buy_amount
    elif sell_amount == buy_amount:
      self.sell_orders.pop(0)
      self.buy_orders.pop(0)
      sold = buy_amount
    else:
      self.buy_orders[0][1] -= sell_amount
      self.sell_orders.pop(0)
      sold = sell_amount
    
    total = sold * sell_price
    refund = sold * (buy_price - sell_price)
    #Increase available funds for seller by total and buyer by refund
    #Increase stock for buyer by sold
    self.users.Modify_User_Cash(buyer, refund)
    self.users.Modify_User_Cash(seller, total)
    self.users.Modify_User_Stock(buyer, self.name, sold)
    self.users.Export_To_NME()




users = User()
users.Import_From_NME()
users.Create_User('j')
users.Create_User('k')
users.Export_To_NME()
del users
apple = Stock('apple')
apple.clear_stock()

apple.place_sell_order('h', 6, 10)
apple.place_sell_order('j', 1, 11)
apple.market_buy('k', 7)
#apple.place_buy_order('j', 7, 10)
#apple.market_sell('k', 7)

print(apple.buy_orders)
print(apple.sell_orders)

