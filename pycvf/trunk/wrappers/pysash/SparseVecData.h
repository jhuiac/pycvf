/**
 * SparseVecData.h:   Container class and distance measures
 *                    for sparse vector data.
 * 
 * Author:            Michael Houle
 * Date:              4 Jan 2006
 * Version:           1.0
 */

#ifndef SPARSEVECDATA_H_
#define SPARSEVECDATA_H_

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "DistData.h"

#ifndef SPARSEVECDATA_VECTORANGLE_
#define SPARSEVECDATA_VECTORANGLE_
#endif

// #ifndef SPARSEVECDATA_EUCLIDEAN_
// #define SPARSEVECDATA_EUCLIDEAN_
// #endif

#ifndef SPARSEVECDATA_INVALID_
#define SPARSEVECDATA_INVALID_ (-1.0F)
#endif

#ifndef SPARSEVECDATA_ERROR_
#define SPARSEVECDATA_ERROR_ (-1)
#endif

#ifndef SPARSEVECDATA_BUFSIZE_
#define SPARSEVECDATA_BUFSIZE_ (1024)
#endif


////////////////////////////////////////////////////////////////////////
//                            SparseVecData                           //
////////////////////////////////////////////////////////////////////////

class SparseVecData: public DistData {

  //////////////////////////////////////////////////////////////////////
  //                           Properties                             //
  //////////////////////////////////////////////////////////////////////

// protected:
public:

  int* position;
  float* value;
  int length;

  //////////////////////////////////////////////////////////////////////
  //                         Public Methods                           //
  //////////////////////////////////////////////////////////////////////

public:

  //////////////////////////////////////////////////////////////////////


  /**
   * Constructor building vector object from sparse coordinate lists.
   */

  SparseVecData (int* pos, float* val, int len);


  //////////////////////////////////////////////////////////////////////


  /**
   * Constructor building vector object from sparse coordinate lists.
   * For the sake of compactness, the coordinate values are
   *   converted from double to float.
   */

  SparseVecData (int* pos, double* val, int len);


  //////////////////////////////////////////////////////////////////////


  /**
   * Copy constructor.
   */

  SparseVecData (SparseVecData* vec);


  //////////////////////////////////////////////////////////////////////


  /**
   * Destructor.
   */

  ~SparseVecData ();


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

  float distanceTo (SparseVecData* vec);


  //////////////////////////////////////////////////////////////////////


  /**
   * Fills the supplied buffer with the vector coordinate positions
   *   occupied by non-zero values.
   * If the buffer is not sufficiently large, nothing is done.
   * The method returns the number of positions actually copied to the buffer.
   */

  int getCoordPositions (int* buffer, int capacity);


  //////////////////////////////////////////////////////////////////////


  /**
   * Fills the supplied buffer with all non-zero vector coordinate values.
   * If the buffer is not sufficiently large, nothing is done.
   * The method returns the number of values actually copied to the buffer.
   */

  int getCoordValues (float* buffer, int capacity);


  //////////////////////////////////////////////////////////////////////


  /**
   * Returns the number of non-zero vector coordinate values.
   */

  int getLength ();


  //////////////////////////////////////////////////////////////////////

};


////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

#endif
