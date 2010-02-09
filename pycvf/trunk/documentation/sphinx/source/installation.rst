PyCVF Installation Procedure
============================

PyCVF is not under 1.0 release, but we are slowly getting ready for a 0.1 release,
hence it is not targetted to "end-user yet" that do not want to program at all,
for the moment it is targeted to researchers and programmers, that want to use a cutting edge framework,
want to use Python, and are willingful to contribute to the opensource code

So forth, all installations are done in a way, were the user is invited to have its own branch of the code
and to modify it. In further version, we may think about providing to the user some specific "project" branch
like web-framework do it. For the moment it is not the case.

 

Linux
-----

If you are under ubuntu, the easiest way to do the installation for the moment is to use the installation script : pycvf_install_on_ubuntu.sh  

This installation script, will check that you have the necessary packages on your system, retrieve branch of the project, modify your ".bashrc" 
to make your python envirionment ready. Invite you to make registration, and compile the additional wrappers for your system.
If you are lucky everything shall go fine, else try to understand what's going on, and if necessary open a ticket on the installation forum.


Hence, once the installation has been finished be sure to reload your bashrc::

  ./pycvf_install_on_ubuntu.sh
  . ~/.bashrc


Once you  finished that you should be able to watch picture from a directory by doing::

  pycvf_dbshow --db 'image.directory(select_existing_directory())'


Ubuntu/Debian packages shall be made available in near future from  My Launchpad PPA  . For the moment, there is no automated install for you. The install script may work on your distrib. 
 
However, the best is to read the install-script, and to translate it for your distrib, 

Other Unixes and MacOS
----------------------

For the moment you are on your own, but basically if you follow the instructions that are applied by the pycvf_install_on_ubuntu script, you should be able to get a working version of PyCVF on your mac.



Windows
-------
 We have already managed to make work PyCVF under windows, but you need to be quite experienced with the porting of unix software to windows. For the moment, there is no distribution of PyCVF for windows.
