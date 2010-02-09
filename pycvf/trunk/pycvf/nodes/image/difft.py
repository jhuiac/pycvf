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

class DiffT:
    def __init__(self):
        self.prev=None
        self.process=self.idiff
    def idiff(self,x):
        self.prev=x
        self.process=self.rdiff
        return x
    def rdiff(self,x):
        if (x.shape!=self.prev.shape):
           return self.idiff(x)
        d=x-self.prev
        self.prev=x
        return d

Model=generic.pycvf_model_class(image.Datatype,image.Datatype)(DiffT)
__call__=Model
