#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pycvf.core.generic_application import *
from pycvf.core.autoimp import *

def mse(a,b):
  return ((a-b)**2).mean()  

def psnr(a,b):
  return -10*numpy.log10(1./mse(a,b))

class ModelCompareApp(DatabaseUsingApplication):
  class ProgramMetadata(object):
      name="Model Comparing Application"
      version="1.0"
      author="Bertrand Nouvel bertrand.nouvel@gmail.com"
      copyright="        COPYRIGHT Bertrand Nouvel - JFLI - CNRS 2009"


  frameworkv=CmdLineString(None,"framework_version","frameworkv","version of the framework to be used",settings.DEFAULT_FRAMEWORK)
  mymodel1=CmdLineString('m',"model1","model","set the model to be used",settings.DEFAULT_MODEL)
  session=CmdLineString('s',"session1",'name_of_session',"name of the session",settings.DEFAULT_SESSION)                             
  mymodel1=CmdLineString('n',"model2","model","set the model to be used",settings.DEFAULT_MODEL)
  session=CmdLineString('t',"session2",'name_of_session',"name of the session",settings.DEFAULT_SESSION)                             
  metricname=CmdLineString('M',"metric",'metricname',"name of the metric","psnr")                             

  delay=CmdLineString("i","interval","interval","wait for specified interval in-between entries","0")                             

  @classmethod
  def process(cls,nrels=1,*args,**kwargs):
                                                                                       
     delay=float(cls.delay.value)
     metric=eval(cls.metricname.value)

     for i in cls.vdb:
       r=(metric(cls.mdl.process(i[0]),cls.mdl.process(i[1])),e[1])
       print r 

if __name__=="__main__":       
  ModelCompareApp.run(sys.argv[1:])

