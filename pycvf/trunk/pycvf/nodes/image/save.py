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

import os
from pycvf.core.genericmodel import pycvf_model_class
from pycvf.core import genericmodel
from pycvf.datatypes import image
import PIL
from PIL import Image
from pycvf.lib.graphics.imgfmtutils import *

class ImageSaver(object):
  def __init__(self,filename="img-$n.png",label_op=None,*args,**kwargs):
      self.c=0
      self.filename=filename
      self.args=args
      self.kwargs=kwargs
      self.mdl=None
      if (label_op==None):
          label_op=lambda x:x
      self.label_op=label_op
      self.model_node=None
  def set_model_node(self,model):
        self.model_node=model
  def on_model_destroy(self,model):
        self.model_node=None        
  def process(self,x):
      filename=self.filename.replace("$n","%08d"%(self.c,))    
      filename=filename.replace("$address","%r"%(self.label_op(self.model_node.get_curaddr()),))
      NumPy2PIL(x).save(filename,*self.args,**self.kwargs)
      self.c+=1
      return x

Model=pycvf_model_class(image.Datatype, image.Datatype)(ImageSaver)
__call__=Model

