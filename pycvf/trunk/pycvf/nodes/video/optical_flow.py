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
from pycvf.datatypes import video
import pycvf.lib.video.opticalflow as opticalflow 
from pycvf.structures.list import PointListStructure
import numpy
import time

class Model(genericmodel.Model):
        """ 
          Methods :
             OpticalFlowHS=
        """
        def input_datatype(self,x):
            assert(isinstance(x,video.Datatype) or issubclass(x,video.Datatype))
            return video.Datatype
        def output_datatype(self,x):
            return video.Datatype
        def init_model(self,method="HS",id="",*args,**kwargs):
                 self.processline='src|optflow'+id
                 def transformed_reader(reader):
                    class NewReader():
                        def __init__(self,reader):
                          h,w,d=reader[0].shape
                          self.of=eval("opticalflow.OpticalFlow"+method+"((h,w),*args,**kwargs)",{'args':args,'kwargs':kwargs,'opticalflow':opticalflow,'h':h,'w':w})
                          self.reader=reader
                        def transform_pic(self,x):
                           try:
                              t0=time.clock()
                              r=self.of.push(x.mean(axis=2).astype(numpy.uint8))
                              t1=time.clock()                              
                              r=opticalflow.flow2rgb(r)
                              t2=time.clock()    
                              pycvf_debug(10,"s=%s, optical flow: %f , hsv polar reprentation: %f "%(str(r.shape),t2-t1,t2-t1))
                              return r
                           except Exception  ,e :
                             print e
                        def get_tracks(self):
                          return self.reader.get_tracks()
                        def copy(self):
                          return NewReader(self.reader.copy())
                        def set_observer(self,observer):
                           self.reader.set_observer(lambda x:observer(self.transform_pic(x)))
                        def step(self):
                           self.reader.step()   
                        def get_current_address(self):
                           r=self.reader.get_current_address()
                        def __len__(self):
                           l=len(self.reader)
                           print l
                           return l
                        def seek_to(self,pos):
                           pycvf_warning("seeking not allowed with this player")
                           #return self.reader.seek_to(pos)
                        def __getitem__(self,addr):
                           #print addr
                           #print dir(self.reader),self.reader.get_current_frame()[0][2]
                           pycvf_warning("MVP related code  : TODO: repare simpleplayer")
                           r=self.transform_pic(self.reader.get_current_frame()[0][2])
                           return r
                        def run(self):
                           try:
                              while True:
                                 self.step()
                           except StopIteration:
                                 pass
                    return NewReader(reader)
                 self.context['optflow'+id]=transformed_reader

__call__=Model