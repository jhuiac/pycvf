D=/databases/101ObjectCategories/PNGImages/; 
pycvf_dbshow --db "exploded(db=LF('pycvf.databases.imageset.directory','$D'),
                            structure=pycvf.structures.generator.DefaultStructure()
			   )" -A 1

pycvf_dbshow --db "image.directories('$D',dbop=lambda x:limit(x,10),rescale=(256,256,'T'))" -A 1

pycvf_dbshow --db "caltech101()" -A 1

##
## Training models on CALTECH 101
##

pycvf_dbshow --db "exploded(caltech101(),structure=pycvf.structures.spatial.RegularPatchEdges(1,(32,32),0))" -A 1
pycvf_dbshow --db "exploded(caltech101(),structure=pycvf.structures.spatial.RegularPatchEdges(1,(32,32),1))" -A 1
pycvf_dbshow --db "exploded(caltech101(),structure=pycvf.structures.spatial.RegularPatches(1,(32,32),1))" -A 1




pycvf_model_features_view  --db 'caltech101()' -m 'LF("pycvf.nodes.image.descriptors.HOG")|(free("x.reshape(1,-1)",datatype=pycvf.datatypes.basics.NumericArray.Datatype)|(vectors.PCA(10,burnin=100)|free("x.flat",datatype=pycvf.datatypes.histogram.Datatype)))'


pycvf_compute_features --db 'caltech101()' -m 'LF("pycvf.nodes.image.descriptors.HOG")' -t "caltech101-HOG" 
pycvf_model_run --db 'as_once(from_trackfile(t="caltech101-HOG"))'



pycvf_model_run \\
  --db "image.directories('$D',dbop=lambda x:limit(x,10),rescale=(256,256,'T'))" \
  -m "PL(
         image.descriptor.LBP(),
	 vectors.train_classifier_and_confusion_matrix(ML('CLS.weka_bridge','weka.classifiers.trees.J48'))
	)"
  -s "caltech101-trees"
	
pycvf_model_run \\
  --db "image.directories('$D',dbop=lambda x:limit(x,10),rescale=(256,256,'T'))" \
  -m "PL(
         image.descriptor.LBP(),
	 vectors.svm.libsvm()
	)" \
  -s "caltech101-svm"


pycvf_model_run --db "image.directories('$D',dbop=lambda x:limit(x,10),rescale=(256,256,'T'))" \
  -m "PL(
         image.keypoints.SIFT(),
	 vectors.bagorwords(),
	 vectors.train_classifier_and_confusion_matrix(ML('CLS.weka_bridge'))
	)"

