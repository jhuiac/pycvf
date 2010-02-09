#!/usr/bin/env python
# -*- coding: utf-8 -*-
## ##########################################################################################################
## 
## This file is released under GNU Public License v3
## See LICENSE File at the top the pycvf tree.
##
## Author : Bertrand NOUVEL / CNRS (2009)
##
##
##
## Revision FILE: $Id$
##
## ###########################################################################################################
## copyright $Copyright$
## @version $Revision$
## @lastrevision $Date$
## @modifiedby $LastChangedBy$
## @lastmodified $LastChangedDate$
#############################################################################################################


# -*- coding: utf-8 -*-

import sys
import traceback
import numpy
import scipy
import random
import cPickle as pickle
import marshal

class DimReducedModel():
    def __init__(self,dimreduc,pmodel,burnin=None):
        self.dimreduc=dimreduc
        self.pmodel=pmodel
        self.burnin=burnin
    def train(self,positive_training_set,negative_training_set=None, *args, **kwargs):
        if (self.burnin):
            self.dimreduc.add_train(positive_training_set)
            self.burnin-=positive_training_set.shape[0]
            if (self.burnin<=0):
                self.burnin=None
            if (self.burnin):
               return
            else:
                self.dimreduc.recompute()
        positive_training_set_r=self.dimreduc.dimred(positive_training_set)
        negative_training_set_r=None
        if (negative_training_set):
           negative_training_set_r=self.dimreduc.dimred(negative_training_set)
        self.pmodel.train(numpy.asarray(positive_training_set_r),negative_training_set_r and numpy.asarray(negative_training_set_r) or None, *args, **kwargs)
    def test(self,data,log=True):
        rdata=self.dimreduc.dimred(data)
        return self.pmodel.test(numpy.asarray(rdata),log)
    def sample(self,n=100):
        rdata=self.pmodel.sample(n)
        return self.dimreduc.dimaug(rdata)
    def dump(self,file_):
        pickle.dump(self,file_)
    @staticmethod
    def load(file_,*args, **kwargs):
      return pickle.load(file_)
    def memory_cost(self, *args, **kwargs):
        assert(False)
    def cpu_cost(self, *args, **kwargs):
        assert(False)
    def random_improve(self,value,amount=0.5, prec=1):
        ###
        ### TODO : Since we have a projection only the really updated part should be upgraded
        ###
        print "TODO : better implementation !!!"
        return self.dimreduc.dimaug(self.pmodel.random_improve(self.dimreduc.dimred(value),amount,prec))
        assert(False)
        pass
