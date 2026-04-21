#!/usr/bin/env python3
import sys
import shutil
import subprocess
from pathlib import Path

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf

class StickerPicker(Gtk.Window):
    def __init__(self):
        super().__init__(title="Sticker Picker")
        
        # Floating window with fixed dimensions
        self.set_type_hint(Gdk.WindowTypeHint.POPUP_MENU)
        self.set_default_size(400, 600)
        self.set_resizable(False)
        self.set_size_request(400, 600)
        self.set_keep_above(True)
        self.set_decorated(True)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        self.connect("key-press-event", self.on_key_press)
        
        # FOLDER
        self.stickers_dir = Path.home() / ".config" / "stickers"
        self.stickers_dir.mkdir(parents=True, exist_ok=True)
        
        self.supported_extensions = ('.png', '.jpg', '.jpeg', '.gif', 'webp')
        
        self.setup_ui()
        self.load_stickers()
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
    
    def on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            Gtk.main_quit()
            return True
        return False
    
    def setup_ui(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(vbox)
        
        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        header_bar.set_title("Sticker Picker")
        self.set_titlebar(header_bar)
        
        add_button = Gtk.Button(label="+")
        add_button.connect("clicked", self.on_add_sticker)
        header_bar.pack_end(add_button)
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(scrolled, True, True, 0)
        
        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_valign(Gtk.Align.START)
        self.flowbox.set_max_children_per_line(3)
        self.flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        scrolled.add(self.flowbox)
    
    def load_stickers(self):
        for child in self.flowbox.get_children():
            child.destroy()
        
        sticker_files = []
        for ext in self.supported_extensions:
            sticker_files.extend(self.stickers_dir.glob(f"*{ext}"))
            sticker_files.extend(self.stickers_dir.glob(f"*{ext.upper()}"))
        sticker_files.sort()
        
        if not sticker_files:
            label = Gtk.Label(label="No stickers found.\nClick '+' to add stickers")
            label.set_justify(Gtk.Justification.CENTER)
            self.flowbox.add(label)
            return
        
        for path in sticker_files:
            self.add_sticker_button(path)
    
    def add_sticker_button(self, sticker_path):
        event_box = Gtk.EventBox()
        event_box.connect("button-press-event", self.on_sticker_clicked, sticker_path)
        
        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(str(sticker_path), 100, 100)
            image = Gtk.Image.new_from_pixbuf(pixbuf)
        except Exception:
            image = Gtk.Image.new_from_icon_name("image-missing", Gtk.IconSize.DIALOG)
        
        event_box.add(image)
        event_box.set_tooltip_text(sticker_path.name)
        self.flowbox.add(event_box)
        event_box.show_all()
    
    def on_sticker_clicked(self, widget, event, sticker_path):
        if event.button == 1:
            self.copy_and_close(sticker_path)
    
    def copy_and_close(self, sticker_path):
        """Copies the sticker as a file URI (text/uri-list) and closes"""
        try:
            # Convert path to file URI
            file_uri = Path(sticker_path).resolve().as_uri()
            # Copy using wl-copy with text/uri-list type
            subprocess.run(['wl-copy', '-t', 'text/uri-list'], 
                           input=file_uri, 
                           encoding='utf-8', 
                           check=True)
        except Exception as e:
            print(f"Error copying: {e}")
        finally:
            Gtk.main_quit()
    
    def on_add_sticker(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Add Stickers",
            parent=self,
            action=Gtk.FileChooserAction.OPEN,
            buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                    Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        )
        dialog.set_select_multiple(True)
        
        filter_images = Gtk.FileFilter()
        filter_images.set_name("Image files")
        for ext in ['png', 'jpg', 'jpeg', 'gif', 'webp']:
            filter_images.add_pattern(f"*.{ext}")
            filter_images.add_pattern(f"*.{ext.upper()}")
        dialog.add_filter(filter_images)
        
        if dialog.run() == Gtk.ResponseType.OK:
            for file in dialog.get_files():
                src = file.get_path()
                dst = self.stickers_dir / Path(src).name
                try:
                    shutil.copy2(src, dst)
                except Exception as e:
                    print(f"Error copying: {e}")
            self.load_stickers()
        dialog.destroy()

def main():
    if shutil.which('wl-copy') is None:
        print("ERROR: wl-clipboard is required. Install with: sudo apt install wl-clipboard")
        sys.exit(1)
    
    app = StickerPicker()
    Gtk.main()

if __name__ == "__main__":
    main()
