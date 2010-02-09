# -*- coding: utf-8 -*-
import sys
import numpy

class PseudoIncrementalIndex():
    def __init__(self,idx_factory):
      self.root_class=idx_factory
      self.idx_factory=idx_factory
      self.idx=None
      self.dirty=False
      self._keys=[]
      self._values=[]
    def reset(self):
      try:
          self.idx.reset()
      except:
          self.idx=None
      self.dirty=False
      self._keys=[]
      self._values=[]        
    def add(self,key,value,*args, ** kwargs):
      self._keys.append(key)
      self._values.append(value)
      self.dirty=True
    def add_many(self,keys,values):
      self._keys.extend(keys )
      self._values.extend(values )
      self.dirty=True
    def recompute(self):
      print "computing index"#, self.keys.shape, self.values.shape
      try:
        keys=numpy.vstack(self._keys)          
      except:
        print self._keys[0]
        print self._keys[1]        
        print set(map(lambda x:type(x),self._keys))          
        print set(map(lambda x:x.shape,self._keys))
      #  print self._keys          
        keys=numpy.array(self._keys)
      try:
        values=numpy.array(self._values)
      except:
        values=numpy.array(self._values,dtype=object)
      self.idx=self.idx_factory()
      self.idx.add_many(keys,values)
    def commit(self):
        if (self.dirty):
            self.recompute()
    def save(self,filename,recompute=False, *args, **xargs):
      if (self.dirty or recompute):
        self.recompute()
      print "saving lowlevel"
      self.idx.save(filename,*args,**xargs)
    def load(self):
      return cls.idx_factory.load
    def __getitem__(self,key):
      return self.idx[key]
    def getitem(self,key,*args,**xargs):
      return self.idx.getitem(key,*args,**xargs)
    def getitems(self,key,*args,**xargs):
      return self.idx.getitems(key,*args,**xargs)
    def __getball__(self,key,radius):
      return self.idx.__getball__(key,radius)
    def getball(self,key,radius,*args,**xargs):
      return self.idx.getball(key,radius,*args, **xargs)
    def keys(self):
      return iter(self._keys)
    def values(self):
      return iter(self._values)

__call__=PseudoIncrementalIndex
