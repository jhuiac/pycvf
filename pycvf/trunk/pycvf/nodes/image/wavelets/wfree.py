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
import pywt
from pycvf.core import genericmodel
from pycvf.datatypes import image
from pycvf.datatypes import list as ldt


def wfree(x,expr):
      if (type(x) in [list,tuple]):
	  return map(lambda y:wfree(y,expr),x)
      else:
         return eval(expr)


Model=genericmodel.pycvf_model_function(ldt.Datatype(ldt.Datatype(image.Datatype)),ldt.Datatype(ldt.Datatype(image.Datatype)))(wfree)
__call__=Model
                 
