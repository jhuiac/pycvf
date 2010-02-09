# -*- coding: utf-8 -*-
[  ('inriaperson',
         {  
            'title':'INRIA Person',
            'url':["http://pascal.inrialpes.fr/data/human/INRIAPerson.tar"],
            'disclaimer':"""
THIS DATA SET IS PROVIDED "AS IS" AND WITHOUT ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
The images provided above may have certain copyright issues. We take no guarantees or responsibilities, whatsoever, arising out of any copyright issue. Use at your own risk.
                         """,
           'decompress' : [ untar ], 
           'uncompressed' :  987*Mb
         }),
  ('inriahollidays',
         {
          'title':'INRIA Hollidays images',
          'url':["http://pascal.inrialpes.fr/data/holidays/jpg1.tar.gz","http://pascal.inrialpes.fr/data/holidays/jpg2.tar.gz"],
           'uncompressed' :  -1,
           'decompress' : [ untargz ],    
         }),
  ('inriahollidays_flickrdescripors',
         {
          'title':'INRIA Hollidays Flickr60k descriptors',
          'url':['http://pascal.inrialpes.fr/data/holidays/flickr60K.siftgeo.gz'],
           'uncompressed' :  -1,
           'decompress' : [ ungz ],    
         }),
]
