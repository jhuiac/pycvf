# -*- coding: utf-8 -*-

#import numpy, sys
from pycvf.core.errors import *
from pycvf.core.builders import *
from pycvf.core.genericmodel import pycvf_model_class
from pycvf.datatypes import basics
from pycvf.datatypes import basics


class ModelIdxQuery(object):
    """
    This model does query for nearest neighbors in an already build databases for queries
    The input is a set of query vectors / query elements and the output are there nearest neighbors 
      in our database.
    """
    def __init__(self,idxclass,k=10,*args, **kwargs):
        self.idx=(pycvf_builder(idxclass) if type(idxclass) in [str, unicode] else idxclass)
        self.args=args
        self.kwargs=kwargs
        self.k=k
        self.model_node=None
    def set_model_node(self,model):
        self.model_node=model
    def on_model_destroy(self,model):
        self.model_node=None
    def process(self,x):
          if (x.ndim==1):
             x=x.reshape(-1,1)
             label=[label]
          elif (x.ndim>2):
             pycvf_error("Your data is too high dimensional for querying\n")
          return self.idx.getitems(x,self.k)


Model=pycvf_model_class(basics.NumericArray.Datatype,basics.NumericArray.Datatype)(ModelIdxQuery)
__call__=Model
