SHRT_MAX=32767
INVALID_TYPE_ERROR=0

cimport cython
import numpy
cimport numpy
from numpy import ndarray

cdef extern from "Python.h":
	ctypedef unsigned long size_t
	object PyBuffer_FromMemory( void *ptr, int size)
	object PyBuffer_FromReadWriteMemory( void *ptr, int size)
	object PyString_FromStringAndSize(char *s, int len)
	void* PyMem_Malloc( size_t n)
	void PyMem_Free( void *p)

cdef extern from "numpy/arrayobject.h":
	void *PyArray_DATA(numpy.ndarray arr)

cdef extern from 'stdlib.h':
	void memcpy(void * dst, void * src, unsigned int len)
	void free(void * ptr)

def memory_addr_of_numpy_array(ar):
	cdef %POINTERTYPE% ptr=<%POINTERTYPE%>PyArray_DATA(ar)
	return ptr

import ctypes

cdef %POINTERTYPE% _str_addr(object w):
	return ctypes.cast(ctypes.pointer(ctypes.c_char_p(w)),ctypes.POINTER(ctypes.c_ulong)).contents.value

def str_addr(w):
	return _str_addr(w)

import zopencv_lowlevel
import zopencv_highlevel
import zopencv_classes
cimport zopencv_lowlevel
cimport zopencv_highlevel
cimport zopencv_classes
import sys

def NumPy2IplFast(input,copy=False):
	mode_list = {
		numpy.dtype(numpy.uint8) : int( ctypes.c_int(IPL_DEPTH_8U).value),
		numpy.dtype(numpy.uint16) :int( ctypes.c_int(IPL_DEPTH_16U).value),
		numpy.dtype(numpy.int8) : int( ctypes.c_int(IPL_DEPTH_8S).value),
		numpy.dtype(numpy.int16) : int( ctypes.c_int(IPL_DEPTH_16S).value),
		numpy.dtype(numpy.int32) : int( ctypes.c_int(IPL_DEPTH_32S).value),
		numpy.dtype(numpy.float32) : int( ctypes.c_int(IPL_DEPTH_32F).value),
		numpy.dtype(numpy.float64) : int( ctypes.c_int(IPL_DEPTH_64F).value),
	}
	if not mode_list.has_key(input.dtype):
		raise ValueError, 'unknown or unsupported input mode'
	d=1
	try:
		d=input.shape[2]
	except:
		pass
	mode=mode_list[input.dtype]
	sz=zopencv_lowlevel._raw_cvSize(input.shape[1], <int><unsigned int>input.shape[0])
	if copy:
		result= zopencv_lowlevel._raw_cvCreateImage(sz,mode,d)
		print "copying data from %d to %d len =%d  "%d(<%POINTERTYPE%>PyArray_DATA(input),result.imageData,input.shape[0]*input.shape[1]*d*input.dtype.type().nbytes)
		memcpy(<void *>result.imageData,<void *><%POINTERTYPE%>(PyArray_DATA(input)),input.shape[0]*input.shape[1]*d*input.dtype.type().nbytes)
		return result
	else:
		result = zopencv_lowlevel._raw_cvCreateImageHeader(sz,  mode, d)
		result.imageData=<%POINTERTYPE%>(PyArray_DATA(input))
		result.imageDataOrigin=result.imageData
		return result



def NumPy2CvMatFast(input):
	mode_list = {
		numpy.dtype(numpy.uint8) : int( ctypes.c_int(CV_8U).value),
		numpy.dtype(numpy.uint16) : int( ctypes.c_int(CV_16U).value),
		numpy.dtype(numpy.int8) : int( ctypes.c_int(CV_8S).value),
		numpy.dtype(numpy.int16) : int( ctypes.c_int(CV_16S).value),
		numpy.dtype(numpy.int32) : int( ctypes.c_int(CV_32S).value),
		numpy.dtype(numpy.float32) : int( ctypes.c_int(CV_32F).value),
		numpy.dtype(numpy.float64) : int( ctypes.c_int(CV_64F).value),
	}
	s=input.shape
	assert(input.ndim==2)
	ns=numpy.array(list(s),dtype=numpy.uint32)
	mh=zopencv_classes.CvMat()
	mh.initMatHeader(ns[0],ns[1],mode_list[input.dtype],<%POINTERTYPE%>PyArray_DATA(input),CV_AUTOSTEP)
	return mh


def NumPy2CvMatNDFast(input):
	mode_list = {
		numpy.dtype(numpy.uint8) : int( ctypes.c_int(CV_8U).value),
		numpy.dtype(numpy.uint16) : int( ctypes.c_int(CV_16U).value),
		numpy.dtype(numpy.int8) : int( ctypes.c_int(CV_8S).value),
		numpy.dtype(numpy.int16) : int( ctypes.c_int(CV_16S).value),
		numpy.dtype(numpy.int32) : int( ctypes.c_int(CV_32S).value),
		numpy.dtype(numpy.float32) : int( ctypes.c_int(CV_32F).value),
		numpy.dtype(numpy.float64) : int( ctypes.c_int(CV_64F).value),
	}
	s=input.shape
	ns=numpy.array(list(s),dtype=numpy.uint32)
	mh=zopencv_classes.CvMat()
	mh.InitMatHeader(input.ndim,<%POINTERTYPE%>PyArray_DATA(ns),mode_list[input.dtype])
	zopencv_lowlevel._raw_cvSetData(mh,<%POINTERTYPE%>PyArray_DATA(input),CV_AUTOSTEP)
	return mh


def Ipl2NumPyFast(input_img):
	"""Converts an OpenCV/IPL image to Numpy"""
	input_ptr=input_img.get_pointer()
	mode_list = {
		int( ctypes.c_int(IPL_DEPTH_8U).value): numpy.uint8 ,
		int( ctypes.c_int(IPL_DEPTH_16U).value):numpy.uint16,
		int( ctypes.c_int(IPL_DEPTH_8S).value):numpy.int8,
		int( ctypes.c_int(IPL_DEPTH_16S).value):numpy.int16 ,
		int( ctypes.c_int(IPL_DEPTH_32S).value):numpy.int32 ,
		int( ctypes.c_int(IPL_DEPTH_32F).value):numpy.float32 ,
		int( ctypes.c_int(IPL_DEPTH_64F).value):numpy.float64
	}
	if input_img.origin == 0:
		orientation = 1 # top left
	elif input_img.origin == 1:
		orientation = -1 # bottom left
	else:
		raise ValueError, 'origin must be 0 or 1!'
	if input_img.dataOrder == 0:
		bufp=input_img.imageData
		print "data order 0",bufp
		dtype=mode_list[input_img.depth]
		strides=(input_img.widthStep*dtype().nbytes,dtype().nbytes*input_img.nChannels,dtype().nbytes)
		print "strides : ",strides
		assert(orientation!=-1)
		shape=(input_img.height,input_img.width, input_img.nChannels)
		buffer=PyBuffer_FromReadWriteMemory(<void *><unsigned long long int> bufp,input_img.widthStep*input_img.height*dtype().nbytes )
		ar=numpy.ndarray(dtype=dtype,shape=shape,buffer=buffer,strides=strides)#.copy('C') # data
		return ar#[:,:,::-1]
	else:
		print "data order 1",input_img.imageData
		dtype=mode_list[input.depth]
		shape=( input_img.nChannels,input_img.height,input_img.width)
		#strides=(input_img.width*input_img.nChannels,input_img.nChannels,1)
		strides=(input_img.widthStep*input_img.height,dtype().nbytes*input_img.widthStep,dtype().nbytes)
		print "strides : ",strides
		assert(orientation!=-1)
		buffer=PyBuffer_FromReadWriteMemory( <void *>(input_img.imageData),input_img.widthStep*input_img.height*dtype().nbytes )
		ar=numpy.ndarray(dtype=dtype,shape=shape,buffer=buffer,strides=strides)#.copy('C') # data
		return ar


def CvMat2NumPyFast(input_img):
	"""Converts an OpenCV matrix to Numpy"""
	input_ptr=input_img.get_pointer()
	mode_list = {
		int( ctypes.c_int(CV_8U).value): numpy.uint8 ,
		int( ctypes.c_int(CV_16U).value):numpy.uint16,
		int( ctypes.c_int(CV_8S).value):numpy.int8,
		int( ctypes.c_int(CV_16S).value):numpy.int16 ,
		int( ctypes.c_int(CV_32S).value):numpy.int32 ,
		int( ctypes.c_int(CV_32F).value):numpy.float32 ,
		int( ctypes.c_int(CV_64F).value):numpy.float64
	}
	dtype=mode_list[input_img.depth]
	shape=(input_img.height,input_img.width, input_img.nChannels)
	buffer=PyBuffer_FromReadWriteMemory( <void *>input_img.imageData,input_img.width*input_img.height*dtype().nbytes*input_img.nChannels )
	ar=numpy.ndarray(dtype=dtype,shape=shape,buffer=buffer) # data
	return ar





cdef int zopencvErrorHandler(int code, char * func_name, char * err_msg, char * file , int line, void * p):
	sys.stderr.write("opencv error code "+str(code)+"\n")
	sys.stderr.write("raised at "+str(func_name)+":"+str(line)+"\n")
	sys.stderr.write("with msg "+str(err_msg)+"\n")
	zopencv_highlevel.cvSetErrStatus( 0 );
	#sys.stderr.write(cvErrorStr(code))
	sys.stderr.write("trying to continue\n")
	raise Exception, "OpenCV Error"
	return 0


def CV_FOURCC(a,b,c,d):
	return ord(a)<<24+ord(b)<<16+ord(c)<<8+ord(d)


cimport declarations

declarations.cvRedirectError(<declarations.CvErrorCallback><void *>&zopencvErrorHandler,<void*>0,<void **>0)
