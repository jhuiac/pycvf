#!/bin/bash

pycvf_dbshow --db "vectorset.from_vectordb(lambda:vectors.clustered_points(ndim=2,sigma=2))"
pycvf_model_features_view --db "vectorset.from_vectordb(lambda:vectors.clustered_points(ndim=2,sigma=0.2))" --model "LN('naive')|LF('pycvf.nodes.vectorset.train_and_sample',ML('DE.histogram',(20,20),(0,0),(20,20)))"
pycvf_model_features_view --db "vectorset.from_vectordb(lambda:vectors.clustered_points(ndim=2,sigma=0.2))" --model "LN('naive')|LF('pycvf.nodes.vectorset.train_and_sample',ML('DE.pyem_gmm',2,10))"
pycvf_model_features_view --db "vectorset.from_vectordb(lambda:vectors.clustered_points(ndim=2,sigma=0.2))" --model "LN('naive')|LF('pycvf.nodes.vectorset.train_and_sample',ML('DE.parzen',2,0.7))"

pycvf_model_features_view --db "vectorset.from_vectordb(lambda:vectors.clustered_points(ndim=2,sigma=0.2))" --model "LN('naive')|LF('pycvf.nodes.vectorset.train_and_2dtestmap',ML('DE.histogram',(20,20),(0,0),(20,20)))"
pycvf_model_features_view --db "vectorset.from_vectordb(lambda:vectors.clustered_points(ndim=2,sigma=0.2))" --model "LN('naive')|LF('pycvf.nodes.vectorset.train_and_2dtestmap',ML('DE.pyem_gmm',2,10))"
pycvf_model_features_view --db "vectorset.from_vectordb(lambda:vectors.clustered_points(ndim=2,sigma=0.2))" --model "LN('naive')|LF('pycvf.nodes.vectorset.train_and_2dtestmap',ML('DE.parzen',2,0.5,100),48,48)"

pycvf_model_features_view --db "vectorset.from_vectordb(lambda:vectors.clustered_points(ndim=2,sigma=0.2))" --model "LN('naive')|LF('pycvf.nodes.vectorset.train_decision_and_confusion_matrix',ML('DEC.svm_shogun'),vectorset.random_vectors(ndim=2,amplitude=20))"
pycvf_model_features_view --db "vectorset.from_vectordb(lambda:vectors.clustered_points(ndim=2,sigma=0.2, clusters=3,shuffled=False))" --model "LN('naive')|LF('pycvf.nodes.vectorset.train_classification_and_confusion_matrix',ML('CLS.weka_bridge','weka.classifiers.functions.LibSVM'),label='clusterid')"

