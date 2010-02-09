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
from pycvf.lib.info.cacheable import *
import sys, traceback

class MultipleObserver:
    def __init__(self,observers,track=[],context=None):
        self.observers=observers
        if (type(context)==str):
            self.context=__import__(context,fromlist=context.split('.')[:-1])
        if (context==None):
            self.context=globals()
        self.memproceed=track
    def xeval(self,s,xobject):
        return eval(s,self.context,{'xobject':xobject})
    def xeval_s(self,s,xobject):
        try :   
          return eval(s,self.context,{'xobject':xobject})
        except NotReady:
          raise
        except Exception, e:
          print "Error while evalutation sub-expression"
          print e
          print "s",s
          #print "xobject",xobject
          if (hasattr(sys,"last_traceback")):
               traceback.print_tb(sys.last_traceback)
          else:
               traceback.print_tb(sys.exc_traceback)
          #sys.exit(-1)
          assert(False)
    def proceed(self,numpyimg):
        self.context['src']=numpyimg
        i=CacheableObject(numpyimg,transform_catalog=SimpleEvaluatorTransformCatalog(self.xeval))
        self.context['thesrc']=i ## allow complex observers...
        r=map(lambda o:i[o],self.observers)
        return r
    def iterproceed(self,numpyimg):
        self.memproceed.append(self.proceed(numpyimg))
