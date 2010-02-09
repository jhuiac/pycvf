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


import pyglet
from pyglet import font
from pyglet.text import Label

from pyglet.gl import *
glEnable(GL_TEXTURE_2D)
import numpy


class LazyDisplay(object):
    def __init__(self,title="Python Experiment"):
        self.window = pyglet.window.Window()
        self.event_loop = pyglet.app.EventLoop()
        self.on_draw=self.window.event(self.on_draw)
        self.on_window_close=self.event_loop.event(self.on_window_close)
        self.ip=None
#        self.window.set_title(title)
    def on_window_close(self,window):
       self.event_loop.exit()
       return pyglet.event.EVENT_HANDLED
    def __del__(self):
            self.window.close()
            self.ev_dispatch()
    def f(self,img):
            """ this function updates the image on the screen (this function does a copy of the image)"""
            (h,w,c)=numpy.shape(img)
            self.window.set_size(w,h)
            if (c==3):
                self.ip=pyglet.image.ImageData(w,h,'RGB',img.astype(numpy.uint8).tostring())#[0])
            elif (c==4):
                self.ip=pyglet.image.ImageData(w,h,'RGBA',img.astype(numpy.uint8).tostring())#[0])
            else:
                raise Exception,"unsupported number of channels"
#            i=self.stream.GetCurrentFrameRGBA32()
#            i=i.transpose(Image.FLIP_TOP_BOTTOM)
#            self.ip=pyglet.image.ImageData(i.size[0],i.size[1],'RGBA',i.tostring())
            self.ev_dispatch()
    def push(self,stamped_img):
         """ we ignore the timestamp and directly display the image on the screen"""
         self.f(stamped_img[0])
    def on_draw(self):
        """ this is the event handler that draws the window"""
        try:
            if (not self.ip):
                print "No Image"
                return
            self.window.clear()
            glPushMatrix()
            glTranslatef(0,self.ip.height,0)
            glScalef(1,-1,1)
            self.ip.blit(0,0)
            glPopMatrix()
            #print "."
        except Exception,e:
            print str(e)
            pass
    def ev_dispatch(self):
         """ this is an element of the event handler loop """
         pyglet.clock.tick()
         for window in pyglet.app.windows:
             window.switch_to()
             window.dispatch_events()
             window.dispatch_event('on_draw')
             window.flip()

