import os, subprocess, sys

class MPlayer(object):

    '''
        Class for interfacing with MPlayer. 
        Provides functions to load files, set volume and play/pause
    '''
    
    def __init__(self):
        # Start the mplayer process
        self.mplayer = subprocess.Popen(
                ['mplayer', '-slave', '-quiet', '-idle', '-softvol', '-msglevel', 
                 'statusline=6', '-msglevel', 'global=6', '-really-quiet', '-volume', '0'],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
                
        self.sound_file = '' # This stores the sound file location
        self.name = '' # This stores the name to be read by other classes
        self.volume = 0 # To allow classes to access the output volume   

    def load_file (self, filename):
        self.sound_file = filename
        name_start = filename.rfind ('/')
        extension_start = filename.rfind ('.')
        self.name = filename [name_start + 1:extension_start]
        
        self.mplayer.stdin.write('loadfile ' + filename + '\n')
        self.set_volume (self.volume)
        
    def set_volume (self, vol):
        self.volume = vol
        self.mplayer.stdin.write('pausing_keep set volume ' + str (vol) + '\n')
        
    def mute (self): self.mplayer.stdin.write('pausing_keep mute 1\n')
         
    def quit (self):
        self.mplayer.stdin.write('quit\n')
        self.mplayer.kill ()
        return
        
    def pause (self): self.mplayer.stdin.write ('pause\n') # Confusingly, this pauses and plays it
