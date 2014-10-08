import numpy as np
import bisect

def getPrintTagLenght(): return 25

def returnPrintTag(intag): return intag.ljust(getPrintTagLenght())[0:getPrintTagLenght()]

def returnPrintPostTag(intag): return intag.ljust(getPrintTagLenght()-15)[0:(getPrintTagLenght()-15)]

def partialEval(s):
  try:
    r = int(s)
    return r
  except ValueError:
    pass
  try:
    r = float(s)
    return r
  except ValueError:
    pass
  return s

def toString(s):
  if type(s) == type(""):
    return s
  else:
    return s.decode()
    
def toBytes(s):
  if type(s) == type(""):
    return s.encode()
  elif type(s).__name__ in ['unicode','str','bytes']: return bytes(s)
  else:
    return s

def toBytesIterative(s):
  if type(s) == list: return [toBytes(x) for x in s]
  elif type(s) == dict:
    if len(s.keys()) == 0: return None
    tempdict = {}
    for key,value in s.items(): tempdict[toBytes(key)] = toBytesIterative(value)
    return tempdict
  else: return toBytes(s) 

def toStrish(s):
  if type(s) == type(""):
    return s
  elif type(s) == type(b""):
    return s
  else:
    return str(s)

def convertDictToListOfLists(inputDict):
  if type(inputDict) == dict:
    returnList = [[],[]]
    for key, value in inputDict.items():
      returnList[0].append(key)
      if type(value) == dict: returnList[1].append(convertDictToListOfLists(value))
      else: returnList[1].append(value)
  else:   
    print(returnPrintTag('UTILS') + ': '+returnPrintPostTag('WARNING')+ ' -> in method "convertDictToListOfLists", inputDict is not a dictionary!')
    returnList = None
  return returnList


def convertNumpyToLists(inputDict):
  returnDict = inputDict
  if type(inputDict) == dict:
    for key, value in inputDict.items():
      if   type(value) == np.ndarray: returnDict[key] = value.tolist() 
      elif type(value) == dict      : returnDict[key] = (convertNumpyToLists(value))
      else                          : returnDict[key] = value 
  elif type(inputDict) == np.ndarray:
    returnDict = inputDict.tolist()  
  return returnDict


def keyIn(dictionary,key):
  """Returns the key or toBytes key if in,
  else returns none.  Use like
  inKey = keyIn(adict,key)
  if inKey is not None:
     foo = adict[inKey]
  else:
     pass #not found"""
  if key in dictionary:
    return key
  else:
    bin_key = toBytes(key)
    if bin_key in dictionary:
      return bin_key
    else:
      return None

def first(c):
  """Returns the first element of collections,
  for a list this is equivalent to c[0], but this also
  work for things that are views"""
  return next(iter(c))

def importFromPath(filename, printImporting = True):
    if printImporting: print(returnPrintTag('UTILS') + ': '+returnPrintPostTag('Message')+ '-> importing module '+ filename)
    import imp, os.path
    try:
      (path, name) = os.path.split(filename)
      (name, ext) = os.path.splitext(name)
      (file, filename, data) = imp.find_module(name, [path])
      importedModule = imp.load_module(name, file, filename, data)
    except: importedModule = None   
    return importedModule

def index(a, x):
    'Locate the leftmost value exactly equal to x'
    i = bisect.bisect_left(a, x)
    if i != len(a) and a[i] == x: return i
    return None

def find_lt(a, x):
    'Find rightmost value less than x'
    i = bisect.bisect_left(a, x)
    if i: return a[i-1],i-1
    return None,None

def find_le_index(a,x):
    'Find the index of the rightmost value less than or equal to x'
    i = bisect.bisect_right(a, x)
    if i: return i
    return None
  
def find_le(a, x):
    'Find rightmost value less than or equal to x'
    i = bisect.bisect_right(a, x)
    if i: return a[i-1],i-1
    return None,None

def find_gt(a, x):
    'Find leftmost value greater than x'
    i = bisect.bisect_right(a, x)
    if i != len(a): return a[i],i
    return None,None

def find_ge(a, x):
    'Find leftmost item greater than or equal to x'
    i = bisect.bisect_left(a, x)
    if i != len(a): return a[i],i
    return None,None 

def metaclass_insert(metaclass,*base_classes):
  """This allows a metaclass to be inserted as a base class.
  Metaclasses substitute in as a type(name,bases,namespace) function,
  and can be anywhere in the hierarchy.  This instantiates the 
  metaclass so it can be used as a base class.
  Example use:
  class Foo(metaclass_insert(Metaclass)):
  This function is based on the method used in Benjamin Peterson's six.py
  """
  namespace={}
  return metaclass("NewMiddleMeta",base_classes,namespace)

class abstractstatic(staticmethod):
  """This can be make an abstract static method
  import abc
  class A(metaclass_insert(abc.ABCMeta)):
    @abstractstatic
    def test():
      pass
  class B(A):
    @staticmethod
    def test():
      return 5
  """
  def __init__(self, function):
    super(abstractstatic, self).__init__(function)
    function.__isabstractmethod__ = True
  __isabstractmethod__ = True
