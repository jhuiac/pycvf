# -*- coding: utf-8 -*-

from pycvf.core.errors import pycvf_debug, pycvf_warning

class CachedIndex():
    def __init__(self,idx_class,filename,idx_factory=None,verbose=True):
      if idx_factory==None:
        idx_factory=lambda : idx_class()
      try: 
         self.idx=idx_class.load(filename)
         pycvf_debug(10,"index "+filename+"sucessfully loaded !!!")
         self.dirty=False
      except Exception,e:
         pycvf_debug(10,"failed to load "+filename+"..."+str(e))
         pycvf_debug(10,"creating new index "+filename+"...")
         self.idx=idx_factory()
         self.dirty=True
      self.filename=filename
    def __del__(self):
      self.save()
    def save(self):
      if (self.dirty):
         pycvf_debug(10,"saving index "+self.filename+"...")
         try:
           self.idx.save(self.filename)
         except TypeError:
           pycvf_warning("Strange, strange, strange ... it seems that your index class "+str(type(self.idx))+(str(self.idx))+" does not accept a name while saving ")
           self.idx.save()
           pycvf_debug(20,"cache save without name done")
         self.dirty=False
    def add(self,key,value,*args, ** kwargs):
      self.idx.add(key,value,*args, ** kwargs)
      self.dirty=True
    def add_many(self,keys,values,*args, ** kwargs):
      self.idx.add(keys,values,*args, ** kwargs)
      self.dirty=True
    def recompute(self):
      self.idx.recompute()
      self.dirty=True
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
      return self.idx.keys()
    def values(self):
      return self.idx.values()
    def reset(self):
      return self.idx.reset()
    def commit(self):
      return self.idx.commit()

__call__=CachedIndex