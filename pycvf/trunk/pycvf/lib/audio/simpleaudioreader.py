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
import numpy,sys
import pyffmpeg
from pycvf.core.errors import pycvf_debug


class SimpleAudioReader:
    def __init__(self,file,obs=None,track_selector=None,*args, **xargs):
        self.vr=None
        try:
          self.vr = pyffmpeg.FFMpegReader(*args,**xargs)
          self.file=file
          if track_selector==None:
              ts=pyffmpeg.TS_AUDIO
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
    def copy(self):
        print "COPY READER"
        nvr=SimpleAudioReader(self.file,self.ts)
        nvr.vr.seek_to_pts(self.vr.get_current_frame_pts())
        return nvr
    def __del__(self):
        if (self.vr):
          self.tracks=[]
          self.vr.close()
          del self.vr
        self.vr=None
        self.stream=None
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
               self.stream.seek_to_frame(max(0,f))
            self.frameno=f
    def get_current_address(self):
        return (self.file,int(self.get_current_frame_no()))
    def get_current_frame(self):
            return self.vr.get_current_frame()
    def get_current_frame_no(self):
            return self.frameno
    def close(self):
        self.stream.close()
        del self.stream
    def set_observer(self, observer):
        self.stream.set_observer(observer)
    def rewind(self):
        self.seek_to(0)
    def __len__(self):
         return int(self.vr.duration_time()*self.tracks[0].get_fps())
    def __getitem__(self,addr):
         self.seek_to(addr)
         return self.get_current_frame()[0][2]
