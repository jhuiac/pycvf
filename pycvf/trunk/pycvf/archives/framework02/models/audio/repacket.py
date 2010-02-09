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


import numpy
from pycvf.core import genericmodel
from pycvf.datatypes import basics
from pycvf.datatypes import image

##
## This is the basic for 
##

class Model(genericmodel.GenericModel):
        input_datatype=lambda self,x:audio.AudioPacket.Datatype
        datatype=lambda self,x:audio.AudioPacket.Datatype
        def init(self,basefreq,npacketperseconds,lenpackets):
           self.basefreq=basegreq
           self.npacketpersonds
           self.lenpackets=lenpackets
           self.deltapackets=self.basefreq//self.lenpackets
           self.aq=pyffmpeg.AudioQueue()
           self.cntr=0
           genericmodel.GenericModel.init(self) 
        def aqprocess(self,data):
           amount=data.shape[0]
           self.aq.push(data)
           ncntr=self.cntr+amount
           while (cntr//self.deltapackets!=ncntr//self.deltapackets):
               aq[0:self.lenpack]
               aq.pop()
               ncntr-=self.deltapackets
        def init_featurefilter(self):
              self.featurefilter=('aq'  ,{'aq':self.aqprocess},  {})
        def init_structures(self):
              return {}

__call__=Model