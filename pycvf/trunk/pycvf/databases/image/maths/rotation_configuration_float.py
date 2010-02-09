# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# Video Database for Training
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
################################################
#

import re, os, math, random, time,sys, traceback, datetime
from pycvf.lib.graphics.imgfmtutils import *
from pycvf.core import database
from pycvf.datatypes import image

import numpy as np

def cgrid(sz):
  r=np.mgrid[-sz:(sz+1),-sz:(sz+1)]
  return r[0]+1J*r[1]
class SymMap:
  def __init__(self,angle):
     self.ca=(1+np.cos(angle))%1
     self.sa=(1+np.sin(angle))%1
     if (self.ca-self.sa<1e10): 
        self.ca=self.sa=(self.ca+self.sa)/2.
     self.lv=( [ self.ca, self.sa, 1.-self.ca, 1-self.sa ] if (self.ca!=self.sa) else [self.ca,1-self.ca] )
     self.nc=(4 if  (self.ca!=self.sa) else 2)
  def symbolic_map(self,p):
    x,y,t=(np.real(p)+1000.5)%1, (np.imag(p)+1000.5)%1,0
    for v in self.lv:
       if x>=v: t+=1
       if y>=v: t+=1        
    return (t%self.nc)*128


class DB(database.ContentsDatabase):
  """
    * Rotation configuration according to my PhD Thesis (Bertrand Nouvel)
    = For some particular angles autosimilar pattern occur see thesis for more details
  """
  def datatype(self):
    return image.Datatype
  def __init__(self,angles=np.arange(0,np.pi/4.,np.pi/(4*256)),size=40):
      self.angles=angles
      self.size=size
  def __iter__(self):
      for angle in self.angles:
         r=cgrid(self.size)*np.exp(1j*angle)
         m=SymMap(angle)
         res=np.vectorize(m.symbolic_map)(r)
         yield (res,angle)
  def __getitem__(self,a):
         r=cgrid(self.size)*np.exp(1j*angle)
         m=SymMap(angle)
         return np.vectorize(m.symbolic_map)(r)


ContentsDatabase=DB
__call__=DB
