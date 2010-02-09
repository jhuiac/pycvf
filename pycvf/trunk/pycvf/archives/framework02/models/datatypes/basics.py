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
from pycvf.lib.ui.qtdisplay import QtDisplay
from pycvf.nodes.structures.array import ArrayStructure


class Label.Datatype:
  ld=None
  content_type="Label"
  @classmethod
  def display(cls,x):
      print x
  @classmethod
  def get_numpy(cls,x):
      assert(False)
  @staticmethod
  def pylab_display(cls,x):
     assert(False)
  @classmethod
  def get_widget(cls,*args):
     from PyQt4.QtGui import QLineEdit
     q=QLineEdit(*args)
     return q
  @classmethod
  def set_widget_value(cls,widget,x):
     widget.setText((str(x)))
  @classmethod 
  def distance(cls,x1,x2): 
       return (x1!=x2) and 1 or 0
  @classmethod
  def get_typerelated_structures(cls):
        return { }
  @classmethod
  def get_default_structure(cls):
       return None
  

class RGBColorDatatype:
  ld=None
  content_type="RGBColor"
  @classmethod
  def display(cls,x):
      print x
  @classmethod
  def get_numpy(cls,x):
      assert(False)
  @staticmethod
  def pylab_display(cls,x):
     assert(False)
  @classmethod
  def get_widget(cls,*args):
     from PyQt4.QtGui import QLineEdit
     q=QLineEdit(*args)
     return q
  @classmethod
  def set_widget_value(cls,widget,x):
     widget.setText((str(x)))
  @classmethod 
  def distance(cls,x1,x2): 
       return (x1!=x2) and 1 or 0
  @classmethod
  def get_typerelated_structures(cls):
        return { }
  @classmethod
  def get_default_structure(cls):
       return None


class FloatDatatype:
  ld=None
  content_type="Float"
  @classmethod
  def display(cls,x):
      print x
  @classmethod
  def get_numpy(cls,x):
      return numpy.matrix(x)
  @staticmethod
  def pylab_display(cls,x):
     assert(False)
  @classmethod
  def get_widget(cls,*args):
     from PyQt4.QtGui import QLineEdit
     q=QLineEdit(*args)
     return q
  @classmethod
  def set_widget_value(cls,widget,x):
     widget.setText((str(x)))
  @classmethod 
  def distance(cls,x1,x2): 
       return abs(x-y)
  @classmethod
  def get_typerelated_structures(cls):
        return { }
  @classmethod
  def get_default_structure(cls):
       return None

class NumericArrayDatatype:
  ld=None
  content_type="NumericMatrix"
  @classmethod
  def display(cls,x):
      print x
  @classmethod
  def get_numpy(cls,x):
      return numpy.matrix(x)
  @staticmethod
  def pylab_display(cls,x):
     if (x.ndim==2) or (x.ndim==3):
         pylab.imshow(x)
  @classmethod
  def get_widget(cls,*args):
     from PyQt4.QtGui import QLineEdit
     q=QLineEdit(*args)
     return q
  @classmethod
  def set_widget_value(cls,widget,x):
     widget.setText((str(x)))    
  @classmethod 
  def distance(cls,x1,x2): 
       return numpy.linalg.norm(x1-x2)
  @classmethod
  def get_typerelated_structures(cls):
        return { "SimplyFlat" : (ArrayStructure,("Flat",[]))}
  @classmethod
  def get_default_structure(cls):
       return "SimplyFlat"


class NumericVectorDatatype:
  ld=None
  content_type="NumericVector"
  @classmethod
  def display(cls,x):
      print x
  @classmethod
  def get_numpy(cls,x):
      return numpy.matrix(x)
  @staticmethod
  def pylab_display(cls,x):
      assert(False)
  @classmethod
  def get_widget(cls,*args):
     from PyQt4.QtGui import QLineEdit
     q=QLineEdit(*args)
     return q
  @classmethod
  def set_widget_value(cls,widget,x):
     widget.setText((str(x)))    
  @classmethod 
  def distance(cls,x1,x2): 
       return numpy.linalg.norm(x1-x2)
  @classmethod
  def get_typerelated_structures(cls):
        return { }
  @classmethod
  def get_default_structure(cls):
       return None
  @classmethod
  def get_typerelated_structures(cls):
        return { "SimplyNeutral" : (ArrayStructure,("Neutral",[]))}
  @classmethod
  def get_default_structure(cls):
       return "SimplyNeutral"

     
def ListDatatype(ElemType):
  class _ListDatatype:
    ld=None
    ElementType=ElemType
    content_type="List("+ElemType.content_type+")"
    @classmethod
    def display(cls,x):
      for e in x:
        ElemType.display(x)
    @classmethod
    def get_numpy(cls,x):
      return numpy.array( [ ElemType.get_numpy(e) for e in x  ])
    @staticmethod
    def pylab_display(cls,x):
       assert(False)
    @classmethod
    def get_widget(cls,*args):
       from PyQt4.QtGui import QListWidget
       q=QListWidget(*args)
       return q
    @classmethod 
    def distance(cls,x1,x2): 
       return min(scipy.spatial.distance.cdist(x1,x2,ElemType.distance))
    @classmethod
    def set_widget_value(cls,widget,x):
        #print widget
        widget.clear()
        for i in range(len(x)):
            q=ElemType.get_widget(widget)
            ElemType.set_widget_value(q,x[i])
            widget.addItem(str(i))
            widget.setItemWidget(widget.item(i),q)
    @classmethod
    def get_typerelated_structures(cls):
        return { }
    @classmethod
    def get_default_structure(cls):
       return None
  return _ListDatatype
