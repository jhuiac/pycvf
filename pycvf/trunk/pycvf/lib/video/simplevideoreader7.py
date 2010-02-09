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
#try:
import pyffmpeg
#except:
#  import pycvf.lib.video.pyffmpeg.pyffmpegb as pyffmpeg
from pycvf.core.errors import pycvf_debug
import numpy,sys

class SimpleVideoReader7:
    def __init__(self,file,obs=None,with_audio=False,track_selector=None,*args, **xargs):
        #pycvf_debug(10,"opening "+str(file))
        #sys.stderr.write("***")        
        #sys.stderr.flush()
        try:
          self.vr = pyffmpeg.FFMpegReader(*args,**xargs)
          self.file=file
          if(not track_selector):
            if (with_audio):
              ts=pyffmpeg.TS_AUDIOVIDEO
            else:
              ts=pyffmpeg.TS_VIDEO
          else:
            ts=track_selector
          self.ts=ts
          self.vr.open(file,ts)
          self.tracks=self.vr.get_tracks()
        except TypeError,e:
            print "ERROR", file,e
            raise
        except:
            raise
        self.stream=self.tracks[0]
        assert(self.stream!=None)
        self.frameno=0
        pycvf_debug(10,"/opening "+str(file))        
    def copy(self):
        pycvf_debug(10,"copying "+str(self.file))                
        nvr=SimpleVideoReader7(self.file,self.ts)
        try:
          nvr.seek_to(self.get_current_frame_no())
        except:
           pass
        return nvr
    def __del__(self):
        pycvf_debug(10,"deleting "+str(self.file))        
        if (self.vr):
          self.tracks=[]
          self.vr.close()
          del self.vr
        self.vr=None
        self.stream=None
        #pycvf_debug(10,"/deleting "+str(self.file))                
    def run(self):
        try:
            while True:
                self.step()
        except IOError:
            return True
    def step(self):
        r=self.vr.step()
        self.frameno+=1
        return self.vr.get_current_frame()
    def seek_to(self,f):
            if (self.frameno<=f) and (f<=(self.frameno+10)):
               for i in range(f-self.frameno):
                  self.step()
            else:
               try:
                 self.stream.seek_to_frame(max(0,f))
               except:
                 pass
            self.frameno=f
    def rewind(self):
        self.seek_to(0)
    def get_current_address(self):
        return (self.file,int(self.get_current_frame_no()))
    def get_current_frame(self):
            #return self.stream.get_current_frame()
            return self.vr.get_current_frame()
    def get_current_frame_no(self):
            return self.frameno
    def close(self):
        self.stream.close()
        del self.stream
    def set_observer(self, observer):
        self.stream.set_observer(observer)
    def __len__(self):
         return int(self.vr.duration_time()*self.tracks[0].get_fps())
    def __getitem__(self,addr):
         self.seek_to(addr)
         return self.get_current_frame()[0][2]
    def __getslice__(self,tfrom=None,tdest=None):
         assert(tfrom!=None)
         assert(tdest!=None)
         assert(type(tfrom)==type(tdest))
         l=[]
         xtfrom=tfrom*self.tracks[0].get_fps()
         xtdest=tdest*self.tracks[0].get_fps()
         if (xtfrom<xtdest):
                       def get_iter():
                          yield ( self.seek_to(xtfrom))
                          for i in range(xtfrom+1,xtdest):
                             yield self.step()
                       return get_iter()
         else:
                       return []
