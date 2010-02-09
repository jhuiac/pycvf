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
from pycvf.nodes.structure import ModelStructure
from itertools import *
import numpy

def unit(n,d):
  v=numpy.zeros(n,dtype=int)
  v[d]=1
  return v

class GraphStructure(ModelStructure):
  ## ITERATE_POS
  ## EXTRACT_POS
  ## EXTRACT_ALL
  ## CONTENTS
  def __init__(self,field):
      self.field=field
  def shape(self,instance):
     return instance
  def cshape(self,instance):
     return None
  def iterate(self,instance):
     for n in n.Nodes():
        yield n
  def extract(self,instance,pos):
     return n.extras()[self.field]
  def extract_all(self, instance):
      return map(lambda x:self.extract(instance,x),instance.nodes)
  def recompose_all(self,instance):
      s=instance.copy()
      
  def distance(self,x1,x2):
     assert(False) # NOTY YET IMPLEMENTED
     return numpy.linalg.norm(numpy.array(x1)-numpy.array(x2))
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
  def cliques(self,instance,key,*args,**kwargs):
    return eval("self.CliqueSet"+key)(self,instance,*args,**kwargs).cliques

  def cliques_extract_all(self,instance,key,*args,**kwargs):
    return eval("self.CliqueSet"+key)(self,instance,*args,**kwargs).extract_all()

  def cliques_extract_all_rec(self,instance,key,*args,**kwargs):
    return eval("self.CliqueSet"+key)(self,instance,*args,**kwargs).extract_all_rec()

  def cliques_iterate_all(self,instance,key,*args,**kwargs):
    return eval("self.CliqueSet"+key)(self,instance,*args,**kwargs).iterate_all()
