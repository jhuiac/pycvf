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
### this defines a framework for applying filter on image, when we know
### that concurrent process are going to run on the image...

import sys,re,traceback

class NotReady(Exception):
   pass

class SimpleEvaluatorTransformCatalog1:
    def __init__(self,evalf=(lambda x,object:eval(x))):
        self.xeval=evalf
    def apply(self,transform,xobject):
        idx=None
        try:
            idx=transform.index('(')
        except ValueError:
            idx=None
        if (idx):
            return self.xeval(transform[:idx]+'(xobject,'+transform[idx+1:],xobject)
        else:
            return self.xeval(transform+'(xobject)',xobject)

SimpleEvaluatorTransformCatalog=SimpleEvaluatorTransformCatalog1

class CacheableObject:
    def __init__(self,base,transform_catalog=SimpleEvaluatorTransformCatalog()):
        self.dict={'src':base}
        self.transform_catalog=transform_catalog
    def keys(self):
        return self.dict.keys()
    def __getitem__(self,xstr):
        if (self.dict.has_key(xstr)):
            return self.dict[xstr]
        else:
            l=xstr.split('|')
            try:
              if (len(l)==1):
                #raise Exception, ("no base object : path should start with src. (not %s )"%xstr)
                #print self.dict
                self.dict[xstr]=self.transform_catalog.xeval(l[-1],None)
                return self.dict[xstr]
              else:
                self.dict[xstr]=self.transform_catalog.apply(l[-1],self['|'.join(l[:-1])])
                return self.dict[xstr]
            except KeyboardInterrupt:
              raise
            except NotReady:
              raise
            except Exception, e:
              print "Error while evalutation expression"
              print "error " , e
              print "xstr " ,xstr
              if (hasattr(sys,"last_traceback")):
                traceback.print_tb(sys.last_traceback)
              else:
                traceback.print_tb(sys.exc_traceback)
              raise 

              




