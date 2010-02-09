#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pycvf.core.generic_application import *
from pycvf.core.errors import *

class SimpleIndexerApp(IndexUsingApplication):
  class ProgramMetadata(object):
      name="Simple Indexer Application"
      version="1.0"
      author="Bertrand Nouvel bertrand.nouvel@gmail.com"
      copyright="        COPYRIGHT Bertrand Nouvel - JFLI - CNRS 2009"
      license="GPLv3"

  
  @classmethod
  def process(cls,nrels=1,*args,**kwargs):
     pycvf_debug(10, "Reading database")      
     for e in cls.vdb:
       cls.mdl.process(e[0],processf=lambda x:cls.idx.add(x,e[1]))
     pycvf_debug(10, "Saving index structure")
     cls.idx.save()
   
SimpleIndexerApp.run(sys.argv[1:])