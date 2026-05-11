import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib, Gdk
import requests

latest = requests.get("https://xkcd.com/info.0.json").json()
comic = latest["num"]
max = latest["num"]


class MyWindow(Gtk.ApplicationWindow):
    def __init__(self, **kargs):
        super().__init__(**kargs, title="xkcd Viewer")
        self.grid = Gtk.Grid()
        self.set_child(self.grid)
        self.img = Gtk.Picture.new_for_paintable(fetch_xkcd(comic))
        self.left = Gtk.Button(label="<")
        self.right = Gtk.Button(label=">")
        self.left.connect("clicked", self.left_cl)
        self.right.connect("clicked", self.right_cl)
        self.grid.attach(self.img, 0, 0, 2, 2)
        self.grid.attach(self.left, 0, 3, 1, 1)
        self.grid.attach(self.right, 1, 3, 1, 1)
        self.present()

    def left_cl(self, _widget):
        global comic
        comic -= 1
        if comic < 1:
            comic += 1
        self.img.set_paintable(fetch_xkcd(comic))

    def right_cl(self, _widget):
        global comic
        global max
        comic += 1
        if comic > max:
            comic -= 1
        self.img.set_paintable(fetch_xkcd(comic))


def fetch_xkcd(comicN):
    ciurl = "https://xkcd.com/"+str(comicN)+"/info.0.json"
    comicInfo = requests.get(ciurl).json()
    url = comicInfo["img"]
    raw = requests.get(url, stream=True)
    image_file = raw.raw.read()
    return Gdk.Texture.new_from_bytes(GLib.Bytes.new(image_file))


def on_activate(app):
    win = MyWindow(application=app)
    win.present()


app = Gtk.Application(application_id="com.xkcd.viewer")
app.connect("activate", on_activate)
app.run(None)
