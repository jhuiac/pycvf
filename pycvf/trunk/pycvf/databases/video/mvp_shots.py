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

import re, os, math, random, time,sys, traceback, datetime
from pycvf.lib.readers.sequencereader import *
from pycvfext.niiindex.mvp.mvpaccess import *

#########################################################################################################################################
# Create the ContentsDatabase Object
#########################################################################################################################################
from pycvf.core import database
from pycvf.datatypes import video 


class DB(database.ContentsDatabase,video.Datatype):
  CONTENT_TYPE="VIDEO"
  TRACK_SELECTOR={ 'video1':(0, -1,{})}
  ld=None
  def __init__(self,shotlist,with_mvp=True,startfrom=None,keyframes_only=False, smallpics=False,track_selector=None):
     """
     shot list is a set of time code
     """
     x.shotlist=list(shotlist)
     if (with_mvp):
       self.mvp=MvpAccess(with_ontology=False);
     self.td=datetime.datetime.today()
     self.tdb=datetime.datetime(self.td.year,self.td.month, self.td.day,6,0,0,0)
     self.tdb=self.td-datetime.timedelta(3,0,0)
     self.startfrom=(startfrom==None) and  -20*29.97 or startfrom
     self.track_selector=track_selector or DB.TRACK_SELECTOR
     if (smallpics):
        self.track_selector['video1'][2]['dest_width']=128
        self.track_selector['video1'][2]['dest_height']=96
     if (keyframes_only):
        self.track_selector['video1'][2]['skip_frame']=32
  def __iter__(self):
      for shotno in range(len(x.shotlist)):
          channel,datefrom,dateto=x.shotlist[shotno]
          tvflow=self.mvp.get_flow(channel)
          assert(dateto>=datefrom)
          dt=(dateto-datefrom)
          t=math.floor(29.97*(dt.seconds+dt.days*3600*24))
          ssr=SequenceReader(tvflow.__getslice__(channel,datefrom,dateto),
          lenseq)
          yield (generated_reader(ssr), x.shotlist[shotno])

ContentsDatabase=DB
__call__=DB
