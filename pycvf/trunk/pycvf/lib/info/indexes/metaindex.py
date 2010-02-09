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
class BinBasedIndex():
    def __init__(self,shape,dp1,idxfact):
        self.dp1=dp1
        self.idx=numpy.zeros(dtype="object")
        for p in numpy.ndindex():
           self.idx[p]=idxfact(p)
    def add(self,key,value):
        self.idx[self.dp1[key]].add(key,value )
    def add_many(self,keys,values):
        for k in range(len(keys)):
           self.add(keyx[k],values[k])
    def __getitem__(self,key):
        return self.idx[self.dp1[key]][key]
    def getitem(self,key,*args,**xargs):
        return self.idx[self.dp1[key]].getitem(key)
    def __getball__(self,key,radius):
        """ We can do better here !!! """
        return self.idx[self.dp1[key]].__getball__(key,radius)
    def getball(self,key,*args,**xargs):
        """ We can do better here !!! """
        return self.idx[self.dp1[key]].getball(key,radius)


