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
from pycvf.stats.DR.PCA import IncrementalPCAdimred




#methods={
#"IPCA":'pycvf.lib.stats.dimred.PCA.IncrementalPCA',
#"NMF":'pycvf.lib.stats.dimred.NMF.nmf',
#}


class IPCAProcessor(object):
  def __init__(self,*args, **kwargs):     
     self.args=args
     self.kwargs=kwargs
     self.directory=None
  def init(self,odim, totrain=2000,*args, **kwargs):
     self.pcafilename=self.directory+"/pca.pcl"
     try:
        self.ipca=IncrementalPCAdimred.load(self.pcafilename)
        if (self.ibow==None):
            raise Exception
        self.model_node.status=genericmodel.STATUS_READY
        pycvf_debug(10, "loaded"+ self.pcafilename+"...")
     except:
        self.ipca=IncrementalPCAdimred(-1,odim,*args, **kwargs)
        #self.ibow.set_filename(self.bowfilename)
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
        self.ipca.add_train(v[:q])
        if (self.totrain==0):
           self.ipca.recompute()
           self.save()
        if (v.shape[0]==q):
          self.model_node.status=genericmodel.STATUS_NOT_READY
          raise NotReady
        else:
          v=v[q:]
     try:
        assert(v.ndim==2)
        r=self.ipca.dimred(v)
     except KeyboardInterrupt:
       raise
     except Exception,e:
       print e
       self.model_node.status=genericmodel.STATUS_NOT_READY
       raise NotReady
     self.model_node.status=genericmodel.STATUS_READY
     return r
  def save(self):
     if (self.ipca) and (self.totrain==0):
        self.ipca.save(file(self.pcafilename,"w"))

    
Model=genericmodel.pycvf_model_class(basics.NumericArray.Datatype,basics.NumericArray.Datatype)(IPCAProcessor)
__call__=Model
