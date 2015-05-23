#!/usr/bin/env python2

import os, sys, glob, DistUtilsExtra.auto

# Create data files
data = [ ('/usr/share/coffee-shop', glob.glob('coffee-shop/*')),
         ('/usr/bin', glob.glob ('bin/*')),
         ('/usr/share/coffee-shop/icons', glob.glob('share/coffee-shop/icons/*')),
         ('/usr/share/coffee-shop/sounds', glob.glob('share/coffee-shop/sounds/*')),
         ('/usr/share/icons/hicolor/scalable/apps', glob.glob('share/icons/scalable/*')),
         ('/usr/share/applications', glob.glob('share/coffee-shop.desktop')),
         ('/usr/share/coffee-shop', glob.glob('share/coffee-shop/mpv.conf')) ]

# Setup stage
DistUtilsExtra.auto.setup(
    name         = "coffee-shop",
    version      = "0.1",
    description  = "Coffee Shop Noise Player",
    author       = "Aporva Varshney",
    author_email = "",
    url          = "",
    license      = "GPL3",
    data_files   = data
    )
