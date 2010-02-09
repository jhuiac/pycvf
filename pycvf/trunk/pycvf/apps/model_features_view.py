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

from PyQt4 import QtCore
from PyQt4 import QtGui
from pycvf.core import settings
from pycvf.core.generic_application import *
from pycvf.lib.ui.qt import qapp
from pycvf.lib.ui.qtfeaturesview import QtFeaturesViewerDialog

def is_prefix(a,b):
    return (b[:len(a)]==a)

# -*- coding: utf-8 -*-
class DbMdlFeatureView(ModelUsingApplication):
  class ProgramMetadata(object):
      name="Model Feature Printer Application"
      version="1.0"
      author="Bertrand Nouvel bertrand.nouvel@gmail.com"
      copyright="        COPYRIGHT Bertrand Nouvel - JFLI - CNRS 2009"

  delay=CmdLineString("i","interval","interval","wait for specified interval in-between entries","0")                             
  alle=CmdLineString(None,"all","boolean","shall we display all nodes or only final ones","0")
 

  @classmethod
  def process(cls,nrels=1,*args,**kwargs):     
    all=int(cls.alle.value)
    if int(cls.frameworkv.value)  not in [1,2]:   
      print cls.mmeta                 
      d=[ ([mm[0]],mm[1]['data_out']) for mm in cls.mmeta.items() ]
    else: 
      d=[ ([mm[0]],mm[1]) for mm in cls.mmeta ]
    print "D=",d
    if (not all):
      names=reduce(lambda b,n:b+[n[0][0]],d,[])
      nd=filter(lambda x: len(filter(lambda t:is_prefix(x[0][0][0], t),names ))==1 ,zip(d,range(len(d))))
      print "ND=",nd
    else:
      nd=zip(d,range(len(d)))
    delay=float(cls.delay.value)
    qmw=QtGui.QMainWindow()
    qv=QtFeaturesViewerDialog(map(lambda x:x[0],nd),qmw)
    subex=map(lambda x:x[1],nd)
    qv.show()
    qapp.processEvents()
    for e in cls.vdb:
       cls.mdl.metainfo_curaddr=e[1]
       cls.mdl.process(e[0],processf=lambda x:qv.push(reduce(lambda b,i:b+[x[i]],subex,[]),cls.vdb.datatype(),e[1]),addr=e[1])
       #mdl.process(e[0],processf=lambda x:sys.stdout.write(str(x)+"\n"))
       qapp.processEvents()
       if (delay):
          for i in range(int(delay*50)):
            qapp.processEvents()  
            time.sleep(0.02)
  
if __name__=="__main__":       
  DbMdlFeatureView.run(sys.argv[1:])

