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


from pycvf.core import genericmodel
from pycvf.datatypes import basics
from pycvf.datatypes import image
from jfli import stats.models

##
## This is simply a color model that is to apply by filtering
##

class Model(genericmodel.GenericModel):
        input_datatype=lambda self,x:image.DataType
        datatype=lambda self,x:image.DataType
        def __init__(colormodel)
              self.colormodel=colormodel
        def init_featurefilter(self):
                 self.featurefilter=('src|colorfilter'  ,{'colorfilter':self.structures[0].recompose(self.colormodel.test(self.strucutures[0].decompose(x)))},  {})
        def init_structure(self):
                 self.structures=[ SpatialStructure() ] 

                 
 
__call__=Model

