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
from pycvf.datatypes import basics

def histogram_alt(x,*args,**kwargs):
   return numpy.histogram(x,*args,**kwargs)[0]

Model=genericmodel.pycvf_model_function(None,basics.NumericArray.Datatype,numpy.histogram_alt)
__call__=Model
