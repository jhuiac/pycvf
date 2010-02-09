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


### this defines a framework for applying filter on image, when we know
### that concurrent process are going to run on the image...


class SimpleEvaluatorTransformCatalog:
    def apply(self,transform,object):
        if (transform[-1]==')'):
            return eval(transform[:-1]+',object)');
        else:
            return eval(transform+'(object)');


class CacheableObject:
    def __init__(self,base,transform_catalog=SimpleEvaluatorTransformCatalog()):
        self.dict={'src':base}
        self.transform_catalog=transform_catalog
    def __getitem__(self,str):
        if (self.dict.has_key(str)):
            return self.dict[str]
        else:
            l=str.split('.')
            if (len(l)==1):
                raise Exception, "cannot find base object"
            else:
                self.dict[str]=self.transform_catalog.apply(l[-1],self['.'.join(l[:-1])])
                return self.dict[str]
