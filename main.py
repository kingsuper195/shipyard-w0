import gi
gi.require_version('Gtk','4.0')
from gi.repository import Gtk, GLib, GdkPixbuf, Gdk
import requests
from PIL import Image
import io


class MyWindow(Gtk.ApplicationWindow):
    def __init__(self, **kargs):
        super().__init__(**kargs, title="xkcd Viewer")
        self.raw = requests.get("https://imgs.xkcd.com/comics/crystal_gazing.png",stream=True)
        self.image_file = io.BytesIO(self.raw.raw.read())
        self.im = Image.open(self.image_file)
        self.w, self.h = self.im.size
        self.pixbuf = GdkPixbuf.Pixbuf.new_from_bytes(GLib.Bytes.new(self.im.tobytes()), GdkPixbuf.Colorspace.RGB, False, 8, self.w, self.h, self.w * 3)
        self.pnt = Gdk.Texture.new_for_pixbuf(self.pixbuf)
        self.img = Gtk.Picture.new_for_paintable(self.pnt)
        self.set_child(self.img)
        self.present()



def on_activate(app):
    win = MyWindow(application=app)
    win.present()


app = Gtk.Application(application_id='com.xkcd.viewer')
app.connect('activate', on_activate)
app.run(None)