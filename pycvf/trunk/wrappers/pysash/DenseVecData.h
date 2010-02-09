/**
 * DenseVecData.h:   Container class and distance measures
 *                   for dense vector data.
 * 
 * Author:           Michael Houle
 * Date:             4 December 2006
 * Version:          1.0
 */

#ifndef DENSEVECDATA_H_
#define DENSEVECDATA_H_

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "DistData.h"

// #ifndef DENSEVECDATA_VECTORANGLE_
// #define DENSEVECDATA_VECTORANGLE_
// #endif

#ifndef DENSEVECDATA_EUCLIDEAN_
#define DENSEVECDATA_EUCLIDEAN_
#endif

// #ifndef DENSEVECDATA_L_ONE_
// #define DENSEVECDATA_L_ONE_
// #endif

// #ifndef DENSEVECDATA_CHISQUAREDPLUS_
// #define DENSEVECDATA_CHISQUAREDPLUS_
// #endif

// #ifndef DENSEVECDATA_JSDIVERGENCEPLUS_
// #define DENSEVECDATA_JSDIVERGENCEPLUS_
// #endif

#ifndef DENSEVECDATA_INVALID_
#define DENSEVECDATA_INVALID_ (-1.0F)
#endif

#ifndef DENSEVECDATA_ERROR_
#define DENSEVECDATA_ERROR_ (-1)
#endif

#ifndef DENSEVECDATA_BUFSIZE_
#define DENSEVECDATA_BUFSIZE_ (1024)
#endif


////////////////////////////////////////////////////////////////////////
//                            DenseVecData                            //
////////////////////////////////////////////////////////////////////////

class DenseVecData: public DistData {

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

  DenseVecData (float* val, int len);


  //////////////////////////////////////////////////////////////////////


  /**
   * Constructor building vector object from dense coordinate list.
   * For the sake of compactness, the coordinate values are
   *   converted from double to float.
   */

  DenseVecData (double* val, int len);


  //////////////////////////////////////////////////////////////////////


  /**
   * Copy constructor.
   */

  DenseVecData (DenseVecData* vec);


  //////////////////////////////////////////////////////////////////////


  /**
   * Destructor.
   */

  ~DenseVecData ();


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

  float distanceTo (DenseVecData* vec);


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
