/**
 * DistData.h:        Interface class for data having a pairwise 
 *                    distance measure.
 *                    (All SASH data classes must implement this interface.)
 * 
 * Author:            Michael Houle
 * Date:              4 Jan 2006
 * Version:           1.0
 */

#ifndef DISTDATA_H_
#define DISTDATA_H_


////////////////////////////////////////////////////////////////////////
//                              DistData                              //
////////////////////////////////////////////////////////////////////////

class DistData {

public:

  //////////////////////////////////////////////////////////////////////


  /**
   * Destructor.
   */

  virtual ~DistData () {};


  //////////////////////////////////////////////////////////////////////


  /**
   * Distance function.
   * A return value of 0.0F indicates that the supplied object is
   *   considered identical to the supplied object.
   * Otherwise, the return value should be positive.
   */

  virtual float distanceTo (DistData* obj) = 0;


  //////////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////

};

#endif
