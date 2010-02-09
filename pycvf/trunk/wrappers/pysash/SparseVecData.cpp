/**
 * SparseVecData.cpp: Container class and distance measures
 *                    for sparse vector data.
 * 
 * Author:            Michael Houle
 * Date:              4 Jan 2006
 * Version:           1.0
 */

#include "SparseVecData.h"

////////////////////////////////////////////////////////////////////////
//                            SparseVecData                           //
////////////////////////////////////////////////////////////////////////


  //////////////////////////////////////////////////////////////////////
  //                         Public Methods                           //
  //////////////////////////////////////////////////////////////////////


  /**
   * Constructor building vector object from sparse coordinate lists.
   */

  SparseVecData:: SparseVecData (int* pos, float* val, int len)
  //
  {
    int i;

    if (len <= 0)
    {
      position = NULL;
      value = NULL;
      length = 0;
      return;
    }

    position = new int [len];
    value = new float [len];
    length = len;

    for (i=0; i<len; i++)
    {
      position[i] = pos[i];
      value[i] = val[i];
    }
  }


  //////////////////////////////////////////////////////////////////////


  /**
   * Constructor building vector object from sparse coordinate lists.
   * For the sake of compactness, the coordinate values are
   *   converted from double to float.
   */

  SparseVecData:: SparseVecData (int* pos, double* val, int len)
  //
  {
    int i;

    if (len <= 0)
    {
      position = NULL;
      value = NULL;
      length = 0;
      return;
    }

    position = new int [len];
    value = new float [len];
    length = len;

    for (i=0; i<len; i++)
    {
      position[i] = pos[i];
      value[i] = (float) val[i];
    }
  }


  //////////////////////////////////////////////////////////////////////


  /**
   * Copy constructor.
   */

  SparseVecData:: SparseVecData (SparseVecData* vec)
  //
  {
    int i;
    int len;

    if ((vec == NULL) || (vec->length == 0))
    {
      this->position = NULL;
      this->value = NULL;
      this->length = 0;
      return;
    }

    len = vec->length;

    this->position = new int [len];
    this->value = new float [len];
    this->length = len;

    for (i=0; i<len; i++)
    {
      this->position[i] = vec->position[i];
      this->value[i] = vec->value[i];
    }
  }


  //////////////////////////////////////////////////////////////////////


  /**
   * Destructor.
   */

  SparseVecData:: ~SparseVecData ()
  //
  {
    if (position != NULL)
    {
      delete [] position;
      position = NULL;
    }

    if (value != NULL)
    {
      delete [] value;
      value = NULL;
    }
  }


  //////////////////////////////////////////////////////////////////////


  /**
   * Returns the distance between two vectors.
   * A return value of 0.0F indicates that this vector object is
   *   identical to the supplied object.
   * If either vector is invalid, then a negative value is returned.
   */

  float SparseVecData:: distanceTo (DistData* vec)
  // 
  {
    return distanceTo ((SparseVecData*) vec);
  }


  //////////////////////////////////////////////////////////////////////


  /**
   * Returns the distance between two vectors.
   * A return value of 0.0F indicates that this vector object is
   *   identical to the supplied object.
   * If either vector is invalid, then a negative value is returned.
   */

  float SparseVecData:: distanceTo (SparseVecData* vec)
  // 
  {
#ifdef SPARSEVECDATA_VECTORANGLE_

    int locThis = 0;
    int locVec = 0;
    double normThis = 0.0F;
    double normVec = 0.0F;
    double cosine = 0.0F;

    // Calculate the norm of this vector.

    normThis = 0.0F;

    for (locThis=0; locThis<length; locThis++)
    {
      normThis += ((double) value[locThis]) * value[locThis];
    }

    if (normThis <= 0.0F)
    {
      return SPARSEVECDATA_INVALID_;
    }

    normThis = sqrt (normThis);

    // Calculate the norm of the supplied vector.

    normVec = 0.0F;

    for (locVec=0; locVec<vec->length; locVec++)
    {
      normVec += ((double) vec->value[locVec]) * vec->value[locVec];
    }

    if (normVec <= 0.0F)
    {
      return SPARSEVECDATA_INVALID_;
    }

    normVec = sqrt (normVec);

    // Compute the dot product of the two vectors.

    locThis = 0;
    locVec = 0;
    cosine = 0.0F;

    while ((locThis < length) && (locVec < vec->length))
    {
      if (position[locThis] < vec->position[locVec])
      {
        locThis++;
      }
      else if (position[locThis] > vec->position[locVec])
      {
        locVec++;
      }
      else
      {
        cosine += (value[locThis] / normThis) * (vec->value[locVec] / normVec);
        locThis++;
        locVec++;
      }
    }

    // Compute the vector angle from the cosine value, and return.
    // Roundoff error could have put the cosine value out of range.
    // Handle these cases explicitly.

    if (cosine >= 1.0F)
    {
      return 0.0F;
    }
    else if (cosine <= -1.0F)
    {
      return (float) acos (-1.0F);
    }
    else
    {
      return (float) acos (cosine);
    }

#else
#ifdef SPARSEVECDATA_EUCLIDEAN_

    int locThis = 0;
    int locVec = 0;
    double diff = 0.0F;
    double squareSum = 0.0F;

    // Compute the dot product of the two vectors.

    while ((locThis < length) && (locVec < vec->length))
    {
      if (position[locThis] < vec->position[locVec])
      {
        diff = value[locThis];
        squareSum += diff * diff;
        locThis++;
      }
      else if (position[locThis] > vec->position[locVec])
      {
        diff = vec->value[locVec];
        squareSum += diff * diff;
        locVec++;
      }
      else
      {
        diff = (value[locThis] - vec->value[locVec]);
        squareSum += diff * diff;
        locThis++;
        locVec++;
      }
    }

    return (float) sqrt (squareSum);

#else

    return SPARSEVECDATA_INVALID_;

#endif
#endif
  }


  //////////////////////////////////////////////////////////////////////


  /**
   * Fills the supplied buffer with the vector coordinate positions
   *   occupied by non-zero values.
   * If the buffer is not sufficiently large, nothing is done.
   * The method returns the number of positions actually copied to the buffer.
   */

  int SparseVecData:: getCoordPositions (int* buffer, int capacity)
  //
  {
    int i;

    if ((buffer == NULL) || (capacity < length))
    {
      return 0;
    }

    for (i=0; i<length; i++)
    {
      buffer[i] = position[i];
    }

    return length;
  }


  //////////////////////////////////////////////////////////////////////


  /**
   * Fills the supplied buffer with all non-zero vector coordinate values.
   * If the buffer is not sufficiently large, nothing is done.
   * The method returns the number of values actually copied to the buffer.
   */

  int SparseVecData:: getCoordValues (float* buffer, int capacity)
  //
  {
    int i;

    if ((buffer == NULL) || (capacity < length))
    {
      return 0;
    }

    for (i=0; i<length; i++)
    {
      buffer[i] = value[i];
    }

    return length;
  }


  //////////////////////////////////////////////////////////////////////


  /**
   * Returns the number of non-zero vector coordinate values.
   */

  int SparseVecData:: getLength ()
  //
  {
    return length;
  }


  //////////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////

