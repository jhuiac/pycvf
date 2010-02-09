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
import re, os, math, random, time,sys, traceback, datetime

import Image
from pycvf.core import database
from pycvf.datatypes import image
from pycvf.lib.graphics.genkanjis import *
#########################################################################################################################################
# Create the ContentsDatabase Object
#########################################################################################################################################

class DB(database.ContentsDatabase,image.Datatype):
    """
       Displays all the kanjis from the database, you may specify the size of the destination area, the size of the rendering area, the size
       of the font, and an upper bound on the number of kanjis that we want to see displayed.
       The rendering engine is QT. So you need to have a working display somewhere.
    """
    def __init__(self,scl=(48,48),fontsz=32,maxcnt=10000,invert=False):
        self.scl=scl
        self.fontsz=fontsz
        self.maxcnt=maxcnt
        self.invert=invert
    def __iter__(self):
        global kanjidic
        for i in range(min(len(kanjidic)-1,self.maxcnt)):
            if (len(kanjidic[1+i][0])):
              x=(plot_kanji_bw(self.scl[0],self.scl[1],kanjidic[1+i][0], fontsz=self.fontsz)).reshape(self.scl+(1,))
              yield ((255-x if self.invert else x) ,unicode(kanjidic[1+i][0]))             
    def __len__(self):
        return min(len(kanjidic)-1,self.maxcnt)
    def __getitem__(self, addr):
        x=(plot_kanji_bw(self.scl[0],self.scl[1],addr, fontsz=self.fontsz)).reshape(self.scl+(1,))
        return (255-x if self.invert else x)    
    def labeling_category(selfdb):
        import unicodedata
        class Labels:
            @staticmethod
            def datatype(self):
                from pycvf.datatypes.basics import Label
                return Label.Datatype
            @staticmethod
            def __iter__():
                for i in set(map( unicodedata.category(c[1]),selfdb)):
                    yield i
            @staticmethod
            def __getitem__(x):
                return unicodedata.category(x)
        return Labels()      
    def labeling_name(selfdb):
        import unicodedata
        class Labels:
            @staticmethod
            def datatype(self):
                from pycvf.datatypes.basics import Label
                return Label.Datatype
            @staticmethod
            def __iter__():
                for i in set(map( lambda c:unicodedata.name(c[1]),selfdb)):
                    yield i
            @staticmethod
            def __getitem__(x):
                return unicodedata.name(x)
        return Labels()      

        
ContentsDatabase=DB
__call__=DB
