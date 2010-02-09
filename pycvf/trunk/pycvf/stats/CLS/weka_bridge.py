#!/usr/bin/env python
# -*- coding: utf-8 -*-
## ##########################################################################################################
## 
## This file is released under GNU Public License v3
## See LICENSE File at the top the pycvf tree.
##
## Author : Bertrand NOUVEL / CNRS (2009)
##
##
##
## Revision FILE: $Id$
##
## ###########################################################################################################
## copyright $Copyright$
## @version $Revision$
## @lastrevision $Date$
## @modifiedby $LastChangedBy$
## @lastmodified $LastChangedDate$
#############################################################################################################


# -*- coding: utf-8 -*-
import sys, os
import traceback
import numpy
import scipy
import random
import cPickle as pickle
import marshal
import arff
###
###
###
from pycvf.core.distribution import *
from pycvf.core.utilities import TempDirectory, pycvf_config_var
pycvf_dist(PYCVFD_REQUIRE_PACKAGE,"weka")

WEKACLASSPATH=pycvf_config_var("WEKACLASSPATH","/usr/share/java/weka-3.6.0.jar:/home/tranx/build/yumegraphe.contrib/libsvm-2.85/java/libsvm.jar")
JAVA_CMD=pycvf_config_var("JAVA_CMD","java")

def numpy2arff(filename,matrix):
       infilecsv=filename+".csv"
       infilearff=filename
       os.system(' '.join(["CLASSPATH='%s'"%(WEKACLASSPATH,),
                           JAVA_CMD,
                           "weka.core.converters.CSVLoader", 
                           infilecsv, 
                           ">",
                           infilearff
                          ]))   
            
    
def numpy2arff(filename,matrix):
    alist=map(lambda x:("a%03d"%(x,),1,[]),range(matrix.shape[1]))
    alist[-1]=(alist[-1][0],0,list(set(matrix[:,-1])))
    print filename, alist,matrix
    arff.arffwrite(file(filename,"wb"), alist,matrix)

class WekaModel:
   def __init__(self, weka_model="weka.classifiers.trees.J48",addops=[]):
       self.weka_model=weka_model
       self.addops=addops
       self.tmpdir=TempDirectory()
   @staticmethod
   def load(file_, *args, **kwargs):
       assert(False)
   def train(self,data,label,online=False,cross_validation_result=True):
       assert(online==False)
       #print "DATA=",data
       #print "LABEL=",label
       infile=os.path.join(self.tmpdir.get(),"train.arff")
       mdlfile=os.path.join(self.tmpdir.get(),"out.mdl")
       addops=["-r", "-v"]
       if cross_validation_result==False:
           addops+=["-no-cv" ]
       xdata=numpy.hstack([data,label])
       numpy2arff(infile,xdata)
       cmdline=' '.join(["CLASSPATH='%s'"%(WEKACLASSPATH,),JAVA_CMD,self.weka_model, "-t",infile , "-d",mdlfile]+self.addops+addops)
       print cmdline
       os.system(cmdline)
   def test(self,test_data,ground_truth=None):
       assert(online==False)
       infile=os.path.join(self.tmpdir.get(),"test.arff")       
       mdlfile=os.path.join(self.tmpdir.get(),"out.mdl")
       addops=[]
       numpy2arff(infile,test_data)
       os.system(' '.join(["CLASSPATH='%s'"%(WEKACLASSPATH,),JAVA_CMD,self.weka_model, "-l",mdlfile, "-T",infile ]))
   def memory_cost(self, *args, **kwargs):
        assert(False)
   def cpu_cost(self, *args, **kwargs):
        assert(False)
   def random_improve(self,value,amount=0.5, prec=1):
        ## TRY TO RANDOMLY CHANGE WITH A NEAREST NEIGHBOR
        #print "random_improve not yet implemented doing sample instead !!! hist"
        #return self.sample(value.shape[0])
        assert(False)   

__call__=WekaModel
StatModel=WekaModel

###
### For Jython-Weka ...
###
"""

from weka.core.converters.ConvertUtils import DataSource
from weka.core import Instances

data1=DataSource.read("filename.csv") #arff xrff
classifier=classifer()
classifier.buildClassifier(train)
for x in range(test.numInstances()):
"""