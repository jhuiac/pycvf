# -*- coding: utf-8 -*-

#import numpy, sys
from pycvf.core.errors import *
from pycvf.core.builders import *
from pycvf.core.genericmodel import pycvf_model_class
from pycvf.datatypes import basics
from pycvf.datatypes import basics


class ModelTrainer:
    """
    ## Here we train a model on sample set and then we use that model to reproduct a new set of values no filename is required
    """
    def __init__(self,statmodel,npoints=1000,negative_data=None,with_label=None,label_op=None,*args, **kwargs):
        self.statmodel=(pycvf_builder(statmodel) if type(statmodel) in [str, unicode] else statmodel)
        self.args=args
        self.kwargs=kwargs
        self.npoints=npoints
        self.with_label=with_label
        self.label_op=((lambda x:x) if label_op==None else label_op)
        self.model_node=None
        self.negative_data=negative_data
        if (self.negative_data!=None):
          self.negative_data=iter(self.negative_data)
    def set_model_node(self,model):
        self.model_node=model
    def on_model_destroy(self,model):
        self.model_node=None
    def process(self,x):
        if (self.with_label==None):
          if (self.negative_data):
            neg,negaddr=self.negative_data.next()
          self.statmodel.train(x,online=False,*self.args,**self.kwargs)
        else:
          if (self.with_label==True):
            self.with_label="default"
          if (self.negative_data):
            neg,negaddr=self.negative_data.next()
            nld=eval("self.negative_data.labeling_"+self.with_label)()
            
          ld=eval("self.model_node.get_curdb().labeling_"+self.with_label)()
          label=self.label_op(
                                ld[self.model_node.get_curaddr()]
                                )
          if (x.ndim==1):
             pycvf_warning("Your data is one dimensional only\n")
             pycvf_warning("Learning gonna be slow !\n")
             x=x.reshape(-1,1)
             label=[label]
          elif (x.ndim>2):
             pycvf_error("Your data is too high dimensional for learning\n")
          self.statmodel.train(x,
                               label ,
                                online=False,
                                *self.args,
                                **self.kwargs
                                ) 
        return self.statmodel.sample(self.npoints)


Model=pycvf_model_class(basics.NumericArray.Datatype,basics.NumericArray.Datatype)(ModelTrainer)
__call__=Model
