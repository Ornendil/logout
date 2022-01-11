#!/usr/bin/python3
# coding: utf-8

# In[1]:


#Innstillinger

# Hvor mange sekunder med inaktivitet før brukeren får beskjed om at han snart logges ut
loggUtBeskjedTid = 1 * 60

# Hvor mange sekunder etter det igjen før brukeren logges ut
loggUtTid = 4 * 60

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, Pango
from threading import Timer, Thread, Event
from datetime import datetime, timedelta
import subprocess
from subprocess import run

import locale
spraak = locale.getlocale()
print(spraak)
if 'nb_NO' in spraak:
    logoutButtonText = 'Logg ut og slett alt'
    inactiveUserText = 'Inaktiv bruker'
    tilLogoutText = 'til utlogging'
    loggedOnText = 'Pålogget tid'
else:
    logoutButtonText = 'Logout and delete everything'
    inactiveUserText = 'Inactive user'
    tilLogoutText = 'until logout'
    loggedOnText = 'Logged on'

#import warnings
#warnings.simplefilter("error")

timeout = 0
idleTime = 0
fullScreen = 'false'

class MyWindow(Gtk.Window):

    def __init__(root):
        Gtk.Window.__init__(root, title="Utloggings-timer : Ullensaker bibliotek")
        
        root.set_border_width(8)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        root.add(box)


        # Lag delene av vinduet
        root.tekst1 = Gtk.Label(label="")
        root.tekst1.set_name('tekst1')
        box.pack_start(root.tekst1, True, True, 0)

        root.counter = Gtk.Label(label="")
        root.counter.set_name('counter')
        box.pack_start(root.counter, True, True, 0)

        root.tekst2 = Gtk.Label(label="")
        root.tekst2.set_name('tekst2')
        box.pack_start(root.tekst2, True, True, 0)

        root.logoutButton = Gtk.Button(label=logoutButtonText)
        #for child in root.logoutButton.get_children():
        #    child.set_label('<span font="13.5">Logg ut og slett alt</span>\nLogout and delete everything')
        #    child.set_use_markup(True)
        #root.logoutButton.get_style_context().add_class(class_name='bold-text')
        root.logoutButton.set_name('logoutButton')
        root.logoutButton.set_can_focus(False)
        root.logoutButton.connect("clicked", root.logOff)
        box.pack_start(root.logoutButton, True, True, 0)
        
        root.gtk_style()
        
        root.startTime = root.currentTime()
        
        root.clock()
        global timeout
        timeout = GLib.timeout_add_seconds(1, root.clock)
    
    def clock(root):
        tid = root.currentTime() - root.startTime
        
        global idleTime
        global fullScreen
        
        # Hvis brukeren ser på film eller no sånt, sett idle time til null
        if root.isFullScreen() == 'true':
            idleTime = 0
            fullScreen = 'true'
        # Men hvis brukeren slutter å se på film
        elif root.isFullScreen() != 'true' and fullScreen == 'true':
            fullscreen = 'false'
            run("/opt/logout/fakeinput.sh")
            idleTime = root.idleTimer()
        # Ellers la klokka gå
        else:
            idleTime = root.idleTimer()
            
        if idleTime >= loggUtBeskjedTid:
            secondsLeft = timedelta(seconds = (loggUtBeskjedTid + loggUtTid) - int(idleTime))
            root.tekst1.set_text(inactiveUserText)
            root.counter.set_text(str(secondsLeft))
            root.tekst2.set_text(tilLogoutText)
        else:
            root.tekst1.set_text(loggedOnText)
            root.counter.set_text(str( timedelta(seconds = tid.seconds )))
            root.tekst2.set_text("")

        if idleTime >= loggUtTid + loggUtBeskjedTid:
            root.logOff('root')
            return 'false'
        else:
            return 'true'
        
    def currentTime(root):
        return datetime.now()
        
    # Funksjon som skjekker om det finnes et vindu som kjører i fullskjerm og svarer "true" hvis det er det
    def isFullScreen(root):
        full = run("/opt/logout/isfullscreen.sh", stdout=subprocess.PIPE).stdout.decode('utf-8').strip(' \t\n\r')
        return full

    # Funksjon som logger ut brukeren hardt og brutalt
    def logOff(root, widget):
        GLib.source_remove(timeout)
        run("/opt/logout/loggut.sh")

    def idleTimer(root):
        return float(run("/opt/logout/idle.sh", stdout=subprocess.PIPE).stdout.decode('utf-8')) / 1000


    def gtk_style(root):
        style_provider = Gtk.CssProvider()
        css = open('/opt/logout/style.css')
        css_data = css.read().encode()
        style_provider.load_from_data(css_data)
        css.close()

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.set_decorated(False)
win.set_skip_taskbar_hint(True)
win.set_keep_above('true')

def moveMainWindow(self,event):
        self.begin_move_drag(event.button, event.x_root, event.y_root, event.get_time())

win.connect('button_press_event', moveMainWindow)

screen = win.get_screen()
win.set_default_size(170,110)
width, height = win.get_size()
if 'ar_SA' in spraak:
    win.set_gravity(Gdk.Gravity.SOUTH_WEST)
    win.move(14, screen.get_height() - height - 28)
else:
    win.set_gravity(Gdk.Gravity.SOUTH_EAST)
    win.move(screen.get_width() - width - 24, screen.get_height() - height - 48)

win.show_all()
Gtk.main()

GLib.source_remove(timeout)
