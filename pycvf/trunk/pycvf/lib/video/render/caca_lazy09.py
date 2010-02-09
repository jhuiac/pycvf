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
import ctypes
from pycvf.lib.graphics.imgfmtutils import *
from pycvf.core import settings

lcaca = ctypes.cdll.LoadLibrary('libcaca.so.0')

class LazyDisplay(object):
    def __init__(self):
           lcaca.caca_init()        
           lcaca.caca_set_window_title("pycvf");
           self.ww = lcaca.caca_get_width();
           self.hh = lcaca.caca_get_height();

            
           #self.display= lcaca.caca_create_display(None)
           #lcaca.caca_set_display_title(self.display, "sPyCVF")
           pass
    def __del__(self):
          # lcaca.caca_free_display(self.display);
          pass
    def f(self,img):
            """ this function updates the image on the screen (this function does a copy of the image)"""
            #ximg=img.mean(axis=2)
            ximg=img   
            try:
              image = NumPy2PIL(ximg)
            except Exception,e:
              print "Error during conversion"
              print e
            bmwidth,bmheight=300,200
            image=image.resize((bmwidth,bmheight)).convert('RGBA')
            #self.screen.put_image((0, 0), image)
            #self.dither= lcaca.caca_create_dither(72,bmwidth,bmheight,)
            #
            pixels=image.tostring()
            bitmap=lcaca.caca_create_bitmap(32,bmwidth,bmheight,4*bmwidth,0x000000ff,0x0000ff00,0x00ff0000,0x00000000)
            
            lcaca.caca_draw_bitmap(0,0,self.ww,self.hh,bitmap, pixels);
            lcaca.caca_free_bitmap(bitmap)
            #lcaca.caca_free_dither(self.dither)
            #lcaca.caca_refresh_display(self.display)
            lcaca.caca_refresh()
    def push(self,stamped_img):
         """ we ignore the timestamp and directly display the image on the screen"""
         self.f(stamped_img[0])
    def render(self):
            lcaca.caca_refresh()
            
            #gcc -shared -fPIC -o libcaca.so.0 caca.c graphics.c event.c math.c line.c box.c conic.c triangle.c sprite.c bitmap.c time.c -I .. -DHAVE_CONFIG_H -O2 -DPIC -DOPTIMISE_SLANG_PALETTE=1   -lslang -lncurses -lX11
