import os

def parse(text, start, char):
  i = start
  returnVal = ""
  while text[i] != char:
    returnVal += text[i]
    i += 1
  return returnVal


class Decoder:
  def __init__(self, filename):
    self.number = None
    self.slashnum = None
    self.filename = filename
  def num(self, number):
    if not isinstance(number, int) or number < 1:
      raise TypeError("Enter correct input (positive integer)")
    self.number = number
  def check_file(self):
    if not self.filename[-4:] == ".nme":
      raise TypeError("Wrong File Type")
    return os.path.isfile(self.filename)
  def file_contents(self):
    with open(self.filename, 'r') as file:
      content = file.readlines()
    returnval = content[self.number]
    self.slashnum = int(content[0])
    return returnval
  def decode(self):
    if not self.check_file():
      raise FileNotFoundError(self.filename)
    contents = self.file_contents()
    lst = []
    i = 0
    for j in range(0, self.slashnum):
      text = parse(contents, i, "/")
      lst.append(text)
      i += len(text) + 1
    return lst

def NME_Decode_Line(filename, number):
  dcdr = Decoder(filename)
  dcdr.num(number)
  return dcdr.decode()
def NME_Decode_File(filename):
  kale = Decoder(filename)
  if not kale.check_file():
    raise FileNotFoundError(self.filename)
  with open(filename, 'r') as file:
    length = len(file.readlines())
  lists = []
  for i in range(1, length):
    lists.append(NME_Decode_Line(filename, i))
  return lists

def NME_Encode_File(filename, data):
    with open(filename, 'w') as file_contents:
        if len(data) != 0:
            file_contents.write(str(len(data[0])))
            for line in data:
                text = ''
                for item in line:
                    item = str(item)
                    if len(item) == 0:
                        text += '/'
                    else:
                        if '/' in item:
                            raise ValueError('NME files do not support /')
                        text += item
                        text += '/'
                file_contents.write('\n' + text)

