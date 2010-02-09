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
from pycvf.datatypes import image
from pycvf.lib.graphics import features

Model=genericmodel.pycvf_function_model(image.Datatype,basics.NumericArray.Datatype)(features.phog)
__call__=Model
                 