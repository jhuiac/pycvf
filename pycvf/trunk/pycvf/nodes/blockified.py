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

def blockifier(gen,nb):
    i=iter(gen)
    try:
      while True:
	r=[]
	for x in range(nb):
	    r.append(i.next())
	yield r
    except StopIteration:
	if r!=[]:
	    yield r

Model=genericmodel.pycvf_model_function(generator.Datatype(basics.NumericArray.Datatype),generator.Datatype(basics.NumericArray.Datatype))(blockifier)
__call__=Model
