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

from pycvf.core import settings
import numpy


from pycvf.structures import spatial

class Datatype:
  ld=None
  content_type="Image"
  @classmethod
  def check(cls,x):
     return hasattr(x,"content_type") and x.content_type==cls.content_type
  @classmethod
  def display(cls,x):
     from pycvf.lib.video.render.lazy import LazyDisplay      
     if (cls.ld==None):
        cls.ld=LazyDisplay()
     if (x.ndim==2 or x.shape[2]==1):
        x=numpy.asarray(x)         
        cls.ld.f(x.reshape((x.shape[0],x.shape[1],1)).repeat(3,axis=2))
     else:
        cls.ld.f(x)
  @classmethod
  def get_numpy(cls,x):
     return x
  @staticmethod
  def pylab_display(cls,x):
     pylab.imshow(x)
  @classmethod
  def get_widget(cls,x,*args, **kwargs):
     from pycvf.lib.ui.qtdisplay import QtDisplay
     q=QtDisplay(*args,**kwargs)
     return q
  @classmethod
  def set_widget_value(cls,widget,x,*args,**kwargs):
     try:
       if (x.ndim==2 or x.shape[2]==1):
         x=numpy.asarray(x)
         widget.f(x.reshape(x.shape[0],x.shape[1],1).repeat(3,axis=2),*args,**kwargs)
       else:
          widget.f(x)
     except Exception,e:
       print "Exception while displaying image",e
  @classmethod
  def get_structure(cls):
     #if (instance.ndim==2) or (instance.shape[2]==1):
     #  return self.SpatialStructure()
     #else:
     return spatial.SpatialStructure(1)
  @classmethod
  def get_typerelated_structures(cls):
        return {"datas": spatial.ImageStructure(0), 
                "color-pixels": spatial.ImageStructure(1), 
                "color-horizontal-edges": (spatial.ImageStructure(1),("D",[0])), 
                "color-vertical-edges": (spatial.ImageStructure(1),("D",[1])), 
                "monochrome-horizontal-edges": (spatial.ImageStructure(0),("D",[0])), 
                "monochrome-vertical-edges": (spatial.ImageStructure(0),("D",[1])), 
                "monochrome-V4": (spatial.ImageStructure(0),("VN",[])),
                "monochrome-V8": (spatial.ImageStructure(0),("VL",[])),  
                "color-horizontal-edges": (spatial.ImageStructure(1),("D",[0])), 
                "color-vertical-edges": (spatial.ImageStructure(1),("D",[1])), 
                "color-V4": (spatial.ImageStructure(1),("VN",[])),
                "color-V8": (spatial.ImageStructure(1),("VL",[])),  
               }
  @classmethod
  def get_default_structure(cls):
       return "datas"
  
