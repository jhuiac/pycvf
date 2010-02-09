# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# MyModel By Bertrand NOUVEL
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
# ###############################################
#

import numpy, sys, scipy
import scipy.stats
from pycvf.core import genericmodel
from pycvf.datatypes import basics

class Model(genericmodel.Model):
        def input_datatype(self,x):
            return x
        def output_datatype(self,x):
            return basics.NumericArrayDatatype()
        def init_model(self, moments=[ 1,2,3 ] , layersdim=0):
              def compute_moments(x):
                  v=reduce(lambda x1,x2:x1*x2,x.shape[:x.ndim-layersdim],1)
                  h=reduce(lambda x1,x2:x1*x2,x.shape[x.ndim-layersdim:],1)
                  x=x.reshape(v,h)
                  return [ scipy.stats.moment(x,m,0) for m in moments ]
              self.processing=[ ('compute_moments' , {'compute_moments':compute_moments} )]

__call__=Model
