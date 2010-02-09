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
    def __init__(self,statmodel,label=None,label_op=None,*args, **kwargs):
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
    def set_model_node(self,model):
        self.model_node=model
    def on_model_destroy(self,model):
        self.model_node=None
    def process(self,x):
          #neg=numpy.array(map(lambda x:x[0],self.negative_data.next()))
          labelv=eval("self.model_node.get_curdb().labeling_"+self.label,{'self':self})()
          addr=eval("self.model_node.get_curaddr()",{'self':self})
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
          assert(labels.ptp()>0)
          self.statmodel.train(x,labels,online=False,*self.args,**self.kwargs)
          aclass=self.statmodel.predict(data)
          return multiplicity(zip(numpy.sign(aclass),labels.flat))

Model=pycvf_model_class(basics.NumericArray.Datatype,basics.Label.Datatype)(ModelTrainer)
__call__=Model
