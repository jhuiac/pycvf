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

from pycvf.lib.video.lazydisplay import LazyDisplay
from pycvf.lib.video.lazydisplayqt import LazyDisplayQt
from pycvf.lib.ui.qtdisplay import QtDisplay
from pycvf.nodes.structures import spatial

class Datatype:
  ld=None
  content_type="Image"
  prefered_display=None
  @classmethod
  def display(cls,x):
     if (not cls.ld):
        if (cls.prefered_display=="qt"):
          cls.ld=LazyDisplayQt()
        else:
          cls.ld=LazyDisplay()
     if (x.ndim==2 or x.shape[2]==1):
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
     q=QtDisplay(*args,**kwargs)
     return q
  @classmethod
  def set_widget_value(cls,widget,x):
     if (x.ndim==2 or x.shape[2]==1):
        widget.f(x.reshape((x.shape[0],x.shape[1],1)).repeat(3,axis=2))
     else:
        widget.f(x)
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
  
