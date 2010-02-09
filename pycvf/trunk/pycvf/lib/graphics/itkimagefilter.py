import itk
import numpy

itkUC1=itk.image[scipy.UC,1]
itkUC2=itk.image[scipy.UC,2]
itkUC3=itk.image[scipy.UC,3]
itkUC4=itk.image[scipy.UC,4]
itkUS1=itk.image[scipy.US,1]
itkUS2=itk.image[scipy.US,2]
itkUS3=itk.image[scipy.US,3]
itkUS4=itk.image[scipy.US,4]
itkUL1=itk.image[scipy.UL,1]
itkUL2=itk.image[scipy.UL,2]
itkUL3=itk.image[scipy.UL,3]
itkUL4=itk.image[scipy.UL,4]
itkF1=itk.image[scipy.F,1]
itkF2=itk.image[scipy.F,2]
itkF3=itk.image[scipy.F,3]
itkF4=itk.image[scipy.F,4]

itkt2numpy_type={
  ("UC",1):(numpy.uint8,1),
  ("UC",2):(numpy.uint8,2), 
  ("UC",3):(numpy.uint8,3), 
  ("UC",4):(numpy.uint8,4), 
  ("US",1):(numpy.uint16,1),
  ("US",2),(numpy.uint16,2),
  ("US",3),(numpy.uint16,3),
  ("US",4),(numpy.uint16,4),
  ("F",1),(numpy.float,1), 
  ("F",2),(numpy.float,2), 
  ("F",3),(numpy.float,3), 
  ("F",4),(numpy.float,4) 
}


numpy2itk_dict={
  (numpy.uint8,1) : itkUC1,
  (numpy.uint8,2) : itkUC2,
  (numpy.uint8,3) : itkUC3,
  (numpy.uint8,4) : itkUC4,
  (numpy.uint16,1) : itkUS1,
  (numpy.uint16,2) : itkUS2,
  (numpy.uint16,3) : itkUS3,
  (numpy.uint16,4) : itkUS4,
  (numpy.float,1) : itkF1,
  (numpy.float,2) : itkF2,
  (numpy.float,3) : itkF3,
  (numpy.float,4) : itkF4
}

class ItkImageFilter:
    def __init__(self, filtername, itktype, channels, **kwargs):
        self.filter=eval("itk."+filtername+"ImageFilter[itk"+itktype+str(channels)+",itk"+itktype+str(channels)+"].New()")
        self.itk_py_converter = itk.PyBuffer[eval("itk"+itktype+str(channels))]
        for x in kwargs.items():
            exec "self.filter.Set"+x[0][0].upper()+X[0][1:]+"(v)" in {'self':self, 'v':x[1]} 
    def process(self,image):
        self.filter.SetInput(self.itk_py_converter.GetImageFromArray( image ))
        self.filter.Update()
        return self.itk_py_converter.GetArrayFromImage( self.filter.GetOutput() ) 

