# -*- coding: utf-8 -*-
import zopencv
import scipy
import numpy
l=scipy.lena().astype(numpy.float32)/256.
#l=numpy.zeros((512,512),dtype=numpy.float32)
#l[252:258,:]=1
x=zopencv.NumPy2CvMatFast(l)
m=zopencv.CvMoments()
mu=zopencv.CvHuMoments()
zopencv.cvMoments(x,m,0)
zopencv.cvGetHuMoments(m,mu)
#l,x,m
eps=0.000000000000000001
print m.m00,m.m01,m.m02,m.m03,m.m10,m.m11,m.m12,m.m20,m.m21,m.m30
print m.mu02, m.mu03, m.mu11, m.mu12, m.mu20, m.mu21, m.mu30
print mu.hu1, mu.hu2, mu.hu3,mu.hu4, mu.hu5, mu.hu6,mu.hu7
#print dir(mu)
xb=m.m10/m.m00
yb=m.m01/m.m00
mu20=m.m20-xb*m.m10
mu02=m.m02-yb*m.m01
mu11=m.m11-xb*m.m01
print mu20,mu02,mu11
mu02p=mu02/m.m00
mu20p=mu20/m.m00
mu11p=mu11/m.m00
print mu20p,mu02p,mu11p
r=numpy.linalg.eig(numpy.matrix([[mu20p,mu11p],[mu11p,mu02p]]))
print r
o=numpy.dot(r[1],r[0])
print scipy.angle(o[0,0]+1j*o[0,1] )

orientation=.5*scipy.arctan((2.*mu11p)/(mu20p-mu02p+eps))*180/scipy.pi
print orientation

del r
del m
x.data_ptr=0
del x

l=scipy.lena().T[:,:].astype(numpy.float32)/256.
#l=numpy.zeros((512,512),dtype=numpy.float32)
#l[:,252:258]=1
x=zopencv.NumPy2CvMatFast(l)
m=zopencv.CvMoments()
mu=zopencv.CvHuMoments()
zopencv.cvMoments(x,m,0)
zopencv.cvGetHuMoments(m,mu)
#l,x,m
print m.m00,m.m01,m.m02,m.m03,m.m10,m.m11,m.m12,m.m20,m.m21,m.m30
print m.mu02, m.mu03, m.mu11, m.mu12, m.mu20, m.mu21, m.mu30
print mu.hu1, mu.hu2, mu.hu3,mu.hu4, mu.hu5, mu.hu6,mu.hu7
xb=m.m10/m.m00
yb=m.m01/m.m00
mu20=m.m20-xb*m.m10
mu02=m.m02-yb*m.m01
mu11=m.m11-xb*m.m01
print mu20,mu02,mu11
mu02p=mu02/m.m00
mu20p=mu20/m.m00
mu11p=mu11/m.m00
print mu20p,mu02p,mu11p
r=numpy.linalg.eig(numpy.matrix([[mu20p,mu11p],[mu11p,mu02p]]))
print r
o=numpy.dot(r[1],r[0])
print scipy.angle(o[0,0]+1j*o[0,1] )
orientation=.5*scipy.arctan((2.*mu11p)/(mu20p-mu02p))*180/scipy.pi
print orientation
del r
del m
x.data_ptr=0
del x

del l
print "ok"