# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# Video Database for Training
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
# ###############################################
#
#########################################################################################################################################
# Import required objects
#########################################################################################################################################

import re, os, math, random, time,sys, traceback, datetime, itertools

#from pycvf.lib.video.lazydisplay import LazyDisplay
from pycvf.lib.video.shotreader import ShotReader
from pycvfext.niiindex.trecvid import tv2007
from pycvf.lib.readers.iterreader import IterReader
from pycvf.datatypes import video
#########################################################################################################################################
# Create the ContentsDatabase Object
#########################################################################################################################################
from pycvf.core import database
class DB(database.ContentsDatabase,video.Datatype):
  CONTENT_TYPE="VIDEO"
  TRACK_SELECTOR={ 'video1':(0, -1,{})}
  ld=None
  def __init__(self,conceptname='Dog',positive=True,randomized=True,videoset="devel"):
    self.positive=positive
    self.conceptname=conceptname
    self.randomized=randomized
    self.videoset=videoset
    self.tvobj=tv2007.TV2007(self.videoset)
  def __iter__(self):
     if (self.positive):
       return self.tvobj.concept_positive_shots(self.conceptname,self.randomized)
     else:
       return self.tvobj.concept_negative_shots(self.conceptname,self.randomized)
  def keys(self):
       return self.tvobj.concept_positive_shotsids(self.conceptname)
  def __getitem__(self,k): 
       #print k     
       return self.tvobj.get_shot_by_id(k)[0]
  def __len__(self):
      return len(self.keys())

__call__=DB
ContentsDatabase=DB
