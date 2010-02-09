#!/usr/bin/env python
# -*- coding: utf-8 -*-
## ##########################################################################################################
## 
## This file is released under GNU Public License v3
## See LICENSE File at the top the pycvf tree.
##
## Author : Bertrand NOUVEL / CNRS (2009)
##
##
##
## Revision FILE: $Id$
##
## ###########################################################################################################
## copyright $Copyright$
## @version $Revision$
## @lastrevision $Date$
## @modifiedby $LastChangedBy$
## @lastmodified $LastChangedDate$
#############################################################################################################


# -*- coding: utf-8 -*-
from pycvf.core.structure import ModelStructure
from itertools import *
import numpy

def unit(n,d):
  v=numpy.zeros(n,dtype=int)
  v[d]=1
  return v

class ArrayStructure(ModelStructure):
  def __init__(self,layersdim=0):
     self.layersdim=layersdim
  def shape(self,instance):
     if self.layersdim:
        return instance.shape[:-self.layersdim]
     return instance.shape
  def cshape(self,instance):
     if self.layersdim:
        return instance.shape[-self.layersdim:]
     return (1,)
  def iterate(self,instance):
     if self.layersdim:
        return numpy.ndindex(instance.shape[:-self.layersdim])
     return numpy.ndindex(instance.shape)
  def extract(self,instance,pos):
     return instance[pos]
  def extract_all(self, instance):
      """ extraire tous les elements d'un tableau"""
      if type(instance)==list:
        instance=numpy.vstack(instance)
      return instance.reshape(reduce(lambda x,y:x*y,self.shape(instance),1), *self.cshape(instance))
  def recompose_all(self,instance):
     return instance.reshape(reduce(lambda x,y:x*y,instance.shape,1),1)  
  def distance(self,x1,x2):
     return numpy.linalg.norm(numpy.array(x1)-numpy.array(x2))
  ## 
  ##


  class CliqueSetNeutral():
     """ Vosinage , Topologie et Contraintes...."""
     def __init__(self,structure,instance):
       self.structure=structure
       self.instance=instance
       if (type(self.instance)==list):
           self.instance=numpy.vstack(self.instance)
     def cliques(self,x):
        return self.instance
     def extract_all(self):        
        r=self.instance
        return r
     def extract_all_rec(self):
        return self.instance
     def iterate_all(self):
        return iter([None])
     def recompose_all(self,v):
        return v.reshape(self.instance.shape)



  class CliqueSetFlat():
     """ Vosinage , Topologie et Contraintes...."""
     def __init__(self,structure,instance):
       self.structure=structure
       self.instance=instance
       if (type(self.instance)==list):
           self.instance=numpy.vstack(self.instance)
#       print self.instance.shape
       self.shpprod=reduce(lambda x,y:x*y,self.instance.shape,1)
     def cliques(self,x):
        return self.instance.reshape(1,self.shpprod)
     def extract_all(self):        
        r=self.instance.reshape(1,self.shpprod)
        #print """ r = """,r.shape,r
        return r
     def extract_all_rec(self):
        return self.instance.reshape(1,self.shpprod)
     def iterate_all(self):
        return iter([None])
     def recompose_all(self,v):
        return v.reshape(self.instance.shape)

  class CliqueSetD():
     """ Vosinage , Topologie et Contraintes...."""
     def __init__(self,structure,instance,d):
       self.structure=structure
       self.instance=instance
       self.d=d
     def cliques(self,x):
        return [ tuple(numpy.array(x,dtype=int)+unit(self.instance.ndim,self.d))]
     def extract_all(self):
        return map(lambda x:map(self.instance.__getitem__,self.cliques(x)),numpy.ndindex(tuple(map(lambda x,y:x-y, self.instance.shape,unit(self.instance.ndim,self.d)))))
     def extract_all_rec(self):
        return zip(self.instance.flat, numpy.roll(self.instance,-1,axis=self.d).flat)
     def iterate_all(self):
        return itertools.imap(lambda x:map(self.instance.__getitem__,self.cliques(x)),numpy.ndindex(tuple(map(lambda x,y:x-y, self.instance.shape,unit(self.instance.ndim,self.d)))))
     def recompose_all(self,v):
         return v.reshape(self.instance.shape)

  class CliqueSetI():
     """ Vosinage , Topologie et Contraintes...."""
     def __init__(self,structure,instance,d):
       self.structure=structure
       self.instance=instance
       self.d=d
     def cliques(self,x):
        return [ tuple(numpy.array(x,dtype=int)-unit(self.instance.ndim,self.d))]
     def extract_all(self):
        return numpy.array(map(lambda x:map(self.instance.__getitem__,self.cliques(x)),numpy.ndindex(tuple(map(lambda x,y:x-y, self.instance.shape,unit(self.instance.ndim,self.d))))))
     def extract_all_rec(self):
        return numpy.array(zip(self.instance.flat, numpy.roll(self.instance,1,axis=self.d).flat))
     def iterate_all(self):
        return itertools.imap(lambda x:map(self.instance.__getitem__,self.cliques(x)),numpy.ndindex(tuple(map(lambda x,y:x-y, self.instance.shape,unit(self.instance.ndim,self.d)))))
     def recompose_all(self,v):
         return v.reshape(self.instance.shape)


  def cliques(self,instance,key,*args,**kwargs):
    return eval("self.CliqueSet"+key)(self,instance,*args,**kwargs).cliques

  def cliques_extract_all(self,instance,key,*args,**kwargs):
    return eval("self.CliqueSet"+key)(self,instance,*args,**kwargs).extract_all()

  def cliques_extract_all_rec(self,instance,key,*args,**kwargs):
    return eval("self.CliqueSet"+key)(self,instance,*args,**kwargs).extract_all_rec()

  def cliques_iterate_all(self,instance,key,*args,**kwargs):
    return eval("self.CliqueSet"+key)(self,instance,*args,**kwargs).iterate_all()

