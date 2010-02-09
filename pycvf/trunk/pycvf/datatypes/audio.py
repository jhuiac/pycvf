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

from pycvf.lib.audio.render.lazy import *
from pycvf.structures.readers import ReaderStructure
from pycvf.datatypes  import basics

##
## By default audio are readers
## 

class Datatype:
  al=None
  content_type="Audio"
  @classmethod
  def display(cls,elr):
     #tracks=elr.get_tracks()
     if (not cls.al):   
        cls.al=LazyAudioSink(rate=elr.tracks[0].get_samplerate(),channels=elr.tracks[0].get_channels())
     #tracks[0].set_observer(cls.al.push_nowait)
     #elr.tracks[0].seek_to_seconds(30)     
     elr.set_observer(cls.al.push)
     #elr.vr.step()
     try:
       elr.run()
     except IOError:
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
     #from PyQt4.QtGui import QPushButton
     #return QPushButton("play",x)
     from pycvf.lib.ui.qtplaysoundbutton import QtPlaySoundButton
     return QtPlaySoundButton(x)
  @classmethod
  def set_widget_value(cls,widget,x):
         widget.set_player(x)
  @classmethod
  def get_typerelated_structures(cls):
        return {"audio-packets": ReaderStructure }
  @classmethod
  def get_default_structure(cls):
       return "audio-packets"



##
## audio are list of samples
## 

class Samples:
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

##
## audio are list of samples
## 

import numpy
from pycvf.datatypes import histogram
from pycvf.datatypes import generated

class Spectrum:
  class Datatype(generated.Datatype(histogram.Datatype)):
    @classmethod
    def set_widget_value(cls,widget,x):
        #print widget
        widget.clear()
        xc=x#.copy()
        for i in range(3):#len(x)):
            q=cls.ElementType.get_widget(widget)
            xv=numpy.abs(xc.next())
            cls.ElementType.set_widget_value(q,xv[0])
            widget.addItem(str(i))
            widget.setItemWidget(widget.item(i),q)
