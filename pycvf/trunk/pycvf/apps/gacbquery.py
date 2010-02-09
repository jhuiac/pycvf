#!/usr/bin/env python
# -*- coding: utf-8 -*-
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



# -*- coding: utf-8 -*-
from pycvf.core.errors import *
from pycvf.core.generic_application import *
from pycvf.lib.ui.qtnearestneighborview import *
from pycvf.lib.ui.qt import *
from pycvf.indexes import load_index

class SimpleIndexQueryApp(IndexUsingApplication):
  class ProgramMetadata(object):
      name="Graphical Query of Nearest Neighbors"
      version="1.0"
      author="Bertrand Nouvel bertrand.nouvel@gmail.com"
      license="GPLv3"
      copyright="        COPYRIGHT Bertrand Nouvel - JFLI - CNRS 2009"

  number_query=CmdLineString('n',"numberofneighbors",'number',"name of neighbours","3")  
  key=CmdLineString(None,"key","modelpath","specified within the model what should be used as key when indexing","/")
  feature_select=["selected_feature"] # we only create one index here
  delay=CmdLineString("i","interval","interval","wait for specified interval in-between entries","0")                            
  block=CmdLineString('b',"block",'number',"do block-queries","1")

  @classmethod
  def process(cls,nrels=1,*args,**kwargs):
    cls.idx=load_index.__call__((cls.idx.root_class if hasattr(cls.idx,"root_class") else cls.idx.__class__),cls.index_filename)
    delay=float(cls.delay.value)
    cls.mdl.print_tree()
    nq=int(cls.number_query.value)
    bv=int(cls.block.value)
    d=[ (mm[0],mm[1]) for mm in cls.mmeta.items() ]
    qmw=QtGui.QMainWindow()
    qv=QtNearestNeighborsViewerDialog(d[0],nq,bv,qmw)
    qv.show()
    qapp.processEvents()
    
    idb=iter(cls.vdb)
    try:
       while True:
          e=[ idb.next() for i in range(bv) ]
          keys=cls.mdl.process_path(map(lambda f:f[0],e),map(lambda f:f[1],e),cls.key.value,lambda x:x)
          #print keys
          #for c in keys:
          if True:
                ## compute nearest neighbours
                #pycvf_warning( "keysKEYSkeys:"+str( keys))
                #time.sleep(0.5)
                keys=numpy.array(keys)
                l=cls.idx.getitems(keys,nq)          # get the nearest element for the keys                
                ## Extract nearest neighbours value from database
                #pycvf_warning( "resultRESULTresult:"+str( l))
                #time.sleep(5.5)                
                xxx=map (lambda y:map(lambda x:(cls.vdb[x[0][0]],x[1]),y),l)
                ## Display the results
                qv.push((map(lambda f:f[0],e),xxx))
                qapp.processEvents()
                #print c
          if (delay):
              for i in range(int(delay*50)):
                qapp.processEvents()  
                time.sleep(0.02)
    except StopIteration,e:
          print e
          

SimpleIndexQueryApp.run(sys.argv[1:])




