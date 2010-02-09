##
## various utility function for image processing
##

def dumb_zoom(img,factor):
  """ do simple zoom by the mean of standard interpolation """
  zoommap=numpy.mgrid[:img.shape[0]*factor,:img.shape[1]*factor].astype(float)/
factor
  return numpy.dstack([ scipy.ndimage.map_coordinates(img[:,:,d],zoommap) for d
 in range(img.shape[2]) ])

def enframed(img,l,safety=(1,1)):
  """ adds a boundary around an image"""
  rimg=numpy.zeros((img.shape[0]+2*l[0]+safety[0],img.shape[1]+2*l[1]+safety[1]
,img.shape[2]))
  rimg[l[0]:l[0]+img.shape[0],l[1]:l[1]+img.shape[1],:]=img
  return rimg

