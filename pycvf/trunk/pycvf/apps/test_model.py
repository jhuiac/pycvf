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

import re, os, math, random, time,sys, traceback, getopt
import sys
from pycvf.core.generic_application import *

class MTesterApp(ModelUsingApplication):
  class ProgramMetadata(object):
      name="PyCvF Application"
      version="0.1"
      license="GPLv3"
      author="Bertrand Nouvel bertrand.nouvel@gmail.com"
      copyright="        COPYRIGHT Bertrand Nouvel - JFLI - CNRS 2009"

  @classmethod
  def process(cls, * args, **kwargs):
     print "process"
     for x in cls.vdb.values():
        print cls.mdl.test([x])
     print "/process"

if __name__=="__main__":
  MTesterApp.run(sys.argv[1:])

