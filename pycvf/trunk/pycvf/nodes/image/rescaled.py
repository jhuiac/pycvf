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


import numpy
from pycvf.core import genericmodel
from pycvf.datatypes import basics
from pycvf.datatypes import image
from pycvf.lib.graphics import rescale
#from jfli import stats.models

##
## This is simply a color model that is to apply by filtering
##

class Model(genericmodel.GenericModel):
        def input_datatype(self,x):
            assert(isinstance(x,image.Datatype))
            return image.Datatype
        def output_datatype(self,x):
            return image.Datatype
        def init_model(self,dsize=(30,20,'T'),*args, **kwargs):
              self.processing=[ ('rescale' , {'rescale':rescale.Rescaler2d(dsize).process} )]

__call__=Model
