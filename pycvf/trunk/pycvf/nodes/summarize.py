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

def is_prefix(a,b):
    return (b[:len(a)]==a)

class Summarizer:
  """ This agglomerates all the outputs of a node"""
  def __init__(self):
      self.model_node=None
      self.model_node_info=None
  def set_model_node(self,model):
        self.model_node=model
        self.model_root_node=model
        while self.model_root_node.parent!=None:
           self.model_root_node=self.model_root_node.parent
  def on_model_destroy(self,model):
        self.model_node=None        
        self.model_root_node=None
  def process(self,points):
       if self.model_node_info==None:
          self.metas=self.model_node.parent.get_features_meta()
          d=[ [mm[0]] for mm in self.metas.items() ]
          names=reduce(lambda b,n:b+[n[0]],d,[])
          nd=filter(lambda x: (("/"+self.model_node.name+"/") not in x[0][0]) and (len(filter(lambda t:is_prefix(x[0][0], t),names ))==1) ,zip(d,range(len(d))))
          self.model_node_info=nd
          print nd
       return map( lambda x: self.model_root_node.context['thesrc'][self.metas[x[0][0]]['processline']],self.model_node_info )
                                                                   
Model=genericmodel.pycvf_model_class(None,None)(Summarizer)
__call__=Model

