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


import numpy, scipy,sys
from pycvf.core import genericmodel
from pycvf.datatypes import basics
from pycvf.datatypes import image
from pycvf.datatypes import histogram
from pycvf.lib.graphics.features import lbph

##
## This is simply a color model that is to apply by filtering
##

Model=genericmodel.pycvf_model_function(image.Datatype,histogram.Datatype)(lbph)
__call__=Model
