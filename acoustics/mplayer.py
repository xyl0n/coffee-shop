import os, subprocess, sys
from ctypes import *
import locale
locale.setlocale(locale.LC_NUMERIC, 'C')

class MPlayer(object):

    '''
        Class for interfacing with MPlayer. 
        Provides functions to load files, set volume and play/pause
    '''
        
    def __init__(self, conf_file_path):
    
        self.mpv = CDLL ('libmpv.so')
        self.handle = self.mpv.mpv_create ()
                
        self.sound_file = '' # This stores the sound file location
        self.name = '' # This stores the name to be read by other classes
        self.volume = 100 # To allow classes to access the output volume   
        
        self.mpv.mpv_load_config_file(self.handle, c_char_p (conf_file_path));
        
        self.mpv.mpv_initialize (self.handle)
        

    def load_file (self, filename):
        self.sound_file = filename
        name_start = filename.rfind ('/')
        extension_start = filename.rfind ('.')
        self.name = filename [name_start + 1:extension_start]
        
        _arg_type = c_char_p * 3
        args = _arg_type (b'loadfile', filename, c_char_p())
        self.mpv.mpv_command (self.handle, args)
                
        self.set_volume (self.volume)
        
    def set_volume (self, vol):

        self.mpv.mpv_set_property_string (self.handle, 'volume', str(vol))  
        self.volume = vol
        
        self.unmute ()

        
    def mute (self): self.mpv.mpv_set_property_string (self.handle, 'mute', 'yes')  
    
    def unmute (self): self.mpv.mpv_set_property_string (self.handle, 'mute', 'no')  
         
    def quit (self):
        self.mpv.mpv_terminate_destroy (self.handle)
        return
        
    def pause (self): self.mpv.mpv_set_property_string (self.handle, 'pause', 'yes')  
    def play (self): self.mpv.mpv_set_property_string (self.handle, 'pause', 'no')
