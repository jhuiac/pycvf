D=/databases/101ObjectCategories/PNGImages/; 
pycvf_dbshow --db "exploded(db=LF('pycvf.databases.imageset.directory','$D'),
                            structure=pycvf.structures.generator.DefaultStructure()
			   )" -A 1

pycvf_dbshow --db "image.directories('$D',dbop=lambda x:limit(x,10),rescale=(256,256,'T'))" -A 1

##
## Training models on CALTECH 101
##

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

