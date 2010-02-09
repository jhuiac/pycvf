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


from pycvf.lib.video.simplevideoreader7 import *
import random

class RandomSubsequenceGenerator:
    def __init__(self,video,observer=None,*args,**kwargs):
        if (isinstance(video,SimpleVideoReader7)):
            self.vr=video
        else:
            self.vr=SimpleVideoReader7(video,*args,**kwargs)
        self.fps=self.vr.tracks[0].get_fps()
        self.tlen=int(self.vr.vr.duration_time()*self.vr.tracks[0].get_fps())
        self.observer=observer
    def random(self,len=10):
        import random
        tstart=random.randint(0,self.tlen-len)
        return self.vr.__getslice__(tstart/self.fps,(tstart+len)/self.fps)
    def step(self,len=10):
        vs=self.random(len)
        if (self.observer):
            self.observer(vs)
    def run(self,len=10):
        while True:
            self.step(len)
    
    


class RandomSubsequencesFromDirectory:
    def __init__(self,d):
        from pycvf.lib.graphics.directoryreader import VideoDirectoryReader
        self.d=d
        self.vdr=VideoDirectoryReader(self.d)
    def random(self,len=10):
        try:
          f=self.vdr.next()
        except:
          self.vdr.reset()
          f=self.vdr.next()
        s=RandomSubsquenceGenerator(f[0]).random(len)
        return s
    def step(self,len=10):
        vs=self.random(len)
        if (self.observer):
            self.observer(vs)
    def run(self,len=10):
        while True:
            self.step(len)
    
