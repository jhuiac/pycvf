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
##
## Models can be specified either directly either through loading
## filename are resolved by application
##

"""
 Structures (have no direct clique concept yet)

 Algorithm may be based on different structures.

 
"""


import re, os, math, random, time,sys, traceback,logging

from pycvf.lib.info.observations import *
from pycvf.lib.info.cacheable import *
from pycvf.lib.info.track import *
from pycvf.core.errors import *

ltick=0

from pycvf.nodes.structure import *
from pycvf.lib.stats.cachedmodel import CachedModel
class Structure(object):
  """
  """
  anonymous_ctr=0
  name=None

  @classmethod
  def input_datatype(cls,datatype):
     return datatype

  @classmethod
  def output_datatype(cls,datatype):
     return datatype

  def __init__(self,  *args, ** kwargs):
      self.parent=None ## parent node... (to be reseted to node on  delete)
      self.args=args        ## initialize arguments
      self.kwargs=kwargs   ##
      self._input_datatype=None  
      self._output_datatype=None 
      if (self.kwargs.has_key("name")):
           self.name=self.kwargs["name"]
  

  def init(self,application,*args, **kargs):
     self.application=application # the application

  def instantiate_types():
      """
          This function is called to instantantiate the correct structure all 
          along the models 
      """


  ############################################################
  ############################################################
  ############################################################


class ArrayStructure(Structure):
  def init(self):
     if self.kwargs.has_key('layersdim'): 
       self.layersdim=layersdim
     else:
       self.layersdim=0
  
  def output_datatype(self,datatype):
     from pycvf.datatypes import basics
     if (self.layersdim==0):
        return basics.FloatDatatype
     else:
        return basics.NumericVectorDatatype
  
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

  def zeros_array(self,shape,dtype=numpy.float):
     """ instantiate an array with same geometry as the example objects """
     return numpy.zeros(shape,dtype=dtype)

  def ones_array(self,shape,dtype=numpy.float):
     """ instantiate an array with same geometry as the example objects """
     return numpy.ones(shape,dtype=dtype)

  def random_array(self,shape,dtype=numpy.float):
     """ instantiate an array with same geometry as the example objects """
     return numpy.random.random(shape,dtype=dtype)


  ##
  ## SHAPE RELATED ISSUES
  ##
  def shape(self,instance):
     if self.layersdim:
        return instance.shape[:-self.layersdim]
     return instance.shape
  
  def cshape(self,instance):
     if self.layersdim:
        return instance.shape[-self.layersdim:]
     return (1,)


  ##
  ## ITERATE POSITIONS (KEYS)
  ## RETURN TYPE=VECTOR OU ITERATOR
  def keys(self,instance):
     if self.layersdim:
        return numpy.ndindex(instance.shape[:-self.layersdim])
     return numpy.ndindex(instance.shape)


  ##
  ## EXTRACT 1 POSITION
  ## RETURN TYPE=VECTOR
  def getitem(self,instance,pos):
     return instance[pos]


  ##
  ## EXTRACT ALL POSITIONS (VALUES)
  ## RETURN TYPE=ARRAY OU ITERATOR
  def values(self, instance, iterator=0): ## -1 = not possible / 0=don't care / 1=required
      x=instance.reshape(reduce(lambda x,y:x*y,self.shape(instance),1), *self.cshape(instance))
      if (iterator==1):
         return iter(x)
      else:
         return x


  ##
  ## values is an iterator or an array
  ##
  def recompose(self,shape, values):
     assert(type(values)==numpy.ndarray)
     return values.reshape(reduce(lambda x,y:x*y,instance.shape,1),1)  

  ##
  ## DISTANCE IN-BETWEEN TO POSITIONS
  ## 
  def distance(self,instance,x1,x2):
     """ distance in between positions """
     return numpy.linalg.norm(numpy.array(x1)-numpy.array(x2))




## >>> xas=gs.ArrayStructure()
## >>> xas.init()
## >>> xas.shape(scipy.lena())

