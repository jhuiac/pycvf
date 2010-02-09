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
import scipy
from pycvf.core import genericmodel
from pycvf.datatypes import basics

class MyModel(genericmodel.GenericModel):
  inpiut_datatype=lambda self,x:x
  datatype=lambda self,x:x.ElementType
  def init_featurefilter(self):
     self.featurefilter=('src'  ,{},  {}) 
  def test_fusion(self,l):
    return max(l)


