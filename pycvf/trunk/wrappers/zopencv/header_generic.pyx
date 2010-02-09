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


cimport declarations
import sys

