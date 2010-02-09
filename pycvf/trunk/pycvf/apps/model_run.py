#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pycvf.core.generic_application import *

# -*- coding: utf-8 -*-
class MdlRunner(ModelUsingApplication):
  class ProgramMetadata(object):
      name="Model Feature Printer Application"
      version="1.0"
      author="Bertrand Nouvel bertrand.nouvel@gmail.com"
      copyright="        COPYRIGHT Bertrand Nouvel - JFLI - CNRS 2009"
      license="GPLv3"

  @classmethod
  def process(cls,*args,**kwargs):                         
     for e in cls.vdb:
       sys.stderr.write('.')
       #sys.stderr.write(e[1])
       cls.mdl.process(e[0],addr=e[1])
     sys.stderr.write('\n')

if __name__=="__main__":
  MdlRunner.run(sys.argv[1:])
