#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# VideoModel Trainer builder By Bertrand NOUVEL
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
# ###############################################
#
#########################################################################################################################################
# Import required objects
#########################################################################################################################################

import sys
from pycvf.lib.info.graph import *
from pycvf.core.generic_application import *
from pycvf.lib.ui.qt import qapp
from pycvf.lib.ui import qtdbevaluator


class DbEvaluator(DatabaseUsingApplication):
  class ProgramMetadata(object):
      name="Database Show Application"
      version="1.0"
      author="Bertrand Nouvel bertrand.nouvel@gmail.com"
      copyright="        COPYRIGHT Bertrand Nouvel - JFLI - CNRS 2009"
      license="GPLv3"

  session=CmdLineString("s","session","sessionname","name of the session","std")
  annfilename=CmdLineString(None,"weightfile","path","file should be use to store evaluation result",os.environ["HOME"]+"/"+"weights/$database-$session.pcl")

  @classmethod
  def process(cls,nrels=1,*args,**kwargs):                                                                                    
     annfile=cls.annfilename.value
     annfile=annfile.replace("$database",cls.database.value)
     annfile=annfile.replace("$session",cls.session.value)
     qapp.processEvents()
     try:
        vdbval=pickle.load(file(annfile,"rb"))
     except:
         vdbval=None
     d=qtdbevaluator.QtDBEvaluatorDialog(cls.vdb,cls.vdbval)
     qapp.processEvents()
     if d.exec_():
       pickle.dump(d.pwl.vdbval,file(annfile,"wb"),protocol=2)
  

if __name__=="__main__":
   DbEvaluator.run(sys.argv[1])