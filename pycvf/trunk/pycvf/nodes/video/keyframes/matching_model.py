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
import pycvf.datatypes.list 
from pycvf.datatypes import video,image,basics

class Model(genericmodel.Model):
        def input_datatype(self,x):
           return video.Datatype
        def output_datatype(self,x):
           return pycvf.datatypes.list.Datatype(image.Datatype)
        def init_model(self,model, threshold=0.5, return_images=True, return_positions=False, modelpath="/", *args,**kwargs):
          self.kfmodel=(pycvf_builder(model) if type(model) in [str,unicode] else model)
          self.kfmodel.init("/",image.Datatype,self)
          self.modelpath=modelpath
          metak= self.model.get_features_meta().keys()
          self.kfmodelpathno=metak.index(modelpath)
          def matchingmodelkf(vr):
              while True:
                  f=vr.get_current_frame()
                  if (self.kfmodel.process(f)[self.kfmodelpathno]>threshold):
                      if (return_images):
                        if return_positions
                          yield (f,vr.get_current_frameno())
                        else:
                         yield f
                  else:
                      yield vr.get_current_frameno()
                  vr.step()
          self.processing=[('matchingmodelkf'  ,{'matchingmodelkf':matchingmodelkf})]

__call__=Model
