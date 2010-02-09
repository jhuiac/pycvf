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
from pycvf.datatypes import video,image,basics

class MyModel(genericmodel.GenericModel):
        input_datatype=lambda self,x:video.Datatype
        datatype=lambda self,x:list.Datatype(image.Datatype)
        def init(self,num_images=3, *args,**kwargs):
              self.num_images=num_images
              genericmodel.GenericModel.init(self, *args,**kwargs)
        def middleimages(vr):
              return [ vr[ (i) *len(vr)/ (2*self.num_images)  ] for i in range(1,2*self.num_images,2) ]
        def init_featurefilter(self):
              self.featurefilter=('src|middleimages'+str(self.num_images)  ,{'middleimages'+str(self.num_images):self.middleimages},  {})

