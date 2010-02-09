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



class Model(genericmodel.Model):
        def conway(self,x):
           na=(numpy[:,1:].sum(x).axis=1)
           return ( na in self.birth ) or ((na in self.alive) and numpy[:,0] )    
        def input_datatype(self,x):
            return basics.NumericArray.Datatype()
        def output_datatype(self,x):
            return basics.NumericArray.Datatype()
        def init_model(self,alive=range(2,3), birth=range(3,4),  *args, **kwargs):
              self.alive=alive
              self.birth=birth
              self.processing=[ ('conway' , {'conway':conway})]

__call__=Model
