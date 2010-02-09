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
        input_datatype=lambda self,x:image.Datatype
        datatype=lambda self,x:image.Datatype
	def init(self,dsize=(30,20,'T')):
           self.dsize=dsize
           genericmodel.GenericModel.init(self)
        def init_featurefilter(self):
            self.featurefilter=('src|rescale'  ,{'rescale':rescale.Rescaler2d(self.dsize).process},  {})
        
__call__=Model
