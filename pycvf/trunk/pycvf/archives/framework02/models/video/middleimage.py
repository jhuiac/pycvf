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

from pycvf.core import genericmodel
from pycvf.datatypes import video,image

def middleimage(vr):
  return vr[len(vr)/2]

class Model(genericmodel.GenericModel):
        input_datatype=lambda self,x:video.Datatype
        datatype=lambda self,x:image.Datatype
        def init_featurefilter(self):
                 self.featurefilter=('src|middleimage'  ,{'middleimage':middleimage},  {})

__call__=Model
 
