Implementation of the SASH index for approximate similarity search,
as described in 
  Michael E. Houle,
  "SASH: a Spatial Approximation Sample Hierarchy for Similarity Search",
  IBM Tokyo Research Laboratory Technical Report RT-0517, 5 March 2003.
&
  Michael E. Houle & Jun Sakuma,
  "Fast Approximate Similarity Search in Extremely High-Dimensional Data Sets",
  In Proc. 21st IEEE International Conference on Data Engineering (ICDE 2005),
  Tokyo, Japan, April 2005, pp. 619-630.

Any references to this work should include a citation of the ICDE 2005 paper.

Please note the conditions of use outlined in the source code comments.


FILES
-----

Sash.cpp           -- The main SASH source code.
Sash.h                Descriptions of SASH operations and examples of
                        their use can be found as comments within Sash.h.

mtrand.cpp         -- Mersenne Twister random number generator used by
mtrand.h                the SASH.
                      The SASH performance does not depend heavily on the
                        quality of the random number generator.

DistData.h         -- Virtual class (interface) from which all
                        SASH data object classes must be derived.
                      It declares a pairwise distance function which 
                        must be implemented.

DenseVecData.cpp   -- An example of a derived class of DistData.
DenseVecData.h        Each data item is represented as a real-valued vector
                        whose coordinate values are explicitly stored.
                      A variety of distance metrics can be selected
                        as compile-time options.
                        
SparseVecData.cpp  -- An example of a derived class of DistData.
SparseVecData.h       Each data item is represented as a real-valued vector
                        where only non-negative coordinate values are 
                        explicitly stored.
                      A variety of distance metrics can be selected
                        as compile-time options.

rt0517.pdf         -- The IBM TRL technical report.
                      The ICDE 2005 version is more complete, and should
                      be referenced in preference to the technical report. 
                      However, the ICDE version could not be included in
                      the distribution due to copyright restrictions.

README.txt         -- This file.


NOTES
-----

Before the SASH can be used, a derived class of DistData must be created
for storing a single data item, and computing the distance to another data 
item. The DenseVecData and SparseVecData classes serve as examples that
can be adapted for this purpose.

In order to perform approximate similarity search using the SASH, certain
parameters must be tuned. Recommended starting parameters for tuning are:

  Methods           Parameter     Value               Comments
  -------           ---------     ---------------     --------
  build             numParents    4                   Increasing this value 
                                  (default value)     increases query accuracy
                                  (recommended)       and execution time,
                                                      SASH construction time,
                                                      and SASH storage cost.

  findNear          scaleFactor   1.0F                Increasing this value
  findMostInRange                 (minimum value      increases query accuracy
                                   recommended)       and execution time.
                                                      Lowering the value
                                                      is also possible!

Tuning is best done by fixing the numParents parameter, and then varying the 
scaleFactor parameter until the most desirable accuracy-time tradeoff is 
achieved. If the best tradeoff point is still not good enough, then query-time
performance may often be boosted (at the expense of construction time) and
a better accuracy-time trade-off obtained, first by increasing numParents
and then varying scaleFactor again.

Accuracy can be checked by 
  1) performing an exact search using findNearest or findAllInRange,
  2) extracting the distances from query to result items using getResultDists,
  3) performing the desired findNear or findMostInRange operation, and then
  4) supplying the list of exact distances to getResultAcc.
An example of accuracy checking appears as comments in the file Sash.h.

