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

from PyQt4 import QtCore
from PyQt4 import QtGui

from pylab import cm

import numpy

from pycvf.lib.ui.qt import qapp

try:
    LazyDisplayQt__imgconvarray={
                      1:QtGui.QImage.Format_Indexed8,
                      3:QtGui.QImage.Format_RGB888,
                      4:QtGui.QImage.Format_RGB32
                      }
except:
    LazyDisplayQt__imgconvarray={
                      1:QtGui.QImage.Format_Indexed8,
                      4:QtGui.QImage.Format_RGB32
                      }

#al=numpy.dstack([  scipy.lena().astype(numpy.uint16).reshape(512,512,1).repeat(3,axis=2),  numpy.ones((512,512),dtype=numpy.uint8)*255])
#l.f(al)
class QtDisplay(QtGui.QWidget):
        imgconvarray=LazyDisplayQt__imgconvarray
        def __init__(self,parent=None,aspectratio=-1, *args):
            QtGui.QWidget.__init__(self, parent,  *args)
            self._i=numpy.zeros((1,1,4),dtype=numpy.uint8)
            self.aspectratio=aspectratio
            self.setMinimumHeight(48)            
            self.setMinimumWidth(64)                        
            self.i=QtGui.QImage(self._i.data,self._i.shape[1],self._i.shape[0],self._i.shape[1]*self._i.shape[2],self.imgconvarray[self._i.shape[2]])
            self.colortable=[ (numpy.array(cm.jet(x)[0:3])*256.).astype(numpy.uint8) for x in range(0,256) ]
        def set_colormap(self,cma):
            self.colortable=cma
        def f(self,thearray,*args,**kwargs):
            self._i=thearray.astype(numpy.uint8).copy('C')
            self.i=QtGui.QImage(self._i.data,self._i.shape[1],self._i.shape[0],self._i.shape[1]*self._i.shape[2],self.imgconvarray[self._i.shape[2]])
            if (self._i.shape[2]==1):
                self.i.setColorTable(self.colortable)
            self.setMinimumHeight(min(self._i.shape[0]//4,240))
            self.setMinimumWidth(min(self._i.shape[1]//4,320))
            self.update()
        def paintEvent(self, ev):
            self.p = QtGui.QPainter()
            self.p.begin(self)
            if (self.aspectratio<0):
               aspectratio=(float(self.i.width())/self.i.height())*-self.aspectratio
            else:
               aspectratio=self.aspectratio
            #w,h=self._i.shape[1],self._i.shape[0]
            w,h=self.width(),self.height()
            #print w,h,aspectratio
            if (h*aspectratio>w):
               h=(float(w)/aspectratio)
            else:
               w=(h*aspectratio)
            #print w,h
            self.p.drawImage(QtCore.QRect(0,0,w,h),
                             self.i,
                             QtCore.QRect(0,0,self.i.width(),self.i.height()))
            self.p.end()

