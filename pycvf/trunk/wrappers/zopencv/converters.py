import numpy
from jfli.misc.hack import *

###########################################################################
def Ipl2NumPyFast(input):
    """Converts an OpenCV/IPL image to Numpy
    """
    mode_list = {
        IPL_DEPTH_8U: numpy.uint8 ,
        IPL_DEPTH_16U:numpy.uint16,
        IPL_DEPTH_8S:numpy.int8,
        IPL_DEPTH_16S:numpy.int16 ,
        IPL_DEPTH_32S:numpy.int32 ,
        IPL_DEPTH_32F:numpy.float32 ,
        IPL_DEPTH_64F:numpy.float64
        }
    if not isinstance(input, cv.CvMat):
        raise TypeError, 'must be called with a cv.CvMat!'
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



def NumPy2ZCVMat(input):
    mode_list = {
        numpy.dtype(numpy.uint8) : CV_8U,
        numpy.dtype(numpy.uint16) : CV_16U,
        numpy.dtype(numpy.int8) : CV_8S,
        numpy.dtype(numpy.int16) : CV_16S,
        numpy.dtype(numpy.int32) : CV_32S,
        numpy.dtype(numpy.float32) : CV_32F,
        numpy.dtype(numpy.float64) : CV_64F,
    }
    s=input.shape
    ns=numpy.array(list(s),dtype=numpy.int32)
    mh=cvCreateMatNDHeader(input.ndim,memory_addr_of_numpy_array_ptr(ns,dtype=ctypes.c_long),mode_list[input.dtype])
    cvSetData(mh,memory_addr_of_numpy_array_ptr(input),CV_AUTOSTEP)
    return mh





def NumPy2ZIplFast(input):
    mode_list = {
        numpy.dtype(numpy.uint8) : IPL_DEPTH_8U,
        numpy.dtype(numpy.uint16) :IPL_DEPTH_16U,
        numpy.dtype(numpy.int8) : IPL_DEPTH_8S,
        numpy.dtype(numpy.int16) : IPL_DEPTH_16S,
        numpy.dtype(numpy.int32) : IPL_DEPTH_32S,
        numpy.dtype(numpy.float32) : IPL_DEPTH_32F,
        numpy.dtype(numpy.float64) : IPL_DEPTH_64F,
        }
    if not mode_list.has_key(input.dtype):
        raise ValueError, 'unknown or unsupported input mode'
    d=1
    try:
        d=input.shape[2]
    except:
        pass
    mode=mode_list[input.dtype]
    sz=zopencv._raw_cvSize(input.shape[1], input.shape[0])
    result = zopencv._raw_cvCreateImageHeader(sz,  mode, d)
    result.imageData=memory_addr_of_numpy_array(input)
    result.imageDataOrigin=result.imageData
    return result


###########################################################################
def ZIpl2NumPyFast(input_img):
    """Converts an OpenCV/IPL image to Numpy"""
    input_ptr=input_img.get_pointer()
    mode_list = {
        IPL_DEPTH_8U: numpy.uint8 ,
        IPL_DEPTH_16U:numpy.uint16,
        IPL_DEPTH_8S:numpy.int8,
        IPL_DEPTH_16S:numpy.int16 ,
        IPL_DEPTH_32S:numpy.int32 ,
        IPL_DEPTH_32F:numpy.float32 ,
        IPL_DEPTH_64F:numpy.float64
        }
    if input_img.origin == 0:
        orientation = 1 # top left
    elif input_img.origin == 1:
        orientation = -1 # bottom left
    else:
        raise ValueError, 'origin must be 0 or 1!'
    if input_img.dataOrder == 0:
        dtype=mode_list[input_img.depth]
        strides=(input_img.width*dtype().nbytes*input_img.nChannels,dtype().nbytes*input_img.nChannels,dtype().nbytes)
        assert(orientation!=-1)
        shape=(input_img.height,input_img.width, input_img.nChannels)
        buffer=ycv.IplPtrGetBuffer(get_pointer_as_ulong(input_ptr))
        ar=numpy.ndarray(dtype=dtype,shape=shape,buffer=buffer,strides=strides) # data
        return ar
    else:
        dtype=mode_list[input.depth]
        shape=( input_img.nChannels,input_img.height,input_img.width)
        strides=(input_img.width*input_img.nChannels,input_img.nChannels,1)
        assert(orientation!=-1)
        buffer=ycv.IplPtrGetBuffer(get_pointer_as_ulong(input_ptr))
        ar=numpy.ndarray(dtype=dtype,shape=shape,buffer=buffer,strides=Strides) # data
        return ar
