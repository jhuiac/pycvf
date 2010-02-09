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
from pycvf.lib.graphics.imgfmtutils import *
import os,random
import PIL
import PIL.Image
    


def tesseract(img):
    k=random.randint(0,99999999)
    tmpfile="/tmp/tesseractxchg-%08d"%(k,)
    try:
      os.mkdir(tmpfile)
      infile=os.path.join(tmpfile,"in.png")
      resfile=os.path.join(tmpfile,"out.txt")
      pandorecmd="""
export PATH=%s/bin:$PATH
cd %s
tesseract in.png out.txt -l %s 
    """%(TESSERACTPATH,tmpfile,lang)
      NumPy2PIL(img).save(infile)
      os.system(pandorecmd)
      img=PIL2NumPy(PIL.Image.open(resfile))
    finally:
      try:
         os.unlink(resfile)
      except:
         pass
      try:
         os.unlink(infile)
      except:
         pass 
      os.rmdir(tmpfile)    
    return img

class Model(genericmodel.Model):
        def input_datatype(self,x):
            assert(isinstance(x,image.Datatype) or issubclass(x,image.Datatype))
            return image.Datatype
        def output_datatype(self,x):
            return image.Datatype
        def init_model(self,variant="",*args,**kwargs):
                 self.processline='src|tesseract'
                 f=ocropus
                 self.context['tesseract']=lambda x:(f(x,*args,**kwargs))

__call__=Model
