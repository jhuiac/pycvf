# -*- coding: utf-8 -*-

#import numpy, sys
from pycvf.core.errors import *
from pycvf.core.builders import *
from pycvf.core.genericmodel import pycvf_model_class
from pycvf.datatypes import basics
from pycvf.datatypes import basics


class ModelIdxBuilder(object):
    """
    This model is used to build an index from a set of vector / objects.
    The Input Vector Set is directly returned from the process...
    That thus may be used transparently anywhere...
    """
    def __init__(self,idxclass,label="default",label_op=None,indexfilename="idx",*args, **kwargs):
        self.idx=(pycvf_builder(idxclass) if type(idxclass) in [str, unicode] else idxclass)
        self.args=args
        self.kwargs=kwargs
        self.label=label
        self.indexfilename=indexfilename
        self.label_op=((lambda x:x) if label_op==None else label_op)
        self.model_node=None
    def set_model_node(self,model):
        self.model_node=model
    def on_model_destroy(self,model):
        self.model_node=None
        self.idx.save(self.indexfilename)
    def process(self,x):
          if (self.label==True):
            self.label="default"            
          ld=eval("self.model_node.get_curdb().labeling_"+self.label)()
          label=self.label_op(
                                ld[self.model_node.get_curaddr()]
                                )
          if (x.ndim==1):
             pycvf_warning("Your data is one dimensional only\n")
             pycvf_warning("Indexing gonna be slow ?\n")
             x=x.reshape(-1,1)
             label=[label]
          elif (x.ndim>2):
             pycvf_error("Your data is too high dimensional for learning\n")
          for c in zip(x,label):
               self.idx.add(c[0],c[1])
          return x


Model=pycvf_model_class(basics.NumericArray.Datatype,basics.NumericArray.Datatype)(ModelIdxBuilder)
__call__=Model
