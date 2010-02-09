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
#from jfli import stats.models

##
## This is simply a color model that is to apply by filtering
##

class Model(genericmodel.GenericModel):
        input_datatype=lambda self,x:image.Datatype
        datatype=lambda self,x:image.Datatype
        def init_featurefilter(self):
              self.featurefilter=('src|dogray'  ,{'dogray':lambda x:x.mean(axis=2).reshape(x.shape[0],x.shape[1],1)},  {})
        def init_structures(self):
              return {}

__call__=Model

                 