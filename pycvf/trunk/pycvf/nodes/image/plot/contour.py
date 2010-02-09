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


import numpy, sys
from pycvf.core import genericmodel
from pycvf.datatypes import basics
from pycvf.datatypes import image
import zopencv

class Contour:
  def __init__(self,*args,**kwargs):
      self.model_node=None
  def set_model_node(self,model):
        self.model_node=model
        while (self.model_node.parent!=None):
           self.model_node=self.model_node.parent
  def on_model_destroy(self,model):
        self.model_node=None        
  def process(self,points):
        srcb=self.model_node.context['thesrc']['src'].copy('C')
        length=len(points)
        for x in range(length-1):
            src_point=zopencv.cvPoint(points[x,0],points[x,1])
            dst_point=zopencv.cvPoint(points[x+1,0],points[x+1,1])
            color=zopencv.cvScalar(255,0,0,0)
            zopencv.cvLine( srcb,src_point, dst_point,color,1,8,0 )
        return srcb
                                                                   
Model=genericmodel.pycvf_model_class(basics.Label.Datatype,image.Datatype)(Contour)
__call__=Model

