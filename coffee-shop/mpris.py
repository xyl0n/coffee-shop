#!/usr/bin/env python2

import dbus
import dbus.service

class Mpris (dbus.service.Object):
    
    def __init__ (self, name):
        
        bus_name = dbus.service.BusName ("org.mrpis.MediaPlayer2." + name, bus = dbus.SessionBus ())
        dbus.service.Object.__init__ (self, bus_name, "/org/mpris/MediaPlayer2")
        
    def set_information (self):
        
        self.data = dbus.Dictionary ({
                        "xesam:album"  : '',
                        "xesam:title"  : 'Acoustics',
                        "xesam:artist" : '',
                        "mpris:artUrl" : '',},
                        "sv", variant_level = 1)
        
        
        
    
