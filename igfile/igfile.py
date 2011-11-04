from zipfile import ZipFile
import sys
from types import ClassType

nan = None

class IgColumn(object):
  class IgColumnIterator:
    def __init__(self, collection, index):
      self.__collection = collection
      self.__index = index
      self.__num = 0

    def __iter__(self):
      return self

    def next(self):
      try:
        item = self.__collection.data()[self.__num][self.__index]
        self.__num += 1
      except IndexError:
        raise StopIteration
      return item

  def __init__(self, collection, index):
    self.__collection = collection
    self.__index = index

  def __repr__(self):
      return repr([x for x in self])
    
  def __iter__(self):
    return self.IgColumnIterator(self.__collection, self.__index)

class IgCollection:    
  def __init__(self, event, name, schema):
    self.__data = event.data()[name]
    self.__name = name
    self.__schemaIndex = []
    self.__schema = {}
    i = 0
    for k,v in schema:
      self.__schemaIndex.append(k)
      self.__schema[k] = v
      self.__dict__[k] = IgColumn(self, i)
      i += 1

  name = property(lambda self : self.__name)
  
  def column(self, name):
    return self.__dict__[name]
  
  def columns(self):
    for column in self.__schemaIndex:
      yield column
      
  def data(self):
    return self.__data

  def __repr__(self):
    return ",".join(self.__schema.keys())

class IgEvent(object):
  def __init__(self, data, types, collectionNames):
    self.__data = data
    self.__types = types
    self.__collections = dict([ (n, IgCollection(self, n, types[n]))
                                 for n in collectionNames])
  
  def collections(self):
    return self.__collections.itervalues()
  
  def collection(self, label):
    return self.__collections[label]
  
  def types(self):
    return self.__types
  
  def data(self):
    return self.__data["Collections"]

def createEvent(label, text):
  """Create a specialized class for the given event. This class
     will be populated with accessors for all the collections, using the 
     collection name. It will therefore be possible to say:
     
     event.Tracks_V1
     
     or alikes.
  """
  data = eval(text)
  types = data["Types"]
  collectionNames = [ x.split("\":")[0].strip("\"")
                      for x in text.split("\'Types\': {")[1]
                                   .split("\'Collections\'")[0]
                                   .split("\n")
                      if '":' in x]

  eventClass = ClassType(label, (IgEvent,), {})

  obj = eventClass(data, types, collectionNames)
  # We need to use an external maker, because if we use the lambda directly
  # n will be the last item of the iteration for all the lambdas.
  def make_getter(name):
    return lambda o : o.collection(name)
  for n in collectionNames:
    setattr(eventClass, n, property(make_getter(n)))
  return obj
  
class IgArchive:
  def __init__(self, filename):
    if type(filename) == list:
      filename = filename[0]
    self.__file = ZipFile(filename)
    self.__currentEvent = self.getEvent(self.events()[0])

  def events(self):
    return [ x for x in self.__file.namelist() if x.startswith("Events")]

  def __getitem__(self, key):
    if type(key) == int:
      return self.getEvent(self.events()[key])
    else:
      return self.getEvent(key)

  def getEvent(self, eventName):
    self.__currentEvent = createEvent(eventName, self.__file.read(eventName))
    return self.__currentEvent

Leaf = {
  "createIgArchive": lambda filename : IgArchive(filename),
  "test": lambda x : "test"
}
