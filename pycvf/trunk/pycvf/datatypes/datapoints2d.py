# -*- coding: utf-8 -*-
import pylab
import os
import PIL
import PIL.Image
import numpy
from pycvf.lib.graphics.imgfmtutils import *
from pycvf.lib.video.render.lazy import LazyDisplay
from pycvf.lib.ui.qtdisplay import QtDisplay

def palette(x):
    r=0
    b=0
    g=0
    rc=0
    gc=0
    bc=0
    for y in range(6):
      tx=(x>>(3*y))
      rc^=(tx&1)
      r|=rc<<(7-y-0)
      gc^=(tx&2)      
      g|=gc<<(7-y-1)
      bc^=(tx&4)      
      b|=bc<<(7-y-2) 
    return [(256-r)/256.,(256-g)/256.,(256-b)/256.]

if False: 
 class Datapoint2dDatatype:
  content_type="Datapoints"
  dataset=None
  @classmethod
  def display(cls,x):
      f=pylab.figure()
      a=f.gca()
      pylab.scatter(cls.dataset[:,0],cls.dataset[:,1])
      a.scatter([x[0]],[x[1]])
      f.show()
  @classmethod
  def get_numpy(cls,x):
      return numpy.matrix(x)
  @staticmethod
  def pylab_display(cls,x):     
      f=pylab.figure()
      a=f.gca()
      if (cls.dataset):
         a.scatter(cls.dataset[:,0],cls.dataset[:,1],'b')
      a.scatter([x[0]],[x[1]], 'g')
      return f
  @classmethod
  def get_widget(cls,*args):
     q=QtDisplay(*args,**kwargs)
     return q
  @classmethod
  def set_widget_value(cls,widget,x):
      f=pylab.figure()
      a=f.gca()
      if (cls.dataset[:,0]):
         a.scatter(cls.dataset[:,0],cls.dataset[:,1],'b')
      a.scatter([x[0]],[x[1]],'g')
      tmpfile=os.tmpnam()+".png"      
      f.savefig(tmpfile)  
      widget.f(PIL2NumPy(PIL.Image.open(tmpfile)))
      os.remove(tmpfile)
  @classmethod 
  def distance(cls,x1,x2): 
       return numpy.linalg.norm(x1-x2)
  @classmethod
  def get_typerelated_structures(cls):
        return { "SimplyFlat" : (ArrayStructure,("Flat",[]))}
  @classmethod
  def get_default_structure(cls):
       return "SimplyFlat"


class Datatype:
  content_type="Datapoints"
  dataset=None
  ld=None
  @classmethod
  def display(cls,x):
      if (not cls.ld):
          cls.ld=LazyDisplay()
      f=pylab.figure(figsize=(4,4))
      f.clf()
      a=f.gca()
      x=x.astype(numpy.float32)
      a.scatter(x[:,0],x[:,1])
      tmpfile="/tmp/buf.png"
      f.savefig(tmpfile)  
      cls.ld.f(PIL2NumPy(PIL.Image.open(tmpfile)))
  @classmethod
  def get_numpy(cls,x):
      return numpy.matrix(x)
  @staticmethod
  def pylab_display(cls,x):     
      f=pylab.figure()
      a=f.gca()
      a.scatter([x[0]],[x[1]], 'g')
      return f
  @classmethod
  def get_widget(cls,*args):
     q=QtDisplay(*args)
     return q
  @classmethod
  def set_widget_value(cls,widget,x,vdb=None,addr=None):
      f=pylab.figure(figsize=(4,4))
      f.clf()
      a=f.gca()
      x=x.astype(numpy.float32)
      displayed=False
      if (vdb):
        if (hasattr(vdb,"labeling_clusterid")):
             car=numpy.array(map(palette,eval("vdb.labeling_clusterid")()[addr])).squeeze()
             print car.shape
             a.scatter(x[:,0],x[:,1],c=car)
             displayed=True
      if (not displayed):
        a.scatter(x[:,0],x[:,1])
      tmpfile=os.tmpnam()+".png"
      f.savefig(tmpfile)        
      widget.f(PIL2NumPy(PIL.Image.open(tmpfile)))
      os.remove(tmpfile)
  @classmethod 
  def distance(cls,x1,x2): 
       return numpy.linalg.norm(x1-x2)
  @classmethod
  def get_typerelated_structures(cls):
        return { "SimplyFlat" : (ArrayStructure,("Flat",[]))}
  @classmethod
  def get_default_structure(cls):
       return "SimplyFlat"
