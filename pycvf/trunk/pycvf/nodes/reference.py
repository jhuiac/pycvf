# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# MyModel By Bertrand NOUVEL
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
# ###############################################


import numpy, sys
from pycvf.core import genericmodel
from pycvf.datatypes import basics

class Reference:
  """ This is use to make reference to other elements in the pipeline"""
  def __init__(self,node='src'):
      self.node=node
      self.model_node=None
  def set_model_node(self,model):
        self.model_node=model
        while (self.model_node.parent!=None):
           self.model_node=self.model_node.parent
  def on_model_destroy(self,model):
        self.model_node=None        
  def process(self,points):
        return self.model_node.context['thesrc'][self.node]
                                                                   
Model=genericmodel.pycvf_model_class(None,None)(Reference)
__call__=Model

