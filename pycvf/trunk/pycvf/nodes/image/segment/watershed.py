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
from pycvf.lib.graphics.watershed import watershed


Model=pycvf_model_function(image.Datatype, image.Datatype)(watershed)
__call__=Model
