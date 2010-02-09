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


import numpy
from pycvf.core import genericmodel
from pycvf.datatypes import basics
from pycvf.datatypes import image
#from jfli import stats.models



class MyModel(genericmodel.GenericModel):
        """ Processor aims at a being a generic module for allowing 
            to execute any arbitratry Function
        """
        input_datatype=lambda self,x:x
        datatype=lambda self,x:x
        def init(self,fct,optmodul,outputtype):
           self.fct=fct
           self.optmodul=optmodul
           self.outputtype=outputtype
           genericmodel.GenericModel.init(self)
        def doqueueeffect(self,x):
            if (x.ndim==3):
              assert(x.shape[2]==1)
              x=x.reshape(x.shape[0],x.shape[1])
            if (self.postfilter!=None):
              return self.postfilter(self.fftcenter(numpy.fft.fft2(x))).reshape(x.shape[0],x.shape[1],1)
            else:
              return numpy.fft.fft2(self.fftcenter(x)).reshape(x.shape[0],x.shape[1],1)
        def init_featurefilter(self):
              self.featurefilter=('src|fft2'  ,{'fft2':self.dofft2},  {})
        def init_structures(self):
              return {}

