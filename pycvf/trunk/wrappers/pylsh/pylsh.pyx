"""
// Python Wrapper by Bertrand NOUVEL (CNRS-JFLI) 2009
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions
// are met:
//
// 1. The source code and derived binary forms may be used only for
//    non-commercial, non-profit research purposes.
//
// 2. Redistributions of source code must retain the above copyright
//    notice, these conditions, and the following disclaimer.
//
// 3. Redistributions in binary form must reproduce the above copyright
//    notice, these conditions, and the following disclaimer in the
//    documentation and/or other materials provided with the distribution.
//
// 4. The names of its contributors may not be used to endorse or promote
//    products derived from this software without specific prior written
//    permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
// OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
// EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
// PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
// PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
// LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
// NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
// SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//

"""

import numpy as np
cimport numpy

cdef extern from "stdlib.h":
  void *calloc (size_t __nmemb, size_t __size)
  void free (void *__ptr) 

cdef extern from "numpy/arrayobject.h":
    void *PyArray_DATA(numpy.ndarray arr)


cdef extern from "pylshbase.h":
  ctypedef struct PyMPLSHIdx:
    int load_index(char* index_file)
    int save_index(char * index_file)  
    void build_index()
    void query(float * queryv,int Q,int w, int *res_keys,double
*res_dists, int * k, int do_recall)
  PyMPLSHIdx * new_PyMPLSHIdx "new PyMPLSHIdx" (int m, int n, float * data)
  void del_PyMPLSHIdx "delete" (PyMPLSHIdx * s)



cdef class MPLSHIndex(object):
  cdef PyMPLSHIdx * lshidx
  cdef object ar
  def __init__(int self, numpy.ndarray[numpy.float32_t,ndim=2] ar):
     self.ar=ar
     self.lshidx=new_PyMPLSHIdx(ar.shape[0],ar.shape[1],<float *>PyArray_DATA(ar))
  
  def __del__(self):
    del_PyMPLSHIdx(self.lshidx)
  
  def build(self):
     self.lshidx.build_index()

  def query(self,numpy.ndarray[numpy.float32_t,ndim=2] qar, int
k=5,recall=False):
     res_keys=np.zeros(shape=(qar.shape[0],k),dtype=np.uint32)
     res_dists=np.zeros(shape=(qar.shape[0],k),dtype=np.float64)
     cnt=np.zeros(shape=(qar.shape[0],),dtype=np.uint32)
     self.lshidx.query(<float *>PyArray_DATA(qar),
                       qar.shape[0],
		       k,
		       <int *>PyArray_DATA(res_keys),
		       <double *>PyArray_DATA(res_dists),
		       <int *>PyArray_DATA(cnt),
		       recall)
     return res_keys,res_dists,cnt

  def load(self,filename):
    if (not self.lshidx.load_index(filename)):
      raise IOError, "unable load lsh index"
  
  def save(self,filename):
    if (not self.lshidx.save_index(filename)):
      raise IOError, "unable to save lsh index"
