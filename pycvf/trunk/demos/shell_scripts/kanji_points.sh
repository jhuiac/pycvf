DB="LF('pycvf.databases.vectorset.points_sampled_according_to_image',image.kanji(invert=True),48**1.3)" 
timelimit 10 pycvf_dbshow --db $DB
timelimit 15 pycvf_model_features_view --db $DB --model "LN('naive')|LF('pycvf.nodes.vectorset.train_and_2dtestmap',ML('DE.histogram',(20,20),(0,0),(48,48)))"
timelimit 15 pycvf_model_features_view --db $DB --model "LN('naive')|LF('pycvf.nodes.vectorset.train_and_2dtestmap',ML('DE.pyem_gmm',2,10))"
timelimit 15 pycvf_model_features_view --db $DB --model "LN('naive')|LF('pycvf.nodes.vectorset.train_and_2dtestmap',ML('DE.parzen',2,0.5,10),48,48)"
