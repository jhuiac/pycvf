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
import itertools
from itertools import *
import numpy
import scipy.spatial



class DefaultStructure(ModelStructure):
  def __init__(self,layersdim=0):
     self.layersdim=layersdim
  def output_datatype(self,datatype):
    try:
      return datatype.ElementType
    except:
      return None
  @classmethod
  def return_flat_datatype(cls):
     return True
  ##
  ## INSTANCE FOR ALGORITHMS
  ##
  def instantiate_element(self,shape,cshape,dtype):
     """ instantiate a targer element"""
     return numpy.ndarray(shape=shape+cshape,dtype=dtype)

  def instantiate_array(self,shape,dtype):
     """ instantiate an array with same geometry as the example objects """
     return numpy.ndarray(shape=shape,dtype=dtype)

  ##
  ## SHAPE RELATED ISSUES
  ##
  def shape(self,instance):
     return (len(instance),)
  
  def cshape(self,instance):
     return (1,)


  ##
  ## ITERATE POSITIONS (KEYS)
  ## RETURN TYPE=VECTOR OU ITERATOR
  def keys(self,instance):
     return range(len(instance))


  ##
  ## EXTRACT 1 POSITION
  ## RETURN TYPE=VECTOR
  def getitem(self,instance,pos):
     return instance[pos]


  ##
  ## EXTRACT ALL POSITIONS (VALUES)
  ## RETURN TYPE=ARRAY OU ITERATOR
  def values(self, instance, iterator=0):
      if (iterator==1):
         return iter(instance)
      else:
         return instance

  def items(self, instance):
      return itertools.izip(self.keys(instance),self.values(instance,1))
     
     
  ##
  ## values is an iterator or an array
  ##
  def recompose(self,shape, values):
     return map(lambda x:x[0],values)

  ##
  ## DISTANCE IN-BETWEEN TO POSITIONS
  ## 
  def distance(self,instance,x1,x2):
     """ distance in between positions """
     return x1-x2




def unit(n,d):
  v=numpy.zeros(n,dtype=int)
  v[d]=1
  return v

class PointListStructure(ModelStructure):
  def __init__(self,point_extractor_f=lambda x:(x[0],x[1])):
     self.point_extractor_f=point_extractor_f
  def shape(self,instance):
     return (len(instance),)
  def cshape(self,instance):
     return N(1,)
  def iterate(self,instance):
     return range(len(instance))
  def extract(self,instance,pos):
     return instance[pos]
  def extract_all(self, instance):
      return numpy.array(instance,dtype=object)
  def recompose_all(self,instance):
     return instance.tolist()
  def distance(self,x1,x2):
     return abs(x1,x2)

  class CliqueSetD():
     """ Vosinage , Topologie et Contraintes...."""
     def __init__(self,structure,instance,d=2):
       self.structure=structure
       self.instance=instance
       self.d=d
     def cliques(self,x):
        return  [x + y for y in range(self.d)] 
     def extract_all(self):
        return map(lambda x:map(self.instance.__getitem__,self.cliques(x)),range(len(self.instance)-self.d+1))
     def extract_all_rec(self):
        return map(lambda x:map(self.instance.__getitem__,self.cliques(x)),range(len(self.instance)-self.d+1))
     def iterate_all(self):
        return itertools.imap(lambda x:map(self.instance.__getitem__,self.cliques(x)),numpy.ndindex(tuple(map(lambda x,y:x-y, self.instance.shape,unit(self.instance.ndim,self.d)))))
     def recompose_all(self,v):
         return v

  class CliqueSetNP():
     """ Vosinage , Topologie et Contraintes...."""
     def __init__(self,structure,instance,maxdist=1,*args,**kwargs):
       self.structure=structure
       self.instance=instance
       self.maxdist=maxdist
       self.dm=scipy.spatial.distance.squareform(scipy.spatial.distance.pdist(self.instance),*args,**kwargs)
     def cliques(self,x):
        return (self.dm[x]<self.maxdist).nonzero()
     def extract_all(self):
        return map(lambda x:map(self.instance.__getitem__,self.cliques(x)[0]),range(len(self.instance)))
     def extract_all_rec(self):
        return self.extract_all()
     def iterate_all(self):
        return itertools.imap(self.extract_all())
     def recompose_all(self,v):
         return v


  class CliqueSetNNP():
     """ Vosinage , Topologie et Contraintes...."""
     def __init__(self,structure,instance,maxn=3,*args,**kwargs):
       self.structure=structure
       self.instance=instance
       self.maxn=maxn
       self.dm=scipy.spatial.distance.squareform(scipy.spatial.distance.pdist(self.instance),*args,**kwargs)
     def cliques(self,x):
        return scipy.argsort(self.dm[x])[:self.maxn]
     def extract_all(self):
        return map(lambda x:map(self.instance.__getitem__,self.cliques(x)),range(len(self.instance)))
     def extract_all_rec(self):
        return self.extract_all()
     def iterate_all(self):
        return itertools.imap(self.extract_all())
     def recompose_all(self,v):
         return v



  def cliques(self,instance,key,*args,**kwargs):
    return eval("self.CliqueSet"+key)(self,instance,*args,**kwargs).cliques

  def cliques_extract_all(self,instance,key,*args,**kwargs):
    return eval("self.CliqueSet"+key)(self,instance,*args,**kwargs).extract_all()

  def cliques_extract_all_rec(self,instance,key,*args,**kwargs):
    return eval("self.CliqueSet"+key)(self,instance,*args,**kwargs).extract_all_rec()

  def cliques_iterate_all(self,instance,key,*args,**kwargs):
    return eval("self.CliqueSet"+key)(self,instance,*args,**kwargs).iterate_all()
