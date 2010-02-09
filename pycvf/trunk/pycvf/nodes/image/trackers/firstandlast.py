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
from pycvf.datatypes import image




class FirstAndLast:
    """
    First and last is not a tracker / or it is a tracker when you assume to have only one possible object and you want to 
    have always a result. 
    
    It takes as input a collection of element, and returns its first element.
    If there is no element in the collection, thet it return it used to return.
    """
    def __init__(self):
        self.prev=numpy.zeros(1,1,1)
    def process(self,x):
        if (len(self.x)!=0):
            self.prev=x[0]
            return self.prev
        else:
            return self.prev

    
              
Model=generic.pycvf_model_class(FirstAndLast)
__call__=Model
                 