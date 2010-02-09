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

import os
from pycvf.core.genericmodel import pycvf_model_function
from pycvf.core import genericmodel
from pycvf.datatypes import image
import scipy
import scipy.ndimage

distance_transform_edt=scipy.ndimage.distance_transform_edt

Model=pycvf_model_function(image.Datatype, image.Datatype)(distance_transform_edt)
__call__=Model
