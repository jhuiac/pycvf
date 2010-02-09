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
from pycvf.datatypes import basics
from pycvf.datatypes import image
from pycvf.datatypes import list as ldt
from pycvf.lib.graphics.kp_sift import sift
from pycvf.structures.list import PointListStructure

Model=genericmodel.pycvf_model_function( image.Datatype,ldt.Datatype(basics.NumericArray.Datatype))(sift)
__call__=Model
