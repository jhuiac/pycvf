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
  
from pycvf.core.errors import pycvf_warning, pycvf_debug

class StatModel:
    def __init__(self,class_, filename,factory=None,suppkwargs=None,verbose=True):
        if (suppkwargs==None):
            suppkwargs={}
        self.class_=class_
        self.factory=factory
        self.filename=filename
        self.verbose=verbose
        self.dirty=False
        try:
          f=file(self.filename,"rb")
          self.instance=self.class_.load(f,**suppkwargs)
        except Exception, e:
          if (self.verbose):
            pycvf_warning( (u"Failed to load "+ self.filename+u":"+str(type(e))+u","+str(e)+u"\n").encode('utf8'))
            #if (hasattr(sys,"last_traceback")):
            #  traceback.print_tb(sys.last_traceback)
            #else:
            #  traceback.print_tb(sys.exc_traceback)
          self.instance=(self.factory(**suppkwargs) if self.factory else self.class_(**suppkwargs))
    def __del__(self):
        if self.dirty:
          if (self.verbose):
            pycvf_debug(10, "writing "+self.filename+"...")
          f=file(self.filename,"wb")
          self.instance.dump(f)
          f.close()
          self.dirty=False
    def save(self):
        if self.dirty:
          pycvf_debug(10, "writing "+self.filename+"...")
          f=file(self.filename,"wb")
          self.instance.dump(f)
          f.close()
          self.dirty=False
    def train(self,*args, **xargs):
        self.dirty=True
        return self.instance.train(*args, **xargs)
    def train_separated(self,*args, **xargs):
        self.dirty=True
        return self.instance.train_separated(*args, **xargs)
    def online_train(self,*args, **xargs):
        self.dirty=True
        return self.instance.online_train(*args, **xargs)        
    def online_train_separated(self,*args, **xargs):
        self.dirty=True
        return self.instance.online_train_separated(*args, **xargs)        
    def test(self,*args, **xargs):
        return self.instance.test(*args, **xargs)
    def test_separated(self,*args, **xargs):
        return self.instance.test_separated(*args, **xargs)
    def sample(self,*args, **xargs):
        return self.instance.sample(*args, **xargs)
    def random_improve(self,*args, **xargs):
        return self.instance.random_improve(*args, **xargs)
    def external_process(self,A,external_process_f,*args, **xargs):
        return external_process_f(A,self)

         
__call__=StatModel
