# -*- coding: utf-8 -*-
import numpy,scipy, sys
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
    ## Here we train a model on sample set and then we use that model to reproduct a new set of values no filename is required
    """
    def __init__(self,statmodel,negative_data,*args, **kwargs):
        self.statmodel=(pycvf_builder(statmodel) if type(statmodel) in [str, unicode] else statmodel)
        self.args=args
        self.kwargs=kwargs
        self.model_node=None
        self.negative_data=negative_data
        if (self.negative_data!=None):
          self.negative_data=iter(self.negative_data)
    def set_model_node(self,model):
        self.model_node=model
    def on_model_destroy(self,model):
        self.model_node=None
    def process(self,x):
          #neg=numpy.array(map(lambda x:x[0],self.negative_data.next()))
          neg=self.negative_data.next()[0]
          if (x.ndim==1):
             pycvf_warning("Your data is one dimensional only\n")
             pycvf_warning("Learning gonna be slow !\n")
             x=x.reshape(-1,1)
          elif (x.ndim>2):
             pycvf_error("Your data is too high dimensional for learning\n")          
          if (neg.ndim==1):
             pycvf_warning("Your data is one dimensional only\n")
             pycvf_warning("Learning gonna be slow !\n")
             neg=neg.reshape(-1,1)
          elif (neg.ndim>2):
             pycvf_error("Your data is too high dimensional for learning\n")                       
          self.statmodel.train(x,neg,online=False,*self.args,**self.kwargs)
          adata=numpy.vstack([x,neg])
          aclass=self.statmodel.test(adata)
          rclass=[0]*x.shape[0]+[1]*neg.shape[0]
          return multiplicity(zip(numpy.sign(aclass),rclass))

Model=pycvf_model_class(basics.NumericArray.Datatype,basics.Label.Datatype)(ModelTrainer)
__call__=Model
