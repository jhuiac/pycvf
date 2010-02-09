# -*- coding: utf-8 -*-

#import numpy, sys
from pycvf.core import genericmodel
from pycvf.datatypes import basics
from pycvf.datatypes import basics

class Model(genericmodel.Model):
        def __init__(self,*args,**kwargs):
            super(Model,self).__init__(*args,**kwargs)
            self.model=None
        def input_datatype(self,x):
            return x
        def output_datatype(self,x):
            return basics.NumericArrayDatatype()
        def init_model(self,*args):
             self.model=[None]*len(args)
             self.modelpathno=[None]*len(args)
             for m,i in zip(args,range(len(args))):
               model, modelpath = m
               self.model[i]=(pycvf_builder(model) if type(model) in [str,unicode] else model)
               self.model[i].init("/",dtp,self)
               metak= self.model.get_features_meta().keys()
               self.modelpathno[i]=metak.index(modelpath)
             def tcombined(x):
               return numpy.vstack([ self.model[i].process(x)[self.modelpathno[i]]  for i in range(len(args)) ])
             self.processing=[ ('combined' , {'combined':tcombined })]

__call__=Model
