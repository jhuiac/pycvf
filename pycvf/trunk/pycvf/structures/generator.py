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
    if (datatype!=None):
      return datatype.ElementType
    else:
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
     return (1,)
  
  def cshape(self,instance):
     return (1,)


  ##
  ## ITERATE POSITIONS (KEYS)
  ## RETURN TYPE=VECTOR OU ITERATOR
  def keys(self,instance):
     it1,it2=tee(instance)
     i=0
     for x in it2:
         yield i
         i+=1


  ##
  ## EXTRACT 1 POSITION
  ## RETURN TYPE=VECTOR
  def getitem(self,instance,pos):
     assert False


  ##
  ## EXTRACT ALL POSITIONS (VALUES)
  ## RETURN TYPE=ARRAY OU ITERATOR
  def values(self, instance):
      it1,it2=tee(instance)
      return it2

  def items(self, instance):
      it1,it2=tee(instance)
      i=0
      for x in it2:
         yield i,it2.next()
         i+=1      
      
     
  ##
  ## values is an iterator or an array
  ##
  def recompose(self,shape, values):
     return iter(values)

  ##
  ## DISTANCE IN-BETWEEN TO POSITIONS
  ## 
  def distance(self,instance,x1,x2):
     """ distance in between positions """
     return x1-x2


