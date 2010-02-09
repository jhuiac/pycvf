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

from pycvf.core.distribution import *

pycvf_dist(PYCVFD_MODULE_STATUS, PYCVFD_STATUS_BETA)

Model=genericmodel.pycvf_model_function(image.Datatype,image.Datatype)(scipy.ndimage.laplace)
__call__=Model
