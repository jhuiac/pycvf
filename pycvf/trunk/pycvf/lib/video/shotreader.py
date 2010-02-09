#!/usr/bin/env python
# -*- coding: utf-8 -*-
## ##########################################################################################################
## 
## This file is released under GNU Public License v3
## See LICENSE File at the top the pycvf tree.
##
## Author : Bertrand NOUVEL / CNRS (2009)
##
##
##
## Revision FILE: $Id$
##
## ###########################################################################################################
## copyright $Copyright$
## @version $Revision$
## @lastrevision $Date$
## @modifiedby $LastChangedBy$
## @lastmodified $LastChangedDate$
#############################################################################################################


import numpy
#from pycvf.lib.video.videosequencereader import *
from pycvf.lib.readers.subsequencereader import *
from pycvf.lib.stats.models import *

class ShotReader:
    def __init__(self,reader,observer=None,minlen=5, maxlen=60*30, threshold=0.00007):
        class O:
            def __init__(self):
                self.o=None
            def f(self,o):
                self.o=o
        self.o=O()
        assert(minlen>=2)
        self.reader=reader
        self.minlen=minlen
        self.maxlen=maxlen
        self.reader.set_observer(self.o.f)
        self.observer=observer
        self.nr=None
        self.threshold=threshold
        self.get_nr()
    def extract_diff_features(self,x,px):
        ps=reduce(lambda y,z:y*z,x.shape,1)
        return [ numpy.linalg.norm((px-x).reshape(ps),2) ]
    def get_nr(self):
        bt=self.reader.get_current_address()
        ns=[]
        dsm=SimpleMeanVarianceModel()
        try:
           self.reader.step()
        except:
           return None
        px=self.o.o
        df=[]
        for x in range(self.minlen-1):
           try:
             self.reader.step()
           except:
               break
           x=self.o.o
           df.append(self.extract_diff_features(x,px))
           px=x
        dsm.train(df,online=True)
        ni=0
        while True:
          if (ni>self.maxlen-self.minlen):
            break
          df=[] 
          try:
            self.reader.step()
          except:
            break  
          x=self.o.o
          df.append(self.extract_diff_features(x,px))
          lp=dsm.test(df,log=False)
          sys.stderr.write("%s %s %s"%( str(dsm.mean()),str(dsm.std()),str( df)))
          sys.stderr.write("lp : %f \n"%(lp,))
          if (lp<self.threshold):
             break
          px=x
          dsm.train(df,online=True)
          ni+=1
          ## TODO : bugfix :  we loose one picture
        et=self.reader.get_current_address()
        sys.stderr.write( "shot:"+str(bt)+"-"+str(et)+"\n")
        #self.nr=SubsequenceReader(self.reader,bt[1],et[1])
        self.nr=SubsequenceReader(self.reader.__class__(bt[0]),bt[1],et[1])
    def step(self):
        if (not self.nr):
            raise StopIteration
        if (self.observer):
            self.observer(self.nr)
        self.get_nr()
    def run(self):
        while True:
            self.step()
    def get_current_address(self):
        return self.ns
    def set_observer(self,o):
        self.observer=o

