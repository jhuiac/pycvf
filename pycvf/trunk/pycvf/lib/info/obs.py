# -*- coding: utf-8 -*-
import scipy.weave
import numpy



def make_observation(l=[ [-1,-1], [-1,0],[-1,1] ], bordermode="mirror" ,cropbefore=None, cropafter=None):
  """
  returns a function that extract elements according the function specified.
  the elements are consequently provided as a 2d array.
  """
  
  minpos=numpy.array(l)
  ndim=len(l[0])
  l=numpy.array(l)
  if (cropbefore==None):
    cropbefore=numpy.zeros((ndim,),dtype=int)
  else:
    cropbefore=numpy.array(cropbefore,dtype=int).copy('C')
  if (cropafter==None):
    cropafter=numpy.zeros((ndim,),dtype=int)
  else:
    cropafter=numpy.array(cropafter,dtype=int).copy('C')
  
  
  BIA="""#define BIA(x,w,b,i,a) (((x)<0)?(b):(((x)>=w)?(a):(i)))\n"""


  if bordermode in [ "mirror" , "torus"]:
    bordersf={
      "mirror":BIA+"#define B(x,w) BIA(x,w,-x,x,2*w-x-1)",
      "torus" :BIA+"#define B(x,w) BIA(x,w,w+x,x,x-w)"
    }      
    copycode=bordersf[bordermode]+"\n"
    copycode+="int nbytes=initarr_array->strides[ndim-1];"
    copycode+= (reduce(
               lambda b,l:
               b+"tp[%d]=B((cp[%d]+l[cl*ndim+%d]),(initarr_array->dimensions[%d]));\n"%(l,l,l,l),
               range(ndim),
               ""
               )
              +
              "resarr[p*L+cl]=initarr["+"+".join(map(lambda x:"""tp[%d]*(initarr_array->strides[%d]/nbytes)"""%(x,ndim-1-x), range(ndim)))+"];"
             )
  elif bordermode in [ "cmode" ]:
     copycode="""
         int nbytes=initarr_array->strides[ndim-1];
         int cval=0;
         int d=0;
         for (d=0;d<ndim;d++) {
           tp[d]=cp[d]+l[cl*ndim+d];
           if (tp[d]<0) {
             resarr[p*L+cl]=cval;
             d=ndim+2;
             break;
           }
           if (tp[d]>= initarr_array->dimensions[d]) {
             resarr[p*L+cl]=cval;
             d=ndim+2;
             break;
           }           
         }
         if (d==ndim) {
             resarr[p*L+cl]=initarr["""+"+".join(map(lambda x:"""tp[%d]*(initarr_array->strides[%d]/nbytes)"""%(x,ndim-1-x), range(ndim)))+"""];
         }
      """
  else: 
      raise ValueError,"Unsupported Value"
            
  
  
  obslines=""
  for i in l:
    obslines+="""resarr[c,l]=initarr(%s);\n"""
  
  
  
  def f(initarr):
    avolume=reduce(lambda x,y:x*(y[0]-y[1]),zip(initarr.shape,(cropbefore+cropafter).flat),1)
    avolume=int(avolume)
    print avolume
    resarr=numpy.ndarray(shape=(avolume,len(l)))


    code=("""
      /* ********************************************* */
      /* DECLARE VALUES                                */
      /* ********************************************* */
      
      int * cp; // current position in source
      //int * dcp; // current position in result
      int * tp; // target position
      int xr;
      
      /* ********************************************* */
      /* INITIALIZE VALUES                             */      
      /* ********************************************* */
      
      cp=(int *)calloc(ndim,sizeof(int));
      //dcp=(int *)calloc(ndim,sizeof(int));
      tp=(int *)calloc(ndim,sizeof(int));      
     // sizes=initarr_array->sizes;
      
      for (int  i=0; i<ndim;i++) {
        cp[i]=cropbefore[i];
        printf("%d", cp[i]);
      }
      
      /* forall positions */
      for (int p=0;p<NP;p++) {      
        /* forall lines */
        for (int cl=0;cl<L;cl++) {
      """
      +
      copycode
      +
      """
        }
        xr=0;
        cp[xr]+=1;
        while (cp[xr]>=(initarr_array->dimensions[xr]-cropafter[xr])) {
              cp[xr]=cropbefore[xr];
              xr+=1;
              cp[xr]+=1;
           }

      }
      
      free(cp);
      free(tp);
      """)
    ndim=len(l[0])
    NP=int(avolume)
    L=l.shape[0]
    #print L
    x=scipy.weave.inline(code,['initarr', 'resarr','ndim','cropbefore','cropafter','NP','L','l'], compiler='gcc', extra_compile_args="-O3")#,type_converters = scipy.weave.converters.blitz)
    return resarr
  
  return f

if __name__=="__main__":
  #import scipy
  #l=scipy.lena()
  l=numpy.arange(16).reshape((4,4))
  dcropbefore=[1,1]
  dcropafter=[1,1]
  r=make_observation([ [0,0],[2,2],[-1,-1] ],"torus",cropbefore=dcropbefore,cropafter=dcropafter)(l)
  print r
  r=r.reshape(tuple((numpy.array(l.shape)-numpy.array(dcropafter)-numpy.array(dcropbefore)).flat) +(3,))
  #print l.shape
  print r.swapaxes(0,2).swapaxes(1,2)  # (r[:,0]-r[:,1]).mean()
  