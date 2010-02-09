#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pycvf.core.generic_application import *


# -*- coding: utf-8 -*-
class DbMdlFeaturePrint(ModelUsingApplication):
  class ProgramMetadata(object):
      name="Model Feature Printer Application"
      version="1.0"
      author="Bertrand Nouvel bertrand.nouvel@gmail.com"
      copyright="        COPYRIGHT Bertrand Nouvel - JFLI - CNRS 2009"

  @classmethod
  def process(cls,*args,**kwargs):                         
     print "META"
     print cls.mdl.get_features_meta()
     print "CNAMES"
     print cls.mdl.get_cnames()
     print "TREE"
     cls.mdl.print_tree()
     print "OK"
     def print_e(x):
        sys.stdout.write(unicode(x).encode('utf8')+"\n")
     for e in cls.vdb:
       cls.mdl.process(e[0],processf=print_e)
 

if __name__=="__main__":
  DbMdlFeaturePrint.run(sys.argv[1:])
