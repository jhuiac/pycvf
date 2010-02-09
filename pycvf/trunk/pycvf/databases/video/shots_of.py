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

import re, os, math, random, time,sys, traceback, datetime,itertools

from pycvf.lib.readers.subsequencereader import *

#########################################################################################################################################
# Create the ContentsDatabase Object
#########################################################################################################################################
from pycvf.core import database
from pycvf.datatypes import video

class DB(database.ContentsDatabase, video.Datatype):
  """
    This database returns the videoshots of another video database according to some keyframe model.

    The keyframe model is expected to return a generator for getting the next keyframe according to a video 
    object.
  """
  def __init__(self,db, keyframemodel,keyframemodelpath="/"):
     self.db=db
     self.keyframemodel=(pycvf_builder(keyframemodel) if type(keyframemodel) in [str,unicode] else keyframemodel)
     self.keyframemodel.init("/",self.db,self)
     self.keyframemodelpath=keyframemodelpath
     metak= self.keyframemodel.get_features_meta().keys()
     pycvf_warning("KEYFRAME MODEL BE SURE TO HAVE CHOSEN THE GOOD MODEL OUTPUT !")      
     pycvf_warning("metak = %r"%(metak,))
     self.keyframemodelpathno=metak.index(keyframemodelpath)
     
  def __iter__(self):
      lf=0 # last frame
      for e in self.db:
        s=0
        for kf in self.keyframemodel.process(e[0],addr=e[1])[self.keyframemodelpathno]:
          print "shot :",lf,"-",kf 
          if (lf!=kf):
            yield (SubsequenceReader(e[0],lf,kf),(e[1],s))
            lf=kf
            s+=1
            
        
ContentsDatabase=DB       
__call__=DB

