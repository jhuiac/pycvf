from pycvf.nodes.image.maps import polar
from pycvf.nodes.image.spectral import fft
from pycvf.nodes.image.spectral import ifft
from pycvf.nodes.image import gaussian
from pycvf.nodes.image import rescaled
from pycvf.nodes import free
from pycvf.nodes.debug import write

def psychovisual(resolution=(8,8),invert=False,fisheye=2,logoff=1,phase=None,blur=3,*args,**kwargs):
    if (not invert):
       return (fft.__call__()
              -free.__call__('numpy.log(%d+numpy.abs(x))'%(logoff,))
              -polar.__call__(fisheye=fisheye)
              -gaussian.__call__(blur)
              -rescaled.__call__(resolution+('R',)))
    else:
       return (rescaled.__call__(resolution+('R',))
              -polar.__call__(invert=True,fisheye=fisheye)
              -free.__call__("numpy.exp(x)-%d"%(logoff,))
              #-rephase(phase)
              #-free.__call__("(numpy.abs(thesrc['src|_|___submodel__0001_imgfft_'])*numpy.exp(1J*numpy.angle(thesrc['src|_|___submodel__0001_imgfft_']).reshape(resolution+(1,))))",resolution=resolution)#*numpy.exp(1J*numpy.angle(numpy.fft(thesrc['src|_'])))")              
              -free.__call__("(x*numpy.exp(1J*numpy.angle(thesrc['src|_|___submodel__0001_imgfft_']).reshape(resolution+(1,))))",resolution=resolution)#*numpy.exp(1J*numpy.angle(numpy.fft(thesrc['src|_'])))")
              #-free.__call__("(x*numpy.exp(1J*numpy.angle(thesrc['src|_']).reshape(resolution+(1,)))).reshape(resolution+(1,))",resolution=resolution)#*numpy.exp(1J*numpy.angle(numpy.fft(thesrc['src|_'])))")                            
              #-free.__call__("x*numpy.exp(1J*numpy.angle(numpy.fft(thesrc['src|_|___submodel__0001_imgfft_'])))")
              -ifft.__call__()
              -free.__call__("numpy.real(x)")
              #-write.__call__()
              )
   

Model=psychovisual
__call__=Model
