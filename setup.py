#!/usr/bin/env python2

import os, sys, glob, DistUtilsExtra.auto

# Create data files
data = [ ('/usr/share/acoustics', glob.glob('acoustics/*')),
         ('/usr/bin', glob.glob ('bin/*')),
         ('/usr/share/acoustics/icons', glob.glob('share/acoustics/icons/*')),
         ('/usr/share/acoustics/sounds', glob.glob('share/acoustics/sounds/*')),
         ('/usr/share/acoustics', glob.glob('share/acoustics/mpv.conf')) ]

# Setup stage
DistUtilsExtra.auto.setup(
    name         = "acoustics",
    version      = "0.0.1",
    description  = "Acoustics Noise Player",
    author       = "Aporva Varshney",
    author_email = "",
    url          = "",
    license      = "GPL3",
    data_files   = data
    )
