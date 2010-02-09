# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# Video Database for Training
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
################################################
#
#########################################################################################################################################
# Import required objects
#########################################################################################################################################

import re, os, math, random, time,sys, traceback, datetime

from pycvf.lib.audio.simpleaudioreader import *
from pycvf.lib.readers.directoryreader import *
from pycvf.core.errors import *

#########################################################################################################################################
# Create the ContentsDatabase Object
#########################################################################################################################################
from pycvf.core import database
from pycvf.datatypes import audio

# audio returns a redaer
class DB(database.ContentsDatabase, audio.Datatype):
  TS_AUDIO={ 'audio1':(1, -1, {}) }
  #self.al
  al=None
  def __init__(self,path=None,filefilter=None,extensions="wav|ogg|mp3"):
     if (filefilter==None):
       filefilter="(.*).("+extensions+")"
     self.ir=DirectoryReader(path,filefilter)
  def __iter__(self):
      try:
        while True:
          fn=self.ir.step()
          pycvf_warning("sound.directory opening "+fn)
          rdr=SimpleAudioReader(fn)
          #print "duration_time =",rdr.vr.duration_time()
          #import random
          #st=random.random()*rdr.vr.duration_time()
          # print "seeking_to =",st
          #rdr.tracks[0].seek_to_seconds(st)
          #rdr.tracks[0].seek_to_seconds(st)          
          #rdr.vr.step()
          yield (rdr, fn)
      except StopIteration:
        pass
          
ContentsDatabase=DB       
__call__=DB

