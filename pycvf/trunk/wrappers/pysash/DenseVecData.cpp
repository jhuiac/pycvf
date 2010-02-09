/**
 * DenseVecData.cpp: Container class and distance measures
 *                   for dense vector data.
 * 
 * Author:           Michael Houle
 * Date:             4 December 2006
 * Version:          1.0
 */

#include "DenseVecData.h"

////////////////////////////////////////////////////////////////////////
//                            DenseVecData                            //
////////////////////////////////////////////////////////////////////////


  //////////////////////////////////////////////////////////////////////
  //                         Public Methods                           //
  //////////////////////////////////////////////////////////////////////


  /**
   * Constructor building vector object from dense coordinate list.
   */

  DenseVecData:: DenseVecData (float* val, int len)
  //
  {
    int i;

    if (len <= 0)
    {
      value = NULL;
      length = 0;
      return;
    }

    value = new float [len];
    length = len;

    for (i=0; i<len; i++)
    {
      value[i] = val[i];
    }
  }


  //////////////////////////////////////////////////////////////////////


  /**
   * Constructor building vector object from dense coordinate list.
   * For the sake of compactness, the coordinate values are
   *   converted from double to float.
   */

  DenseVecData:: DenseVecData (double* val, int len)
  //
  {
    int i;

    if (len <= 0)
    {
      value = NULL;
      length = 0;
      return;
    }

    value = new float [len];
    length = len;

    for (i=0; i<len; i++)
    {
      value[i] = (float) val[i];
    }
  }


  //////////////////////////////////////////////////////////////////////


  /**
   * Copy constructor.
   */

  DenseVecData:: DenseVecData (DenseVecData* vec)
  //
  {
    int i;
    int len;

    if ((vec == NULL) || (vec->length == 0))
    {
      this->value = NULL;
      this->length = 0;
      return;
    }

    len = vec->length;

    this->value = new float [len];
    this->length = len;

    for (i=0; i<len; i++)
    {
      this->value[i] = vec->value[i];
    }
  }


  //////////////////////////////////////////////////////////////////////


  /**
   * Destructor.
   */

  DenseVecData:: ~DenseVecData ()
  //
  {
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

  float DenseVecData:: distanceTo (DistData* vec)
  // 
  {
    return distanceTo ((DenseVecData*) vec);
  }


  //////////////////////////////////////////////////////////////////////


  /**
   * Returns the distance between two vectors.
   * A return value of 0.0F indicates that this vector object is
   *   identical to the supplied object.
   * If either vector is invalid, then a negative value is returned.
   */

  float DenseVecData:: distanceTo (DenseVecData* vec)
  // 
  {
#ifdef DENSEVECDATA_VECTORANGLE_

    int loc = 0;
    int minLength = 0;
    double normThis = 0.0F;
    double normVec = 0.0F;
    double cosine = 0.0F;

    // Calculate the norm of this vector.

    normThis = 0.0F;

    for (loc=0; loc<length; loc++)
    {
      normThis += ((double) value[loc]) * value[loc];
    }

    if (normThis <= 0.0F)
    {
      return DENSEVECDATA_INVALID_;
    }

    normThis = sqrt (normThis);

    // Calculate the norm of the supplied vector.

    normVec = 0.0F;

    for (loc=0; loc<vec->length; loc++)
    {
      normVec += ((double) vec->value[loc]) * vec->value[loc];
    }

    if (normVec <= 0.0F)
    {
      return DENSEVECDATA_INVALID_;
    }

    normVec = sqrt (normVec);

    // Compute the dot product of the two vectors.

    cosine = 0.0F;

    minLength = vec->length;

    if (minLength > length)
    {
      minLength = length;
    }

    for (loc=0; loc<minLength; loc++)
    {
      cosine += (value[loc] / normThis) * (vec->value[loc] / normVec);
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
#ifdef DENSEVECDATA_EUCLIDEAN_

    int loc = 0;
    int minLength = 0;
    double diff = 0.0F;
    double squareSum = 0.0F;

    minLength = vec->length;

    if (minLength > length)
    {
      minLength = length;
    }

    for (loc=0; loc<minLength; loc++)
    {
      diff = (value[loc] - vec->value[loc]);
      squareSum += diff * diff;
    }

    return (float) sqrt (squareSum);

#else
#ifdef DENSEVECDATA_L_ONE_

    int loc = 0;
    int minLength = 0;
    double diff = 0.0F;
    double absSum = 0.0F;

    minLength = vec->length;

    if (minLength > length)
    {
      minLength = length;
    }

    for (loc=0; loc<minLength; loc++)
    {
      diff = (value[loc] - vec->value[loc]);

      if (diff < 0.0F)
      {
        absSum -= diff;
      }
      else
      {
        absSum += diff;
      }
    }

    return (float) absSum;

#else
#ifdef DENSEVECDATA_CHISQUAREDPLUS_

    // Uses absolute values of raw data, incremented by one.
    // As a result, data values are guaranteed to be at least 1.0F.

    int loc = 0;
    int minLength = 0;
    double thisValue = 0.0F;
    double vecValue = 0.0F;
    double sum = 0.0F;
    double diff = 0.0F;
    double term = 0.0F;

    minLength = vec->length;

    if (minLength > length)
    {
      minLength = length;
    }

    for (loc=0; loc<minLength; loc++)
    {
      thisValue = value[loc];
      vecValue = vec->value[loc];

      if (thisValue < 0.0F)
      {
        thisValue = 1.0F - thisValue;
      }
      else
      {
        thisValue += 1.0F;
      }

      if (vecValue < 0.0F)
      {
        vecValue = 1.0F - vecValue;
      }
      else
      {
        vecValue += 1.0F;
      }

      diff = thisValue - vecValue;
      sum = thisValue + vecValue;
      term += diff * (diff / sum);
    }

    return (float) sqrt (term);

#else
#ifdef DENSEVECDATA_JSDIVERGENCEPLUS_

    // Uses absolute values of raw data, incremented by one.
    // As a result, data values are guaranteed to be at least 1.0F.

    int loc = 0;
    int minLength = 0;
    double avgValue = 0.0F;
    double thisValue = 0.0F;
    double vecValue = 0.0F;
    double avgEntropy = 0.0F;
    double thisEntropy = 0.0F;
    double vecEntropy = 0.0F;

    minLength = vec->length;

    if (minLength > length)
    {
      minLength = length;
    }

    for (loc=0; loc<minLength; loc++)
    {
      thisValue = value[loc];
      vecValue = vec->value[loc];

      if (thisValue < 0.0F)
      {
        thisValue = 1.0F - thisValue;
      }
      else
      {
        thisValue += 1.0F;
      }

      if (vecValue < 0.0F)
      {
        vecValue = 1.0F - vecValue;
      }
      else
      {
        vecValue += 1.0F;
      }

      avgValue = (thisValue + vecValue) / 2.0F;

      thisEntropy -= thisValue * log ((double) thisValue);
      vecEntropy -= vecValue * log ((double) vecValue);
      avgEntropy -= avgValue * log ((double) avgValue);
    }

    return (float) ((2.0F * avgEntropy) - (thisEntropy + vecEntropy));

#else

    return DENSEVECDATA_INVALID_;

#endif
#endif
#endif
#endif
#endif
  }


  //////////////////////////////////////////////////////////////////////


  /**
   * Fills the supplied buffer with all vector coordinate values.
   * If the buffer is not sufficiently large, nothing is done.
   * The method returns the number of values actually copied to the buffer.
   */

  int DenseVecData:: getCoordValues (float* buffer, int capacity)
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

  int DenseVecData:: getLength ()
  //
  {
    return length;
  }


  //////////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////

