/**
 * DenseArrayData.h:   Container class and distance measures
 *                   for dense vector data.
 * 
 */

#ifndef DENSEARRDATA_H_
#define DENSEARRDATA_H_

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "DistData.h"

// #ifndef DENSEARRDATA_VECTORANGLE_
// #define DENSEARRDATA_VECTORANGLE_
// #endif

#ifndef DENSEARRDATA_EUCLIDEAN_
#define DENSEARRDATA_EUCLIDEAN_
#endif

// #ifndef DENSEARRDATA_L_ONE_
// #define DENSEARRDATA_L_ONE_
// #endif

// #ifndef DENSEARRDATA_CHISQUAREDPLUS_
// #define DENSEARRDATA_CHISQUAREDPLUS_
// #endif

// #ifndef DENSEARRDATA_JSDIVERGENCEPLUS_
// #define DENSEARRDATA_JSDIVERGENCEPLUS_
// #endif

#ifndef DENSEARRDATA_INVALID_
#define DENSEARRDATA_INVALID_ (-1.0F)
#endif

#ifndef DENSEARRDATA_ERROR_
#define DENSEARRDATA_ERROR_ (-1)
#endif

#ifndef DENSEARRDATA_BUFSIZE_
#define DENSEARRDATA_BUFSIZE_ (1024)
#endif


////////////////////////////////////////////////////////////////////////
//                            DenseArrayData                            //
////////////////////////////////////////////////////////////////////////

class DenseArrayData: public DistData {

  //////////////////////////////////////////////////////////////////////
  //                           Properties                             //
  //////////////////////////////////////////////////////////////////////

// protected:
public:

  float* value;
  int length;

  //////////////////////////////////////////////////////////////////////
  //                         Public Methods                           //
  //////////////////////////////////////////////////////////////////////

public:

  //////////////////////////////////////////////////////////////////////


  /**
   * Constructor building vector object from dense coordinate list.
   */

  DenseArrayData (float* val, int len);






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

  float distanceTo (DenseArrayData* vec);


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
