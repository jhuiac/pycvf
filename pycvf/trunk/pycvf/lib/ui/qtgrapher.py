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

class CurveWidget(QWidget):
    def __init__(self,parent,data,color=(255,255,255),minv=-1,maxv=1,plotindividualpoints=False,pointsz=3,inverty=False,*args):
        apply(QWidget.__init__,(self, parent,) + args)
        self.setMinimumHeight(50)
        self.setMinimumWidth(400)
        self.color=color
        self.pointsz=pointsz
        self.minv=minv
        self.maxv=maxv
        self.inverty=inverty
	self.amplitude=self.maxv-self.minv
        self.plotindividualpoints=plotindividualpoints
	self.data=data
    def paintEvent(self,ev):
	r=QWidget.paintEvent(self,ev)
        pa= QPainterPath()
	ld=len(self.data)
	pa.moveTo(0,self.data[0])
	for i in range(1,ld):
	  x,y=int(((i)*self.width()/ld)),(self.inverty) and int((float(self.data[i]-self.minv)/float(self.amplitude))*self.height()) or (self.height()-int((float(self.data[i]-self.minv)/float(self.amplitude))*self.height()))
	  #print x,y
	  pa.lineTo(x,y)
        pa.lineTo(self.width(),0)
        pa.lineTo(0,0)
        self.p = QPainter(self)
        self.p.setBrush(QBrush(QColor(0,0,0)))
        self.p.setPen(QPen(QColor(0,0,0)))
        self.p.drawRect(0,0,self.width(),self.height())
        self.p.setBrush(QBrush(QColor(*self.color)))
        self.p.setPen(QPen(QColor(*self.color)))
        self.p.drawPath(pa)
        self.p.end()
        return r
    def f(self,data):
	self.data=data
	self.update()
    def resizeEvent(self, ev):
        print ev.size()


class QtGrapherDialog(QtGui.QDialog):
        def __init__(self,*args, **kwargs):
            QtGui.QDialog.__init__(self )
            self.cw=self
            self.layout=QtGui.QVBoxLayout(self.cw)
            self.layout.setContentsMargins(0,0,0,0)
            self.pwl=CurveWidget(self,*args, **kwargs)
            self.layout.addWidget(self.pwl)
            self.pbok=QtGui.QPushButton(self.cw)
            self.pbok.setText("Ok")
            self.connect(self.pbok,QtCore.SIGNAL("clicked()"),self,QtCore.SLOT("accept()"))
            self.layout.addWidget(self.pbok)
            self.pbcancel=QtGui.QPushButton(self.cw)
            self.pbcancel.setText("Cancel")
            self.connect(self.pbcancel,QtCore.SIGNAL("clicked()"),self,QtCore.SLOT("reject()"))
            self.layout.addWidget(self.pbcancel)
            self.update()
        def accept(self):
            QtGui.QDialog.accept(self)
        def __del__(self):
            self.hide()
        def f(self,data):
            return self.pwl.f(data)
