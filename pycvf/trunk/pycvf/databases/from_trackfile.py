# -*- coding: utf-8 -*-

import sys
import itertools
from pycvf.core import database
from pycvf.core.errors import *
from pycvf.lib.info.track import OnDiskMultiTrackLarge, OnDiskMultiTrackLargeZ

class DB(database.ContentsDatabase):
  """
    When your features are heavy to compute, it is smart to precompute them in a trackfile.
    You may then access the computed features through this module.
  """
  def __init__(self,trackfilename,st=0,datatype=None,filter_nulls=True,filter_emptylists=True):
      self.trackfilename=trackfilename
      self.tf=OnDiskMultiTrackLargeZ(trackfilename)     
      self.tfidx=dict([ (self.tf[x][1],x) for x in range(len(self.tf)) ] )
      self.tf.tryloadmeta()
      self.st=st
      self.filter_nulls=filter_nulls
      self.filter_emptylists=filter_emptylists
      if (datatype):
          self.dtp=datatype
          #for i in dir(datatype):
          #    if (not (hasattr(self,i))):
          #        setattr(self,i,getattr(datatype,i))
      else:
        try:
          print self.tf.meta
          self.dtp=self.tf.meta["inbound_datatype"]
          #self.display=self.tf.meta["inbound_datatype"].display
        except:
          pycvf_warning("Failed to use information stored in metadata for typing reverting to no datatype")
          def print_e(x):
            sys.stdout.write(str(x)+"\n")
          self.display=print_e
  def datatype(self):
      return self.dtp
  def __iter__(self):
      ltf=len(self.tf)
      for x in range(ltf):
         tfx=self.tf[x]
         if (not self.filter_nulls) or (tfx[0]!=None):
           if (self.st==-1):
               yield tfx[0],tfx[1]               
           else:
             if (not self.filter_emptylists) or (tfx[0][self.st]!=[]):             
               yield tfx[0][self.st],tfx[1]
  def keys(self):
      return self.tfidx.keys()
  def __getitem__(self,x):
      #print x
      #print self.tfidx      
      return self.tf[self.tfidx[x]][0]
  def values(self,x):
      return itertools.imap(lambda x: self[x],self.keys() )
  def items(self,x):
      return itertools.izip(self.keys(),self.values())

# Framework 2 compatibility
ContentsDatabase=DB
__call__=DB
