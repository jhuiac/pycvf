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
from pycvf.core.errors import *
    
    
class Model(genericmodel.Model):
        type_in=None
        type_out=None
        def input_datatype(self,x):
            return self.type_in or x
        def output_datatype(self,x):
            return self.type_out or x
        def debuginfo(self,x):
          self.datatype_out.display(x)
          return x
        
        def init_model(self,id="",*args,**kwargs):
                 self.processline='src|debuginfo'+id 
                 self.context['debuginfo'+id]=self.debuginfo

__call__=Model
