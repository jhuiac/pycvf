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
from pycvf.lib.backgroupsep.opencv import OpenCVBackgroundForegroundSeparation
from pycvf.structures.list import PointListStructure

class Model(genericmodel.Model):
        def input_datatype(self,x):
            assert(isinstance(x,video.Datatype) or issubclass(x,video.Datatype))
            return video.Datatype
        def output_datatype(self,x):
            return video.Datatype
        def init_model(self,id="",background=False,*args,**kwargs):
                 self.processline='src|bgfg'+id
                 def transformed_reader(reader):
                    class NewReader():
                        def __init__(self,reader):
                          self.bgfg=OpenCVBackgroundForegroundSeparation(*args,**kwargs)
                          self.reader=reader
                        def transform_pic(self,x):
                           r=self.bgfg.process(x)
                           print r[0].mean(),r[0].shape,r[1].mean(),r[1].shape
                           if background:
                             #return r[0].reshape(r[0].shape[0],r[0].shape[1],r[0].shape[2]).swapaxes(0,1).copy('C')
                            return r[0].copy('C')
                           else: 
                             #return r[1].reshape(r[1].shape[0],r[1].shape[1],r[1].shape[2]).swapaxes(0,1).repeat(3,axis=2).copy('C')
                             return r[1].repeat(3,axis=2).copy('C')
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
                 self.context['bgfg'+id]=transformed_reader

__call__=Model