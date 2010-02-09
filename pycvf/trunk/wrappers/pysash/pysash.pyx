"""
// Implementation of the SASH index for approximate similarity search,
// as described in 
//   Michael E. Houle (author),
//   "SASH: a Spatial Approximation Sample Hierarchy for Similarity Search",
//   IBM Tokyo Research Laboratory Technical Report RT-0517, 5 March 2003.
// and
//   Michael E. Houle and Jun Sakuma (authors),
//   "Fast Approximate Search in Extremely High-Dimensional Data Sets",
//   in Proc. 21st International Conference on Data Engineering (ICDE 2005),
//   Tokyo, Japan, April 2005, pp. 619-630.
//
// Copyright (C) 2004-2006 Michael E. Houle,
// All rights reserved.
//
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
// Comments, bug fixes, etc welcome!
// Contact e-mail address: meh@nii.ac.jp, meh@acm.org
"""

import numpy
cimport numpy

cdef extern from "stdlib.h":
  void *calloc (size_t __nmemb, size_t __size)
  void free (void *__ptr) 

cdef extern from "numpy/arrayobject.h":
    void *PyArray_DATA(numpy.ndarray arr)


cdef extern from "DistData.h":
  ctypedef struct DistData:
     pass

cdef extern from "DenseVecData.h":
  ctypedef struct c_DenseVecData "DenseVecData":
     float * value
     int length
     float distanceTo (c_DenseVecData* vec)
     int getLength ()
  c_DenseVecData * new_DenseVecData "new DenseVecData" (float * l, int len)
  void del_DenseVecData "delete" (c_DenseVecData * s)





cdef extern from "Sash.h":
  ctypedef struct c_Sash "Sash":
    int build (DistData** inputData, int numItems)
    int build_with_numParents "build" (DistData** inputData, int numItems, int numParents)
    int build_with_filename "build" (char* fileName, DistData** inputData, int numItems)
    int findAllInRange (DistData* query, float limit)
    int findAllInRange_with_sampleRate "findAllInRange" (DistData* query, float limit, int sampleRate)
    int findMostInRange (DistData* query, float limit)
    int findMostInRange_with_sampleRate "findMostInRange" (DistData* query, float limit, int sampleRate)
    int findMostInRange_with_scaleFactor "findMostInRange" (DistData* query, float limit, float scaleFactor)
    int findMostInRange_full "findMostInRange"  (DistData* query, float limit, int sampleRate, float scaleFactor)
    int findNear (DistData* query, int howMany)
    int findNear_with_sampleRate "findNear" (DistData* query, int howMany, int sampleRate)
    int findNear_with_scaleFactor "findNear" (DistData* query, int howMany, float scaleFactor)
    int findNear_full "findNear" (DistData* query, int howMany, int sampleRate, float scaleFactor)
    int findNearest (DistData* query, int howMany)
    int findNearest_full "findNearest"  (DistData* query, int howMany, int sampleRate)
    DistData** getData ()
    int getExternToInternMapping (int* result, int capacity)
    int getInternToExternMapping (int* result, int capacity)
    int getMaxParents ()
    int getNumItems ()
    int getNumLevels ()
    int getNumOrphans ()
    float getResultAcc (float* exactDistList, int howMany)
    int getResultDists (float* result, int capacity)
    unsigned long getResultDistComps ()
    int getResultIndices (int* result, int capacity)
    int getResultNumFound ()
    int getResultSampleSize ()
    unsigned long getRNGSeed ()
    int getSampleAssignment (int* result, int capacity)
    int getSampleSizes (int* result, int capacity)
    void resetQuery ()
    int saveToFile (char* fileName)
    void setVerbosity (int verbosity)
  c_Sash * new_Sash "new Sash" ()
  c_Sash * new_Sash_with_seed "new Sash" (long unsigned int seed)
  void del_Sash "delete" (c_Sash * s)




###
### Dense Datas
###

cdef class SashInputVec(object):
  cdef DistData * data
  def __init__(self,arr):
    cdef float * arrptr
    cdef unsigned long lrow
    assert(arr.dtype==numpy.float32)
    assert(arr.ndim==1)
    lrow=arr.shape[0]
    arrptr=<float *>PyArray_DATA(arr)
    self.data=<DistData *>new_DenseVecData(arrptr,lrow)
  def __del__(self,arr):
    del_DenseVecData(<c_DenseVecData *>self.data)


cdef class SashInputArray(object):
  cdef DistData ** data
  cdef int numItems
  def __init__(self,arr):
    cdef float * arrptr
    cdef unsigned long lrow
    assert(arr.dtype==numpy.float32)
    assert(arr.ndim==2)
    self.numItems=arr.shape[0]
    self.data=<DistData**>calloc(self.numItems,sizeof(c_DenseVecData *))
    lrow=arr.shape[1]
    arrptr=<float *>PyArray_DATA(arr)
    for i in range(self.numItems):
      self.data[i]=<DistData *>new_DenseVecData(arrptr,lrow)
      arrptr=arrptr+lrow 
  def __del__(self,arr):
    for i in range(self.numItems):
      del_DenseVecData(<c_DenseVecData *>self.data[i])
    free(self.data)
    
    
###
### Python Datas
###


ctypedef float (*distance_f )(void * a, void *b,void *f)

cdef extern from "PythonVecData.h":
  ctypedef struct c_PythonVecData "PythonVecData":
     float distanceTo (c_PythonVecData* vec)
     int getLength ()
  c_PythonVecData * new_PythonVecData "new PythonVecData"  (void * val, float (*callback_distance)(void * a, void * b,void *f) , void * pcb)
  void del_PythonVecData "delete" (c_PythonVecData * s)

#cdef extern from "cheesefinder.h":
#  ctypedef void (*cheesefunc)(char *name, void *user_data)
#  void find_cheeses(cheesefunc user_func, void *user_data)
	
#def find(f):
#  find_cheeses(callback, <void*>f)
	        
#cdef void callback(char *name, void *f):
#  (<object>f)(name)	    

cdef class WContainer:#(object):
  cdef object value
  def __init__(self,value):
    self.value=value
  def __repr__(self):
    return str(self.value)
  def __str__(self):
    return str(self.value)    


cdef float generic_distance_callback(void * a,void * b, void * dist):
      return (<object>dist)((<WContainer>a).value,(<WContainer> b).value)


cdef class SashInputVecPython(object):
  cdef DistData * data
  cdef object container_obj
  def __init__(self,obj,dist):
    self.container_obj=WContainer(obj)
    self.data=<DistData *>new_PythonVecData(<void *> self.container_obj,generic_distance_callback,<void*> dist)  
  def __del__(self,arr):
    del_PythonVecData(<c_PythonVecData *>self.data)


cdef class SashInputArrayPython(object):
  cdef DistData ** data
  cdef int numItems  
  cdef object container_objlist
  def __init__(self,arr,dist):
    self.numItems=len(arr)
    self.container_objlist=[]
    self.data=<DistData**>calloc(self.numItems,sizeof(c_PythonVecData *))
    for i in range(self.numItems):
      wc=WContainer(arr[i])
      self.container_objlist.append(wc)
      self.data[i]=<DistData *>new_PythonVecData(<void *>wc,generic_distance_callback,<void*> dist)
  def __del__(self,arr):
    for i in range(self.numItems):
      del_PythonVecData(<c_PythonVecData *>self.data[i])
    free(self.data)
    
cdef class Sash(object):
  cdef c_Sash * sashinstance
  def __init__(int self,seed=0):
    """
     Constructor with optional seed for random number generator initialization.
    """
    if (not seed):
      self.sashinstance=new_Sash()
    else:
      self.sashinstance=new_Sash_with_seed(seed)
  def __del__(self):
    del_Sash(self.sashinstance)  
  def _build(self,SashInputArray arr,filename=None,numParents=None):
    if (filename):
      self.sashinstance.build_with_filename(filename,arr.data, arr.numItems)
    else:
       if (numParents):
         self.sashinstance.build_with_numParents(arr.data, arr.numItems,numParents)
       else:
         self.sashinstance.build(arr.data, arr.numItems)
  
  def build(self,arr,*args,**xargs):
    """
     Constructs or load a new sash from a file.
     When no numParents is specified  the default is assumed to be 4.
    """
    return self._build(SashInputArray(arr),*args,**xargs)
  
  def _findAllInBall(self,SashInputVec query,float radius=10,int sampleRate=-1):
     if (sampleRate==-1):
       return self.sashinstance.findAllInRange(query.data, radius)
     else:
       return self.sashinstance.findAllInRange_with_sampleRate(query.data,radius,sampleRate)
  
  def findAllInBall(self,query, *args, **xargs):
    return self._findAllInBall(SashInputVec(query), *args, **xargs )
  
  def _findMostInBall(self,SashInputVec query,float radius=10,int sampleRate=-1,int scaleFactor=-1):
     if (scaleFactor==-1):
       if (sampleRate==-1):
         return self.sashinstance.findMostInRange(query.data, radius)
       else:
         return self.sashinstance.findMostInRange_with_sampleRate(query.data,radius,sampleRate)
     else:
       if (sampleRate==-1):
         return self.sashinstance.findMostInRange_with_scaleFactor(query.data,  radius, scaleFactor)
       else:
         return self.sashinstance.findMostInRange_full(query.data,radius,sampleRate, scaleFactor)

  def findMostInBall(self,query, *args, **xargs):
    """
    * Perform an approximate range query for the specified item.
    * The upper limit on the query-to-item distance must be supplied (radius).
    * The number of elements actually found is returned.
    * The search may be relative to a data sample of size N / 2^r,
    *   where N is the number of items in the set, and r is 
    *   a non-negative integer ("sampleRate").
    * A "sampleRate" of zero indicates a search relative to the entire set.
    * The method may also makes use of a parameter ("scaleFactor")
    *   that influences the trade-off between time and accuracy.
    * The default value of this parameter is 1.0 - increasing the value
    *   will increase running time (roughly proportionally) and increase
    *   the accuracy of the result.
    """
    return self._findMostInBall(SashInputVec(query), *args, **xargs )

  def _findNearest(self, SashInputVec query, int limit=10, int sampleRate=-1):
     if (sampleRate==-1):
       return self.sashinstance.findNearest(query.data , limit)
     else:
       return self.sashinstance.findNearest_full(query.data,limit,sampleRate)
  
  def findNearest(self,query, *args, **xargs):
    return self._findNearest(SashInputVec(query), *args, **xargs )
  
  def _findNear(self,SashInputVec query,int limit=10,int sampleRate=-1,int scaleFactor=-1):
     if (scaleFactor==-1):
       if (sampleRate==-1):
         return self.sashinstance.findNear(query.data,  limit)
       else:
         return self.sashinstance.findNear_with_sampleRate(query.data,limit,sampleRate)
     else:
       if (sampleRate==-1):
         return self.sashinstance.findNear_with_scaleFactor(query.data,  limit, scaleFactor)
       else:
         return self.sashinstance.findNear_full(query.data,limit,sampleRate, scaleFactor)
  
  def findNear(self,query, *args, **xargs):
    """ Find a set of approximate nearest neighbours for the specified
        query item.
        The number of elements actually found is returned.
       A "sampleRate" of zero indicates a search relative to the entire set.
        The method also may  use a parameter ("scaleFactor")
          that influences the trade-off between time and accuracy.
        The default value of this parameter is 1.0 - increasing the value
          will increase running time (roughly proportionally) and increase
          the accuracy of the result.
    """
    return self._findNear(SashInputVec(query), *args, **xargs )
  
  def getMaxParents (self):
    """ Returns the upper limit on the number of parents per SASH node."""
    return self.sashinstance.getMaxParents()
  
  def getNumItems (self):
    """  Returns the number of data items of the SASH. """
    return self.sashinstance.getNumItems()
  
  def getNumLevels (self):
    """  Returns the number of levels of the SASH. """
    return self.sashinstance.getNumLevels()
  
  def getNumOrphans (self):
    """Returns the number of orphan nodes encountered during SASH construction. """
    return self.sashinstance.getNumOrphans()
  
  def getResultAcc (self,int howMany=1):
    """
    Computes the recall accuracy of the most recent query result.
    A list of the exact distances must be provided, sorted
      from smallest to largest.
    The number of exact distances provided determines the size
      of the neighbourhood within which the accuracy is assessed.
    The list must contain at least as many entries as the number of
      items found in the query result.
    If unsuccessful, a negative value is returned.
    """
    r=numpy.ndarray(shape=(howMany,),dtype=numpy.float32)
    rf=self.sashinstance.getResultAcc (<float *> PyArray_DATA(r), howMany)
    return r,rf
  
  def getResultDists (self,int maxresults=-1):
    """
      returns q list filled with the query-to-neighbour
      distances found in the most recent SASH query.
      If successful, the number of items found is returned.
      If unsuccessful, zero is returned.
    """
    if maxresults==-1:
      maxresults=self.getResultNumFound()
      if (maxresults==0):
         return []
    r=numpy.ndarray(shape=(maxresults,),dtype=numpy.float32)
    ri=self.sashinstance.getResultDists (<float *> PyArray_DATA(r), maxresults)
    return r[:ri]
  
  def getResultDistComps(self):
    """
     Returns the number of distance computations performed during
       the most recent SASH operation.
    """
    return self.sashinstance.getResultDistComps ()
  
  def getResultIndices(self, int maxresults=-1):
    """
       returns a list with the (external) indices of the
       items found in the most recent SASH query.
       If successful, the number of items found is returned.
       If unsuccessful, zero is returned.
    """
    if maxresults==-1:
     maxresults=self.getResultNumFound()
     if (maxresults==0):
        return []
    r=numpy.ndarray(shape=(maxresults,),dtype=numpy.uint32)
    ri=self.sashinstance.getResultIndices (<int *> PyArray_DATA(r), maxresults)
    return r[:ri]
  
  def getResultNumFound(self):
    """
     Returns the number of items found in the most recent query.
    """
    return self.sashinstance.getResultNumFound ()
  
  def getResultSampleSize (self):
    """
    Returns the sample size used in the most recent query.
    """
    return self.sashinstance.getResultSampleSize()
  
  def getRNGSeed(self):
    """
     Returns the seed value used for random number generator initialization.
    """
    return self.sashinstance.getRNGSeed ()
  
  def resetQuery(self):
     """
       Resets the current query object to NULL.
       This has the effect of clearing any saved distances - subsequent
       findNear and findNearest operations would be forced to compute
       all needed distances from scratch.
     """
     self.sashinstance.resetQuery ()
  
  def save(self,filename):
    """
     Save the SASH to the specified file.
     The extension ".sash" is automatically appended to the file name.
     If successful, the number of SASH items is returned.
     If unsuccessful, zero is returned.
    """
    if (not self.sashinstance.saveToFile(filename)):
      raise IOError, "unable to save sash"



####
####
#####

cdef class GenericSash(Sash):
  cdef object distance
  cdef object persistent_data
  def get_persistent_data(self):
    return self.persistent_data
  def __init__(self,distance,seed=0):
    """
     Constructor with optional seed for random number generator initialization.
    """
    if (not seed):
      self.sashinstance=new_Sash()
    else:
      self.sashinstance=new_Sash_with_seed(seed)
    self.distance=distance
    self.persistent_data=None
  def _build(self,SashInputArrayPython arr,filename=None,numParents=None):
    if (filename):
      self.sashinstance.build_with_filename(filename,arr.data, arr.numItems)
    else:
       if (numParents):
         self.sashinstance.build_with_numParents(arr.data, arr.numItems,numParents)
       else:
         self.sashinstance.build(arr.data, arr.numItems)
  
  def build(self,arr,*args,**xargs):
    """
     Constructs or load a new sash from a file.
     When no numParents is specified  the default is assumed to be 4.
    """
    self.persistent_data=SashInputArrayPython(arr,self.distance)
    return self._build(self.persistent_data,*args,**xargs)    
  
  def _findAllInBall(self,SashInputVecPython query,float radius=10,int sampleRate=-1):
     if (sampleRate==-1):
       return self.sashinstance.findAllInRange(query.data, radius)
     else:
       return self.sashinstance.findAllInRange_with_sampleRate(query.data,radius,sampleRate)
  
  def findAllInBall(self,query, *args, **xargs):
    return self._findAllInBall(SashInputVecPython(query,self.distance), *args, **xargs )
  
  def _findMostInBall(self,SashInputVecPython query,float radius=10,int sampleRate=-1,int scaleFactor=-1):
     if (scaleFactor==-1):
       if (sampleRate==-1):
         return self.sashinstance.findMostInRange(query.data, radius)
       else:
         return self.sashinstance.findMostInRange_with_sampleRate(query.data,radius,sampleRate)
     else:
       if (sampleRate==-1):
         return self.sashinstance.findMostInRange_with_scaleFactor(query.data,  radius, scaleFactor)
       else:
         return self.sashinstance.findMostInRange_full(query.data,radius,sampleRate, scaleFactor)

  def findMostInBall(self,query, *args, **xargs):
    """
    * Perform an approximate range query for the specified item.
    * The upper limit on the query-to-item distance must be supplied (radius).
    * The number of elements actually found is returned.
    * The search may be relative to a data sample of size N / 2^r,
    *   where N is the number of items in the set, and r is 
    *   a non-negative integer ("sampleRate").
    * A "sampleRate" of zero indicates a search relative to the entire set.
    * The method may also makes use of a parameter ("scaleFactor")
    *   that influences the trade-off between time and accuracy.
    * The default value of this parameter is 1.0 - increasing the value
    *   will increase running time (roughly proportionally) and increase
    *   the accuracy of the result.
    """
    return self._findMostInBall(SashInputVecPython(query,self.distance), *args, **xargs )

  def _findNearest(self, SashInputVecPython query, int limit=10, int sampleRate=-1):
     if (sampleRate==-1):
       return self.sashinstance.findNearest(query.data , limit)
     else:
       return self.sashinstance.findNearest_full(query.data,limit,sampleRate)
  
  def findNearest(self,query, *args, **xargs):
    return self._findNearest(SashInputVecPython(query,self.distance), *args, **xargs )
  
  def _findNear(self,SashInputVecPython query,int limit=10,int sampleRate=-1,int scaleFactor=-1):
     if (scaleFactor==-1):
       if (sampleRate==-1):
         return self.sashinstance.findNear(query.data,  limit)
       else:
         return self.sashinstance.findNear_with_sampleRate(query.data,limit,sampleRate)
     else:
       if (sampleRate==-1):
         return self.sashinstance.findNear_with_scaleFactor(query.data,  limit, scaleFactor)
       else:
         return self.sashinstance.findNear_full(query.data,limit,sampleRate, scaleFactor)
  
  def findNear(self,query, *args, **xargs):
    """ Find a set of approximate nearest neighbours for the specified
        query item.
        The number of elements actually found is returned.
       A "sampleRate" of zero indicates a search relative to the entire set.
        The method also may  use a parameter ("scaleFactor")
          that influences the trade-off between time and accuracy.
        The default value of this parameter is 1.0 - increasing the value
          will increase running time (roughly proportionally) and increase
          the accuracy of the result.
    """
    return self._findNear(SashInputVecPython(query,self.distance), *args, **xargs )
  
  def getMaxParents (self):
    """ Returns the upper limit on the number of parents per SASH node."""
    return self.sashinstance.getMaxParents()
  
  def getNumItems (self):
    """  Returns the number of data items of the SASH. """
    return self.sashinstance.getNumItems()
  
  def getNumLevels (self):
    """  Returns the number of levels of the SASH. """
    return self.sashinstance.getNumLevels()
  
  def getNumOrphans (self):
    """Returns the number of orphan nodes encountered during SASH construction. """
    return self.sashinstance.getNumOrphans()
  
  def getResultAcc (self,int howMany=1):
    """
    Computes the recall accuracy of the most recent query result.
    A list of the exact distances must be provided, sorted
      from smallest to largest.
    The number of exact distances provided determines the size
      of the neighbourhood within which the accuracy is assessed.
    The list must contain at least as many entries as the number of
      items found in the query result.
    If unsuccessful, a negative value is returned.
    """
    r=numpy.ndarray(shape=(howMany,),dtype=numpy.float32)
    rf=self.sashinstance.getResultAcc (<float *> PyArray_DATA(r), howMany)
    return r,rf
  
  def getResultDists (self,int maxresults=-1):
    """
      returns q list filled with the query-to-neighbour
      distances found in the most recent SASH query.
      If successful, the number of items found is returned.
      If unsuccessful, zero is returned.
    """
    if maxresults==-1:
      maxresults=self.getResultNumFound()
      if (maxresults==0):
         return []
    r=numpy.ndarray(shape=(maxresults,),dtype=numpy.float32)
    ri=self.sashinstance.getResultDists (<float *> PyArray_DATA(r), maxresults)
    return r[:ri]
  
  def getResultDistComps(self):
    """
     Returns the number of distance computations performed during
       the most recent SASH operation.
    """
    return self.sashinstance.getResultDistComps ()
  
  def getResultIndices(self, int maxresults=-1):
    """
       returns a list with the (external) indices of the
       items found in the most recent SASH query.
       If successful, the number of items found is returned.
       If unsuccessful, zero is returned.
    """
    if maxresults==-1:
     maxresults=self.getResultNumFound()
     if (maxresults==0):
        return []
    r=numpy.ndarray(shape=(maxresults,),dtype=numpy.uint32)
    ri=self.sashinstance.getResultIndices (<int *> PyArray_DATA(r), maxresults)
    return r[:ri]
  
  def getResultNumFound(self):
    """
     Returns the number of items found in the most recent query.
    """
    return self.sashinstance.getResultNumFound ()
  
  def getResultSampleSize (self):
    """
    Returns the sample size used in the most recent query.
    """
    return self.sashinstance.getResultSampleSize()
  
  def getRNGSeed(self):
    """
     Returns the seed value used for random number generator initialization.
    """
    return self.sashinstance.getRNGSeed ()
  
  def resetQuery(self):
     """
       Resets the current query object to NULL.
       This has the effect of clearing any saved distances - subsequent
       findNear and findNearest operations would be forced to compute
       all needed distances from scratch.
     """
     self.sashinstance.resetQuery ()
  
  def save(self,filename):
    """
     Save the SASH to the specified file.
     The extension ".sash" is automatically appended to the file name.
     If successful, the number of SASH items is returned.
     If unsuccessful, zero is returned.
    """
    if (not self.sashinstance.saveToFile(filename)):
      raise IOError, "unable to save sash"
