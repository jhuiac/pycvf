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

#########################################################################################################################################
# Create the ContentsDatabase Object
#########################################################################################################################################
from pycvf.core import database
from pycvf.datatypes import video

class DB(database.ContentsDatabase, video.Datatype):
  al=None
  def __init__(self,imagedb, ctrarglist=[('default',([],{}))]):
     self.imagedb=imagedb
     self.ctrarglist=ctrarglist
  def __iter__(self):
      for x in self.ctrarglist:
          y=x[1]
          vdb=self.imagedb(*y[0],**y[1]) 
          vdbkeys=vdb.keys()
          class TSequenceReader():
	      def __init__(self, observer=None):
		  self.observer=observer
		  self.i=0
	      def copy(self):
		  return TSequenceReader()
	      def step(self):
		  try:
		      k=vdbkeys[self.i] 
		      r=vdb[k]
		      if (self.observer):
		          self.observer(r)
		      self.i+=1
		      return r
		  except IndexError:
		    raise StopIteration
	      def get_current_address(self):
		  return (x[0],self.i)
	      def set_observer(self,observer):
		  self.observer=observer
              def seek_to(self,p):
	      	    self.i=p
	      def run(self):
		  try:
		    while True:
		      self.step()
		  except StopIteration:
		      return
	      def __len__(self):
		return vdb.__len__()
          yield (TSequenceReader() , x[0])

ContentsDatabase=DB       
__call__=DB

