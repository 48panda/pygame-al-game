def compare(list1, list2, op):
  if type(list1) == list and type(list2) == list:
    out = []
    for a, b in zip(list1, list2):
      out.append(compare(a, b, op))
    return out
  if type(list1) == list and type(list2) != list:
    out = []
    for a in list1:
      out.append(compare(a, list2, op))
    return out
  if type(list1) != list and type(list2) == list:
    out = []
    for b in list2:
      out.append(compare(list1, b, op))
    return out
  if type(list1) != list and type(list2) != list:
    return op(list1, list2)

def arrayshape(array):
  if type(array) != list:
    return []
  if len(array) == 0:
    return [len(array)]
  return arrayshape(array[0]) + [len(array)]

def toBytes(array):
  if type(array) == int:
    return array.to_bytes(1, byteorder="little")
  else:
    return b"".join([toBytes(i) for i in array])

import copy

copy = copy.deepcopy

class array:
  def __init__(self, image):
    if hasattr(image, "getdata"):
      pixels = list(image.getdata())
      width, height = image.size
      self.data = [pixels[i * width:(i + 1) * width] for i in range(height)]
    else:
      self.data = image
    self.__array_interface__ = {"shape": tuple(arrayshape(self.data)), "typestr":"|i1", "version":1}
  
  def __getitem__(self, sliceArray):
    if type(sliceArray) == int:
      return self.data[sliceArray]
    data = []
    for row in self.data[sliceArray[0]]:
      rw = []
      for pixel in row[sliceArray[1]]:
        rw.append(pixel[sliceArray[2]])
      data.append(rw)
    return array(data)

  def __bytes__(self):
    return toBytes(self.data)

  def __setitem__(self, slicer, setTo):
    for y,row in enumerate(slicer):
      for x,pix in enumerate(row):
        if pix:
          assert len(toBytes(setTo)) == len(toBytes(self.data[y][x])), [self.data[y][x], setTo]
          self.data[y][x] = setTo

  def __gt__(self, other):
    if type(other) == type(self):
      return array(compare(self.data, other.data, lambda x, y: x > y))
    else:
      return array(compare(self.data, other, lambda x, y: x > y))

  def __lt__(self, other):
    if type(other) == type(self):
      return array(compare(self.data, other.data, lambda x, y: x < y))
    else:
      return array(compare(self.data, other, lambda x, y: x < y))

  def __eq__(self, other):
    if type(other) == type(self):
      return array(compare(self.data, other.data, lambda x, y: x == y))
    else:
      return array(compare(self.data, other, lambda x, y: x == y))
  
  def __and__(self, other):
    if type(other) == type(self):
      return array(compare(self.data, other.data, lambda x, y: x and y))
    else:
      return array(compare(self.data, other, lambda x, y: x and y))