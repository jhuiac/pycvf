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
#from pycvf.lib.graphics import xopencv as zcv
#


from pycvf.core.errors import *
import numpy
from pycvf.lib.graphics.imgfmtutils import *

try:
  import zopencv as zcv

  def rgb2hsv(img,copy=True):
    if copy: ires=img.copy()
    else: ires=img
    res=zcv.NumPy2IplFast(ires)
    zcv.cvCvtColor (img, res, zcv.CV_RGB2HSV)
    return ires

  def hsv2rgb(img,copy=True):
    if copy: res=img.copy()
    else: res=img
    zcv.cvCvtColor (img, res, zcv.CV_HSV2RGB)#)55)#zcv.CV_HSV2RGB)
    return res

  def xyz2rgb(img,copy=True):
    frame=NumPy2ZIplFast(img)
    if copy: res=img.copy()
    else: res=img
    hsv=NumPy2ZIplFast(res)
    zcv.cvCvtColor (frame, hsv, zcv.CV_XYZ2RGB)
    return res


  def rgb2xyz(img,copy=True):
    frame=NumPy2ZIplFast(img)
    if copy: res=img.copy()
    else: res=img
    hsv=NumPy2ZIplFast(res)
    zcv.cvCvtColor (frame, hsv, zcv.CV_RGB2XYZ)
    return res


  def lab2rgb(img,copy=True):
    frame=NumPy2ZIplFast(img)
    if copy: res=img.copy()
    else: res=img
    hsv=NumPy2ZIplFast(res)
    zcv.cvCvtColor (frame, hsv, zcv.CV_LAB2RGB)
    return res


  def rgb2lab(img,copy=True):
    frame=NumPy2ZIplFast(img)
    if copy: res=img.copy()
    else: res=img
    hsv=NumPy2ZIplFast(res)
    zcv.cvCvtColor (frame, hsv, zcv.CV_RGB2LAB)
    return res


  def hls2rgb(img,copy=True):
    frame=NumPy2ZIplFast(img)
    if copy: res=img.copy()
    else: res=img
    hsv=NumPy2ZIplFast(res)
    zcv.cvCvtColor (frame, hsv, zcv.CV_HLS2RGB)
    return res


  def rgb2hls(img,copy=True):
    frame=NumPy2ZIplFast(img)
    if copy: res=img.copy()
    else: res=img
    hsv=NumPy2ZIplFast(res)
    zcv.cvCvtColor (frame, hsv, zcv.CV_RGB2HLS)
    return res


  def luv2rgb(img,copy=True):
    frame=NumPy2ZIplFast(img)
    if copy: res=img.copy()
    else: res=img
    hsv=NumPy2ZIplFast(res)
    zcv.cvCvtColor (frame, hsv, zcv.CV_LUV2RGB)
    return res


  def rgb2luv(img,copy=True):
    frame=NumPy2ZIplFast(img)
    if copy: res=img.copy()
    else: res=img
    hsv=NumPy2ZIplFast(res)
    zcv.cvCvtColor (frame, hsv, zcv.CV_RGB2LUV)
    return res


  def ycrcb2rgb(img,copy=True):
    frame=NumPy2ZIplFast(img)
    if copy: res=img.copy()
    else: res=img
    hsv=NumPy2ZIplFast(res)
    zcv.cvCvtColor (frame, hsv, zcv.CV_YCrCb2RGB)
    return res


  def rgb2ycrcb(img,copy=True):
    frame=NumPy2ZIplFast(img)
    if copy: res=img.copy()
    else: res=img
    hsv=NumPy2ZIplFast(res)
    zcv.cvCvtColor (frame, hsv, zcv.CV_RGB2YCrCb)
    return res

except:
  pycvf_warning("failed to load zopencv")
  try:
    import opencv
  except:
    pycvf_warning("failed to load opencv")
    import jfli.graphics.xopencv as opencv
    sys.stderr.write("USING XOPENCV\n")

  def rgb2hsv(img,copy=True):
    res=img.copy()
    #print img, res, opencv.CV_RGB2HSV
    opencv.cvCvtColor (img, res, opencv.CV_RGB2HSV)
    return res

  def hsv2rgb(img,copy=True):
    res=img.copy()
    opencv.cvCvtColor (img, res,opencv.CV_HSV2RGB)
    return res
