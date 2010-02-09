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
from pycvf.nodes.datatypes import image
import scipy,scipy.ndimage

def gaussian(x, value=2,*args,**kwargs):
  return scipy.ndimage.gaussian_filter(x,value,*args,**kwargs)

Model=genericmode.pycvf_model_function(image.Datatype,image.Datatype)(gaussian)
__call__=Model
