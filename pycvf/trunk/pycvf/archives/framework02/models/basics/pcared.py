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
import hashlib
from jfli.dimred import PCA
from pycvf.core import genericmodel
from pycvf.datatypes import basics
from pycvf.lib.info.cacheable import NotReady
#########################################################################################################################################
# Define our model
#########################################################################################################################################

  
  
class MyModel(genericmodel.GenericModel):
  datatype=lambda self,x:basics.NumericVectorDatatype
  def init(self,id,od):
     self.id=id
     self.ddim=od
     self.pcafilename=self.modelpath+"/pcadimred.pcl"
     self.ipca=PCA.IncrementalPCAdimred(id,od,recomputeafter=200,alwaystrain=True)
     try:
        self.ipca.load(file(self.pcafilename,"rb"))
     except:
        pass
     genericmodel.GenericModel.init(self)
  def dimred(self,v):
     #print v.shape
     try:
        return self.ipca.dimred(v.reshape(1,self.id))
     except:
       if (not self.ipca.M):
          self.ipca.add_train(v.reshape(1,self.id))
          raise NotReady
       else: 
          raise Exception
  def __del__(self):
      self.ipca.save(file(self.pcafilename,"wb"))
      genericmodel.GenericModel.__del__(self)
  def init_featurefilter(self):
     #print self.modelpath
     idpca=hashlib.md5(str(self.modelpath)).hexdigest()
     self.featurefilter=('src|ipca'+idpca  ,{'ipca'+idpca:self.dimred},  {}) 

