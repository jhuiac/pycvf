#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re, os, math, random, time,sys, traceback, getopt
import time
import Pyro
import Pyro.core
import Pyro.protocol
from pycvf.lib.info.graph import *
from pycvf.core.generic_application import *


class MyCustomValidator(Pyro.protocol.DefaultConnValidator):
    pass

class DbServer(Pyro.core.ObjBase):
            def __init__(self,vdb):
                    Pyro.core.ObjBase.__init__(self)
                    self.vdb=vdb
                    self.vdbi=iter(self.vdb)
            def next(self, name):
                   try:
                       return self.vdbi.next()
                   except:
                       self.vdbi=iter(self.vdb)
                       return self.vdbi.next()                       
                    

class DbServerApp(DatabaseUsingApplication):
  class ProgramMetadata(object):
      name="Database Server Application"
      version="1.0"
      author="Bertrand Nouvel bertrand.nouvel@gmail.com"
      copyright="        COPYRIGHT Bertrand Nouvel - JFLI - CNRS 2009"

  @classmethod
  def process(cls,nrels=1,*args,**kwargs):
    Pyro.core.initServer()
    daemon=Pyro.core.Daemon()
    mcv=MyCustomValidator()
    daemon.setNewConnectionValidator(mcv)
    mcv.setAllowedIdentifications(["jfli"])
    uri=daemon.connect(DbServer(cls.vdb),"dbserver")
    print "The daemon runs on port:",daemon.port
    print "The object's uri is:",uri
    daemon.requestLoop()

                    
if __name__=="__main__":
   DbServerApp.run(sys.argv[1:])



  
