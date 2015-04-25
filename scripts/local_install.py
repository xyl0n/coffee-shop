#!/usr/bin/env python2

import shutil, glob, os

home = os.path.expanduser('~') + '/.local/share/acoustics'
if not os.path.exists(home):
    os.mkdir(home)
    
shutil.copy (''.join(glob.glob (os.pardir + '/share/local/config')), home)

