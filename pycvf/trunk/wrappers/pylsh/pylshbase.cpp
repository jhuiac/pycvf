#include "pylshbase.h"
#include <cstdio>

template class MultiProbeLshIndex < EMatrix::Accessor >;

int pylsh_verbose=2;


PyMPLSHIdx::PyMPLSHIdx (int m, int n, float *data):
emdata (m, n, data),
accessor (emdata)
{
  if (pylsh_verbose) 
     {  
	fprintf(stderr,"New PyMPLSHIdx\n");
     }
   
  this->desired_recall = 1.0;
  W = 1.0;
  M = 1;
  L = 1;			//hash tables
  R = numeric_limits < float >::max ();	// nearest neighbor range
  H = 1017881;			// "hash table size, use the default value.")
  this->index = NULL;
//       l1=new metric::l1<float>(n);
  index = new Index ();		//, *l1);     

}

PyMPLSHIdx::~PyMPLSHIdx ()
{
  if (pylsh_verbose) 
     {  
	fprintf(stderr,"Del PyMPLSHIdx\n");
     }   
  delete this->index;
  this->index = NULL;
}


int
PyMPLSHIdx::load_index (const char *index_file)
{
  if (pylsh_verbose) 
     {  
	fprintf(stderr,"Load Index '%s'\n",index_file);
     }   
  ifstream is (index_file, ios_base::binary);
  if (is)
    {
      is.exceptions (ios_base::eofbit | ios_base::failbit | ios_base::badbit);
      index->load (is);
      // verify(is);
    }
  else 
     {
	fprintf(stderr,"WARNING LSHINDEX has failed to open your indexfile '%s'\n",index_file);	
	return 0;
     }
   
  return 1;
}

    // **************************************************************************************************************************************************************
    // BUILD
    // **************************************************************************************************************************************************************


void
PyMPLSHIdx::build_index ()
{
  if (pylsh_verbose) 
     {  
	fprintf(stderr,"Build Index\n");
     }      
  // We define a short name for the MPLSH index.
  Index::Parameter param;

  // Setup the parameters.  Note that L is not provided here.
  param.W = W;
  param.range = H;		// See H in the program parameters.  You can just use the default value.
  param.repeat = M;
  param.dim = emdata.getDim ();
  DefaultRng rng;

  index->init (param, rng, L);

  printf ("inserting %d lines of data of dimension %d\n", emdata.getSize (),
	  emdata.getDim ());
  for (unsigned i = 0; i < emdata.getSize (); ++i)
    {
/*      for (unsigned j=0;j<emdata.getDim();++j) 
	 {
	    printf("%f ",emdata[i][j]);
	 }
       printf("\n");
 */
      index->insert (i, emdata[i]);
    }
}

int
PyMPLSHIdx::save_index (const char *index_file)
{
  if (pylsh_verbose) 
     {  
	fprintf(stderr,"Save Index\n");
     }      
  ofstream os (index_file, ios_base::binary);
  os.exceptions (ios_base::eofbit | ios_base::failbit | ios_base::badbit);
  index->save (os);
  return 1;

}

    // **************************************************************************************************************************************************************
    // QUERIES
    // **************************************************************************************************************************************************************

void
PyMPLSHIdx::query (float *queryv, int Q, int K,int *res_keys, double *res_dists, int *k,
		   int do_recall)
{
  if (pylsh_verbose) 
     {  
	fprintf(stderr,"Query Index\n");
     }      
  int MX;
  metric::l2sqr < float >l2sqr (emdata.getDim ());
  TopkScanner < EMatrix::Accessor, metric::l2sqr < float  > >query (accessor, l2sqr, K, R);
  vector < Topk < unsigned > >topks (Q);

  if (do_recall)
    // Specify the required recall
    // and let MPLSH to guess how many bins to probe.
    {
      for (unsigned i = 0; i < Q; ++i)
	{
	  // Query for one point.
	  float desired_recal=do_recall;
	  query.reset (queryv+(i*emdata.getDim()));
	   /*
	   printf("qury="); 
	  for (unsigned j=0; j<emdata.getDim();j++ ) {
	     printf(" %f", (queryv+(i*emdata.getDim()))[j] ); 
	  }
	   printf("\n");*/
	  index->query_recall (queryv+(i*emdata.getDim()), desired_recal, query);
	   k[i]=query.cnt ();
	   MX=k[i];
	   if (MX>K) 
	     MX=K;
	   for (unsigned j=0; j<MX;j++ ) {
  	     res_keys[i*K+j] = query.topk()[j].key;
             res_dists[i*K+j] = query.topk()[j].dist;
	  }
	}
    }
  else
    // specify how many bins to probe.
    {
      for (unsigned i = 0; i < Q; ++i)
	{
	  query.reset (queryv+(i*emdata.getDim()));
	  index->query (queryv+(i*emdata.getDim()),1, query);
	   k[i]=query.cnt ();
	   MX=k[i];
	   if (MX>K) 
	     MX=K;	   
	   for (unsigned j=0; j<MX;j++ ) {
  	     res_keys[i*K+j] = query.topk()[j].key;
             res_dists[i*K+j] = query.topk()[j].dist;
	  }
	}
    }


}
