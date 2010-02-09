#!/usr/bin/env python
# -*- coding: utf-8 -*-
## ##########################################################################################################
## 
## This file is released under GNU Public License v3
## See LICENSE File at the top the pycvf tree.
##
## Author : Bertrand NOUVEL / CNRS (2009)
##
##
##
## Revision FILE: $Id$
##
## ###########################################################################################################
## copyright $Copyright$
## @version $Revision$
## @lastrevision $Date$
## @modifiedby $LastChangedBy$
## @lastmodified $LastChangedDate$
#############################################################################################################


import numpy
import scipy
import scipy.ndimage

def harris(I,alpha=0.04,si=2):
  """ Harris Corner Detector """
  def imsmooth(I,si):
    return scipy.ndimage.gaussian_filter(I,si)
  Ix,Iy = scipy.gradient(I) 
  H11 = imsmooth(Ix*Ix, si) 
  H12 = imsmooth(Ix*Iy, si) 
  H22 = imsmooth(Iy*Iy, si) 
  return (H11*H22 - H12**2) - alpha*(H11+H22)**2 


def harris_noble(I,si):
  """ Noble's variation of Harris Corner Detector """
  eps=1e-16
  def imsmooth(I,si):
    return scipy.ndimage.gaussian_filter(I,si)
  Ix,Iy = scipy.gradient(I) 
  H11 = imsmooth(Ix*Ix, si) 
  H12 = imsmooth(Ix*Iy, si) 
  H22 = imsmooth(Iy*Iy, si) 
  return 2 *  (H11*H22 - H12**2)/(H11+H22+eps) 



#if nargout > 1
#  tr = H11 + H22 ;
#  dt = H11.*H22 - H12.^2 ;
#  Lm = 0.5 * (tr - sqrt(tr.^2 - 4*dt));
#  Lp = 0.5 * (tr + sqrt(tr.^2 - 4*dt));
#  Lm = real(Lm) ;
#  Lp = real(Lp) ;
#  
#  gamma=sqrt(Lm./Lp) ;
#
#  details.sigmap = Lp ;
#  if nargin > 2 
#    details.rho = gamma - alpha * (1+gamma).^2 ;
#  else
#    details.rho   = 2*gamma ./ (1 + gamma) ;
#  end
#end
