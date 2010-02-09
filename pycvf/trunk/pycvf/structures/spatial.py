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
from pycvf.core.errors import *
from pycvf.core.structure import ModelStructure
import itertools
from itertools import *
import numpy

def unit(n,d):
  v=numpy.zeros(n,dtype=int)
  v[d]=1
  return v

def patch(ary,pos,sz):
    print "P"
    print "PPOS=",pos
    print "PSZ=",sz
    pycvf_warning("PATCH")
    off=sum(map(lambda x,y,z:x*(y%z),ary.strides,pos,ary.shape))
    print off
    r=numpy.ndarray(buffer=buffer(ary.data,off,len(ary.data)-off) ,shape=sz, strides=ary.strides, dtype=ary.dtype )
    print "/P"
    return r

def set_patch(ary,pos,sz,value):
    for x in numpy.ndindex(sz):
      ary[pos+x]=value[x]
    return ary

def patches(ary,patsz):
    s0=ary.shape
    ns=reduce(lambda x,y: x+[y[0]//y[1],y[1]],zip(ary.shape,patsz),[])
    ary=ary.reshape(ns)
    for i in range(ary.ndim//2):
         ary=ary.swapaxes(i,2*i)
    #for i in range(ary.ndim//4):
    #     ary=ary.swapaxes(ary.ndim//2+i,ary.ndim//2+2*i)
    ary=ary.swapaxes(ary.ndim//2,ary.ndim//2+1)
         #ary=ary.swapaxes(2*i+1, ary.ndim//2+i)
    ns=(reduce(lambda x,y: x*(y[0]//y[1]),zip(s0,patsz),1) ,) + tuple(patsz)
    print ns, ary.shape 
    return ary.reshape(ns)

class DefaultStructure(ModelStructure):
  ##
  ## BASIC CONSTRUCTION
  ##
  def __init__(self,layersdim=0):
     self.layersdim=layersdim
  def output_datatype(self,datatype):
     from pycvf.datatypes import basics
     if (self.layersdim==0):
        return basics.Float.Datatype
     else:
        return basics.NumericVector.Datatype
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

  def items(self, instance):
      return itertools.izip(self.keys(instance),self.values(instance,1))
     
     
  ##
  ## values is an iterator or an array
  ##s
  def recompose(self,shape, values):
     #
     if (type(values) == list):
       values=numpy.vstack(map(lambda x:x[0],values))
     assert(type(values)==numpy.ndarray)
     return values.reshape(shape)  

  ##
  ## DISTANCE IN-BETWEEN TO POSITIONS
  ## 
  def distance(self,instance,x1,x2):
     """ distance in between positions """
     return numpy.linalg.norm(numpy.array(x1)-numpy.array(x2))

 
 
 
class Subdivide(ModelStructure):
  """
  Subdivide an image according to a division structure...
  """
  ##
  ## BASIC CONSTRUCTION
  ##
  def __init__(self,subdivide=(2,2,1)):
     self.subdivide=subdivide
  def output_datatype(self,datatype):
      return datatype
  @classmethod
  def return_flat_datatype(cls):
     return True
  ##
  ## INSTANCE FOR ALGORITHMS
  ##
  def instantiate_element(self,shape,cshape,dtype):
     """ instantiate a target element"""
     return numpy.ndarray(self.subdivide,dtype=dtype)

  def instantiate_array(self,shape,dtype):
     """ instantiate an array with same geometry as the example objects """
     return numpy.ndarray(self.subdivide,dtype=dtype)

  ##
  ## SHAPE RELATED ISSUES
  ##
  def shape(self,instance):
     return self.subdivide
  
  def cshape(self,instance):
     return tuple(map(lambda x,y:x//y,instance.shape,self.subdivide))


  ##
  ## ITERATE POSITIONS (KEYS)
  ## RETURN TYPE=VECTOR OR ITERATOR
  def keys(self,instance):
     return numpy.ndindex(self.subdivide)


  ##
  ## EXTRACT 1 POSITION
  ## RETURN TYPE=VECTOR
  def getitem(self,instance,pos):
     nshp=tuple(zip(self.shape(),self.cshape()))
     x=instance.reshape(*nshp)
     for i in range(instance.ndim):
         x.swapaxis(2*i+1, 2*instance.ndim-i)     
     return x[pos]


  ##
  ## EXTRACT ALL POSITIONS (VALUES)
  ## RETURN TYPE=ARRAY OR ITERATOR
  def values(self, instance):
      return patches(instance,map(lambda x,y: x//y,instance.shape, self.subdivide))

  def items(self, instance):
      return itertools.izip(self.keys(instance),self.values(instance))     
     
  ##
  ## values is an iterator or an array
  ##
  def recompose(self,shape, values):
     values=numpy.array(values)
     assert(False)
     return values.reshape(shape)

  ##
  ## DISTANCE IN-BETWEEN TO POSITIONS
  ## 
  def distance(self,instance,x1,x2):
     """ distance in between positions """
     return numpy.linalg.norm(numpy.array(x1)-numpy.array(x2)) 
 

class RegularPatches(DefaultStructure):
     """
     Decompose and recompose arrays into regular boxes...
     """
     def __init__(self, layersdim=1, patchsize=(4,4), *args, **kwargs):
         DefaultStructure.__init__(self,*args,**kwargs)
         self.patchsize=patchsize
         self.layersdim=layersdim
     def output_datatype(self,datatype):
        return datatype
     def shape(self,instance):
         sz=tuple(map(lambda x,y:x//y,DefaultStructure.shape(self,instance),self.patchsize))+(1,)*(self.layersdim)
         print "SZ=",sz
         return sz
     def keys(self, instance):
         return numpy.ndindex(self.shape(instance))
     def values(self,instance):
         return map(lambda x:patch(instance,map(lambda c,d:c*d,x,self.patchsize+(1,)*self.layersdim),self.patchsize+(instance.shape[-self.layersdim:] if self.layersdim else () )),self.keys(instance))
     def items(self, instance):
        return itertools.izip(self.keys(instance),self.values(instance))
     def recompose(self,instance,values):
         r=numpy.zeros(shape=instance.shape,dtype=instance.dtype)
         al=addresses(instance)
         for a in range(len(al)):
           set_patch(r,al[a],self.patchsize, v[a] )
         return r
     
     
class RegularPatchEdges(DefaultStructure):
     """
     Decompose and recompose arrays into regular boxes...
     """
     def __init__(self, layersdim, patchsize=(4,4),edge_dim=0, *args, **kwargs):
         DefaultStructure.__init__(self,*args,**kwargs)
         self.patchsize=patchsize
         self.layersdim=layersdim
         self.edge_dim=edge_dim
         self.edgesize=list(self.patchsize)
         self.edgesize[edge_dim]*=2
     def output_datatype(self,datatype):
        return datatype
     def shape(self,instance):
         sz=map(lambda x,y:x//y,DefaultStructure.shape(self,instance),self.patchsize)+[1]*(self.layersdim)
         sz[self.edge_dim]-=1         
         return tuple(sz)
     def keys(self, instance):
         return numpy.ndindex(self.shape(instance))    
     def values(self,instance):

         print "V,",instance
         print self.edgesize
         print instance.shape[-self.layersdim:]
         v1=self.patchsize+(1,)*self.layersdim
         print "v1=", v1
         
         v2=tuple(self.edgesize)+(instance.shape[-self.layersdim:] if self.layersdim!=0 else ())
         print "v2=",v2
         return map(lambda x:patch(instance,map(lambda c,d:c*d,x,v1),v2 ),self.keys(instance))

     
         r=map(lambda x:patch(instance,map(lambda c,d:c*d,x,v1),v2),self.keys(instance))
         print "RET"
         return instance
         print "/V"
         return r
     def items(self, instance):
        return itertools.izip(self.keys(instance),self.values(instance))
     def recompose(self,instance,values):
         r=numpy.zeros(shape=instance.shape,dtype=instance.dtype)
         al=addresses(instance)
         for a in range(len(al)):
           set_patch(r,al[a],self.edgesize, v[a] )
         return r     


     
     
     
     

class Elements(DefaultStructure):
     """
      Simplest topology that returns "Elements" such as pixels.
     """
     @classmethod
     def return_flat_datatype(cls):
        return True
     def __init__(self, *args, **kwargs):
         super(Elements,self).__init__(*args,**kwargs)
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

class DirectEdges(DefaultStructure):
     """ Vosinage , Topologie et Contraintes...."""
     @classmethod
     def return_flat_datatype(cls):
        return True
     def __init__(self,d, *args, **kwargs):
         super(Elements,self).__init__(*args,**kwargs)
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

class ReverseEdges(DefaultStructure):
     """ Vosinage , Topologie et Contraintes...."""
     @classmethod
     def return_flat_datatype(cls):
        return True
     def __init__(self,d, *args, **kwargs):
         super(Elements,self).__init__(*args,**kwargs)
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


     

     
#################################################################################################################################################
#################################################################################################################################################
#################################################################################################################################################

     
     
class Ball(DefaultStructure):
     """ At each position returns a ball ...."""
     @classmethod
     def return_flat_datatype(cls):
        return True
     def __init__(self,structure,instance):
       super(Elements,self).__init__(*args,**kwargs)
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
     
     
class Blocks(DefaultStructure):
     """ Vosinage , Topologie et Contraintes...."""
     @classmethod
     def return_flat_datatype(cls):
        return True
     def __init__(self,structure,instance,blocksz, interleave=None):
       super(Elements,self).__init__(*args,**kwargs)
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

class ABall():
     """ Vosinage , Topologie et Contraintes...."""
     @classmethod
     def return_flat_datatype(cls):
        return True
     def __init__(self,structure,instance):
         super(Elements,self).__init__(*args,**kwargs)
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



#class ImageStructure(SpatialStructure):
#  def extract_all(self, instance):
#    assert(instance.ndim<=3)
#    return SpatialStructure.extract_all(self,instance)