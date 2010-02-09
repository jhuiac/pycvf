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
from pycvf.lib.graphics import randompatches

class Model(genericmodel.GenericModel):
        input_datatype=lambda self,x:image.Datatype
        datatype=lambda self,x:list.Datatype(image.Datatype)
	def init(self,dsize=(24,24),numpatch=3):
           self.dsize=dsize
           self.numpatch=numpatch
           genericmodel.GenericModel.init(self)
        def init_featurefilter(self):
            self.featurefilter=('src|randpatch'  ,{'randpatch':lambda x:randompatches.randompatches(x,self.numpatch,self.dsize)},  {})
        
__call__=Model
