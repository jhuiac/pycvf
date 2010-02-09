#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# VideoModel Trainer builder By Bertrand NOUVEL
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
# ###############################################
#
#########################################################################################################################################
# Import required objects
#########################################################################################################################################

import re, os, math, random, time,sys, traceback, getopt,time
import sys
from pycvf.core.generic_application import *

class MTrainApp(ModelUsingApplication):
  class ProgramMetadata(object):
      name="Model Trainer Application"
      version="0.1"
      license="GPLv3"
      author="Bertrand Nouvel bertrand.nouvel@gmail.com"
      copyright="        COPYRIGHT Bertrand Nouvel - JFLI - CNRS 2009"

  @classmethod
  def process(cls, * args, **kwargs):
     sys.stderr.write( "training...")
     ns=0
     for x in cls.vdb.values():
        cls.mdl.train([x])
        ns+=1 
     sys.stderr.write( "done... \nnumber of samples used ="+str(ns)+" processing time="+str(time.clock())+"\n")

if __name__=="__main__":
  MTrainApp.run(sys.argv[1:])

