from pycvf.nodes.image import map_coordinates

def polar(invert=False,fisheye=1,radius=2**.5,*args,**kwargs):
    if (invert):
       if (fisheye==1):
          return map_coordinates.__call__("numpy.abs(x)/"+str(radius)+"+1J*((numpy.angle(x))/(2*numpy.pi))")
       else:
          return map_coordinates.__call__("(numpy.abs(x)/"+str(radius)+")**"+str(fisheye)+"+1J*((numpy.angle(x))/(2*numpy.pi))")
    else:
       if (fisheye==1):
         return map_coordinates.__call__("numpy.real(x)*numpy.exp(1J*2*numpy.pi*numpy.imag(x))*"+str(radius))
       else:
         return map_coordinates.__call__("numpy.real(x)**"+str(1./fisheye)+"*numpy.exp(1J*2*numpy.pi*numpy.imag(x))*"+str(radius))           

Model=polar
__call__=Model
