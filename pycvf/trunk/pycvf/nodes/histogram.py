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
from pycvf.datatypes import basics


class Model(genericmodel.Model):
        def input_datatype(self,x):
            return x
        def output_datatype(self,x):
            return basics.NumericArray.Datatype()
        def init_model(self,*args, **kwargs):
              self.processing=[ ('histogram' , {'histogram':lambda x:numpy.histogram(x,*args,**kwargs)[0]} )]

__call__=Model
                 