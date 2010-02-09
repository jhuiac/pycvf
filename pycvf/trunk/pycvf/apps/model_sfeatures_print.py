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

class ProgramMetadata:
    name="Model Features Printer"
    version="0.1"
    license="GPLv3"
    author="Bertrand Nouvel bertrand.nouvel@gmail.com"
    copyright="        COPYRIGHT Bertrand Nouvel - JFLI - CNRS 2009"

import re, os, math, random, time,sys, traceback, getopt
from pycvf.lib.info.options import *
        
mymodel=CmdLineString('m',"model","model","set the model to be used","naive")
mymodelargs=CmdLineString(None,"modelargs","model_arguments","set model options","") 
def modelhelp():
    try :
      exec("from "+ mymodel.value +" import *")
    except ImportError:
      exec("from pycvf.nodes."+ mymodel.value +" import *")
    import inspect
    print inspect.getargspec(MyModel.__init__)
    sys.exit(-1)
dbhelp_option=CmdLineOption(None,"modelhelp",None,"show info on parameters required by the database",modelhelp)                             


database=CmdLineString(None,"db","database","set the database to be read","mvp")
databaseargs=CmdLineString(None,"dbargs","database_arguments","set database options","") 
def dbhelp():
    try:
       exec("from "+ database.value +" import *")
    except:
       exec("from jfli.databases."+ database.value +" import *")    
    import inspect
    print inspect.getargspec(ContentsDatabase.__init__)
    sys.exit(-1)
dbhelp_option=CmdLineOption(None,"dbhelp",None,"show info on parameters required by the database",dbhelp)                             


modelpart=CmdLineString(None,"modelpart","modelpath","specified within the mode where the structure is to be extracted","//")
structure=CmdLineString("S","structure","structurename","specifies the structure to be instanciated","//")

#############                                                                          
do_parse_options(ProgramMetadata)
#############



try:
  exec("from "+ database.value +" import ContentsDatabase")
except:
  exec("from jfli.databases."+ database.value +" import ContentsDatabase")    

if __name__=="__main__":
  import datetime
  if (len(databaseargs.value)):
    vdb=ContentsDatabase( **eval('{'+databaseargs.value+'}'))
  else:
    vdb=ContentsDatabase()      
  from pycvf.nodes.modelbuilder import model_build
  mdl=model_build(mymodel.value,vdb,suppargs=mymodelargs.value)
  mmeta=mdl.get_features_meta(vdb)

  submdl=mdl.get_by_cname(modelpart.value)
  print submdl
  print submdl.structures
  
  for e in vdb:
       #print mdl.metas
       #mdl.process(e[0],lambda ee:sys.stdout.write(str(mdl.features_for(submdl,ee))))
       mdl.process(e[0],lambda ee:submdl.extract_structure(mdl.features_for(submdl,ee)[0],submdl.structures.values()[0],processf=lambda x:sys.stdout.write(str(x)+"\n")))
       time.sleep(0.1)
       

  
