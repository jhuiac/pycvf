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


###
###


from pycvf.core import genericmodel
from pycvf.datatypes import image

from pycvf.core.errors import pycvf_debug
import os,random
from pycvf.lib.graphics.itkimagefilter import ItkImageFilter

class Model(genericmodel.Model):
        def input_datatype(self,x):
            assert(isinstance(x,image.Datatype) or issubclass(x,image.Datatype))
            return image.Datatype
        def output_datatype(self,x):
            return image.Datatype
        def init_model(self,filtername,itkt,layers,**kwargs):
                 self.processline='src|itkimagefilter'+filtername
                 itki=ItkImageFilter(filtername,itkt,layers,**kwargs)
                 self.context['itkimagefilter'+filtername]=itki.process

__call__=Model
