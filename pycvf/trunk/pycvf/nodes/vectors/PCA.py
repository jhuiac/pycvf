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
from genericmodel import NotReady
from pycvf.datatypes import basics
from pycvf.lib.stats.dimred.PCA import IncrementalPCAdimred

from pycvf.core.builders import pycvf_loader


methods={
"IPCA":'pycvf.lib.stats.dimred.PCA.IncrementalPCA',
"NMF":'pycvf.lib.stats.dimred.NMF.nmf',
}

class Model(genericmodel.Model):
        def input_datatype(self,x):
            return basics.NumericArrayDatatype()
        def output_datatype(self,x):
            return basics.NumericArrayDatatype()
        def init_model(self,odim, totrain=2000,filename=None,method="ICPA",*args, **kwargs):
              self.dimred=pycvf_loader((methods[method] if  methods.has_key(method) else method))
              self.filename=filename
              if (not self.filename):
                  self.ipca=IncrementalPCAdimred(-1,odim)
                  self.ipca.load(self.filename)
              else:
                  self.ipca=None
              self.totrain=totrain
              def ipcaf(x):
                  try:
                    return self.ipca.dimred(x.reshape(1,-1))       
                  except:
                    if (not self.ipca):
                       idim=(x.shape[1] if x.ndim==2 else x.shape[0])
                       self.ipca=IncrementalPCAdimred(idim,odim,*args,**kwargs)
                    xx=x.reshape(1,-1)
                    #print xx.shape
                    self.ipca.add_train(xx)
                    self.totrain-=1
                    if (self.totrain<=0):
                       self.ipca.recompute()
                       if (self.filename):
                           self.ipca.save(filename)
                    else:
                       raise NotReady
              self.processing=[ ('PCA' , {'PCA':ipcaf}) ]

__call__=Model
                 