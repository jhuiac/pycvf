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



def hessian(img):
        res=numpy.zeros( (img.ndim,img.ndim) )
        for i in range(img.ndim):
           for j in range(img.ndim):
                 res[i,j]=diff(diff(img,axis=j),axis=i)
        return res



Model=genericmodel.pycvf_model_function(image.Datatype,image.Datatype)(hessian)
__call__=Model
                 
