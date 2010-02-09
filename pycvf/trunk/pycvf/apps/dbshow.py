#!/usr/bin/env python 
# -*- coding: utf-8 -*-
from pycvf.core.generic_application import *
from pycvf.core.builders import pycvf_builder

class DbShowApp(DatabaseUsingApplication):
  class ProgramMetadata(object):
      name="Database Show Application"
      version="1.0"
      author="Bertrand Nouvel bertrand.nouvel@gmail.com"
      copyright="        COPYRIGHT Bertrand Nouvel - JFLI - CNRS 2009"

  delay=CmdLineString("i","interval","interval","wait for specified interval in-between entries","0")                             
  print_addr=CmdLineString("A","with_address","boolean","should we see the address","0")                               
  forced_datatype=CmdLineString(None,"force_datatype","expr","specifies a datatype to force","")                    

  @classmethod
  def process(cls,*args,**kwargs):
                                                                                       
     delay=float(cls.delay.value)
     print_addr=int(cls.print_addr.value)
     dtp=(pycvf_builder(cls.forced_datatype.value) if len(cls.forced_datatype.value) else cls.vdb.datatype())

     for i in cls.vdb:
       if print_addr:
           print(i[1])
       dtp.display(i[0])           
       if (delay):
          time.sleep(delay)

if __name__=="__main__":       
  DbShowApp.run(sys.argv[1:])

