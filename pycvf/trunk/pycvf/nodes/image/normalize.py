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
import scipy,scipy.ndimage


class Model(genericmodel.Model):
        @classmethod
        def input_datatype(self,x):
            #assert(isinstance(x,image.Datatype) or issubclass(x,image.Datatype))
            return image.Datatype
        def output_datatype(self,x):
            return image.Datatype
        def init_model(self):
                 self.processline='src|imgnormalize'
                 self.context['imgnormalize']=lambda x:(((x-x.min())*255.)/x.ptp())

__call__=Model
