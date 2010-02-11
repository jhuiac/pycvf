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
import pywt
from pycvf.core import genericmodel
from pycvf.datatypes import image
from pycvf.datatypes import list as ldt

def idwt_one_layer(x,wav):
    return pywt.idwt2(x,wav)

class Imgidwt:
   def __init__(self,wavelet='db5'):
     if (not wavelet in pywt.wavelist()):
        print pywt.wavelist()
     self.wavelet=wavelet
   def process(self,x):
     r=map(lambda y:idwt_one_layer(y,self.wavelet),x)
     return numpy.dstack(r) 


Model=genericmodel.pycvf_model_class( ldt.Datatype(ldt.Datatype(image.Datatype)),image.Datatype)(Imgidwt)
__call__=Model
                 
