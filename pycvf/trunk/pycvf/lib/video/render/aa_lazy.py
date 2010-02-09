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


import numpy
from PIL import Image
import aalib
import curses
from pycvf.lib.graphics.imgfmtutils import *
from pycvf.core import settings

class LazyDisplay(object):
    def __init__(self,ncurses=settings.AA_WITH_CURSES):
           self.ncurses=ncurses
           if ncurses:
             self.stdscr = curses.initscr()
           self.screen = aalib.AsciiScreen(width=80, height=40)
           self.render()
    def __del__(self):
            if (self.ncurses):
             self.ncurses.endwin()
    def f(self,img):
            """ this function updates the image on the screen (this function does a copy of the image)"""
            #ximg=img.mean(axis=2)
            ximg=img   
            try:
              image = NumPy2PIL(ximg)
            except Exception,e:
              print e
            image=image.convert('L').resize(self.screen.virtual_size)
            self.screen.put_image((0, 0), image)
            self.render()
    def push(self,stamped_img):
         """ we ignore the timestamp and directly display the image on the screen"""
         self.f(stamped_img[0])
    def render(self):
          try:
             r=self.screen.render()
             if (self.ncurses):
                self.stdscr.addstr(0, 0, r)
                self.stdscr.refresh()
             else:
                sys.stdout.write(r)
          except Exception,e:
              sys.stderr.write("Error during display"+str(e))
              raise