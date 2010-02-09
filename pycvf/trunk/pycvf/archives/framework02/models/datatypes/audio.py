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

from pycvf.lib.audio.playalsa import *
from pycvf.nodes.structures.readers import ReaderStructure

class Datatype:
  al=None
  content_type="Audio"
  @classmethod
  def display(cls,elr):
     tracks=elr.get_tracks()
     if (not cls.al):   
        cls.al=AlsaSoundLazyPlayer(rate=tracks[0].get_samplerate(),channels=tracks[0].get_channels())
     tracks[0].set_observer(cls.al.push_nowait)
     elr.run()
     tracks[0].set_observer(None)
  @classmethod
  def get_numpy(cls,x):
     assert(False)
  @staticmethod
  def pylab_display(cls,x):
     assert(False)
  @classmethod
  def get_widget(cls,x,*args, **kwargs):
     from PyQt4.QtGui import QPushButton
     return QPushButton("play",x)
  @classmethod
  def get_typerelated_structures(cls):
        return {"audio-packets": ReaderStructure, 
               }
  @classmethod
  def get_default_structure(cls):
       return "audio-packets"

