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
from jfli import stats.models

##
## This is simply a color model that is to apply by filtering
##

class Model(genericmodel.GenericModel):
        input_datatype=lambda self,x:image.DataType
        datatype=lambda self,x:image.DataType
        def __init__(colormodel)
              self.colormodel=colormodel
        def init_featurefilter(self):
                 self.featurefilter=('src|fft2|fft2features'  ,{'fft2|fft2eatures':fft=numpy.fft.fft2,fft2features},  {})

__call__=Model
