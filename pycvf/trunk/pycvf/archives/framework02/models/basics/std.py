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

class MyModel(genericmodel.GenericModel):
  datatype=lambda self,x:basics.FloatDatatype
  def init_featurefilter(self):
     self.featurefilter=('src.std(axis=0)'  ,{},  {}) 



