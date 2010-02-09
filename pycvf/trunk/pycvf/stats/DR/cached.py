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



class CachedDimReduc():
    def __init__(self,dimredclass,filename, burnbefore,*args,**xargs):
        self.dr=dimredclass(*args,**xargs)
        self.filename=filename
        try:
            self.dr.load(file(self.filename,"rb"))
        except:
            self.dr.build(burnbefore())
            #try:
            self.dr.recompute()
            #except AttributeError:
            #    pass 
    def __del__(self):
        self.savenow()
    def savenow(self):
        self.dr.save(file(self.filename,"wb"))
    def dimred(self,M):
        return self.dr.dimred(M)
    def dimaug(self,M):
        return self.dimaug(M)

