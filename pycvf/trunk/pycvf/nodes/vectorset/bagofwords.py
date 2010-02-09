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
#import hashlib
from pycvf.stats.DR.bagofwords import BagOfWords
from pycvf.core.errors import *
from pycvf.core import genericmodel
from pycvf.datatypes import basics
from pycvf.lib.info.cacheable import NotReady
#########################################################################################################################################
# Define our model
#########################################################################################################################################
  
class BagOfWordsProcessor(object):
  def __init__(self,categories=32, burnin=2000, *args, ** kwargs):     
     self.categories=categories
     self.burnin=burnin
     self.directory=None
  def init(self):
     self.bowfilename=self.directory+"/bagofwords.pcl"
     try:
        self.ibow=BagOfWords.load(self.bowfilename)
        if (self.ibow==None):
            raise Exception
        self.model_node.status=genericmodel.STATUS_READY
        pycvf_debug(10, "loaded"+ self.bowfilename+"...")
        pycvf_debug(10,"burnin is "+ str(self.ibow.burnin)+"...")
     except:
        self.ibow=BagOfWords(self.categories,burnin=self.burnin)
        self.ibow.set_filename(self.bowfilename)
        self.model_node.status=genericmodel.STATUS_NOT_READY
        
     #genericmodel.Model.init(self,*args,**kwargs)
     pycvf_debug(10,"burnin is "+ str(self.ibow.burnin)+"...")
  def set_model_node(self,model):
        self.model_node=model
        self.directory=model.get_directory()
        self.init()
  def on_model_destroy(self,model):
        self.save()
        self.model_node=None
  def process(self,v):
     try:
        r=self.ibow.push(v)
     except KeyboardInterrupt:
       raise
     except Exception,e:
       print e
       if (self.ibow.vocabulary==None):
          self.model_node.status=genericmodel.STATUS_NOT_READY
          raise NotReady
       else: 
          self.model_node.status=genericmodel.STATUS_ERROR
          raise
     self.model_node.status=genericmodel.STATUS_READY
     return r
  def save(self):
     if (self.ibow):
        self.ibow.save()

    
Model=genericmodel.pycvf_model_class(None,basics.NumericVector.Datatype)(BagOfWordsProcessor)
__call__=Model
