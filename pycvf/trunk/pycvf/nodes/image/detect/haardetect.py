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

from pycvf.core.errors import *
from pycvf.core import genericmodel
from pycvf.datatypes import basics
from pycvf.datatypes import image
from pycvf.lib.facedetect.haardetect import FaceDetector
from pycvf.structures.list import PointListStructure

class Model(genericmodel.Model):
        def input_datatype(self,x):
            assert(isinstance(x,image.Datatype) or issubclass(x,image.Datatype))
            return image.Datatype
        def output_datatype(self,x):
            return list.Datatype(image.Datatype)
        def init_model(self,id="",background=False,*args,**kwargs):
                 self.processline='src|sift'+id
                 f=FaceDetector(*args,**kwargs)
                 def detectf(i):
                    rects=f.detect(i)
                    return map(lambda r:i[r[1]:(r[1]+r[3]),r[0]:(r[0]+r[2])], rects)
                 self.context['sift'+id]=detectf

__call__=Model