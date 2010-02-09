 /**
 * DenseArrayData.cpp: Container class and distance measures
 *                   for dense vector data stored in a an array that is not recopied !
 * 
 */

#include <cassert>
#include "PythonArrayData.h"

////////////////////////////////////////////////////////////////////////
//                            PythonArrayData                            //
////////////////////////////////////////////////////////////////////////


  //////////////////////////////////////////////////////////////////////
  //                         Public Methods                           //
  //////////////////////////////////////////////////////////////////////


  /**
   * Constructor building vector object from dense coordinate list.
   */

  PythonArrayData:: PythonArrayData (float* val, float (* callback_f)(void * a, void * b))
  //
  {
    
    value = val;
    callback_distance=callback_f;

  }

  //////////////////////////////////////////////////////////////////////


  /**
   * Returns the distance between two vectors.
   * A return value of 0.0F indicates that this vector object is
   *   identical to the supplied object.
   * If either vector is invalid, then a negative value is returned.
   */

  float PythonArrayData:: distanceTo (DistData* vec)
  // 
  {
    return distanceTo ((PythonArrayData*) vec);
  }


  //////////////////////////////////////////////////////////////////////


  /**
   * Returns the distance between two vectors.
   * A return value of 0.0F indicates that this vector object is
   *   identical to the supplied object.
   * If either vector is invalid, then a negative value is returned.
   */

  float PythonArrayData:: distanceTo (PythonArrayData* vec)
  // 
  {
     return callback_distance(value,vec->value);
  }


  //////////////////////////////////////////////////////////////////////


  /**
   * Fills the supplied buffer with all vector coordinate values.
   * If the buffer is not sufficiently large, nothing is done.
   * The method returns the number of values actually copied to the buffer.
   */

  int PythonArrayData:: getCoordValues (float* buffer, int capacity)
  //
  {
    return 0;
  }


  //////////////////////////////////////////////////////////////////////


  /**
   * Returns the number of non-zero vector coordinate values.
   */

  int PythonArrayData:: getLength ()
  //
  {
    return 0;
  }


  //////////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////

