#!/usr/bin/env python2

import os, subprocess, sys, errno
from threading import Thread
from gi.repository import GObject, Gtk, GLib
from gi.repository import AppIndicator3 as appindicator
from mplayer import MPlayer
from interface import Window
                                                    
class App (object):
    
    ''' 
        Main class to connect the backend and frontend
    '''
        
    class State (object):
        PLAYING = 0
        PAUSED = 1
    
    def __init__(self):
        
        # Variables
        self.global_vol = 100
        self.app_state = self.State.PLAYING

        if sys.platform == 'linux2':
            home = os.path.expanduser("~")
            self.local_dir = home + "/.local/share/acoustics/"
            self.data_dir = "/usr/share/acoustics/"
            self.sound_dir = self.data_dir + "sounds/"
            self.icon_dir = self.data_dir + "icons/"
            self.mpv_conf = self.data_dir + "mpv.conf"
                                
        # List to hold mplayer processes
        self.player_list = []
        self.populate_player_list ()
        
        # Create a dictionary to hold volumes for different sounds
        self.player_volumes = {}
        with open (self.local_dir + "config", 'r') as config_file:
            line = config_file.readline()
            while line:
                separator_index = line.rfind(":")
                newline_index = line.rfind("\n")
                player_name = line[:separator_index]
                volume = float(line[separator_index + 1:newline_index])
                print volume
                if player_name == "global":
                    self.player_volumes[player_name] = volume 
                else:
                    for player in self.player_list:
                        if player.name == player_name:
                            self.player_volumes[player_name] = volume 
                            player.set_volume (volume)
                    
                line = config_file.readline()
                
        temp_scale = Gtk.Scale ()
        temp_adjust = Gtk.Adjustment (self.player_volumes["global"], 0, 100, 1, 10, 0)
        temp_scale.set_adjustment (temp_adjust)
        self.on_app_volume_change (temp_scale)

        # GUI
        self.win = Window (self.player_list, self.icon_dir, self.player_volumes)
        self.win.connect ("delete-event", self.on_window_close)
        self.win.app_vol.connect ('button-release-event', lambda widget, event: self.on_app_volume_change(widget))
        self.win.play_button.connect ('clicked', self.on_play_button_click)
        self.win.connect ('player-volume-changed', self.on_player_volume_change)
        self.win.app_vol.set_value (self.player_volumes["global"])

        # Indicator
        self.indicator = appindicator.Indicator.new (
                                         "acoustics",
                                         "app-icon",
                                         appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_icon_theme_path (self.icon_dir)
        self.indicator.set_status (appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_attention_icon ("indicator-messages-new")

        indicator_menu = Gtk.Menu ()
        open_item = Gtk.MenuItem ("Configure")
        open_item.show ()
        open_item.connect ('activate', lambda x: self.win.show_all ())
        indicator_menu.append (open_item)
        
        quit_item = Gtk.MenuItem ("Quit")
        quit_item.connect ('activate', self.on_delete)
        quit_item.show ()
        indicator_menu.append (quit_item)

        self.indicator.set_menu (indicator_menu)   
        
    def populate_player_list (self):
        sound_list = os.listdir (self.sound_dir)
        sound_list.sort ()
        for sound in sound_list:
            player = MPlayer (self.mpv_conf)
            player.load_file (self.sound_dir + sound)
            self.player_list.append (player)
        
    def on_window_close (self, *args):
        if self.app_state is self.State.PLAYING:
            self.win.hide_on_delete ()
        else:
            self.on_delete (args)
        return True    
        
    def on_delete (self, *args):
        [player.quit() for player in self.player_list]
                
        # Write to config file
        with open (self.local_dir + "config", 'r') as config_file:
            lines = config_file.readlines ()
        
        line_no = 0
        for key in self.player_volumes:
            lines[line_no] = key + ":" + str(self.player_volumes[key]) + "\n"
            print lines[line_no]
            if line_no + 1 is not len(lines):
                line_no = line_no + 1 
        
        with open (self.local_dir + "config", 'w') as config_file:
            config_file.writelines(lines)
            
        config_file.close ()
        Gtk.main_quit ()
                
        return True
        
    def on_app_volume_change (self, slider_range):
        # Get new volume, adjust volume of tracks accordingly
        for player in self.player_list:
            # Notes to help me figure out how to math:
            # We want x percent of y percent of 100 (max volume)
            # x is the individual volume
            # y is the global volume
            new_vol = (player.volume / float(100)) * (slider_range.get_value () / float (self.global_vol)) * 100
            player.set_volume (new_vol)
                
        self.global_vol = slider_range.get_value ()
        self.player_volumes["global"] = self.global_vol

    # I have no idea why 'args' is needed, but the needed parameters start from
    # player and if you don't put a parameter before that then python complains about
    # tuples :(
    # tl;dr: I'm bad at python
    
    def on_player_volume_change (self, args, volume, player):
        # The individual volume sliders show how much percent of the total output volume
        # is played for that sound
        if volume < 5: # If it's less than 5 then the user probably meant to mute it
            player.set_volume (0)
            self.player_volumes[player.name] = 0
            player.mute ()
        else:
            new_vol = (volume / float(100)) * self.global_vol
            self.player_volumes[player.name] = volume
            player.set_volume (new_vol)

    def on_play_button_click (self, button):
        if self.app_state is self.State.PLAYING:
            button.set_image (self.win.play_img)
            self.app_state = self.State.PAUSED
            [player.pause() for player in self.player_list]
        else:
            button.set_image (self.win.pause_img)
            self.app_state = self.State.PLAYING
            [player.play() for player in self.player_list]
           
if __name__ == '__main__':
    Gtk.init ()
    app = App ()       
    Gtk.main ()
    
