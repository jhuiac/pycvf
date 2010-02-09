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
from pycvf.datatypes import videoset
#########################################################################################################################################
# Create the ContentsDatabase Object
#########################################################################################################################################

from pycvf.core import database

class DB(database.ContentsDatabase,videoset.Datatype):
  CONTENT_TYPE="VIDEO"
  TRACK_SELECTOR={ 'video1':(0, -1,{})}
  ld=None
  #def __init__(self,keyframes_only=False, smallpics=True,track_selector=None, basedir="/home/tranx/medias/per900a/home/tranx/databases/"):
  #   self.basedir=basedir
  #   self.track_selector=track_selector or ContentsDatabase.TRACK_SELECTOR
  #   if (smallpics):
  #      self.track_selector['video1'][2]['dest_width']=128
  #       self.track_selector['video1'][2]['dest_height']=96
  #   if (keyframes_only):
  #      self.track_selector['video1'][2]['skip_frame']=32
  def __iter__(self):
     tv=tv2007.TV2007()
     rv=range(len(tv.videosequences))
     random.shuffle(rv)
     for v in rv:
       sf=tv.videosequences[v][1]()
       yield (IterReader(iter(itertools.imap(lambda s: sf.get_shots()[s]() , range(len(sf.vseg)) ))),v)
         
ContentsDatabase=DB
__call__=DB