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

def dwt_one_layer(x,wav):
    return pywt.dwt2(x,wav)

def all_layer(f,i):
    return ([f(i[:,:,l]) for l in range(i.shape[2])])

def imgdwt(x,wavelet='db5'):
    if (x.ndim==3):
        r=all_layer(lambda y:dwt_one_layer(y,wavelet),x)
    else:
        r=[dwt_one_layer(x,wavelet)]
    return r 


Model=genericmodel.pycvf_model_function(image.Datatype, ldt.Datatype(ldt.Datatype(image.Datatype)))(imgdwt)
__call__=Model
                 
