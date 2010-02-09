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


"""
This module provides explicit conversion methods for
    - CvMat:  OpenCV / IPL image data
    - PIL:    Python Imaging Library
    - numpy:  Python's Numeric Library

Currently supported image formats are:
    - 3 x  8 bit  RGB (GBR)
    - 1 x  8 bit  Grayscale
    - 1 x 32 bit  Float

In numpy, images are represented as multidimensional arrays with
a third dimension representing the image channels if more than one
channel is present.
"""

import Image, sys
import PIL.Image
import numpy
import ctypes
from pycvf.lib.misc.hack import *
from pycvf.core.errors import *

## import two version of opencv for convenience
#import pycvf.lib.graphics.xopencv as xcv
#import pycvf.lib.graphics.yopencv as ycv



try:
  import zopencv as zcv
except:
  pycvf_warning("failed to load zopencv")

try:
  from opencv import cv
except:
  try:
    import jfli.graphics.xopencv as cv
  except:
    pycvf_warning("failed to load xopencv")
  import sys
  


#import zzopencv as cv

#cdll.load()

###########################################################################
def PIL2NumPy(input):
    """Converts a PIL image to a numpy array.

    Supported input image formats are:
        RGB
        L
        F
    """
    if not (isinstance(input, PIL.Image.Image) or isinstance(input, Image.Image)):
        raise TypeError, 'Must be called with PIL.Image.Image or Image.Image!'
    # modes dictionary:
    # pil_mode : numpy dtype
    modes_map = {
        "RGBA" : numpy.uint8,
        "RGB" : numpy.uint8,
        "L"   : numpy.uint8,
        "F"   : numpy.float32
        }
    if not modes_map.has_key(input.mode):
        raise ValueError, 'Unknown or unsupported input mode!. Supported modes are RGB, L and F.'
    result_ro = numpy.asarray(input, dtype=modes_map[input.mode])  # Read-only array
    return result_ro.copy()  # Return a writeable array


###########################################################################
def NumPy2PIL(input):
    """Converts a numpy array to a PIL image.

    Supported input array layouts:
       2 dimensions of numpy.uint8
       3 dimensions of numpy.uint8
       2 dimensions of numpy.float32
    """
    if not isinstance(input, numpy.ndarray):
        raise TypeError, 'Must be called with numpy.ndarray!'
    # Check the number of dimensions of the input array
    ndim = input.ndim
    if not ndim in (2, 3):
        raise ValueError, 'Only 2D-arrays and 3D-arrays are supported!'
    if ndim == 2:
        channels = 1
    else:
        channels = input.shape[2]
    # supported modes list: [(channels, dtype), ...]
    modes_list = [(1, numpy.uint8), (3, numpy.uint8), (1, numpy.float32), (4,numpy.uint8)]
    mode = (channels, input.dtype)
    if not mode in modes_list:
        raise ValueError, 'Unknown or unsupported input mode'
    return Image.fromarray(input)






#if False:
#try:
    ###########################################################################

def Ipl2PIL(input):
        """Converts an OpenCV/IPL image to PIL the Python Imaging Library.

        Supported input image formats are
           IPL_DEPTH_8U  x 1 channel
           IPL_DEPTH_8U  x 3 channels
           IPL_DEPTH_32F x 1 channel
        """
        if not isinstance(input, cv.CvMat):
            raise TypeError, 'must be called with a cv.CvMat!'
        # assert that the channels are interleaved
        if input.dataOrder != 0:
            raise ValueError, 'dataOrder must be 0 (interleaved)!'
        #orientation
        if input.origin == 0:
            orientation = 1 # top left
        elif input.origin == 1:
            orientation = -1 # bottom left
        else:
            raise ValueError, 'origin must be 0 or 1!'
        # mode dictionary:
        # (channels, depth) : (source mode, dest mode, depth in byte)
        mode_list = {
            (1, cv.IPL_DEPTH_8U)  : ("L", "L", 1),
            (3, cv.IPL_DEPTH_8U)  : ("BGR", "RGB", 3),
            (1, cv.IPL_DEPTH_32F) : ("F", "F", 4)
            }
        key = (input.nChannels, input.depth)
        if not mode_list.has_key(key):
            raise ValueError, 'unknown or unsupported input mode'
        modes = mode_list[key]
        return Image.fromstring(
            modes[1], # mode
            (input.width, input.height), # size tuple
            input.imageData, # data
            "raw",
            modes[0], # raw mode
            input.widthStep, # stride
            orientation # orientation
            )    
    
def zIpl2PIL(input):
        """Converts an OpenCV/IPL image to PIL the Python Imaging Library.

        Supported input image formats are
           IPL_DEPTH_8U  x 1 channel
           IPL_DEPTH_8U  x 3 channels
           IPL_DEPTH_32F x 1 channel
        """
        if not isinstance(input, cv.CvMat):
            raise TypeError, 'must be called with a cv.CvMat!'
        # assert that the channels are interleaved
        if input.dataOrder != 0:
            raise ValueError, 'dataOrder must be 0 (interleaved)!'
        #orientation
        if input.origin == 0:
            orientation = 1 # top left
        elif input.origin == 1:
            orientation = -1 # bottom left
        else:
            raise ValueError, 'origin must be 0 or 1!'
        # mode dictionary:
        # (channels, depth) : (source mode, dest mode, depth in byte)
        mode_list = {
            (1, zcv.IPL_DEPTH_8U)  : ("L", "L", 1),
            (3, zcv.IPL_DEPTH_8U)  : ("BGR", "RGB", 3),
            (1, zcv.IPL_DEPTH_32F) : ("F", "F", 4)
            }
        key = (input.nChannels, input.depth)
        if not mode_list.has_key(key):
            raise ValueError, 'unknown or unsupported input mode'
        modes = mode_list[key]
        return Image.fromstring(
            modes[1], # mode
            (input.width, input.height), # size tuple
            input.imageData, # data
            "raw",
            modes[0], # raw mode
            input.widthStep, # stride
            orientation # orientation
            )


            
            
            
    ###########################################################################
def PIL2Ipl(input):
        """Converts a PIL image to the OpenCV/IPL CvMat data format.

        Supported input image formats are:
            RGB
            L
            F
        """
        if not (isinstance(input, PIL.Image.Image) or isinstance(input, Image.Image)):
            raise TypeError, 'Must be called with PIL.Image.Image or Image.Image!'
        # mode dictionary:
        # (pil_mode : (ipl_depth, ipl_channels)
        mode_list = {
            "RGB" : (cv.IPL_DEPTH_8U, 3),
            "L"   : (cv.IPL_DEPTH_8U, 1),
            "F"   : (cv.IPL_DEPTH_32F, 1)
            }
        if not mode_list.has_key(input.mode):
            raise ValueError, 'unknown or unsupported input mode'
        result = cv.cvCreateImage(
            cv.cvSize(input.size[0], input.size[1]),  # size
            mode_list[input.mode][0],  # depth
            mode_list[input.mode][1]  # channels
            )
        # set imageData
        result.imageData = input.tostring()
        return result

    
def PIL2zIpl(input):
        """Converts a PIL image to the OpenCV/IPL CvMat data format.

        Supported input image formats are:
            RGB
            L
            F
        """
        if not (isinstance(input, PIL.Image.Image) or isinstance(input, Image.Image)):
            raise TypeError, 'Must be called with PIL.Image.Image or Image.Image!'
        # mode dictionary:
        # (pil_mode : (ipl_depth, ipl_channels)
        mode_list = {
            "RGB" : (zcv.IPL_DEPTH_8U, 3),
            "L"   : (zcv.IPL_DEPTH_8U, 1),
            "F"   : (zcv.IPL_DEPTH_32F, 1)
            }
        if not mode_list.has_key(input.mode):
            raise ValueError, 'unknown or unsupported input mode'
        result = zcv.cvCreateImage(
            zcv.cvSize(input.size[0], input.size[1]),  # size
            mode_list[input.mode][0],  # depth
            mode_list[input.mode][1]  # channels
            )
        # set imageData
        result.imageData = input.tostring()
        return result
    



###########################################################################
def NumPy2Ipl(input):
        """Converts a numpy array to the OpenCV/IPL CvMat data format.

        Supported input array layouts:
           2 dimensions of numpy.uint8
           3 dimensions of numpy.uint8
           2 dimensions of numpy.float32
        """
        return PIL2Ipl(NumPy2PIL(input))

    
###########################################################################
def NumPy2zIpl(input):
        """Converts a numpy array to the OpenCV/IPL CvMat data format.

        Supported input array layouts:
           2 dimensions of numpy.uint8
           3 dimensions of numpy.uint8
           2 dimensions of numpy.float32
        """
        return PIL2zIpl(NumPy2PIL(input))
    

###########################################################################
def Ipl2NumPy(input):
        """Converts an OpenCV/IPL image to a numpy array.

        Supported input image formats are
           IPL_DEPTH_8U  x 1 channel
           IPL_DEPTH_8U  x 3 channels
           IPL_DEPTH_32F x 1 channel
        """
        return PIL2NumPy(Ipl2PIL(input))

###########################################################################
def zIpl2NumPy(input):
        """Converts an OpenCV/IPL image to a numpy array.

        Supported input image formats are
           IPL_DEPTH_8U  x 1 channel
           IPL_DEPTH_8U  x 3 channels
           IPL_DEPTH_32F x 1 channel
        """
        return PIL2NumPy(zIpl2PIL(input))    




def NumPy2IplFastWithCopy(input):
        mode_list = {
            numpy.dtype(numpy.uint8) : cv.IPL_DEPTH_8U,
            numpy.dtype(numpy.uint16) : cv.IPL_DEPTH_16U,
            numpy.dtype(numpy.int8) : cv.IPL_DEPTH_8S,
            numpy.dtype(numpy.int16) : cv.IPL_DEPTH_16S,
            numpy.dtype(numpy.int32) : cv.IPL_DEPTH_32S,
            numpy.dtype(numpy.float32) : cv.IPL_DEPTH_32F,
            numpy.dtype(numpy.float64) : cv.IPL_DEPTH_64F,
            }
        if not mode_list.has_key(input.dtype):
            raise ValueError, 'unknown or unsupported input mode'
        result = cv.cvCreateImage(cv.cvSize(input.shape[1], input.shape[0]),  # size
            mode_list[input.dtype],  # depth
            input.shape[2]
            )
        result.imageData = input.tostring()
        return result

def NumPy2zIplFastWithCopy(input):
        mode_list = {
            numpy.dtype(numpy.uint8) : zcv.IPL_DEPTH_8U,
            numpy.dtype(numpy.uint16) : zcv.IPL_DEPTH_16U,
            numpy.dtype(numpy.int8) : zcv.IPL_DEPTH_8S,
            numpy.dtype(numpy.int16) : zcv.IPL_DEPTH_16S,
            numpy.dtype(numpy.int32) : zcv.IPL_DEPTH_32S,
            numpy.dtype(numpy.float32) : zcv.IPL_DEPTH_32F,
            numpy.dtype(numpy.float64) : zcv.IPL_DEPTH_64F,
            }
        if not mode_list.has_key(input.dtype):
            raise ValueError, 'unknown or unsupported input mode'
        result = zcv.cvCreateImage(zcv.cvSize(input.shape[1], input.shape[0]),  # size
            mode_list[input.dtype],  # depth
            input.shape[2]
            )
        result.imageData = input.tostring()
        return result    




        ###########################################################################
    #def NumPy2IplFast(input):
    #    mode_list = {
    #        numpy.dtype(numpy.uint8) : cv.IPL_DEPTH_8U,
    #        numpy.dtype(numpy.uint16) : cv.IPL_DEPTH_16U,
    #        numpy.dtype(numpy.int8) : cv.IPL_DEPTH_8S,
    #        numpy.dtype(numpy.int16) : cv.IPL_DEPTH_16S,
    #        numpy.dtype(numpy.int32) : cv.IPL_DEPTH_32S,
    #        numpy.dtype(numpy.float32) : cv.IPL_DEPTH_32F,
    #        numpy.dtype(numpy.float64) : cv.IPL_DEPTH_64F,
    #        }
    #    if not mode_list.has_key(input.dtype):
    #        raise ValueError, 'unknown or unsupported input mode'
    #    result = cv.cvCreateImage(cv.cvSize(input.shape[1], input.shape[0]),  # size
    #        mode_list[input.dtype],  # depth
    #        input.shape[2]
    #        )
    #    #result.imageData = input.data
    #    cv.cvReleaseData(result)
    #    result.data=input.data
    #    return result


###########################################################################
def Ipl2NumPyFast(input):
        """Converts an OpenCV/IPL image to Numpy
        """
        mode_list = {
            cv.IPL_DEPTH_8U: numpy.uint8 ,
            cv.IPL_DEPTH_16U:numpy.uint16,
            cv.IPL_DEPTH_8S:numpy.int8,
            cv.IPL_DEPTH_16S:numpy.int16 ,
            cv.IPL_DEPTH_32S:numpy.int32 ,
            cv.IPL_DEPTH_32F:numpy.float32 ,
            cv.IPL_DEPTH_64F:numpy.float64
            }
        if not isinstance(input, cv.CvMat):
            raise TypeError, 'must be called with a cv.CvMat! not :'+str(type(input))
        # assert that the channels are interleaved
        #if input.dataOrder != 0:
        #    raise ValueError, 'dataOrder must be 0 (interleaved)!'
        #orientation
        if input.origin == 0:
            orientation = 1 # top left
        elif input.origin == 1:
            orientation = -1 # bottom left
        else:
            raise ValueError, 'origin must be 0 or 1!'
        if input.dataOrder == 0:
            dtype=mode_list[input.depth]
            assert(input.widthStep==(input.width*dtype().nbytes*input.nChannels))
            assert(orientation!=-1)
            ar=numpy.ndarray(dtype=dtype,shape=(input.height,input.width, input.nChannels),buffer=input.imageData) # data
            return ar
        else:
            dtype=mode_list[input.depth]
            assert(input.widthStep==(input.width*dtype().nbytes))
            assert(orientation!=-1)
            ar=numpy.ndarray(dtype=dtype,shape=( input.nChannels,input.height,input.width),buffer=input.imageData) # data
            return ar
        
###########################################################################
def zIpl2NumPyFast(input):
        """Converts an OpenCV/IPL image to Numpy
        """
        mode_list = {
            zcv.IPL_DEPTH_8U: numpy.uint8 ,
            zcv.IPL_DEPTH_16U:numpy.uint16,
            zcv.IPL_DEPTH_8S:numpy.int8,
            zcv.IPL_DEPTH_16S:numpy.int16 ,
            zcv.IPL_DEPTH_32S:numpy.int32 ,
            zcv.IPL_DEPTH_32F:numpy.float32 ,
            zcv.IPL_DEPTH_64F:numpy.float64
            }
        if not isinstance(input, zcv.CvMat):
            raise TypeError, 'must be called with a cv.CvMat! not :'+str(type(input))
        # assert that the channels are interleaved
        #if input.dataOrder != 0:
        #    raise ValueError, 'dataOrder must be 0 (interleaved)!'
        #orientation
        if input.origin == 0:
            orientation = 1 # top left
        elif input.origin == 1:
            orientation = -1 # bottom left
        else:
            raise ValueError, 'origin must be 0 or 1!'
        if input.dataOrder == 0:
            dtype=mode_list[input.depth]
            assert(input.widthStep==(input.width*dtype().nbytes*input.nChannels))
            assert(orientation!=-1)
            ar=numpy.ndarray(dtype=dtype,shape=(input.height,input.width, input.nChannels),buffer=input.imageData) # data
            return ar
        else:
            dtype=mode_list[input.depth]
            assert(input.widthStep==(input.width*dtype().nbytes))
            assert(orientation!=-1)
            ar=numpy.ndarray(dtype=dtype,shape=( input.nChannels,input.height,input.width),buffer=input.imageData) # data
            return ar        



def NumPy2XCVMat(input):
        mode_list = {
            numpy.dtype(numpy.uint8) : xcv.CV_8U,
            numpy.dtype(numpy.uint16) :xcv.CV_16U,
            numpy.dtype(numpy.int8) : xcv.CV_8S,
            numpy.dtype(numpy.int16) : xcv.CV_16S,
            numpy.dtype(numpy.int32) : xcv.CV_32S,
            numpy.dtype(numpy.float32) : xcv.CV_32F,
            numpy.dtype(numpy.float64) : xcv.CV_64F,
        }
        s=input.shape
        ns=numpy.array(list(s),dtype=numpy.int32)
        mh=xcv.cvCreateMatNDHeader(input.ndim,memory_addr_of_numpy_array_ptr(ns,dtype=ctypes.c_long),mode_list[input.dtype])
        xcv.cvSetData(mh,memory_addr_of_numpy_array_ptr(input),xcv.CV_AUTOSTEP)#input.strides[0])
        return mh


def NumPy2XIplFast(input):
        mode_list = {
            numpy.dtype(numpy.uint8) : xcv.IPL_DEPTH_8U,
            numpy.dtype(numpy.uint16) :xcv.IPL_DEPTH_16U,
            numpy.dtype(numpy.int8) : xcv.IPL_DEPTH_8S,
            numpy.dtype(numpy.int16) : xcv.IPL_DEPTH_16S,
            numpy.dtype(numpy.int32) : xcv.IPL_DEPTH_32S,
            numpy.dtype(numpy.float32) : xcv.IPL_DEPTH_32F,
            numpy.dtype(numpy.float64) : xcv.IPL_DEPTH_64F,
            }
        if not mode_list.has_key(input.dtype):
            raise ValueError, 'unknown or unsupported input mode'

        d=1
        try:
            d=input.shape[2]
        except:
            pass
        mode=mode_list[input.dtype]
        result = xcv.cvCreateImageHeader(xcv.cvSize(input.shape[1], input.shape[0]),  # size
            mode,  # depth
            d
            )
        #result.imageData = input.data
        #print dir(result.contents)
        #print result.contents._fields_
        # print result.contents.__dict__
        # print result.contents
        #print type(result.contents.imageData)
        #print ctypes.c_char_p(result.contents.imageData)
        #print type(result.contents.imageDataOrigin)

        #set_pointer_via_ulong(result.contents.imageData,memory_addr_of_numpy_array(input))
        ycv.IplPtrSetDataPtr(get_pointer_as_ulong(result),memory_addr_of_numpy_array(input) )
        return result


###########################################################################
def XIpl2NumPyFast(input_ptr):
        """Converts an OpenCV/IPL image to Numpy
        """
        input=input_ptr.contents
        mode_list = {
            ctypes.c_int(xcv.IPL_DEPTH_8U).value: numpy.uint8 ,
            ctypes.c_int(xcv.IPL_DEPTH_16U).value:numpy.uint16,
            ctypes.c_int(xcv.IPL_DEPTH_8S).value:numpy.int8,
            ctypes.c_int(xcv.IPL_DEPTH_16S).value:numpy.int16 ,
            ctypes.c_int(xcv.IPL_DEPTH_32S).value:numpy.int32 ,
            ctypes.c_int(xcv.IPL_DEPTH_32F).value:numpy.float32 ,
            ctypes.c_int(xcv.IPL_DEPTH_64F).value:numpy.float64
            }
    #    if not isinstance(input, xcv.CvMat):
    #        raise TypeError, 'must be called with a cv.CvMat!'
        # assert that the channels are interleaved
        #if input.dataOrder != 0:
        #    raise ValueError, 'dataOrder must be 0 (interleaved)!'
        #orientation
        if input.origin == 0:
            orientation = 1 # top left
        elif input.origin == 1:
            orientation = -1 # bottom left
        else:
            raise ValueError, 'origin must be 0 or 1!'
        if input.dataOrder == 0:
            dtype=mode_list[input.depth]
            #assert(input.widthStep==(input.width*dtype().nbytes*input.nChannels))
            strides=(input.width*dtype().nbytes*input.nChannels,dtype().nbytes*input.nChannels,dtype().nbytes)
            assert(orientation!=-1)
            shape=(input.height,input.width, input.nChannels)
            #print shape
            #print strides
            buffer=ycv.IplPtrGetBuffer(get_pointer_as_ulong(input_ptr))
            ar=numpy.ndarray(dtype=dtype,shape=shape,buffer=buffer,strides=strides) # data
            return ar
        else:
            dtype=mode_list[input.depth]
            #assert(input.widthStep==(input.width*dtype().nbytes))
            #strides=(input.width*input.height*dtype.nbytes,dtype().nbytes*input.width,dtype().nbytes)
            shape=( input.nChannels,input.height,input.width)
            #print shape
            strides=(input.width*input.nChannels,input.nChannels,1)
            #print strides
            assert(orientation!=-1)
            buffer=ycv.IplPtrGetBuffer(get_pointer_as_ulong(input_ptr))
            ar=numpy.ndarray(dtype=dtype,shape=shape,buffer=buffer,strides=Strides) # data
            return ar

#except:
#    pass
