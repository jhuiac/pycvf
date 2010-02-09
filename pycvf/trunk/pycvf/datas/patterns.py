# -*- coding: utf-8 -*-
import numpy


C3down=numpy.array([ [ 1, 1, 1 ], 
                     [ 0, 2, 0 ] ])
C3right=C3down.T
C3up=numpy.flipud(C3down)
C3left=numpy.fliplr(C3right)


C5down=numpy.array([ [ 1, 1, 1, 1, 1 ], 
                     [ 0, 0, 2, 0, 0 ] ])
C5right=C5down.T
C5up=numpy.flipud(C5down)
C5left=numpy.fliplr(C5right)


C7down=numpy.array([ [ 1, 1, 1, 1, 1, 1, 1], 
                     [ 0, 0, 0, 2, 0, 0, 0 ] ])
C7right=C7down.T
C7up=numpy.flipud(C7down)
C7left=numpy.fliplr(C7right)

AC_V4=numpy.array([ [ 0, 1, 0 ], 
                    [ 1, 2, 1 ],
                    [ 0 ,1, 0 ] ])

                    
AC_V8=numpy.array([ [ 1, 1, 1 ], 
                    [ 1, 2, 1 ],
                    [ 1 ,1, 1 ] ])

