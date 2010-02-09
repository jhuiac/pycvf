/**
 * PythonArrayData.h:   Container class and distance measures
 *                   for dense vector data.
 * 
 */

#ifndef PYTHONARRDATA_H_
#define PYTHONARRDATA_H_


#include "DistData.h"
//////////////////////////////////////////////////////////////////////
//                            PythonArrayData                            //
////////////////////////////////////////////////////////////////////////

class PythonArrayData: public DistData {

  //////////////////////////////////////////////////////////////////////
  //                           Properties                             //
  //////////////////////////////////////////////////////////////////////

// protected:
public:

  void * value;
  float (*callback_distance)(void * a, void * b);
   void * python_callback;

  //////////////////////////////////////////////////////////////////////
  //                         Public Methods                           //
  //////////////////////////////////////////////////////////////////////

public:

  //////////////////////////////////////////////////////////////////////


  /**
   * Constructor building vector object from dense coordinate list.
   */

  PythonArrayData (void * val, float (*callback_distance)(void * a, void * b) );


  //////////////////////////////////////////////////////////////////////


  /**
   * Returns the distance between two vectors.
   * A return value of 0.0F indicates that this vector object is
   *   identical to the supplied object.
   * If either vector is invalid, then a negative value is returned.
   */

  float distanceTo (DistData* vec);


  //////////////////////////////////////////////////////////////////////


  /**
   * Returns the distance between two vectors.
   * A return value of 0.0F indicates that this vector object is
   *   identical to the supplied object.
   * If either vector is invalid, then a negative value is returned.
   */

  float distanceTo (PythonArrayData* vec);


  //////////////////////////////////////////////////////////////////////


  /**
   * Fills the supplied buffer with all vector coordinate values.
   * If the buffer is not sufficiently large, nothing is done.
   * The method returns the number of values actually copied to the buffer.
   */

  int getCoordValues (float* buffer, int capacity);


  //////////////////////////////////////////////////////////////////////


  /**
   * Returns the number of vector coordinate values.
   */

  int getLength ();


  //////////////////////////////////////////////////////////////////////

};


////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

#endif
