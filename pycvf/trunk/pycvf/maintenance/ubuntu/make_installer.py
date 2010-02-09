import os

buffer=file('pycvf_install_on_ubuntu.sh.in').read()
buffer=buffer.replace('%BUILDREQUIREDLIST%'," ".join(map(lambda x:x.split('(')[0].strip(),file('BUILDREQUIRED').readlines())))
buffer=buffer.replace('%REQUIREDLIST%'," ".join(map(lambda x:x.split('(')[0].strip(),file('REQUIRED').readlines())))
file('pycvf_install_on_ubuntu.sh','w').write(buffer)
