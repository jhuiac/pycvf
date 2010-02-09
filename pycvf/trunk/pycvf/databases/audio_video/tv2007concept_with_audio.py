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

from pycvf.lib.video.lazydisplay import LazyDisplay
from pycvf.lib.video.shotreader import ShotReader
from pycvfext.lib.specifics.trecvid import tv2007
from pycvf.lib.readers.iterreader import IterReader
from pycvf.datatypes import audiovideo
#########################################################################################################################################
# Create the ContentsDatabase Object
#########################################################################################################################################
from pycvf.core import database
class DB(database.ContentsDatabase,audiovideo.Datatype):
  CONTENT_TYPE="VIDEO"
  TRACK_SELECTOR={ 'video1':(0, -1,{}), 'audio1':(1, -1,{})}
  ld=None
  def __init__(self,conceptname='Dog',positive=True,randomized=True,videoset="devel"):
    self.positive=positive
    self.conceptname=conceptname
    self.randomized=randomized
    self.videoset=videoset
  def __iter__(self):
     if (self.positive):
       return tv2007.TV2007(self.videoset,track_selector=self.TRACK_SELECTOR).concept_positive_shots(self.conceptname,self.randomized)
     else:
       return tv2007.TV2007(self.videoset,track_selector=self.TRACK_SELECTOR).concept_negative_shots(self.conceptname,self.randomized)

         
ContentsDatabase=DB
__call__=DB