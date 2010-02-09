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
from pycvf.lib.graphics.kp_surf import surf
from pycvf.nodes.structures.list import PointListStructure

class Model(genericmodel.GenericModel):
        input_datatype=lambda self,x:image.Datatype
        datatype=lambda self,x:list.Datatype(basics.NumericArrayDatatype)
        def init(self,NNP=3):
            self.NNP=NNP
            genericmodel.GenericModel.init(self)
        def init_featurefilter(self):
                 self.featurefilter=('src|surf'  ,{'surf':surf},  {})
        def init_structures(self):
                 self.structures["pointlist"]=(PointListStructure(),[("NNP",[self.NNP])])
                                 
  

__call__Model