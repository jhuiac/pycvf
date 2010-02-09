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

def fft_one_layer(x):
    return numpy.fft.fft2(x)

def all_layer(f,i):
    return numpy.dstack([f(i[:,:,l]) for l in range(i.shape[2])])

def imgfft(x,roll=True):
    if (x.ndim==3):
        r=all_layer(fft_one_layer,x)
    else:
        r=fft_one_layer_x
    if roll:
        r=numpy.roll(r,r.shape[0]//2,axis=0)
        r=numpy.roll(r,r.shape[1]//2,axis=1)        
    return r 


Model=genericmodel.pycvf_model_function(image.Datatype,image.Datatype)(imgfft)
__call__=Model
                 
