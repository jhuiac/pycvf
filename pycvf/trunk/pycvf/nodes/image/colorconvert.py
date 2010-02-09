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
from pycvf.lib.graphics import colortransforms

def colorconvert(x,fromto="rgb2hsv"):
    return (eval("colortransforms."+fromto))(x)


Model=genericmodel.pycvf_model_function(image.Datatype,image.Datatype)(colorconvert)
__call__=Model
                 
