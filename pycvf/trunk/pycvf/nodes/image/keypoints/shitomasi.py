# -*- coding: utf-8 -*-
import math
import numpy
from pycvf.core import genericmodel
from pycvf.datatypes import image

import zopencv

def shitomasi(image, quality_level = 0.1, min_distance = 5, eig_block_size = 3, use_harris = 0,MAX_CORNERS = 100,k=0.04):
                timage=image.mean(axis=2).astype(numpy.uint8)
		cornersn=numpy.zeros((MAX_CORNERS,2),dtype=numpy.float32)
		corners=zopencv.zopencv_pclasses.PointerOnCvPoint2D32f(zopencv.zopencv_core.memory_addr_of_numpy_array(cornersn))
		corner_count = numpy.array([MAX_CORNERS],dtype=int)
                mask=zopencv.zopencv_pclasses.PointerOnCvMat(0)
		eig_image=timage.astype(numpy.float32)
		temp_image=timage.astype(numpy.float32)
		zopencv.cvGoodFeaturesToTrack(timage,
				eig_image,                    
				temp_image,
				corners.get_pointer(),
				corner_count,
				quality_level,
				min_distance,
				mask.get_pointer(),
				eig_block_size,
				use_harris,
                                k)
		return cornersn

Model=genericmodel.pycvf_model_function(image.Datatype,image.Datatype)(shitomasi)
__call__=Model