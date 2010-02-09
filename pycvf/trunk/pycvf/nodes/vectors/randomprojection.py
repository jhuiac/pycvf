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
import scipy
import numpy
#import hashlib
from pycvf.stats.DR.bagofwords import BagOfWords
from pycvf.core.errors import *
from pycvf.core import genericmodel
from pycvf.datatypes import basics
from pycvf.lib.info.cacheable import NotReady
#########################################################################################################################################
# Define our model
#########################################################################################################################################
  
class RandomProjection(object):
  def __init__(self,idim=-1, odim=32,reset=False):     
     self.idim=idim
     self.odim=odim
     self.reset=reset
  def init(self):
     self.filename=self.directory+"/randomprojection.npy"
     try:
        if (self.reset):
         raise Exception
        self.rpmat=numpy.load(self.filename)
        if (self.rpmat==None):
            raise Exception
        self.model_node.status=genericmodel.STATUS_READY
        pycvf_debug(10, "loaded"+ self.filename+"...")
     except:
        self.rpmat=None
  def set_model_node(self,model):
        self.model_node=model
        self.directory=model.get_directory()
        self.init()
  def on_model_destroy(self,model):
        self.model_node=None
  def process(self,v):
     if (self.rpmat==None):
        self.rpmat=(numpy.random.random((self.odim,(v.shape[1] if v.ndim==2 else v.shape[0])))-.5)*2
        numpy.save(self.filename,self.rpmat)
        self.model_node.status=genericmodel.STATUS_READY
     x=numpy.dot(self.rpmat,numpy.asmatrix(v).T).T
     #print x.shape
     return x
    
Model=genericmodel.pycvf_model_class(None,basics.NumericVector.Datatype)(RandomProjection)
__call__=Model

