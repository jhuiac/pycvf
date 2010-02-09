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
from pycvf.lib.graphics import features

##
## This is simply a color model that is to apply by filtering
##

class Model(genericmodel.Model):
        def input_datatype(self,x):
            #assert(isinstance(x,image.Datatype)), (str(type(x)) , "is not an image")
            return image.Datatype
        def output_datatype(self,x):
            return basics.NumericArrayDatatype
        def init_model(self,*args, **kwargs):
              self.processing=[ ('PHOG' , {'PHOG':features.phog} )]

__call__=Model
                 