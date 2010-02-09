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


from pycvf.core import genericmodel
from pycvf.datatypes import image
import numpy,scipy,scipy.ndimage


def DoG(x,value1=3,value2=1,*args,**kwargs):
  return numpy.abs(scipy.ndimage.gaussian_filter(x,value1,*args,**kwargs)-scipy.ndimage.gaussian_filter(x,value2,*args,**kwargs))

Model=genericmodel.pycvf_model_function(image.Datatype,image.Datatype)(DoG)
__call__=Model
