DB="limit(LF('pycvf.databases.vectorset.points_sampled_according_to_image',image.kanji(invert=True),48**1.3),6)"
pycvf_dbshow --db $DB
pycvf_model_features_view --db $DB --model "LN('naive')|LF('pycvf.nodes.vectorset.train_and_2dtestmap',ML('DE.histogram',(20,20),(0,0),(48,48)))"
pycvf_model_features_view --db $DB --model "LN('naive')|LF('pycvf.nodes.vectorset.train_and_2dtestmap',ML('DE.pyem_gmm',2,10))"
pycvf_model_features_view --db $DB --model "LN('naive')|LF('pycvf.nodes.vectorset.train_and_2dtestmap',ML('DE.parzen',2,0.5,10),48,48)"
