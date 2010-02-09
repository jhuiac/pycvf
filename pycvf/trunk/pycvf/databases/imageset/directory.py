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

from pycvf.lib.readers.directoryreader import *
from pycvf.core.errors import *

#########################################################################################################################################
# Create the ContentsDatabase Object
#########################################################################################################################################
from pycvf.core import database
from pycvf.datatypes import basics
from pycvf.datatypes import image
from pycvf.datatypes import generated
from pycvf.databases.image import directory as imgdirectory

import itertools

# audio returns a redaer
class DB(database.ContentsDatabase, generated.Datatype(image.Datatype)):
  def __init__(self,path=None, **kwargs):
     self.ir=DirectoryReader(path)
     self.kwargs=kwargs
  def __iter__(self):
      try:
        while True:
          dn=self.ir.step()
          try:
            rdr=itertools.imap(lambda x:x[0],imgdirectory.DB(dn,randomized=False,**self.kwargs))
            yield (rdr, os.path.basename(dn))
          except KeyboardInterrupt:
            raise
          except Exception,e:
            print e
            pass
      except StopIteration:
        pass
          
ContentsDatabase=DB       
__call__=DB

