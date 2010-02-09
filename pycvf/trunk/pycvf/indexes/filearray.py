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


import os
import cPickle as pickle

class FileArray():
    def __init__(self,filename,objectsz,mode="w+"):
        self.f=file(filename,mode)
        self.osz=objectsz
        self.protocol=1
    def __del__(self):
        self.f.close()
    def __getitem__(self,pos):
        self.f.seek(pos*self.osz,os.SEEK_SET)
        r=self.f.read(self.osz)
        return pickle.loads(r)
    def appenditem(self,i):
        self.f.seek(0,os.SEEK_END)
        bufr=pickle.dumps(i,protocol=self.protocol)
        print i,len(bufr)
        assert(len(bufr)<=self.osz)
        bufr+="\0"*(self.osz-len(bufr))
        self.f.write(bufr)
    def appenditems(self,l):
        for i in l:
            self.appenditem(i)
        