#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pycvf.core.generic_application import *
from pycvf.core.builders import pycvf_builder

class DbShowLblApp(DatabaseUsingApplication):
  class ProgramMetadata(object):
      name="Database Show Label Application"
      version="1.0"
      author="Bertrand Nouvel bertrand.nouvel@gmail.com"
      copyright="        COPYRIGHT Bertrand Nouvel - JFLI - CNRS 2009"

  delay=CmdLineString("i","interval","interval","wait for specified interval in-between entries","0")                             
  print_addr=CmdLineString("A","with_address","boolean","should we see the address","0")                               
  forced_datatype=CmdLineString(None,"force_datatype","expr","specifies a datatype to force","")                    
  label=CmdLineString('L',"label","labelname","specifies the name of the labelset to consider","default")

  @classmethod
  def process(cls,*args,**kwargs):                                                      
     delay=float(cls.delay.value)
     print_addr=int(cls.print_addr.value)
     label=str(cls.label.value)
     label_c=eval("cls.vdb.labeling_"+label,{'cls':cls})()
     dtp=(pycvf_builder(cls.forced_datatype.value) if len(cls.forced_datatype.value) else label_c.datatype()) #cls.vdb

     for i in cls.vdb:
       if print_addr:
           print(i[1])
       dtp.display(label_c[i[1]])
       if (delay):
          time.sleep(delay)
     
     print ("all labels" , list(label_c))

if __name__=="__main__":       
  DbShowLblApp.run(sys.argv[1:])

