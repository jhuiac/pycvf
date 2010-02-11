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
import itertools,numpy


from pycvf.core.structure import ModelStructure

def try_getitem(e,i):
  #try:
     return e[i]
  #except:
  #   return None

class ReaderStructure(ModelStructure):
  ## ITERATE_POS
  ## EXTRACT_POS
  ## EXTRACT_ALL
  ## CONTENTS
  @staticmethod
  def output_datatype(datatype):
      from pycvf.datatypes import image
      from pycvf.datatypes import video
      if (datatype==video.Datatype):
          return image.Datatype
      return datatype
  def __init__(self,use_itertools=True):
     self.use_itertools=use_itertools
  def shape(self,instance):
     l=len(instance)
     if (l==0):
       from pycvf.core.errors import pycvf_warning
       pycvf_warning("len of reader equal 0, strange, (debug return 1000 instead")
       return 1000
     return l
  def cshape(self,instance):
     return (1,)
  def iterate(self,instance):
     return range(len(instance))
  def extract(self,instance,pos):
     return instance[pos]
  def extract_all(self, instance):
      if (self.use_itertools):
        return itertools.imap(lambda x: try_getitem(instance,x),range(self.shape(instance)))
      else:
        return map(lambda x: instance[x],range(self.shape(instance)))
  def instantiate_map(self,shp,dtype):
      return numpy.zeros(shp,dtype=dtype)
  def map(self,f,instance):
       im=self.instantiate_map(self.shape(instance),object)
       for k in  range(len(instance)) :
          im[k]=f(instance[k])
       return im
  def items(self,instance):
      for x in iter(instance):
        yield (None,x)
#itertools.izip(
#  def recompose_all(self,list):
#     return SequenceReader(instance)
  def distance(self,x1,x2):
     return x1-x2




  class CliqueSetElements():
     def __init__(self,structure,instance):
       self.structure=structure
       self.instance=instance
     def addresses(self):
         return range(len(self.instance))
     def cliques(self,x):
        ### normally returns clique associated with one position : here degenerated
        return  x 
     def extract_all(self):
        return map(lambda x:self.instance[self.cliques(x)],self.addresses())
     def extract_all_rec(self):
        return map(lambda x:map(self.instance.__getitem__,self.cliques(x)),numpy.ndindex(self.instance.shape))
     def iterate_all(self):
        return numpy.ndindex(self.instance.shape)
     def recompose_all(self,v):
         return SequenceReader(v)

  class CliqueSetIElements():
     def __init__(self,structure,instance):
       self.structure=structure
       self.instance=instance
     def addresses(self):
         return range(len(self.instance))
     def cliques(self,x):
        ### normally returns clique associated with one position : here degenerated
        return [  x ]
     def extract_all(self):
        return map(lambda x:map(lambda e:self.instance[f],self.cliques(x)),self.addresses())
     def extract_all_rec(self):
        return map(lambda x:map(self.instance.__getitem__,self.cliques(x)),numpy.ndindex(self.instance.shape))
     def iterate_all(self):
        return numpy.ndindex(self.instance.shape)
     def recompose_all(self,v):
         return SequenceReader(v)



  class CliqueSetIIElements():
     def __init__(self,structure,instance):
       self.structure=structure
       self.instance=instance
     def addresses(self):
         return range(len(self.instance))
     def cliques(self,x):
        return [  [x] ]
     def extract_all(self):
        return map(lambda x:map(lambda e:map(lambda f:self.instance[f],e),self.cliques(x)),self.addresses())
     def extract_all_rec(self):
        return map(lambda x:map(self.instance.__getitem__,self.cliques(x)),numpy.ndindex(self.instance.shape))
     def iterate_all(self):
        return numpy.ndindex(self.instance.shape)
     def recompose_all(self,v):
         return SequenceReader(v)



