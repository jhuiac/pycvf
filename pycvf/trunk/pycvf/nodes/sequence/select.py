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
from pycvf.datatypes import basics

class Model(genericmodel.Model):
        @classmethod
        def input_datatype(self,x):
            #assert(isinstance(x,list.Datatype) or issubclass(x,list.Datatype))
            return x
        def output_datatype(self,x):
            return x.ElementType
        def init_model(self,n,*args,**kwargs):
                 self.processline='src|select'+str(n)
                 self.context['select'+str(n)]=lambda x:x[n]

__call__=Model
