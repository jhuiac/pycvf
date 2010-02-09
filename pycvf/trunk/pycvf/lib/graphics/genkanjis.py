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
import numpy
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pylab
import pycvf.lib.ui.qt

import sys , gzip
#app =  qa=QApplication(sys.argv)#,"canvasapp")
#app.processEvents()

import pycvf.core.directories as pycvfdir

#KANJIDICFILE=file("/usr/share/edict/kanjidic")
KANJIDICFILE=gzip.open(pycvfdir.PYCVF_STATICDATA+"/kanjidic.gz")

kanjidic=map(lambda e:e.split(u' '),KANJIDICFILE.read().decode('eucjp').split(u'\n'))

def plot_kanji_bw(dx,dy,text,filename=None,fontfamilly="mikachan",fontsz=12,border=0, borderclr=255):
   image=QImage(dx,dy,QImage.Format_Mono)
   image.fill(1)
   paint=QPainter(image)
   #paint.begin(image)
   paint.setFont(QtGui.QFont(fontfamilly,fontsz))
   paint.drawText(QRect(0.,0.,dx,dy),0,QtCore.QString(text))   
   paint.end()
   if (filename):
     if (image.save(filename)):
       pass
     else:
       print "save_error"
   i=image.convertToFormat(QImage.Format_ARGB32)
   ptr=i.bits()
   ptr.setsize(dx*dy*4)
   v=numpy.ndarray(buffer=ptr.asstring(),shape=(dy,dx,4),dtype=numpy.uint8)
   if (not border):
     return v[:,:,0]
   else:
       res=numpy.ones((dy+2*border,dx+2*border))*borderclr
       res[border:-border,border:-border]=v[:,:,0]
       return res


def plot_kanji_gray(dx,dy,text,filename=None,fontfamilly="mikachan",fontsz=12,border=0, borderclr=255):
   image2=QImage(dx,dy,5)
   image2.fill(255)
   paint2=QPainter(image2)
   #paint.begin(image)
   paint2.setFont(QtGui.QFont(fontfamilly,fontsz))
   paint2.drawText(QRect(0.,0.,dx,dy),0,QtCore.QString(text))   
   paint2.end()
   if (filename):
     if (image2.save(filename)):
       pass
     else:
       print "save_error"
   ptr=image2.bits()
   ptr.setsize(dx*dy*4)
   v=numpy.ndarray(buffer=ptr.asstring(),shape=(dy,dx,4),dtype=numpy.uint8)
   if (not border):
       return v[:,:,0]
   else:
       res=numpy.ones((dy+2*border,dx+2*border))*borderclr
       res[border:-border,border:-border]=v[:,:,0]
       return res

#pylab.ion()
#pylab.gray()
#for k in kanjidic[1:]:
#  print k[0]
#  i=plot_kanji_gray(16,16,k[0],k[0]+".png", fontsz=8)
#  pylab.clf()
#  pylab.imshow(i,interpolation="nearest")
  #print v

