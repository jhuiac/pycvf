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
from pycvf.core.autoimp import *


class Model(genericmodel.Model):
        name="free"
        type_in=None
        type_out=None
        def input_datatype(self,x):
            return (self.type_in if (self.type_in!=None) else x)
        def output_datatype(self,x):
            return (self.type_out if (self.type_out!=None) else x)
        def init_model(self,expr,id="",datatype=None,*args,**kwargs):
                 self.type_out=datatype
                 self.xcontext=globals()
                 self.processline='src|freeexpr'+id 
                 self.context['freeexpr'+id]=lambda x:eval(expr,{'x':x},self.xcontext )

__call__=Model
