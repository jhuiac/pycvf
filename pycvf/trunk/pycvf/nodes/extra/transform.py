# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# MyModel By Bertrand NOUVEL
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
# ###############################################



# THIS FILE IS  DEPRECATED 







import numpy

from pycvf.core import genericmodel




class MyModel(genericmodel.GenericModel):
  def init(self,filterf=,processorf=numpy):
      self.filterf=filterf
      self.processorf=processorf
  def init_featurefilter(self):
     self.featurefilter=('src|filter'  ,{'filter':eval(self.filterf,self.processorf)},  {}) 



