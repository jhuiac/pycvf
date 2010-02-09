# -*- coding: utf-8 -*-
import numpy,scipy, sys,os
from pycvf.core.errors import *
from pycvf.core.builders import *
from pycvf.core.genericmodel import pycvf_model_class
from pycvf.datatypes import basics

def multiplicity(l):
  d={}
  for e in l:
      if d.has_key(e):
          d[e]+=1
      else:
          d[e]=1
  return d


class ModelTrainer:
    """
    ## Here we train a model on a labeled sample set and then we try to recover the data from the sample set
    """
    def __init__(self,statmodel,label=None,label_op=None,cross_train=0,*args, **kwargs):
        if (label==None):
            label="default"
        if (label_op==None):
            label_op=lambda x:x
        self.statmodel=(pycvf_builder(statmodel) if type(statmodel) in [str, unicode] else statmodel)
        self.args=args
        self.kwargs=kwargs
        self.model_node=None
        self.label=label
        self.label_op=label_op
        self.cross_train=cross_train
    def set_model_node(self,model):
        self.model_node=model
    def on_model_destroy(self,model):
        self.model_node=None
    def process(self,x):
          #neg=numpy.array(map(lambda x:x[0],self.negative_data.next()))
          labelv=eval("self.model_node.get_curdb().labeling_"+self.label,{'self':self})()
          addr=eval("self.model_node.get_curaddr()",{'self':self})
          assert(addr!=None)
          labels=self.label_op(labelv[addr])
          if (x.ndim==1):
             pycvf_warning("Your data is one dimensional only\n")
             pycvf_warning("Learning gonna be slow !\n")
             x=x.reshape(-1,1)
          elif (x.ndim>2):
             pycvf_error("Your data is too high dimensional for learning\n")          
          if (labels.ndim==1):
             pycvf_warning("Your label data is one dimensional only\n")
             pycvf_warning("Learning gonna be slow !\n")
             labels=labels.reshape(-1,1)
          elif (labels.ndim>2):
             pycvf_error("Your label data is too high dimensional for learning\n")
          #print labels
          if (labels.dtype in [int, float, numpy.uint8,numpy.int, numpy.float, numpy.float32,  numpy.float64] ):
             assert(labels.ptp()>0)
          if (not self.cross_train):
            self.statmodel.train(x,labels,online=False,*self.args,**self.kwargs)
            aclass=self.statmodel.predict(x)
            #print "ACLASS=",aclass
            print "EXACT=", (numpy.array(aclass)==numpy.array(labels.flat)).mean()
            return multiplicity(zip(aclass,labels.flat))
          else:
            sel=(numpy.random.random(x.shape[0]))<(float(self.cross_train)/(1+self.cross_train))
            self.statmodel.train(x[sel],labels[sel],online=False,*self.args,**self.kwargs)
            sel=(1-sel).astype(bool)
            aclass=self.statmodel.predict(x[sel])
            #print "ACLASS=",aclass
            
            print "EXACT=", (numpy.array(aclass)==numpy.array(labels.flat)[sel]).mean()*100
            return multiplicity(zip(aclass,labels.flat))

Model=pycvf_model_class(basics.NumericArray.Datatype,basics.Label.Datatype)(ModelTrainer)
__call__=Model
