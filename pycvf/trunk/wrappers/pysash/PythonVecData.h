/**
 * PythonVecData.h:   Container class and distance measures
 *                   for dense vector data.
 * 
 * Author:           Michael Houle
 * Date:             4 December 2006
 * Version:          1.0
 */

#ifndef PYTHONVECDATA_H_
#define PYTHONVECDATA_H_

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "DistData.h"


class PythonVecData: public DistData {

  //////////////////////////////////////////////////////////////////////
  //                           Properties                             //
  //////////////////////////////////////////////////////////////////////

// protected:
public:

  void * value;
  float (*callback_distance)(void * a, void * b, void *c);
  void * python_distance;

  //////////////////////////////////////////////////////////////////////
  //                         Public Methods                           //
  //////////////////////////////////////////////////////////////////////

public:

  //////////////////////////////////////////////////////////////////////


  /**
   * Constructor building vector object from dense coordinate list.
   */

  PythonVecData (void * val, float (*callback_distance)(void * a, void * b,void *c) , void * pcb);


  //////////////////////////////////////////////////////////////////////




  //////////////////////////////////////////////////////////////////////


  /**
   * Copy constructor.
   */

  PythonVecData (PythonVecData* vec);


  //////////////////////////////////////////////////////////////////////


  /**
   * Destructor.
   */

  ~PythonVecData ();


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

  float distanceTo (PythonVecData* vec);


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
