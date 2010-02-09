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

def patch(ary,pos,sz):
    off=sum(map(lambda x,y,z:x*(y%z),ary.strides,pos,ary.shape))
    return numpy.ndarray(buffer=buffer(ary.data,off,len(ary.data)-off) ,shape=sz, strides=ary.strides, dtype=ary.dtype )


def set_patch(ary,pos,sz,value):
    for x in numpy.ndindex(sz):
      ary[pos+x]=value[x]
    return ary

class SpatialStructure(ModelStructure):
  ###
  ### Where Variable are supposed to be located
  ###
  ## ITERATE_POS
  ## EXTRACT_POS
  ## EXTRACT_ALL
  ## CONTENTS 
  def output_datatype(self,datatype):
     from pycvf.datatypes import basics
     if (self.layersdim==0):
        return basics.FloatDatatype
     else:
        return basics.NumericVectorDatatype
  def __init__(self,layersdim=0):
     self.layersdim=layersdim
  def instantiate(self,shape,dtype):
     return numpy.ndarray(shape=shape,dtype=dtype)
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
      x=instance.reshape(reduce(lambda x,y:x*y,self.shape(instance),1), *self.cshape(instance))
      #print x.shape
      return x
  def recompose_all(self,instance):
     return instance.reshape(reduce(lambda x,y:x*y,instance.shape,1),1)  
  def distance(self,x1,x2):
     return numpy.linalg.norm(numpy.array(x1)-numpy.array(x2))

  class CliqueRegularPatches():
     def __init__(self,structure,instance, shape):
       self.structure=structure
       self.instance=instance
       self.ps=shape
     def addresses(self):
         return numpy.ndindex(map(lambda x,y:x//y,self.instance.shape,self.ps))
     def cliques(self,x):
        return [  patch(x,self.ps)  ]
     def extract_all(self):
        return map(lambda x:map(self.instance.__getitem__,self.cliques(x)),self.addresses(self.instance))
     def iterate_all(self):
         for i in self.addresses(self):
            return self.cliques[x][0]
     def recompose_all(self,v):
         r=numpy.zeros(shape=self.instance.shape,dtype=self.instance.dtype)
         al=self.addresses()
         for a in range(len(al)):
           set_patch(r,al[a],self.ps, v[a] )
         return r

  class CliqueElements():
     def __init__(self,structure,instance):
       self.structure=structure
       self.instance=instance
     def addresses(self):
         return numpy.ndindex(self.instance.shape)
     def cliques(self,x):
        return [  numpy.array[x] ]
     def extract_all(self):
        return map(lambda x:map(self.instance.__getitem__,self.cliques(x)),numpy.ndindex(self.instance.shape))
     def extract_all_rec(self):
        return self.instance.flat
     def iterate_all(self):
        return numpy.ndindex(self.instance.shape)
     def recompose_all(self,v):
         return v.reshape(self.instance.shape)

  class CliqueSetD():
     """ Vosinage , Topologie et Contraintes...."""
     def __init__(self,structure,instance,d):
       self.structure=structure
       self.instance=instance
       self.d=d
     def addresses(self):
         return numpy.ndindex(tuple(map(lambda x,y:x-y, self.instance.shape,unit(self.instance.ndim,self.d))))
     def cliques(self,x):
        return [ tuple(numpy.array(x,dtype=int)+unit(self.instance.ndim,self.d))]
     def extract_all(self):
        print "shape=",self.instance.shape, type(self.instance)
        print "shape[0]",self.instance[0,0].shape
        return map(lambda x:map(self.instance.__getitem__,self.cliques(x)),
                                numpy.ndindex(tuple(map(lambda x,y:x-y, self.instance.shape,unit(self.instance.ndim,self.d)))))
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
     def addresses(self):
         return numpy.ndindex(tuple(map(lambda x,y:x-y, self.instance.shape,unit(self.instance.ndim,self.d))))
     def cliques(self,x):
        return [ tuple(numpy.array(x,dtype=int)-unit(self.instance.ndim,self.d))]
     def extract_all(self):
        return numpy.array(map(lambda x:map(self.instance.__getitem__,self.cliques(x)),self.addresses()))
     def extract_all_rec(self):
        return numpy.array(zip(self.instance.flat, numpy.roll(self.instance,1,axis=self.d).flat))
     def iterate_all(self):
        return itertools.imap(lambda x:map(self.instance.__getitem__,self.cliques(x)),numpy.ndindex(tuple(map(lambda x,y:x-y, self.instance.shape,unit(self.instance.ndim,self.d)))))
     def recompose_all(self,v):
         return v.reshape(self.instance.shape)


  class CliqueSetVN():
     """ Vosinage , Topologie et Contraintes...."""
     def __init__(self,structure,instance):
       self.structure=structure
       self.instance=instance
     def addresses(self):
         szi=tuple(map(lambda x,y:x-y,self.instance.shape[:-self.structure.layersdim],numpy.ones((self.instance.ndim-self.structure.layersdim,))))
         #print "szi", szi
         return [x for x in numpy.ndindex(szi)]
     def cliques(self,x):
        return [ tuple(numpy.array(x,dtype=int)+unit(self.instance.ndim,self.d))]
     def extract_all(self):
        return numpy.array(map(lambda x:map(self.instance.__getitem__,self.cliques(x)),self.addresses()))
     def extract_all_rec(self):
        l=[numpy.roll(self.instance,-1,axis=d).flat for d in range(self.instance.ndim) ] +[numpy.roll(self.instance,1,axis=d).flat for d in range(self.instance.ndim) ]
        return numpy.array(zip(self.instance.flat, *l))
     def iterate_all(self):
        return itertools.imap(lambda x:map(self.instance.__getitem__,self.cliques(x)),numpy.ndindex(tuple(map(lambda x,y:x-y, self.instance.shape,unit(self.instance.ndim,d)))))
     def recompose_all(self,v):
         return v.reshape(self.instance.shape)
     
     
  class CliqueSetBlocks():
     """ Vosinage , Topologie et Contraintes...."""
     def __init__(self,structure,instance,blocksz, interleave=None):
       self.structure=structure
       self.instance=instance
       self.blocksz=numpy.array(blocksz)
       if (not interleave):
          interleave=blocksz
       self.interleave=numpy.array(interleave)
     def cliques(self,x):
        base=numpy.array(x) * self.interleave 
        return [ base + d for d in numpy.ndindex(blocksz) ]
     def extract_all(self):
        return numpy.array(map(lambda x:map(self.instance.__getitem__,self.cliques(x)),numpy.ndindex(tuple(map(lambda x,y:(x-y)/z,self.instance.shape,self.blocksz.flat,self.interleave)))))
     def extract_all_rec(self):
        return numpy.array(map(lambda x:map(self.instance.__getitem__,self.cliques(x)),numpy.ndindex(tuple(map(lambda x,y:(x-y)/z,self.instance.shape,self.blocksz.flat,self.interleave)))))         
     def iterate_all(self):
        return itertools.imap(lambda x:map(self.instance.__getitem__,self.cliques(x)),numpy.ndindex(tuple(map(lambda x,y:(x-y)/z,self.instance.shape,self.blocksz.flat,self.interleave))))
     def recompose_all(self,v):
        return v.reshape(self.instance.shape)

  class CliqueSetVL():
     """ Vosinage , Topologie et Contraintes...."""
     def __init__(self,structure,instance):
       self.structure=structure
       self.instance=instance
     def addresses(self):
         numpy.ndindex(tuple(map(lambda x,y:x-y,self.instance.shape,unit(self.instance.ndim,d))))
     def cliques(self,x):
        return [ tuple(numpy.array(x,dtype=int)+unit(self.instance.ndim,self.d))]
     def extract_all(self):
        return numpy.array(map(lambda x:map(self.instance.__getitem__,self.cliques(x)),self.addresses()))
     def extract_all_rec(self):
        ndim=self.instance.ndim-self.structure.layersdim
        l=[reduce(lambda x,d:numpy.roll(x,p[d]-1,axis=d),range(ndim),self.instance).flat for p in numpy.ndindex((3,)*(ndim)) ]
        return numpy.array(zip(*l))
     def iterate_all(self):
        return itertools.imap(lambda x:map(self.instance.__getitem__,self.cliques(x)),numpy.ndindex(tuple(map(lambda x,y:x-y, self.instance.shape,unit(self.instance.ndim,d)))))
     def recompose_all(self,v):
         return v.reshape(self.instance.shape)



class ImageStructure(SpatialStructure):
  def extract_all(self, instance):
    assert(instance.ndim<=3)
    return SpatialStructure.extract_all(self,instance)