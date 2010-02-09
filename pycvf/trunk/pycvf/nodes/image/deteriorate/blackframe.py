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


from pycvf.core.genericmodel import pycvf_model_function
from pycvf.datatypes import image
import numpy, random

def blackframe(i,amount=0.2):
    i=i.copy()
    h,w=i.shape[0],i.shape[0]
    amount=amount**.5
    dx=int(w*amount)
    dy=int(h*amount)
    x=random.randint(0,w-dx-1)
    y=random.randint(0,h-dy-1)    
    i[y:(y+dy),x:(x+dx)]=0
    return i

Model=pycvf_model_function(image.Datatype, image.Datatype)(blackframe)
__call__=Model

