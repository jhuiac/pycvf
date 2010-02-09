#!/usr/bin/env python
# -*- coding: utf-8 -*-
## ##########################################################################################################
## 
## This file is released under GNU Public License v3
## See LICENSE File at the top the pycvf tree.
##
## Author : Bertrand NOUVEL / CNRS (2009)
##
##
##
## Revision FILE: $Id$
##
## ###########################################################################################################
## copyright $Copyright$
## @version $Revision$
## @lastrevision $Date$
## @modifiedby $LastChangedBy$
## @lastmodified $LastChangedDate$
#############################################################################################################


# -*- coding: utf-8 -*-
# (c) All rights reserved
# ###############################################
#
################################################################################################################################################################################
# Includes
################################################################################################################################################################################


from pycvf.core import genericmodel
from pycvf.datatypes import basics
from pycvf.datatypes import image
from pycvf.lib.graphics.kp_sift import sift
from pycvf.nodes.structures.list import PointListStructure
from pycvf.lib.stats.bagofwords import BagOfWords

def siftfeatures(x):
   return x[0]

def siftpoints(x):
   return x[1]

class Model(genericmodel.GenericModel):
        input_datatype=lambda self,x:image.Datatype
        datatype=lambda self,x:list.Datatype(basics.NumericArrayDatatype)
        def init_featurefilter(self):
                 self.featurefilter=('src|sift|siftfeatures|sift_bagofword'  ,{'sift':sift,'siftfeatures':siftfeatures,'siftpoints':siftpoints,'sift_bagofword':BagOfWords().push},  {})
        def init_structures(self):
                 self.structures=[
                                   PointListStructure(),[("NNP",[3])]
                                 ]

__call__=Model
 
