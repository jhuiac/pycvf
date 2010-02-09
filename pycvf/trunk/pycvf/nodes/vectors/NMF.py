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


import numpy, sys
from pycvf.core import genericmodel
from pycvf.core.genericmodel import NotReady,STATUS_ERROR,STATUS_NOT_READY,STATUS_READY
from pycvf.datatypes import basics
from pycvf.stats.DR import nmf3
from pycvf.stats.DR.nmf3 import NMFdimred


class NMFProcessor(object):
  def __init__(self,*args, **kwargs):     
     self.args=args
     self.kwargs=kwargs
     self.directory=None
     self.trainl=[]
  def init(self,odim, totrain=2000,*args, **kwargs):
     self.filename=self.directory+"/nmf.pcl"
     try:
        self.inmf=NMFdimred.load(self.pcafilename)
        if (self.ibow==None):
            raise Exception
        self.model_node.status=genericmodel.STATUS_READY
        pycvf_debug(10, "loaded"+ self.filename+"...")
     except:
        self.inmf=None
        self.model_node.status=genericmodel.STATUS_NOT_READY        
        self.totrain=totrain
  def set_model_node(self,model):
        self.model_node=model
        self.directory=model.get_directory()
        self.init(*self.args,**self.kwargs)
  def on_model_destroy(self,model):
        self.save()
        self.model_node=None
  def process(self,v):
     if (self.totrain):
        q=min(v.shape[0],self.totrain)
        self.totrain-=q
        self.trainl.append(v[:q])
        if (self.totrain==0):
           self.inmf=NMFdimred(numpy.vstack(self.trainl),algox=nmf3.EG_DJ(), algoa=nmf3.EG_DKL(),*self.args,**self.kwargs)
           self.save()
        if (v.shape[0]==q):
          self.model_node.status=genericmodel.STATUS_NOT_READY
          raise NotReady
        else:
          v=v[q:]
     try:
        assert(v.ndim==2)
        r=self.inmf.dimred(v)
     except KeyboardInterrupt:
       raise
     except Exception,e:
       print e
       self.model_node.status=genericmodel.STATUS_NOT_READY
       raise NotReady
     self.model_node.status=genericmodel.STATUS_READY
     return r
  def save(self):
     if (self.inmf) and (self.totrain==0):
        self.inmf.save(file(self.filename,"w"))

    
Model=genericmodel.pycvf_model_class(basics.NumericArray.Datatype,basics.NumericArray.Datatype)(NMFProcessor)
__call__=Model
