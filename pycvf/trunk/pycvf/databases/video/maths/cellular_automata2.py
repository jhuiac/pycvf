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
import numpy

from pycvf.core import database
from pycvf.datatypes import video
from pycvf.lib.info.obs import make_observation
from pycvf.core.builders import *

class DB(database.ContentsDatabase):
   """
    * Create space-time diagram of Cellular Automata working on $\ZZ^2$
   """
   def datatype(self):
      return video.Datatype
   def __init__(self,
                obsv=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1),(0,0)],
                initcfgdb="DB('image.maths.random',resolution=(64,64),amplitude=2)" ,
                stopcriterion=50,
                rule=lambda st:(min((st.sum()-2),1) if st[:-1].sum() in [2,3] else 0),
                outputf=lambda x:x*255
               ):
     self.initcfgdb=(pycvf_builder(initcfgdb) if type(initcfgdb) in [str, unicode] else initcfgdb)
     self.obsv=obsv
     self.stopcriterion=stopcriterion
     self.rule=rule
     self.mo=make_observation(self.obsv,"torus")
     self.outputf=outputf
     if (type(self.stopcriterion) in [int, long]):
         def stop_after_iterations(*args):
             for i in range(stopcriterion):
                yield False
             yield True
         xe=stop_after_iterations()
         self.stopcriterion=lambda x:xe.next()
   def __iter__(self):
      for x in self.initcfgdb:
          class CellularAutomataReader:
              def __init__(self, c0) :
                  self.c0=c0
                  self.c=c0
                  self.observer=None
              def set_observer(self,obs):
                  self.observer=obs
              def __iter__(selfac):
                  yield selfac.c
                  while not self.stopcriterion(selfac.c):
                     yield selfac.step()
              def len(self):
                  return -1
              def copy(self):
                  return CellularAutomataReader(self.c0)
              def rewind(self):
                  #print "rew"
                  pass
              def step(selfac):
                    #print "pre=",selfac.c.shape, selfac.c.mean()
                    o=self.mo(selfac.c)
                    selfac.c=numpy.array([ self.rule(o[i,:]) for i in range(o.shape[0]) ]).reshape(selfac.c.shape)
                    #print "computed ok=",selfac.c.shape, selfac.c.mean()
                    r=self.outputf(selfac.c)
                    if (selfac.observer):
                        selfac.observer(r)
                    return r
              def run(self):
                  for x in self:
                      self.step()
          yield (CellularAutomataReader(x[0]),x[1])
   #def __getitem__(self,a):
   #       return (numpy.random.random(self.resolution)*255).astype(numpy.uint8)

ContentsDatabase=DB
__call__=DB
