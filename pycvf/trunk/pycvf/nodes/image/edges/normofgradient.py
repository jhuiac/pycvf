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

from pycvf.core.distribution import *

pycvf_dist(PYCVFD_MODULE_STATUS, PYCVFD_STATUS_BETA)

def normofgradient(x,*args, **kwargs):
   g0=scipy.gradient(x,*args,**kwargs)
   return numpy.abs(g0[0]+g0[1]*1J)

Model=genericmodel.pycvf_model_function(image.Datatype,image.Datatype)(normofgradient)
__call__=Model
