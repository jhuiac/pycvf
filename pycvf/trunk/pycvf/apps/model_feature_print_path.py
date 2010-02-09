#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################################################################################
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

class MPathPrintApp(ModelUsingApplication):
  class ProgramMetadata(object):
      name="Model Path Print Application"
      version="0.1"
      author="Bertrand Nouvel bertrand.nouvel@gmail.com"
      copyright="        COPYRIGHT Bertrand Nouvel - JFLI - CNRS 2009"


  modelpath=CmdLineString(None,"modelpath","modelpath","specified within the mode where the structure is to be extracted","//")
  delay=CmdLineString("i","interval","interval","wait for specified interval in-between entries","0")           
  @classmethod
  def process(cls, * args, **kwargs):
    #submdl=mdl.get_by_cname(modelpath.value)
    cls.mdl.print_tree()
    delay=float(cls.delay.value)
    for e in cls.vdb:
       cls.mdl.process_path([e[0]],[e[1]],cls.modelpath.value,lambda x:sys.stdout.write(unicode(x).encode('utf8')+u"\n"))
       if (delay):
          time.sleep(delay)
       
if __name__=='__main__':
  MPathPrintApp.run(sys.argv[1:])

