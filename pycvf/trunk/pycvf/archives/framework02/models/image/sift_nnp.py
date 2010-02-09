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


from pycvf.core import genericmodel
from pycvf.datatypes import basics
from pycvf.datatypes import image
from pycvf.lib.graphics.kp_sift import sift
from pycvf.nodes.structures.list import PointListStructure

class Model(genericmodel.GenericModel):
        input_datatype=lambda self,x:image.Datatype
        datatype=lambda self,x:list.Datatype(basics.NumericArrayDatatype)
        def init_featurefilter(self):
                 self.featurefilter=('src|sift'  ,{'sift':sift},  {})
        def init_structures(self):
                 self.structures["pointlist"]=(PointListStructure(),[("NNP",[3])])
                                 
##
## IN SIFT MOODELS IT MAY BE MORE INTERESTING TO GIVE MORE WEIGHT TO CENTRAL FEATURES
## 

__call__=Model