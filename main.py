import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib, Gdk
import requests
import random

latest = requests.get("https://xkcd.com/info.0.json").json()
comic = latest["num"]
max = latest["num"]


class MyWindow(Gtk.ApplicationWindow):
    def __init__(self, **kargs):
        super().__init__(**kargs, title="xkcd Viewer")
        paintable, title = fetch_xkcd(comic)
        self.img = Gtk.Picture.new_for_paintable(paintable)

        self.start = Gtk.Button(label="|<", hexpand=True)
        self.left = Gtk.Button(label="<", hexpand=True)
        self.random = Gtk.Button(label="Random", hexpand=True)
        self.right = Gtk.Button(label=">", hexpand=True)
        self.end = Gtk.Button(label=">|", hexpand=True)

        self.start.connect("clicked", self.start_cl)
        self.left.connect("clicked", self.left_cl)
        self.random.connect("clicked", self.random_cl)
        self.right.connect("clicked", self.right_cl)
        self.end.connect("clicked", self.end_cl)

        self.title = Gtk.Label()
        self.title.set_markup(f'<span size="x-large">{title}</span>')

        self.outerBox = Gtk.Box()
        self.set_child(self.outerBox)
        self.outerBox.set_orientation(Gtk.Orientation.VERTICAL)

        self.outerBox.append(self.title)
        self.outerBox.append(self.img)

        self.buttonBox = Gtk.Box()
        self.outerBox.append(self.buttonBox)

        self.buttonBox.append(self.start)
        self.buttonBox.append(self.left)
        self.buttonBox.append(self.random)
        self.buttonBox.append(self.right)
        self.buttonBox.append(self.end)

        self.present()

    def start_cl(self, _widget):
        global comic
        comic = 1
        paintable, title = fetch_xkcd(comic)
        self.img.set_paintable(paintable)
        self.title.set_markup(f'<span size="x-large">{title}</span>')

    def left_cl(self, _widget):
        global comic
        comic -= 1
        if comic < 1:
            comic += 1
        paintable, title = fetch_xkcd(comic)
        self.img.set_paintable(paintable)
        self.title.set_markup(f'<span size="x-large">{title}</span>')

    def random_cl(self, _widget):
        global comic
        global max
        comic = random.randint(1, max)
        paintable, title = fetch_xkcd(comic)
        self.img.set_paintable(paintable)
        self.title.set_markup(f'<span size="x-large">{title}</span>')

    def right_cl(self, _widget):
        global comic
        global max
        comic += 1
        if comic > max:
            comic -= 1
        paintable, title = fetch_xkcd(comic)
        self.img.set_paintable(paintable)
        self.title.set_markup(f'<span size="x-large">{title}</span>')

    def end_cl(self, _widget):
        global comic
        global max
        comic = max
        paintable, title = fetch_xkcd(comic)
        self.img.set_paintable(paintable)
        self.title.set_markup(f'<span size="x-large">{title}</span>')


def fetch_xkcd(comicN):
    ciurl = "https://xkcd.com/" + str(comicN) + "/info.0.json"
    comicInfo = requests.get(ciurl).json()
    url = comicInfo["img"]
    raw = requests.get(url, stream=True)
    image_file = raw.raw.read()
    return Gdk.Texture.new_from_bytes(GLib.Bytes.new(image_file)), comicInfo["title"]


def on_activate(app):
    win = MyWindow(application=app)
    win.present()


app = Gtk.Application(application_id="com.xkcd.viewer")
app.connect("activate", on_activate)
app.run(None)
