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

import os
from pycvf.core.genericmodel import pycvf_model_function
from pycvf.core import genericmodel
from pycvf.datatypes import image
import PIL
from PIL import Image
from pycvf.lib.graphics.imgfmtutils import *

def jpegcompress(x,amount=0.94):
    tf=os.tmpnam()+".jpg"
    NumPy2PIL(x).save(tf,quality=(1-amount)*100)
    r=PIL2NumPy(Image.open(tf))
    os.remove(tf)
    return r

Model=pycvf_model_function(image.Datatype, image.Datatype)(jpegcompress)
__call__=Model
