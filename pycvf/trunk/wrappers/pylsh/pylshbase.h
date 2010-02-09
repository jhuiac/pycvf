/*
#include <boost/program_options.hpp>
#include <boost/progress.hpp>
#include <boost/format.hpp>
#include <boost/timer.hpp>
*/
#include <lshkit.h>
#include <cassert>
#include <cstdio>

using namespace std;
using namespace lshkit;

extern int pylsh_verbose;

class EMatrix{
    int r, c;
    float * matrixdata;
public:
    EMatrix(int r_,int c_,float * data_)
        : r(r_), c(c_), matrixdata(data_) {}

    /// Access the ith vector.
    const float *operator [] (int i) const {
         if (pylsh_verbose>=2)
	 { 
           fprintf(stderr, "access vector %d\n",i);
	 }       
       return matrixdata+c*i; }

    /// Access the ith vector.
    float *operator [] (int i) {
        if (pylsh_verbose>=2)
	 { 
           fprintf(stderr, "access vector %d\n",i);
	 }       
       return  matrixdata+c*i; 
    }

    /// Get the list of vectors (be careful!).
    float **const getVecs () const {
        if (pylsh_verbose)
	 { 
           fprintf(stderr, "get Vecs\n");
	 }       
        assert(0); // Used ???
        return NULL;
    }

    int getDim () const {return c; }
    int getSize () const {return r; }

class Accessor
{
    const EMatrix  * em;
    boost::dynamic_bitset<> flags;
public:
    typedef unsigned Key;
    Accessor() :em(NULL){    if (pylsh_verbose) {    fprintf(stderr, "accessor CTOR\n");assert(0);     }  }
    Accessor(const EMatrix & e) :em(&e),flags(e.getSize()) {  if (pylsh_verbose) {fprintf(stderr, "accessor CTORII\n");}       }


    void reset ()
    {
        if (pylsh_verbose)
	 { 
           fprintf(stderr, "accessor reset\n");
	 }
       
        flags.reset();
    }

    bool mark (unsigned key)
    {
        if (pylsh_verbose) {
          fprintf(stderr, "mark key=%d\n",key);
	}
        if (flags[key]) return false;
        flags.set(key);
        return true;
    }

    const float *operator () (unsigned key)
    {
        if (pylsh_verbose) { fprintf(stderr, "accessor key=%d\n",key); }
        return (*em)[key];
    }


};

};

class PyMPLSHIdx  {
    typedef MultiProbeLshIndex<unsigned> Index;
    float W, R, desired_recall;
    unsigned M, L, H;
    unsigned Q, K, T;
    bool do_recall;
    EMatrix emdata;
    EMatrix::Accessor accessor;
    metric::l1<float> * l1;   
   
    Index  * index;
    public:
    PyMPLSHIdx(int m, int n, float *data);
    ~PyMPLSHIdx();
    void build_index();
    void query(float * queryv, int Q, int w,int * res_keys,double *res_dists, int * k, int do_recall);   
    int load_index(const char * index_file);
    int save_index(const char * index_file);    
};
 



