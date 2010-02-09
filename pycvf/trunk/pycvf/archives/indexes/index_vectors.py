# -*- coding: utf-8 -*-


##
## Ici on ne fait que donner des grandes strategies pour la creation d'index
## le schema specifique a chaque model doit ensuite etre preciser dans le modele


##
## THIS FILE IS ENTIRELY DEPRECATED !!!
##

##
## IndexAll cree des indexes naifs pour chacun des structures
##

#import indexer
try:
   from pycvf.indexes.sashindex import *
except:
  pycvf_warning("Failed to import SASH")

try: 
   from pycvf.indexes.lshindex_opencv import *
except:
  pycvf_warning("Failed to import OPENCV LSH indexing structure")

try: 
   from pycvf.indexes.lshindex_lshkit import *
except:
  pycvf_warning("Failed to import LSHKIT LSH indexing structure")

from pycvf.indexes.pseudoincremental import *
from pycvf.indexes.cachedindex import *
from pycvf.indexes.multiplefeaturesindex import *

def normalize_name(fname):
  print fname
  return filter(lambda c : c in "abcdefghijklmnopqrstuvwxyz0123456789.",fname.replace('|','.'))

def new_sash(x,y):
  s=SashIndex()
  s.add_many(x,y)
  return s

def sashpi():
   r=PseudoIncrementalIndex(new_sash)
   r.load=SashIndex.load
   return r

def new_lsh(x,y):
  s=LshIndex()
  s.add_many(x,y)
  return s

def lshpi():
   r=PseudoIncrementalIndex(new_lsh)
   r.load=LshIndex.load
   return r

def new_lshkit(x,y):
  s=LshKitIndex()
  s.add_many(x,y)
  return s

def lshkitpi():
   r=PseudoIncrementalIndex(new_lshkit)
   r.load=LshKitIndex.load
   return r




class AutoIndex:
  applies_to=-1
  def __init__(self,index_method="sash",index_name="_indexall_"):
      self.index_method=index_method
  def init(self,basepath,vm,observed_features,*args,**kwargs):
     #print args,kwargs,basepath,"?2?",vm,"?3?", observed_features
     self.observed_features=observed_features.copy()
     if self.index_method=="sash":
       self.indexes=[  CachedIndex(
                       SashIndex,
                       sashpi,
                        basepath+ "/sash-"+normalize_name(xf[0])+".idx"
                      )     for xf in observed_features.items() ]
     elif self.index_method=="lsh":
       self.indexes=[  CachedIndex(
                       LshIndex,
                        lshpi,
                        basepath+ "/lsh-"+normalize_name(xf[0])+".idx"
                      )     for xf in observed_features.items()  ]
     elif self.index_method=="lshkit":
       self.indexes=[  CachedIndex(
                       LshKitIndex,
                        lshkitpi,
                        basepath+ "/lshkit-"+normalize_name(xf[0])+".idx"
                      ) for xf in observed_features.items()  ]

     else:
         raise Exception, "Unsupported indexing structure"
  def save(self):
    for i in self.indexes:
       i.save()
  def values(self):
     return self.indexes[0].values()
  def keys(self):
     return self.indexes[0].keys()
  def add(self,key,value):
    #print self.observed_features, len (self.observed_features)
    #print len (self.indexes)
    #print value
    for xf in range(len(self.observed_features)):
       self.indexes[xf].add(key,value)
  def reset(self):
    for i in self.indexes:
       i.reset()
  def commit(self):
    for i in self.indexes:
       i.commit()
  def query(self,values,*args, **kwargs):
    #
    #DEPRECATED FUNCTION -> SIMPLIFIED
    #xf=0
    #print values
    #if (kwargs.has_key("xf")):
    #    xf=kwargs["xf"]
    #    if (xf==-1):
    #       return [ self.indexes[xf].getitems(map(lambda x:x[xf],values) *args, **kwargs) for xf in range(len(self.observed_features)) ]
    return self.indexes[0].getitems(values, *args, **kwargs) 


#def indexschema_init(basepath,vm,mmeta,*args,**kwargs):
#   return AutoIndex(basepath,mmeta,*args,**kwargs)

__call__=AutoIndex
