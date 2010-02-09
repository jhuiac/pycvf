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
from pycvf.datatypes import image

def ifft_one_layer(x):
    return numpy.fft.ifft2(x)

def all_layer(f,i):
    return numpy.dstack([f(i[:,:,l]) for l in range(i.shape[2])])

def imgifft(x,roll=True):
    if roll:
        x=numpy.roll(x,x.shape[0]//2,axis=0)
        x=numpy.roll(x,x.shape[1]//2,axis=1)            
    if (x.ndim==3):
        r=all_layer(ifft_one_layer,x)
    else:
        r=ifft_one_layer_x
    return r 


Model=genericmodel.pycvf_model_function(image.Datatype,image.Datatype)(imgifft)
__call__=Model
                 
