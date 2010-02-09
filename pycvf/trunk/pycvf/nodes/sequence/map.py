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
from pycvf.nodes.datatypes import image
from pycvf.nodes.datatypes import basics

class Model(genericmodel.Model):
        @classmethod
        def input_datatype(self,x):
            return x
        def output_datatype(self,x):
            return x
        def init_model(self,mdl,id="",*args,**kwargs):
                 mdl.init('/',self.datatype_in)
                 def xmap(l):
                    return map(lambda e:emdl.process(e),l)
                 self.processline='src|map'+id
                 self.context['map'+id]=xmap

__call__=Model
