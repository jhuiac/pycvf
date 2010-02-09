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


import numpy, sys
from pycvf.core import genericmodel
from pycvf.core.genericmodel import NotReady,STATUS_ERROR,STATUS_NOT_READY,STATUS_READY
from pycvf.datatypes import basics
from pycvf.stats.DR.PCA import IncrementalPCAdimred


class PCABasisProcessor(object):
  def __init__(self,*args, **kwargs):     
     self.args=args
     self.kwargs=kwargs
     self.directory=None
  def process(self,v):
        self.ipca=IncrementalPCAdimred(-1,*self.args, **self.kwargs)
        self.ipca.add_train(v)
        self.ipca.recompute()
        return self.ipca.M

    
Model=genericmodel.pycvf_model_class(basics.NumericArray.Datatype,basics.NumericArray.Datatype)(PCABasisProcessor)
__call__=Model
