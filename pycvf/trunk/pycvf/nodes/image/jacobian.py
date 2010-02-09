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


def jacobian(img):
      res=numpy.zeros( (img.ndim-1,img.shape[2]) , dtype=object)
      for i in range(img.shape[2]):                               
           for j in range(img.ndim-1):                             
               res[i,j]=numpy.diff(res[:,:,i],axis=j)
      return res



Model=genericmodel.pycvf_model_function(image.Datatype,image.Datatype)(jacobian)
__call__=Model
                 
