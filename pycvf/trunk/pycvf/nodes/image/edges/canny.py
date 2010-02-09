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


def canny(image,threshold1=1, threshold2=1,apertureSize=3,L2gradient=0):
   import zopencv
   edges=image.copy('C')   
   print zopencv.cvCanny.__doc__
   zopencv.cvCanny( image,edges, threshold1, threshold2,apertureSize)#, L2gradient)
   return edges

Model=genericmodel.pycvf_model_function(image.Datatype,image.Datatype)(canny)
__call__=Model
