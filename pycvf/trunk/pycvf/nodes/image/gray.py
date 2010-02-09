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


def gray(x):
    return x.mean(axis=2).reshape(x.shape[0],x.shape[1],1)


Model=genericmodel.pycvf_model_function(image.Datatype,image.Datatype)(gray)
__call__=Model
                 
