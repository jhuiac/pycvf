#!/bin/bash

D=~/Music/ja/home/tranx/Desktop/


FRAMESIZE=256
FRAMEOVERLAP=128

## 1. display the spectrogram
pycvf_model_features_view --db "limit(exploded(
                                 transformed(db=sound.directory('$D'),
				             model=(pycvf.nodes.audio.spectrogram(dest_frame_size=$FRAMESIZE,dest_frame_overlap=$FRAMEOVERLAP)|pycvf.nodes.spectrum.blockified(300,name='b')),
				             datatype=pycvf.datatypes.generated.Datatype(pycvf.datatypes.basics.Label.Datatype),
				             modelpath='/b/'
				 ),
			        LF('pycvf.structures.generator').DefaultStructure()),10)" \
				--model "free('numpy.roll(20*numpy.log10(1.0001+numpy.abs(numpy.dstack(x))).mean(axis=1),x[0].shape[0]//2,axis=0).T[:,:,numpy.newaxis].repeat(3,axis=2).copy(\"C\")',datatype=pycvf.datatypes.image.Datatype)|image.normalize()"  -i 0.1
				
## 2. extract some feature from the spetrogram				
pycvf_model_features_view --db "limit(exploded(
                                 transformed(db=sound.directory('$D'),
				             model=(pycvf.nodes.audio.spectrogram(dest_frame_size=$FRAMESIZE,dest_frame_overlap=$FRAMEOVERLAP)|pycvf.nodes.spectrum.blockified(300,name='b')),
				             datatype=pycvf.datatypes.generated.Datatype(pycvf.datatypes.basics.Label.Datatype),
				             modelpath='/b/'
				 ),
			        LF('pycvf.structures.generator').DefaultStructure()),10)" \
				--model "(
				         free('numpy.dstack(x)')
					 +debug.info()
				         -(free('numpy.roll(20*numpy.log10(1.0001+numpy.abs(x)).mean(axis=1),x.shape[0]//2,axis=0).T')
 					  -free('x[:,:,numpy.newaxis].repeat(3,axis=2).copy(\"C\")',datatype=pycvf.datatypes.image.Datatype)
					  -image.normalize()
				          +image.obs([[0,-1],[-1,0],[1,0],[0,0]])
					  -free('x[:(x.shape[0]//200*200),:].reshape(x.shape[0]//200,200*x.shape[1])',datatype=pycvf.datatypes.image.Datatype)
					  -image.normalize()
					  )
					  )"  -i 0.1
					  
					  
pycvf_model_features_view --db "limit(exploded(
                                 transformed(db=sound.directory('$D'),
				             model=(pycvf.nodes.audio.spectrogram(dest_frame_size=$FRAMESIZE,dest_frame_overlap=$FRAMEOVERLAP)|pycvf.nodes.spectrum.blockified(300,name='b')),
				             datatype=pycvf.datatypes.generated.Datatype(pycvf.datatypes.basics.Label.Datatype),
				             modelpath='/b/'
				 ),
			        LF('pycvf.structures.generator').DefaultStructure()),10)" \
				--model "(
				         free('numpy.dstack(x)')
				         -(free('numpy.roll(20*numpy.log10(1.0001+numpy.abs(x)).mean(axis=1),x.shape[0]//2,axis=0).T')
 					  -free('x[:,:,numpy.newaxis].repeat(3,axis=2).copy(\"C\")',datatype=pycvf.datatypes.image.Datatype)
					  -image.normalize()
				          +image.obs([[0,-1],[-1,0],[1,0],[0,0]])
					  -free('x[:(x.shape[0]//200*200),:].reshape(x.shape[0]//200,200*x.shape[1])',datatype=pycvf.datatypes.image.Datatype)
					  -image.normalize()
					  )
					  )"  -i 0.1					  

