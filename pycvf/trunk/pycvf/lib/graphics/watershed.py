##
## THIS FILE IS UNDER LGPL and MAKES PART of PyCVF
## It has been developped by B.Nouvel
##

import scipy,numpy,random  

V4=numpy.array([[0,1,0],[1,1,1],[0,1,0]])

def watershed(img,footprint=V4):
  """
  This function is a slow version of a watershed function that computes for
  according to a grayscale value image, the different components of 
  this image. It can be use in combination with distance transform to 
  do morphological analysis. 
  """
  assert(img.ndim==2)
  footprint=numpy.array(footprint)
  footprintp=[]
  fpw2=footprint.shape[1]//2
  fph2=footprint.shape[0]//2
  for i in numpy.ndindex(footprint.shape):
    if footprint[i]:
      footprintp.append((i[0]-fph2,i[1]-fpw2))
  #img=img.astype(float)
  imgsrt=scipy.argsort(img.ravel())
  #+numpy.arange(0,0.5,0.5/img.ravel().shape[0]))
  L=numpy.ones(img.shape)*-1
  clabel=0
  h,w=img.shape
  LR=L.ravel()
  def collect_around(p):
    res=[]
    stack=[p]
    L[p]=-2
    while len(stack)>0:
      p=stack.pop()
      for pp in map(lambda x:(min(max(x[0]+p[0],0),h-1)*w+min(max(x[1]+p[1],0),w-1)) ,footprintp):
        p2=(pp//w,pp%w)
        if (img[p2]==img[p]):
          if L[p2]==-1:
            L[p2]=-2
            stack.append(p2)
          else:
            res.append(L[p2])
        if (img[p2]<=img[p]):
          res.append(L[p2])
    return res
  def propagate_around(p):
    stack=[p]
    while len(stack)>0:
      p=stack.pop()
      for pp in map(lambda x:(min(max(x[0]+p[0],0),h-1)*w+min(max(x[1]+p[1],0),w-1)) ,footprintp):
        p2=(pp//w,pp%w)
        if (img[p2]==img[p]) and L[p2]<0:
          assert(L[p]>=0)
          L[p2]=L[p]
          stack.append(p2)
  for x in imgsrt:
    p=(x//w,x%w)
    if L[p]<0:
      #surroundlabels=LR.take(map(lambda x:(min(max(x[0]+p[0],0),h-1)*w+min(max(x[1]+p[1],0),w-1)) ,footprintp))
      surroundlabels=collect_around(p)
      surroundlabels=filter(lambda x:x>=0,surroundlabels)
      if len(set(surroundlabels))<=1:
        if len(surroundlabels)==0:
          L[p]=clabel
          propagate_around(p)
          clabel+=1
        else:
          L[p]=surroundlabels[0]
          propagate_around(p)
      else:
        L[p]=random.choice(surroundlabels)
        propagate_around(p)
  return L

if __name__=="__main__":
  r=watershed(scipy.ndimage.distance_transform_edt(scipy.lena()[::4,::4]>128).astype(numpy.uint8),F1)
  pylab.clf();pylab.imshow(r);pylab.show()
