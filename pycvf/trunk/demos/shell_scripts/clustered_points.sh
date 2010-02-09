#!/bin/bash

pycvf_dbshow --db "vectorset.from_vectordb(lambda:vectors.clustered_points(ndim=2,sigma=2))"
pycvf_model_features_view --db "vectorset.from_vectordb(lambda:vectors.clustered_points(ndim=2,sigma=0.2))" --model "LN('naive')|LF('pycvf.nodes.vectorset.train_and_sample',ML('histogram',(20,20),(0,0),(20,20)))"
pycvf_model_features_view --db "vectorset.from_vectordb(lambda:vectors.clustered_points(ndim=2,sigma=0.2))" --model "LN('naive')|LF('pycvf.nodes.vectorset.train_and_sample',ML('pyem_gmm',2,10))"
pycvf_model_features_view --db "vectorset.from_vectordb(lambda:vectors.clustered_points(ndim=2,sigma=0.2))" --model "LN('naive')|LF('pycvf.nodes.vectorset.train_and_sample',ML('parzen',2,0.7))"

pycvf_model_features_view --db "vectorset.from_vectordb(lambda:vectors.clustered_points(ndim=2,sigma=0.2))" --model "LN('naive')|LF('pycvf.nodes.vectorset.train_and_2dtestmap',ML('histogram',(20,20),(0,0),(20,20)))"
pycvf_model_features_view --db "vectorset.from_vectordb(lambda:vectors.clustered_points(ndim=2,sigma=0.2))" --model "LN('naive')|LF('pycvf.nodes.vectorset.train_and_2dtestmap',ML('pyem_gmm',2,10))"
pycvf_model_features_view --db "vectorset.from_vectordb(lambda:vectors.clustered_points(ndim=2,sigma=0.2))" --model "LN('naive')|LF('pycvf.nodes.vectorset.train_and_2dtestmap',ML('parzen',2,0.5,100),48,48)"

pycvf_model_features_view --db "vectorset.from_vectordb(lambda:vectors.clustered_points(ndim=2,sigma=0.2))" --model "LN('naive')|LF('pycvf.nodes.vectorset.train_decision_and_confusion_matrix',ML('svm_shogun'),vectorset.random_vectors(ndim=2,amplitude=20))"


