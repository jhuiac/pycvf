# -*- coding: utf-8 -*-

#import numpy, sys
from pycvf.core.errors import *
from pycvf.core.builders import *
from pycvf.core.genericmodel import pycvf_model_class
from pycvf.datatypes import basics
from pycvf.datatypes import basics

class ModelTrainer:
    def __init__(self,statmodel,filename=None,negative_data=None,with_label=None,label_op=None,*args, **kwargs):
        self.statmodel=(pycvf_builder(statmodel) if type(statmodel) in [str, unicode] else statmodel)
        self.filename=filename
        self.args=args
        self.kwargs=kwargs
        self.with_label=with_label
        self.label_op=((lambda x:x) if label_op==None else label_op)
        self.model_node=None
        self.negative_data=negative_data
        if (self.negative_data!=None):
          self.negative_data=iter(self.negative_data)
    def set_model_node(self,model):
        self.filename=(self.filename if self.filename!=None else model.get_modelpath() + self.statmodel.__module__.split('.')[-1])
        self.model_node=model
    def on_model_destroy(self,model):
        self.model_node=None        
        if (self.filename):
          pycvf_warning("Saving model to "+str(self.filename))
          f=file(self.filename,"wb")
          self.statmodel.dump(f)
          f.close()
        else:
          pycvf_warning("No filename thus not model is not saved")        
    def process(self,x):
        if (self.with_label==None):
          if (self.negative_data):
            neg,negaddr=self.negative_data.next()
          self.statmodel.train(x,online=True,*self.args,**self.kwargs)
        else:
          if (self.with_label==True):
            self.with_label="default"
          if (self.negative_data):
            neg,negaddr=self.negative_data.next()
            nld=eval("self.negative_data.labeling_"+self.with_label)()
            
          ld=eval("self.model_node.get_curdb().labeling_"+self.with_label)()
          #print ld
          #print self.model_node
          #print self.model_node.get_curaddr
          #print self.model_node.get_curaddr()
          #print ld[self.model_node.get_curaddr()]
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
                                online=True,
                                *self.args,
                                **self.kwargs
                                ) 

Model=pycvf_model_class(None,None)(ModelTrainer)
__call__=Model
