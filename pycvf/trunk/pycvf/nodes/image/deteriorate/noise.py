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


###
###


from pycvf.core.genericmodel import pycvf_model_function
from pycvf.datatypes import image
import numpy

def noise(x,amount=0.5):
    if (x.dtype==numpy.uint8):
        amount*=255
        return (x.astype(float)+(numpy.random.random(x.shape)-.5)*amount).clip(0,255).astype(x.dtype)
    else:
        return x+((numpy.random.random(x.shape)-.5)*amount)

Model=pycvf_model_function(image.Datatype, image.Datatype)(noise)
__call__=Model
