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

try:
  from pycvf.lib.video.render.lazy import LazyDisplay
except:
  pass
from pycvf.lib.ui.qtdisplay import QtDisplay



class Label:
  class Datatype:
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
    def set_widget_value(cls,widget,x,*args,**kwargs):
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
  

UnhandledDatatype=Label.Datatype

class RGBColor:
  class Datatype:
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
    def set_widget_value(cls,widget,x,*args,**kwargs):
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


class Float:
  class Datatype:
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
    def set_widget_value(cls,widget,x,*args,**kwargs):
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

class NumericArray:
  class Datatype:
    ld=None
    content_type="NumericArray"
    @classmethod
    def display(cls,x):
      if (x.ndim==2):
        from pycvf.datatypes import datapoints2d
        datapoints2d.Datatype.display(x)
      else:
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
      #if (x.ndim==2):
      from pycvf.datatypes import datapoints2d
      return datapoints2d.Datatype.get_widget(*args)
      #else:
      #  from PyQt4.QtGui import QLineEdit
      #  q=QLineEdit(*args)
      #  return q
    @classmethod
    def set_widget_value(cls,widget,x,vdb=None,addr=None):
      if (x.ndim==2):
        from pycvf.datatypes import datapoints2d
        return datapoints2d.Datatype.set_widget_value(widget,x,vdb,addr)
      else:
        widget.setText((str(x)))    
    @classmethod 
    def distance(cls,x1,x2): 
       return numpy.linalg.norm(x1-x2)
    @classmethod
    def get_typerelated_structures(cls):
        from pycvf.structures.array import ArrayStructure
        return { "SimplyFlat" : (ArrayStructure,("Flat",[]))}
    @classmethod
    def get_default_structure(cls):
       return "SimplyFlat"



class NumericVector:
  class Datatype:
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
    def set_widget_value(cls,widget,x,vdb=None, addr=None):
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
        from pycvf.structures.array import ArrayStructure
        return { "SimplyNeutral" : (ArrayStructure,("Neutral",[]))}
    @classmethod
    def get_default_structure(cls):
       return "SimplyNeutral"
