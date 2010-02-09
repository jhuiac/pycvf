#!/bin/bash

D=~/Music/ja/home/tranx/Desktop/

pycvf_model_features_view --db "exploded(
                                 transformed(db=sound.directory('$D'),
				             model=(pycvf.nodes.audio.spectrogram(dest_frame_size=256,dest_frame_overlap=128)|pycvf.nodes.spectrum.blockified(300,name='b')),
				             datatype=pycvf.datatypes.generated.Datatype(pycvf.datatypes.basics.Label.Datatype),
				             modelpath='/b/'
				 ),
			        LF('pycvf.structures.generator').DefaultStructure())" \
				--model "free('numpy.roll(20*numpy.log10(1.0001+numpy.abs(numpy.dstack(x))).mean(axis=1),x[0].shape[0]//2,axis=0).T[:,:,numpy.newaxis].repeat(3,axis=2).copy(\"C\")',datatype=pycvf.datatypes.image.Datatype)|image.normalize()"  -i 0.1

