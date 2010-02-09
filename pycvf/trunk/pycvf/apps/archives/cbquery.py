#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pycvf.core.generic_application import *


class SimpleIndexQueryApp(IndexUsingApplication):
  class ProgramMetadata(object):
      name="Simple Indexer Application"
      version="1.0"
      author="Bertrand Nouvel bertrand.nouvel@gmail.com"
      copyright="        COPYRIGHT Bertrand Nouvel - JFLI - CNRS 2009"
      license="GPLv3"

  number_query=CmdLineString('n',"numberofneighbors",'number',"name of neighbours","3")  

  @classmethod
  def process(cls,nrels=1,*args,**kwargs):
    nq=int(cls.number_query.value)
    for e in cls.vdb:
       print cls.mdl.process(e[0],processf=lambda x:cls.idx.query([x],nq))

SimpleIndexQueryApp.run(sys.argv[1:])

