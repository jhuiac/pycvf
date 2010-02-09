import numpy as np
cimport numpy as np
cimport cython

U8TYPE = np.uint8
ctypedef np.uint8_t U8TYPE_t

@cython.boundscheck(False)
def rgb2bgr(np.ndarray[U8TYPE_t, ndim=3] x):
    cdef int h
    cdef int w
    cdef int c
    cdef int i
    cdef char t
    (h,w,c)=np.shape(x)
    assert(c==3)
    for i in range(w*h):
        t=x.data[i*3+2]
        x.data[i*3+2]=x.data[i*3]
        x.data[i*3]=t
        