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
from pycvf.core.errors import pycvf_debug
import os,random
import PIL
import PIL.Image
    
PANDOREPATH="/home/tranx/build/pandore"

def pandore(img,cmd):
    k=random.randint(0,99999999)
    tmpfile="/tmp/pandorexchg-%08d"%(k,)
    try:
      os.mkdir(tmpfile)
      infile=os.path.join(tmpfile,"in.bmp")
      resfile=os.path.join(tmpfile,"out.bmp")
      pandorecmd="""
export PATH=%s/bin:$PATH
export LD_LIBRARY_PATH=%s/lib:$LD_LIBRARY_PATH
cd %s
echo "BMP2PAN"
pbmp2pan in.bmp in.pan
echo "OPERATOR"
%s
echo "PAN2BMP"
ppan2bmp out.pan out.bmp
rm *.pan || true
    """%(PANDOREPATH,PANDOREPATH,tmpfile,cmd)
      NumPy2PIL(img).save(infile)
      pycvf_debug(10,"pan")
      os.system(pandorecmd)
      pycvf_debug(10,"/pan")      
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
                 self.processline='src|pandore'
                 f=pandore
                 self.context['pandore']=lambda x:(f(x,*args,**kwargs))

__call__=Model
