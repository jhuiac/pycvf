# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# MyModel By Bertrand NOUVEL
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
# ###############################################
#
################################################################################################################################################################################
# Includes
################################################################################################################################################################################
import scipy
#import hashlib
from pycvf.core.errors import *
from pycvf.core import genericmodel
from pycvf.core import builders
from pycvf.datatypes import basics
from pycvf.lib.info.cacheable import NotReady
#########################################################################################################################################
# Define our model
#########################################################################################################################################
  
class DEModelProcessor(object):
  """
  Here we reduce the dimension of set of points by using a density estimation model
  and by returning the parameters of this density estimation model.
  """
  def __init__(self, modelmodule="pycvf.stat.DE.pyem_gmm", *args, ** kwargs):     
     self.model=__import__(modelmodule,fromlist=modelmodule.split(".")[:-1])
     self.args=args
     self.kwargs=kwargs
     self.modelpath=None
  def process(self,v):
     m=self.model.Model(*self.args, **self.kwargs)
     print v.shape
     m.train(v)
     return m.get_as_vector()

    
Model=genericmodel.pycvf_model_class(None,basics.NumericVector.Datatype)(DEModelProcessor)
__call__=Model
