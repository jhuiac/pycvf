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
from pycvf.core.errors import *

from pycvf.lib.video.render.lazy import LazyDisplay

try:
  from pycvf.lib.ui.qtdisplaymovie import QtDisplayMovie
except:
  pycvf_warning("No X or No QT")
from pycvf.structures import readers as readerstructure

class Datatype:
  ld=None
  content_type="Video"
  @classmethod
  def display(cls,elr):
     if (not cls.ld):
        cls.ld=LazyDisplay()
     elr.set_observer(cls.ld.f)
     try:
       elr.run()
     except:
       pass
     elr.set_observer(None)
  @classmethod
  def get_numpy(cls,x):
     assert(False)
  @staticmethod
  def pylab_display(cls,x):
     assert(False)
  @classmethod
  def get_widget(cls,x,*args, **kwargs):
     print args, kwargs
     q=QtDisplayMovie(x,*args,**kwargs)
     return q
  @classmethod
  def set_widget_value(cls,widget,x,vdb,addr):
     widget.push(x)
  @classmethod
  def get_typerelated_structures(cls):
        return {"images": (readerstructure.ReaderStructure(0), ("Elements",[]))   }
  @classmethod
  def get_default_structure(cls):
       return "images"
