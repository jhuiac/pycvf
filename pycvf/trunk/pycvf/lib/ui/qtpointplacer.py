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
from pycvf.lib.ui.qt import qapp
from PyQt4 import QtCore
from PyQt4 import QtGui
import numpy
import random
    
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class PointWidget(QWidget):
    def __init__(self,parent,color,pointsz=32,*args):
        apply(QWidget.__init__,(self, parent,) + args)
        self.setMinimumHeight(pointsz)
        self.setMinimumWidth(pointsz)
        self.setMaximumHeight(pointsz)
        self.setMaximumWidth(pointsz)
        self.connections=[]
        self.color=color
        self.pointsz=pointsz
        self.cp=
    def paintEvent(self,ev):
        self.p = QPainter()
        self.p.begin(self)
        self.p.setBrush(QBrush(QColor(*self.color)))
        self.p.drawEllipse(0,0,self.pointsz,self.pointsz)
        self.p.end()
    def resizeEvent(self, ev):
        print ev.size()
    #def bpressed(self):
    #    print "pressed"
    #    self.moveButton.grabMouse(QCursor(Qt.ClosedHandCursor))
    #    #self.mouseMoveEvent=self.move_mouseMoveEvent
   #     self.moveButton.mouseMoveEvent=self.move_mouseMoveEvent
    def mousePressEvent(self,ev):
         self.prevmousepos=(ev.x(),ev.y())
         self.previousgeometry=self.geometry()
    def mouseMoveEvent(self,ev):
         g=self.previousgeometry   #self.geometry()
         g.translate(ev.x()-self.prevmousepos[0]+1,ev.y()-self.prevmousepos[1])
         self.setGeometry(g)
         self.parent().repaint()
         self.setGeometry(g)
         self.cp=(g.x()+g.width()//2), (g.y() + g.height()//2)
    #def mouseReleaseEvent(self):
    #    self.releaseMouse()
    #    self.mouseMoveEvent=self.normal_mouseMoveEvent     


class QtPointPlacer(QtGui.QMainWindow):
        def __init__(self, sz, *args):
            QtGui.QMainWindow.__init__(self , *args)
            self._i=numpy.zeros((sz[0],sz[1],4),dtype=numpy.uint8)
            self.i=QtGui.QImage(self._i.data,self._i.shape[1],self._i.shape[0],QtGui.QImage.Format_RGB32)
            self.lp=[]
            self.pwl=[PointWidget(self,(255,0,0)) for x in range(5)]
	    for pw in self.pwl:
              x,y=random.randint(0,sz[0]),random.randint(0,sz[1])
	      pw.setGeometry(QRect(x,y,32,32))
            self.show()
            #self.lp
        def __del__(self):
            self.hide()
        def f(self,thearray):
            self._i=thearray.astype(numpy.uint8).copy('C')
            self.i=QtGui.QImage(self._i.data,self._i.shape[1],self._i.shape[0],self.imgconvarray[self._i.shape[2]])
            if (self._i.shape[2]==1):
                self.i.setColorTable(self.colortable)
            self.update()
            qapp.processEvents()
        def x(self):
            pass

import time

if __name__ == "__main__":
  x=QtPointSelector((400,400))
  for i in range(1000):
    qapp.processEvents()
    time.sleep(0.01)