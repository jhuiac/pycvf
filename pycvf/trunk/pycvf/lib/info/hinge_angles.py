# -*- coding: utf-8 -*-
import numpy
import math
import itertools

def asgn(x):
    return (-1 if (x<0) else 1) 

sgn=numpy.sign

def farey( n, asc=True,first=True ):
    """Python function to print the nth Farey sequence, either ascending or descending."""
    if asc: 
        a, b, c, d = 0, 1,  1  , n     # (*)
    else:
        a, b, c, d = 1, 1, n-1 , n     # (*)
    if first:
      yield (a,b)
    while (asc and c < n) or (not asc and a > 0):
        k = ((n + b)//d)
        a, b, c, d = c, d, k*c - a, k*d - b
        yield (a,b)

def fareyloop( n, asc=True ):
    asc = asc ^ True
    yield (0,1)
    while True:
      for x in farey(n,True ^ asc,False): yield (x[0],x[1])
      for x in farey(n,False ^ asc,False): yield (x[1],x[0])
      for x in farey(n,True ^ asc,False): yield (x[1],-x[0])
      for x in farey(n,False ^ asc,False): yield (x[0],-x[1])
      for x in farey(n,True ^ asc,False): yield (-x[0],-x[1])
      for x in farey(n,False ^ asc,False): yield (-x[1],-x[0])
      for x in farey(n,True ^ asc,False): yield (-x[1],x[0])
      for x in farey(n,False ^ asc,False): yield (-x[0],x[1])


def fareycircle( n, asc=True ):
    return itertools.ifilter(lambda x:(((x[0]**2)+(x[1]**2))<=n**2),fareyloop(n,asc))

class HingeAngle:
    def __init__(self,x,y,h):
      self.x=x
      self.y=y
      self.h=h
      assert (self.DSR()> self.DSH()), ("invalid height for radius",x,y,h,self.DSR(), self.DSH())

    def SR(self): return self.x**2+self.y**2
    def DSR(self): return 4*(self.x**2+self.y**2)
    def X(self): return self.x
    def DX(self):  return 2*self.x
    def DSX(self):  return 4*(self.x**2)
    def Y(self): return self.y
    def DY(self):  return 2*self.y
    def DSY(self):  return 4*(self.y**2)
    def H(self): return self.h
    def DH(self):  return (2*self.h+1)
    def DSH(self):  return (2*self.h+1)**2
    def DSP(self): return self.DSR()-self.DSH()

    def rotm90(self): return HingeAngle(  x=-self.y, y=self.x, h=self.h)
    def rotp90(self): return HingeAngle(  x=self.y, y=-self.x, h=self.h)
    def psym0(self): return HingeAngle(  x=-self.x, y=self.y, h=self.h)
    def psym1(self): return HingeAngle(  x=self.x, y=-self.y, h=self.h)
    def exoctant1(self):
        return self.psym0().rotm90()

    ## changement d'octant du premier quadr vers le premier quadr
    def sym0(self): return (HingeAngle(  x=self.y, y=self.x, h=-(self.h+1))).rotp90().rotp90()

    def __float__(self):
        if (self.x!=0):
            t=-math.atan((float(self.y))/(float(self.x)))
        else:
            t=-numpy.pi/2*asgn(self.y)
        if (self.x<0):
           t-=numpy.pi
        N=self.DH()
        D=math.sqrt(self.DSR())
        t+=math.asin(N/D)
        return t%(2*numpy.pi)
 
    def __repr__(self):
         return ("[<hinge angle>(%d , %d , %d) %f ]"%(self.x,self.y,self.h,self.__float__()))

    def identify_quadr_float(self):
        a=self.__float__()
        xc=asgn(math.cos(a))
        yc=asgn(math.sin(a))

        if ((xc==1) and (yc==1)):
	    return 1;
        if ((xc==-1) and (yc==1)):
	    return 2;
        if ((xc==-1) and (yc==-1)):
	    return 3;
        if ((xc==1) and (yc==-1)):
	    return 4;

    def identify_quadr(self):
        if (asgn(self.DY()*self.DH()*self.DX())==-1) :
            if ((self.DSH()*self.DSY())<(self.DSX()*self.DSP())):
                _xc=1*asgn(self.DX())
            else:
                _xc=-1*asgn(self.DX())
        else:
            _xc=asgn(self.DY()*self.DH())
        xc=_xc
     
        if ((asgn(self.DX()*self.DH()*self.DY()))==1):
            if ((self.DSH()*self.DSX())<(self.DSY()*self.DSP())):
                _yc=1*asgn(-self.DY())
            else:
                _yc=-1*asgn(-self.DY())
        else:
            _yc=asgn(-self.DY())
        yc=_yc             

        if (self.DY() == 0):
            xc=xc*numpy.sign(self.DX());
            if (asgn(self.DX()*self.DH())==1) :
                yc=-_yc
          
        if ((xc==1) and (yc==1)):
           return 1
        if ((xc==-1) and (yc==1)):
           return 2
        if ((xc==-1) and (yc==-1)):
           return 3
        if ((xc==1) and (yc==-1)):
            return 4

    def add_pyth(a,b,c):
	  assert(a**2+b**2==c**2)
          assert(c%2==1)
	  return HingeAngle(a*self.x+b*self.y,
                            -b*self.x+a*self.x,
                            c*self.h+self.h
                            )

    def identify_octant(self):
	q=self.identify_quadr()
	o=(q-1)*2
	n=self.normalized_angle()
	##
	## we add an octant and check again the quadr
	##
	if (n.sym0().__less__(n)):
	   return o+2
	else:
	  return o+1


    #less pour deux angles du premier quadrant....
    def less_q1 (self,b):
      a=self
      adsr2=a.DSR()**2
      bdsr2=b.DSR()**2
      adsr4=a.DSR()**4
      bdsr4=b.DSR()**4
      aprd=a.DSH()*a.DSP()*a.DSY()*a.DSX()
      bprd=b.DSH()*b.DSP()*b.DSY()*b.DSX()
      t1=(a.DSP()*a.DSX()-a.DSP()*a.DSY()-a.DSH()*a.DSX()+a.DSH()*a.DSY())*bdsr2
      t2=(b.DSP()*b.DSX()-b.DSP()*b.DSY()-b.DSH()*b.DSX()+b.DSH()*b.DSY())*adsr2
      if (asgn(a.DX()*a.DY()*a.DH())*asgn(-b.DX()*b.DY()*b.DH())==1):
          us=asgn(a.DX()*a.DY()*a.DH())*-1;
      else : 
        us=(asgn((aprd*bdsr4 ) -(bprd*adsr4 )) )
        if (asgn(a.DX()*a.DY()*a.DH())==1):
          us*=-1;
      if ((sgn(t1-t2)==0) and (sgn((aprd*bdsr4 )-(bprd*adsr4 ))==0)):
              return False;
      if (asgn(t1-t2)<us):
          return False
      if (asgn(t1-t2)>us):
          return True
      s1=16*aprd*bdsr4
      s2=16*bprd*adsr4
      k=((t1-t2)*(t1-t2))-s1-s2
      xs=-asgn(a.DX())*asgn(b.DX())*asgn(a.DY())*asgn(b.DY())*asgn(a.DH())*asgn(b.DH());
      if ((asgn(k)==-1) and (xs==1)):  return (us!=1)
      if ((asgn(k)==1) and (xs==-1)): return (us==1)
      rt=4*s1*s2;
      if (k*k<rt):
          if (us==1):
            return(xs!=1)
          else:
            return (xs==1)
      else:
          if (us!=1):
            return(xs!=1)
          else:
            return (xs==1)

    def normalized_angle(self):
        i=self.identify_quadr();
        r=self
        for x in range(1,i):
            r=r.rotm90();
        return r

    def normalized_angle_first_octant(self):
	n=self.normalized_angle()
	if (n.identify_octant()==2):
	  return n.sym0()
	else:
	  return n

    def __less__ (self, b):
        a=self
        ia,ib=a.identify_quadr(),b.identify_quadr()
        if (ia!=ib) :
            return (ia<ib)
        na,nb=a.normalized_angle(),b.normalized_angle();
        if (((na.DY()!=0) and (nb.DY()!=0)) and ((na.DY()*nb.DH() + nb.DY() * na.DH()==0)and(na.DY()*nb.DX() + nb.DY() * na.DX()==0))) :
                    return (na.DY()>0)
        return na.less_q1(nb);

    def __cmp__(self,b):
       if (b.h*self.x==self.h*b.x) and (b.h*self.y==self.h*b.y):
           return 0
       else:
          if self.__less__(b):
              return -1
          else:
              return 1

    @staticmethod
    def iter_in_ball_test1(r):
       """ experimental code (we try for all heights /!\ but there may be different radius !) """
       lf= [iter(fareyloop(r)) for x in range(2*r) ] 
       ll=[]
       for x in range(2*r):
          print x-r,
          def next_hangle():
            while True:
              try:
                a,b=lf[x].next()
                k=1
                while ((k*a)**2+(k*b)**2<r**2):
                   try:
                      am=HingeAngle(a,b,x-r)                  
                      #yield am
                      return am
                   except:
                      k+=1
              except:
                pass
          am=next_hangle()
          an=next_hangle()
          inf=False
          if (am!=an) and (an.__less__(am)):
             am=an
             inf=True
          while ((am!=an) or (inf)):
            an=next_hangle()
            inf=False
            if (am!=an) and (an.__less__(am)):
               am=an
               inf=True
          print am
          ll.append(am)      
       print ll