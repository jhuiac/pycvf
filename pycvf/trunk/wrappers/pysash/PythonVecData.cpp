/**
 * PythonVecData.cpp: Container class and distance measures
 *                   for dense vector data.
 * 
 * Author:           Michael Houle
 * Date:             4 December 2006
 * Version:          1.0
 */

#include "PythonVecData.h"

////////////////////////////////////////////////////////////////////////
//                            PythonVecData                            //
////////////////////////////////////////////////////////////////////////


  //////////////////////////////////////////////////////////////////////
  //                         Public Methods                           //
  //////////////////////////////////////////////////////////////////////


  /**
   * Constructor building vector object from dense coordinate list.
   */

  PythonVecData:: PythonVecData (void* val, float (* callback_f)(void * a, void * b, void * c), void * c)
  //
  {
    
    value = val;
    callback_distance=callback_f;
    python_distance=c;
  }



  //////////////////////////////////////////////////////////////////////


  /**
   * Copy constructor.
   */

  PythonVecData:: PythonVecData (PythonVecData* vec)
  //
  {
     value=vec->value;
     callback_distance=vec->callback_distance;     
  }


  //////////////////////////////////////////////////////////////////////


 PythonVecData::~ PythonVecData () {}


  //////////////////////////////////////////////////////////////////////


  /**
   * Returns the distance between two vectors.
   * A return value of 0.0F indicates that this vector object is
   *   identical to the supplied object.
   * If either vector is invalid, then a negative value is returned.
   */

  float PythonVecData:: distanceTo (DistData* vec)
  // 
  {
    return distanceTo ((PythonVecData*) vec);
  }


  //////////////////////////////////////////////////////////////////////


  /**
   * Returns the distance between two vectors.
   * A return value of 0.0F indicates that this vector object is
   *   identical to the supplied object.
   * If either vector is invalid, then a negative value is returned.
   */

  float PythonVecData:: distanceTo (PythonVecData* vec)
  // 
  {
     return callback_distance(value,vec->value, python_distance);
  }


  //////////////////////////////////////////////////////////////////////


  /**
   * Fills the supplied buffer with all vector coordinate values.
   * If the buffer is not sufficiently large, nothing is done.
   * The method returns the number of values actually copied to the buffer.
   */

  int PythonVecData:: getCoordValues (float* buffer, int capacity)
  //
  {
return 0;
  }


  //////////////////////////////////////////////////////////////////////


  /**
   * Returns the number of non-zero vector coordinate values.
   */

  int PythonVecData:: getLength ()
  //
  {
    return 0;
  }


  //////////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////

