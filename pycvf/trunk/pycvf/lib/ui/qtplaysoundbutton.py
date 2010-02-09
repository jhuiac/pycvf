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
from pycvf.core.errors import *
from pycvf.lib.ui.qt import qapp
from PyQt4 import QtCore
from PyQt4 import QtGui

from pycvf.lib.audio.render.lazy import LazyAudioSink

class QtPlaySoundButton(QtGui.QWidget):
        def __init__(self,parent,*args):
            QtGui.QWidget.__init__(self,parent, *args)
            self.pb=QtGui.QPushButton("Play",self)
            self.tm=QtCore.QTimer()            
            self.setMinimumHeight(20)
            self.setMinimumWidth(60)
            self.lak=LazyAudioSink()
            self.connect(self.pb,QtCore.SIGNAL("clicked()"),self.playpause)
            self.playing=False
        def playpause(self):
            self.playing=not self.playing 
        def push(self,reader):
            self.reader=reader.copy()
            self.reader.set_observer(self.pushtosink)
            self.tm.setInterval(int(1000./90.)) # we try to update 30 time per seconds
            self.tm.setSingleShot(False)
            self.tm.start()
            self.connect(self.tm,QtCore.SIGNAL("timeout()"),self.ontimer)
        def ontimer(self):
            if self.playing:
              try:
                self.reader.step()
              except Exception,e:
                print e
                self.reader.rewind()
                self.reader.step()
        def set_player(self,reader):
            self.push(reader)
        def pushtosink(self,thearray):
#            print thearray
            self.lak.push((thearray[0],0))
            #self.update()
