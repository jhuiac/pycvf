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

import sys
from pycvf.core import genericmodel
from pycvf.core.errors import *
    
class Writer:
   def __init__(self,stream=sys.stderr,sep="\n"):
       self.stream=stream
       self.sep=sep
   def process(self,x):
       self.stream.write(repr(x)+self.sep)
       return x

Model=genericmodel.pycvf_model_class(None,None)(Writer)
__call__=Model
