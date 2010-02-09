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
from pycvf.nodes import genericmodel
from pycvf.nodes.datatypes import basics
from pycvf.lib.stats.meanvariancemodel import SimpleMeanVarianceModel

class Whitener:
    def __init__(self,filename):
        self.filename=filename        
        try:
           self.model=SimpleMeanVarianceModel.load(file(filename,"rb"))
        except:
           self.model=SimpleMeanVarianceModel()
    def __del__(self):
        self.model.dump(file(filename,"wb"))
    def process(self,x):
        self.model.train([ x ],online=True)
        return (x-self.model.mean())/(0.00001+self.model.std())

class Model(genericmodel.Model):
        def input_datatype(self,x):
            return x
        def output_datatype(self,x):
            return basics.NumericArrayDatatype()
        def init_model(self,*args, **kwargs):
              print dir(self.application)
              #assert(False)
              self.processing=[ ('whiten' , {'whiten':Whitener(*args,**kwargs).process} )]

__call__=Model
                 