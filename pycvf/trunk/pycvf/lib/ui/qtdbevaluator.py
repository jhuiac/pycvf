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

import numpy
import random
    
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from pycvf.lib.ui.qt import qapp

import time
import sys


class QtDBEvaluator(QtGui.QWidget):
        def __init__(self, vdb, vdbval=None, vdbaddr=None, *args):
            QtGui.QWidget.__init__(self,*args) 
            self.blayout=QtGui.QHBoxLayout(self)
            #self.listview=QtGui.QListWidget(self)
            self.listview=QtGui.QTableWidget(self)
            self.blayout.addWidget(self.listview)
            self.xw=QtGui.QWidget(self)
            self.blayout.addWidget(self.xw)
            self.layout=QtGui.QVBoxLayout(self.xw)
            self.centralarea=QtGui.QWidget(self.xw)
            self.centralarea.setMinimumHeight(200)
            self.centralarea.setMinimumWidth(300)
            self.layout.addWidget(self.centralarea)
            self.vdb=vdb
            self.vdbval=vdbval
            self.addr=vdbaddr
            if (self.addr==None):
              try:
                self.addr=map(lambda x:x,self.vdb.keys())
              except:
                self.addr=map(lambda x:x[1],self.vdb)
            if (not(self.vdbval)):
               self.vdbval=map(lambda x:None,self.addr)
            #print self.vdbval
            if (not len(self.addr)):
               raise Exception, "Empty database"
            #for x in range(len(self.addr)):
            #  item=QListWidgetItem(str(self.addr[x]) + "---" + str(self.vdbval[x]))
            #  self.listview.insertItem(x,item)
            #
            #  #help(item.setData)
            #  item.setData(Qt.UserRole,QVariant(x))
            self.listview.setRowCount(len(self.addr))
            self.listview.setColumnCount(2)
            for x in range(len(self.addr)):
              #item=QListWidgetItem(str(self.addr[x]) + "---" + str(self.vdbval[x]))
              item=QTableWidgetItem(unicode(self.addr[x]))
              item.setData(Qt.UserRole,QVariant(x))
              item.setFlags(item.flags()&~2)
              self.listview.setItem(x,0,item)
              item=QTableWidgetItem(unicode(self.vdbval[x]))
              self.listview.setItem(x,1,item)
              #help(item.setData)
              item.setData(Qt.UserRole,QVariant(x))
              item.setFlags(item.flags()&~2)

            self.pos=0  
            self.layout.setContentsMargins(10,10,10,10)
            self.evalbararea=QWidget(self.xw)
            self.layout.addWidget(self.evalbararea)
            self.eblayout=QtGui.QHBoxLayout(self.evalbararea)
            self.eblayout.setContentsMargins(5,5,5,5)           
            self.quickeval=QWidget(self.evalbararea)
            self.quickevalf=QFrame(self.quickeval)
            self.quickevalf.setFrameStyle(QFrame.Panel | QFrame.Raised)
            self.quickevalf.setLineWidth(2);
            self.quickeval.setMinimumWidth(40)
            self.quickeval.setMinimumHeight(40)
            self.quickeval.setMaximumWidth(40)
            self.quickeval.setMaximumHeight(40)
            self.quickeval.mousePressEvent=  self.quick_mousePressEvent
            self.palqev=QPalette()
            self.palqev.setBrush(QPalette.Window,QBrush(QColor(255,255,0)))
            self.quickeval.setPalette(self.palqev)
            self.slider=QSlider(self.evalbararea)
            self.slider.setOrientation(1)
            self.evalbararea.setMinimumHeight(60)
            self.evalbararea.setMaximumHeight(60)
            self.eblayout.addWidget(self.quickeval)
            self.eblayout.addWidget(self.slider)
            self.buttonbar=QWidget(self.xw)
            self.buttonbar.setMaximumHeight(60)
            self.listview.setMaximumWidth(300)
            self.layout.addWidget(self.buttonbar)
            self.bblayout=QtGui.QHBoxLayout(self.buttonbar)
            self.bblayout.setContentsMargins(5,5,5,5)
            self.pbnext=QPushButton(self.buttonbar)
            self.pbnext.setText("Next")
            self.connect(self.pbnext,SIGNAL("clicked()"),self.go_next)
            self.bblayout.addWidget(self.pbnext)
            self.pbprev=QPushButton(self.buttonbar)
            self.pbprev.setText("Previous")  
            self.connect(self.pbprev,SIGNAL("clicked()"),self.go_prev)
            self.bblayout.addWidget(self.pbprev)
            x=self.vdb[self.addr[self.pos]]
            self.dalayout=QtGui.QVBoxLayout(self.centralarea)
            self.displaya=self.vdb.get_widget(x,self.centralarea) 
            #self.displaya.show()
            self.dalayout.addWidget(self.displaya)
            self.vdb.set_widget_value(self.displaya,x)
            self.connect(self.listview,SIGNAL("itemSelectionChanged()"),self.update_from_lv)
            self.listview.selectRow(0)
            self.slider.setRange(0,100)
            self.slider.setValue(int(self.vdbval[self.pos]!=None and (self.vdbval[self.pos]*100) or 50))
            self.ci=self.listview.item(0,1)
            self.connect(self.slider,SIGNAL("valueChanged(int)"),self.on_slider)
        def go_next(self):
            if (self.pos+1<len(self.addr)):
              #self.ci.setSelected(False)
              self.pos+=1
              self.listview.selectRow(self.pos)
              #self.listview.item(self.pos).setSelected(True)
              #x=self.vdb[self.addr[self.pos]]
              #self.vdb.set_widget_value(self.displaya,x)
        def go_prev(self):
            if (self.pos-1>=0):
              #self.ci.setSelected(False)
              self.pos-=1
              self.listview.selectRow(self.pos)
              #self.listview.item(self.pos).setSelected(True)
              #x=self.vdb[self.addr[self.pos]]
              #self.vdb.set_widget_value(self.displaya,x)
        def update_from_lv(self):
              its=self.listview.selectedItems()
              if (len(its)<1): 
                return
              v=its[0].data(Qt.UserRole)
              #print v,v.toInt()[0]
              self.go_index(v.toInt()[0])
        def go_index(self,idx):              
            if (idx>=0) and (idx<len(self.addr)):
              self.pos=idx
              x=self.vdb[self.addr[self.pos]]
              self.vdb.set_widget_value(self.displaya,x)
              self.ci=self.listview.item(self.pos,1)
              self.slider.setValue(int(self.vdbval[self.pos]!=None and (self.vdbval[self.pos]*100) or 50))
              self.listview.scrollToItem(self.listview.item(min(self.pos+3,len(self.addr)-2),1))
        def on_slider(self,value):
              v=float(self.slider.value())/100.
              self.vdbval[self.pos]=v
              self.ci.setText(unicode(v))
        def quick_mousePressEvent(self,ev):
            if ( ev.button()==Qt.LeftButton): 
               self.slider.setValue(100)
            if ( ev.button()==Qt.MidButton): 
               self.vdbval[self.pos]=None
               self.ci.setText(unicode(None))
            if ( ev.button()==Qt.RightButton): 
               self.slider.setValue(0)
            self.go_next()
            
class QtDBEvaluatorDialog(QtGui.QDialog):
        def __init__(self,vdb, vdbval=None, vdbaddr=None, *args):
            QtGui.QDialog.__init__(self , *args)
            self.cw=self
            self.layout=QtGui.QVBoxLayout(self.cw)
            self.layout.setContentsMargins(0,0,0,0)
            self.pwl=QtDBEvaluator(vdb, vdbval,vdbaddr,self.cw)
            self.layout.addWidget(self.pwl)
            self.pbok=QPushButton(self.cw)
            self.pbok.setText("Ok")
            self.connect(self.pbok,SIGNAL("clicked()"),self,SLOT("accept()"))
            self.layout.addWidget(self.pbok)
            self.pbcancel=QPushButton(self.cw)
            self.pbcancel.setText("Cancel")
            self.connect(self.pbcancel,SIGNAL("clicked()"),self,SLOT("reject()"))
            self.layout.addWidget(self.pbcancel)
            self.update()
        def push(self,x):
            self.pwl.push(x)
        def __del__(self):
            self.hide()
