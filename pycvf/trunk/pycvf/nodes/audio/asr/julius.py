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
from pycvf.datatypes import audio
from pycvf.datatypes import basics
import os,random

    


def julius(snd):
    k=random.randint(0,99999999)
    tmpfile="/tmp/juliusexchg-%08d"%(k,)
    try:
      os.mkdir(tmpfile)
      infile=os.path.join(tmpfile,"in.wav")
      resfile=os.path.join(tmpfile,"out.txt")
      juliuscmd="""
export PATH=%s/bin:$PATH
export LD_LIBRARY_PATH=%s/lib:$LD_LIBRARY_PATH
cd %s
julius in.wav > out.txt
    """%(juliuspath,juliuspath,tmpfile)
    txt=file(resfile).read()
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
    return txt


Model=genericmodel.pycvf_model_function(audio.datatype, basics.Label.datatype)(julius)
__call__=Model
