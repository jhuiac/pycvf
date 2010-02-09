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
        def input_datatype(self,x):
            return generator.Datatype(basics.NumericArray.Datatype())            
        def output_datatype(self,x):
            return generator.Datatype(basics.NumericArray.Datatype())
        def init_model(self,nb,*args, **kwargs):
              def blockifier(gen):
                      i=iter(gen)
                      try:
                        while True:
                          r=[]
                          for x in range(nb):
                              r.append(i.next())
                          yield r
                      except StopIteration:
                          if r!=[]:
                             yield r
              self.processing=[ ('blockifier' , {'blockifier':blockifier} )]

__call__=Model
                 