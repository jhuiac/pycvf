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

from pycvf.core.utilities import *
from pycvf.core import genericmodel
from pycvf.datatypes import image
from pycvf.lib.graphics.imgfmtutils import *
from pycvf.core.errors import pycvf_debug
import os,random
import PIL
import PIL.Image
    
PANDOREPATH=pycvf_config_var("PANDOREPATH","/home/tranx/build/pandore")

def pandore(img,cmd):
    t=TempDirectory()
    tmpfile=t.get()
    try:
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
    """%(PANDOREPATH,PANDOREPATH,tmpfile.get(),cmd)
      NumPy2PIL(img).save(infile)
      pycvf_debug(10,"pan")
      os.system(pandorecmd)
      pycvf_debug(10,"/pan")      
      img=PIL2NumPy(PIL.Image.open(resfile))
    return img

                 
Model=genericmodel.pycvf_model_function(image.Datatype,image.Datatype)(pandore)
__call__=Model
