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
# -*- coding: utf-8 -*-

import time

from pycvf.lib.video.render.lazy import LazyDisplay
from pycvf.lib.ui.qtdisplay import QtDisplay

class Datatype:
  ld=None
  content_type="VideoSet"
  @classmethod
  def display_video(cls,elr):
     if (not cls.ld):
        cls.ld=LazyDisplay()
     elr.set_observer(cls.ld.f)
     elr.run()
     time.sleep(1)
     elr.set_observer(None)
  @classmethod
  def display(cls,elr):
     elr.set_observer(cls.display_video)
     elr.run()
     elr.set_observer(None)     
  @classmethod
  def get_numpy(cls,x):
     assert(False)
  @staticmethod
  def pylab_display(cls,x):
     assert(False)
  @classmethod
  def get_widget(cls,x,*args, **kwargs):
     assert(False)
  @classmethod
  def get_typerelated_structures(cls):
        return { }
  @classmethod
  def get_default_structure(cls):
       return None

