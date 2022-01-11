#!/usr/bin/python3
# coding: utf-8

#Innstillinger

# Hvor mange sekunder med inaktivitet før brukeren får beskjed om at han snart logges ut
loggUtBeskjedTid = 1 * 60

# Hvor mange sekunder etter det igjen før brukeren logges ut
loggUtTid = 4 * 60

import cairo
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
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
    loggedOnText = 'Tid pålogget:'
else:
    logoutButtonText = 'Logout and delete everything'
    inactiveUserText = 'Inactive user'
    tilLogoutText = 'until logout'
    loggedOnText = 'Time logged on:'

timeout = 0
idleTime = 0
fullScreen = 'false'

class TransparentWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Utloggings-timer : Ullensaker bibliotek")

        self.set_border_width(8)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        box.set_name('box')
        self.add(box)

        # Lag delene av vinduet
        self.tekst1 = Gtk.Label(label="")
        self.tekst1.set_name('tekst1')
        box.pack_start(self.tekst1, True, True, 0)

        self.counter = Gtk.Label(label="")
        self.counter.set_name('counter')
        box.pack_start(self.counter, True, True, 0)

        self.tekst2 = Gtk.Label(label="")
        self.tekst2.set_name('tekst2')
        box.pack_start(self.tekst2, True, True, 0)

        self.logoutButton = Gtk.Button(label=logoutButtonText)
        self.logoutButton.set_name('logoutButton')
        self.logoutButton.set_can_focus(False)
        self.logoutButton.connect("clicked", self.logOff)
        box.pack_start(self.logoutButton, True, True, 0)

        self.gtk_style()
        
        self.startTime = self.currentTime()
        
        self.clock()
        global timeout
        timeout = GLib.timeout_add_seconds(1, self.clock)

        self.connect('destroy', Gtk.main_quit)
        self.set_decorated(False)
        self.set_skip_taskbar_hint(True)
        self.set_keep_above('true')

        self.connect('draw', self.draw)

        # Gjør det mulig å kunne dra viduet rundt
        def moveMainWindow(self,event):
                self.begin_move_drag(event.button, event.x_root, event.y_root, event.get_time())
        self.connect('button_press_event', moveMainWindow)

        # Sett størrelsen og posisjonen på vinduet
        screen = self.get_screen()
        self.set_default_size(150,120)
        width, height = self.get_size()
        if 'ar_SA' in spraak:
            self.set_gravity(Gdk.Gravity.SOUTH_WEST)
            self.move(14, screen.get_height() - height - 32)
        else:
            self.set_gravity(Gdk.Gravity.SOUTH_EAST)
            self.move(screen.get_width() - width - 10, screen.get_height() - height - 37)

        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)

        self.set_app_paintable(True)
        self.show_all()

    def clock(self):
        tid = self.currentTime() - self.startTime
        
        global idleTime
        global fullScreen
        
        # Hvis brukeren ser på film eller no sånt, sett idle time til null
        if self.isFullScreen() == 'true':
            idleTime = 0
            fullScreen = 'true'
        # Men hvis brukeren slutter å se på film
        elif self.isFullScreen() != 'true' and fullScreen == 'true':
            fullscreen = 'false'
            run("/opt/logout/fakeinput.sh")
            idleTime = self.idleTimer()
        # Ellers la klokka gå
        else:
            idleTime = self.idleTimer()
            
        if idleTime >= loggUtBeskjedTid:
            secondsLeft = timedelta(seconds = (loggUtBeskjedTid + loggUtTid) - int(idleTime))
            self.tekst1.set_text(inactiveUserText)
            self.counter.set_text(str(secondsLeft))
            self.tekst2.set_text(tilLogoutText)
        else:
            self.tekst1.set_text(loggedOnText)
            self.counter.set_text(str( timedelta(seconds = tid.seconds )))
            self.tekst2.set_text("")

        if idleTime >= loggUtTid + loggUtBeskjedTid:
            self.logOff('self')
            return 'false'
        else:
            return 'true'
        
    def currentTime(self):
        return datetime.now()
        
    # Funksjon som skjekker om det finnes et vindu som kjører i fullskjerm og svarer "true" hvis det er det
    def isFullScreen(self):
        full = run("/opt/logout/isfullscreen.sh", stdout=subprocess.PIPE).stdout.decode('utf-8').strip(' \t\n\r')
        return full

    # Funksjon som logger ut brukeren hardt og brutalt
    def logOff(self, widget):
        GLib.source_remove(timeout)
        run("/opt/logout/loggut.sh")

    def idleTimer(self):
        return float(run("/opt/logout/idle.sh", stdout=subprocess.PIPE).stdout.decode('utf-8')) / 1000


    def gtk_style(self):
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

    def draw(self, widget, context):
        context.set_source_rgba(0.75, 0.75, 0.75, 0.8)
        context.set_operator(cairo.OPERATOR_SOURCE)
        context.paint()
        context.set_operator(cairo.OPERATOR_OVER)


TransparentWindow()
Gtk.main()
