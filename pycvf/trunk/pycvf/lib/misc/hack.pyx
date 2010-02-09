import numpy
from numpy import ndarray
import ctypes
cimport numpy

cdef extern from "Python.h":
    ctypedef unsigned long size_t
    object PyBuffer_FromMemory( void *ptr, int size)
    object PyBuffer_FromReadWriteMemory( void *ptr, int size)
    object PyString_FromStringAndSize(char *s, int len)
    void* PyMem_Malloc( size_t n)
    void PyMem_Free( void *p)

cdef extern from "numpy/arrayobject.h":
    void *PyArray_DATA(numpy.ndarray arr)

def rwbuffer_at(pos,len):
    cdef unsigned long ptr=int(pos)
    return PyBuffer_FromReadWriteMemory(<void *>ptr,len)

def numpyarr_at(pos,len,shape,dtype):
    return numpy.ndarray(shape=shape,dtype=dtype,buffer=rwbuffer_at(pos,len))



def memory_addr_of_numpy_array(ar):
    #if (ctypes.sizeof(ctypes.c_void_p)==8):
    cdef unsigned long ptr=<unsigned long>PyArray_DATA(ar)
    return ptr

def memory_addr_of_numpy_array_ptr(ar,dtype=ctypes.c_ubyte):
    cdef unsigned long ptr=<unsigned long>PyArray_DATA(ar)
    return ctypes.cast(ptr,(ctypes.POINTER(dtype)))

def get_pointer_as_ulong(ptr):
    return ctypes.cast(ctypes.pointer(ptr),ctypes.POINTER(ctypes.c_ulong)).contents.value

def set_pointer_via_ulong(ptr,val):
    ctypes.cast(ctypes.pointer(ptr),ctypes.POINTER(ctypes.c_ulong)).contents.value=val

def get_pointer_as_ulonglong(ptr):
    return ctypes.cast(ctypes.pointer(ptr),ctypes.POINTER(ctypes.c_ulonglong)).contents.value

def set_pointer_via_ulonglong(ptr,val):
    ctypes.cast(ctypes.pointer(ptr),ctypes.POINTER(ctypes.c_ulonglong)).contents.value=val


## we should add check for robustness we don't know anything about python sting it may be safe
## to check that the endpointer correspond to the end character

def pointer_of_pythonstring(w):
    return ctypes.cast(ctypes.pointer(ctypes.c_char_p(w)),ctypes.POINTER(ctypes.c_long)).contents.value

def rwstring(w):
    return rwbuffer_at(ctypes.cast(ctypes.pointer(ctypes.c_char_p(w)),ctypes.POINTER(ctypes.c_long)).contents.value,len(w))




cdef class subrwbuffer:
    cdef object buf
    cdef int off
    cdef int sz
    def __init__(self,buf,int off, int sz):
        self.buf=buf
        self.off=off
        self.sz=sz
    def __getitem__(self,int n):
        if (n<0): n+=self.sz
        assert(n<self.sz)
        return self.buf[self.off+n]
    def __setitem__(self,int n,v):
        if (n<0): n+=self.sz
        assert(n<self.sz)
        self.buf[self.off+n]=v
        #return v
    def __getslice__(self,int n,int e):
        if (n<0): n+=self.sz
        if (e<0): e+=self.sz
        if (e>self.sz): e=self.sz
        assert(0<=n<self.sz)
        assert(0<=e<=self.sz)
        return self.buf[(self.off+n):(self.off+e)]
    def __setslice__(self,int n,int e,v):
        if (n<0): n+=self.sz
        if (e<0): e+=self.sz
        if (e>self.sz): e=self.sz
        assert(0<=n<self.sz)
        assert(0<=e<=self.sz)
        self.buf[(self.off+n):(self.off+e)]=v
        #return v
    def __len__(self):
        return self.sz


def strtouint32(x):
    return (ctypes.cast(ctypes.c_char_p(x),ctypes.POINTER(ctypes.c_uint32))).contents.value

def uint32tostr(x):
    return ctypes.string_at(ctypes.pointer(ctypes.c_uint32(x)),4)

def strtouint64(x):
    return (ctypes.cast(ctypes.c_char_p(x),ctypes.POINTER(ctypes.c_uint64))).contents.value

def uint64tostr(x):
    return ctypes.string_at(ctypes.pointer(ctypes.c_uint64(x)),8)

