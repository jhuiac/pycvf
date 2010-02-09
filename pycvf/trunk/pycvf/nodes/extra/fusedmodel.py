# -*- coding: utf-8 -*-
##
## A fused model take 3 arguments
##
##  1. a structure
##  2. a model for the structured elements
##  3. a fusion model for recreating data from the decomposed elements


# DEPRECATED ???

from pycvf.core import genericmodel
from pycvf.core import model


class Model(genericmodel.GenericModel):
  def __init__(self, structure, model, fusion):
     self.structure=structure
     self.model=model
     self.fusion=fusion
  def init_featurefilter(self):
     def fusedf(x):
       return self.fusion(map(model.process,self.structure.decompose(x)))
     self.featurefilter=('src|fused'  ,{'fused':fusedf},  {})   

# nice shortcut
__call__=Model