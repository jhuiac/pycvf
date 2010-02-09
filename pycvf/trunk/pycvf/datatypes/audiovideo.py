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
import sys
from pycvf.lib.video.render.lazy import LazyDisplay
#
from pycvf.lib.ui.qtdisplaymovie import QtDisplayMovie

with_oss=False

if with_oss:
  try:             
    import ossaudiodev as oss
  except:                    
    import oss   
else:
   from pycvf.lib.audio.render.alsa import AlsaSoundLazyPlayer

class Datatype:
  ld=None
  content_type="AudioVideo"
  @classmethod
  def display(cls,elr):
     global with_oss
     if (not cls.ld):
        cls.ld=LazyDisplay()
     tracks=None
     if (hasattr(elr,"tracks")):
        tracks=elr.tracks
        rreader=elr
     elif (hasattr(elr,"vr")): 
        if (hasattr(elr.vr,"tracks")):
           tracks=elr.vr.tracks
           rreader=elr.vr
     elif (hasattr(elr,"reader")): 
        if (hasattr(elr.reader,"tracks")):
           tracks=elr.reader.tracks
           rreader=elr.reader
     else:
        pass
     if (tracks==None):
        sys.stderr.write("don't know how to get sound track info\n")
        raise Exception, "don't know how to get sound track info"
     rate=tracks[1].get_samplerate()
     channels=tracks[1].get_channels()
     fps=tracks[0].get_fps()
     print rate,channels,fps
     if not with_oss:
       ap=AlsaSoundLazyPlayer(rate,channels,fps)
     else:
       try:
        ao=oss.open_audio()
       except:
        ao=oss.open('w')
       if (hasattr(ao,'stereo')):
        ao.stereo(1)
       ao.speed(rate)
       if (hasattr(ao,'format')):
         ao.format(oss.AFMT_S16_LE)
       else:
         ao.setfmt(oss.AFMT_S16_LE)
       ao.channels(channels)
     print tracks
     class D:
      def __init__(self):
        self.ctr=0
      def on_event(self,x):
       global with_oss
       x=rreader.get_current_frame()
       if (self.ctr%4==0):
          cls.ld.f(x[0][2])
       #print x[1].shape
       if with_oss:
         ao.write(x[1].data)
       else: 
         #print "push"
         ap.push((x[1],0))
         #print "/push"
       self.ctr+=1       
     #elr.set_observer(lambda x:(cls.ld.f(x[0]),ap.push(x[1])))
     elr.set_observer(D().on_event)
     try:
       elr.run()
     except Exception,e:
       sys.stderr.write("WARNING: error during playback...\n"+str(e)+"\n")
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
     q=QtDisplayMovie(*args,**kwargs)
     return q
  @classmethod
  def set_widget_value(cls,widget,x):
     widget.push(x)
  @classmethod
  def get_structures(cls):
       return { }
