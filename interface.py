from gi.repository import GObject, Gtk, GLib

class Window (Gtk.Window):
    
    ''' 
        Class for providing a graphical interface for the app
    '''
    
    __gsignals__ = {
        'player-volume-changed' : (GObject.SIGNAL_RUN_FIRST, None, (int, object,))
    }
    
    class VolumeScale (Gtk.Scale):
        '''
            A custom widget for the application's volume sliders 
        '''
        __gsignals__ = {
            # args: the new volume and the MPlayer associated with the scale
            'volume-changed' : (GObject.SIGNAL_RUN_LAST, None, (int, object,))
        }
        
        def __init__ (self, player):
            _adjustment = Gtk.Adjustment(100, 0, 100, 1, 10, 0)
            Gtk.Scale.__init__(self, orientation = Gtk.Orientation.HORIZONTAL,
                               adjustment = _adjustment)
            self.set_draw_value (False)
            
            self._player = player
            self.connect ('value-changed', lambda scale_range: \
                                               self.emit("volume-changed", self.get_value (), 
                                                          self._player))
    
    
    def __init__(self, player_list, icon_path, player_volumes):
        Gtk.Window.__init__(self, title = "Acoustics")
        self.set_wmclass ("Acoustics", "Acoustics")
        self.set_default_size (475, 375)
        self.build_ui ()
        self.build_player_controls (player_list, icon_path, player_volumes)
        self.show_all ()
        
    def build_ui (self):

        # Headerbar
        self.header = Gtk.HeaderBar ()
        self.header.set_show_close_button (True)
        self.header.set_title ("Acoustics")
        self.header.get_style_context ().add_class ('titlebar')
        self.set_titlebar (self.header)

        # Layouts
        self.layout = Gtk.Grid () 
        
        # Play/Pause Button
        self.play_img = Gtk.Image.new_from_icon_name ('media-playback-start-symbolic', 
                                                       Gtk.IconSize.DIALOG)
        self.pause_img = Gtk.Image.new_from_icon_name ('media-playback-pause-symbolic', 
                                                        Gtk.IconSize.DIALOG)
        self.play_button = Gtk.Button ()
        self.play_button.set_image (self.pause_img)
        self.play_button.get_style_context ().add_class ('flat')
        self.play_button.set_always_show_image (True)
        self.play_button.set_vexpand (False)
        self.play_button.set_hexpand (False)
        self.play_button.set_margin_top (12)
        self.play_button.set_margin_bottom (12)
        self.play_button.set_margin_start (12)
        self.play_button.set_margin_end (6)

        # Volume slider

        value = 100
        adjustment = Gtk.Adjustment(value, 1, 100, 1, 10, 0)

        self.app_vol = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=adjustment)
        self.app_vol.set_hexpand(True)
        self.app_vol.set_draw_value (False)
        self.app_vol.set_margin_top (12)
        self.app_vol.set_margin_bottom (12)
        self.app_vol.set_margin_start (6)
        self.app_vol.set_margin_end (12)
        
        self.layout.attach(self.play_button, 0, 0, 1, 1)
        self.layout.attach(self.app_vol, 1, 0, 1, 1)
        
        self.add (self.layout)
        
    def build_player_controls (self, player_list, icon_path, player_volumes):

        icon_grid = Gtk.FlowBox ()
        icon_grid.set_column_spacing (6)
        icon_grid.set_selection_mode (Gtk.SelectionMode.NONE)
        icon_grid.set_max_children_per_line (3)
        icon_grid.set_min_children_per_line (3)        
        icon_grid.set_margin_start (12)
        icon_grid.set_margin_end (12)
        
        self.layout.attach(icon_grid, 0, 1, 2, 1)
        
        for player in player_list:
            box = Gtk.Grid ()
            
            icon_name = icon_path + player.name + '.svg'
            
            image = Gtk.Image.new_from_file (icon_name)
            image.set_hexpand (True)
             
            box.attach (image, 0, 0, 1, 1)
            box.attach (Gtk.Label (player.name.title()), 0, 1, 1, 1)       
            
            sound_vol = self.VolumeScale (player)
            sound_vol.set_value (player_volumes[player.name])
            sound_vol.connect ('volume-changed', lambda arg, val, player: \
                                                     self.emit ('player-volume-changed', val, player))
            sound_vol.set_size_request (108, -1)
            box.attach (sound_vol, 0, 2, 1, 1)
            box.set_hexpand (True)
            icon_grid.add (box)
