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
        
        self.set_type_hint(Gdk.WindowTypeHint.POPUP_MENU)
        self.set_default_size(425, 600)
        self.set_resizable(False)
        self.set_size_request(425, 600)
        self.set_keep_above(True)
        self.set_decorated(True)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        self.connect("key-press-event", self.on_key_press)
        
        self.stickers_dir = Path.home() / ".config" / "stickers"
        self.stickers_dir.mkdir(parents=True, exist_ok=True)
        
        self.supported_extensions = ('.png', '.jpg', '.jpeg', '.gif', 'webp')
        self.toolbar_visible = True
        self.delete_mode = False
        
        self.setup_ui()
        self.load_stickers()
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
    
    def on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            Gtk.main_quit()
            return True
        if event.keyval == Gdk.KEY_Alt_L or event.keyval == Gdk.KEY_Alt_R:
            self.toggle_toolbar()
            return True
        return False
    
    def toggle_toolbar(self):
        if self.toolbar_visible:
            self.toolbar_box.hide()
            self.toolbar_visible = False
        else:
            self.toolbar_box.show()
            self.toolbar_visible = True
    
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
        
        # Toolbar: Edit button with traditional dropdown menu
        self.toolbar_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        
        # Create menu
        menu = Gtk.Menu()
        
        # Preferences option
        prefs_item = Gtk.MenuItem(label="Preferences")
        prefs_item.connect("activate", self.on_prefs_clicked)
        menu.append(prefs_item)
        
        # About option
        about_item = Gtk.MenuItem(label="About")
        about_item.connect("activate", self.on_about_clicked)
        menu.append(about_item)
        
        # Separator
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        
        # Delete mode (toggle)
        self.delete_menu_item = Gtk.CheckMenuItem(label="Delete mode")
        self.delete_menu_item.connect("toggled", self.on_delete_mode_toggled)
        menu.append(self.delete_menu_item)
        
        menu.show_all()
        
        # Edit button that shows the menu
        self.edit_button = Gtk.MenuButton()
        self.edit_button.set_label("Edit")
        self.edit_button.set_relief(Gtk.ReliefStyle.NONE)
        self.edit_button.set_popup(menu)  # Associate the menu
        self.toolbar_box.pack_start(self.edit_button, False, False, 0)
        
        # Info label (shows delete mode status)
        self.info_label = Gtk.Label()
        self.info_label.set_margin_start(10)
        self.toolbar_box.pack_start(self.info_label, False, False, 0)
        
        header_bar.pack_start(self.toolbar_box)
        
        # CSS for Edit button style and uniform background
        css = """
            .toolbar-box {
                background-color: @theme_bg_color;
            }
            .edit-button {
                padding: 4px 10px;
                margin: 0;
                background: none;
                border: none;
                border-radius: 4px;
            }
            .edit-button:hover {
                background-color: shade(@theme_bg_color, 0.92);
            }
            .edit-button-active {
                background-color: #e74c3c;
                color: white;
            }
        """
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css.encode())
        self.toolbar_box.get_style_context().add_class("toolbar-box")
        self.edit_button.get_style_context().add_class("edit-button")
        self.edit_button.get_style_context().add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(scrolled, True, True, 0)
        
        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_valign(Gtk.Align.START)
        self.flowbox.set_max_children_per_line(3)
        self.flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        scrolled.add(self.flowbox)
    
    def on_delete_mode_toggled(self, widget):
        self.delete_mode = widget.get_active()
        if self.delete_mode:
            self.edit_button.get_style_context().add_class("edit-button-active")
            self.info_label.set_text("🗑️ Delete mode ON")
        else:
            self.edit_button.get_style_context().remove_class("edit-button-active")
            self.info_label.set_text("")
        self.load_stickers()
    
    def on_about_clicked(self, widget):
        about_dialog = Gtk.AboutDialog()
        about_dialog.set_transient_for(self)
        about_dialog.set_program_name("Sticker Picker")
        about_dialog.set_version("0.3.0")
        about_dialog.set_comments("Sticker picker for Wayland - Dropdown Edit menu")
        about_dialog.set_website("https://github.com/AlexxAmi/sticker-picker")
        about_dialog.set_website_label("GitHub")
        about_dialog.set_license("GNU General Public License v2")
        about_dialog.set_wrap_license(True)
        about_dialog.set_authors(["Alexx <alejandroavilagonzalez@outlook.es>"])
        about_dialog.run()
        about_dialog.destroy()
    
    def on_prefs_clicked(self, widget):
        dialog = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.INFO,
                                   buttons=Gtk.ButtonsType.OK, text="Preferences")
        dialog.format_secondary_text("Preferences coming soon...")
        dialog.run()
        dialog.destroy()
    
    def create_empty_state_widget(self):
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        container.set_valign(Gtk.Align.CENTER)
        container.set_halign(Gtk.Align.CENTER)
        container.set_margin_top(80)
        container.set_margin_bottom(80)
        container.set_margin_start(30)
        container.set_margin_end(30)
        
        icon_label = Gtk.Label()
        icon_label.set_markup("<span size='80000'>🎨</span>")
        container.pack_start(icon_label, False, False, 0)
        
        title_label = Gtk.Label()
        title_label.set_markup("<span weight='bold' size='large'>No Stickers Yet</span>")
        container.pack_start(title_label, False, False, 0)
        
        subtitle_label = Gtk.Label()
        subtitle_label.set_markup("<span foreground='#888888'>Add some stickers to get started\nClick the <b>+</b> button in the top bar to add images</span>")
        subtitle_label.set_justify(Gtk.Justification.CENTER)
        subtitle_label.set_line_wrap(True)
        subtitle_label.set_max_width_chars(30)
        container.pack_start(subtitle_label, False, False, 0)
        
        hint_label = Gtk.Label()
        hint_label.set_markup("<span foreground='#aaaaaa' size='small'>Supported: PNG, JPG, GIF, WebP</span>")
        container.pack_start(hint_label, False, False, 0)
        
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(10)
        separator.set_size_request(150, -1)
        container.pack_start(separator, False, False, 0)
        
        tip_label = Gtk.Label()
        tip_label.set_markup("<span foreground='#666666' size='small'>💡 Tip: Press ESC to close | Press Alt to hide/show toolbar</span>")
        container.pack_start(tip_label, False, False, 0)
        
        container.show_all()
        return container
    
    def load_stickers(self):
        for child in self.flowbox.get_children():
            child.destroy()
        
        sticker_files = []
        for ext in self.supported_extensions:
            sticker_files.extend(self.stickers_dir.glob(f"*{ext}"))
            sticker_files.extend(self.stickers_dir.glob(f"*{ext.upper()}"))
        sticker_files.sort()
        
        if not sticker_files:
            empty_widget = self.create_empty_state_widget()
            self.flowbox.add(empty_widget)
            return
        
        for path in sticker_files:
            self.add_sticker_button(path, self.delete_mode)
    
    def add_sticker_button(self, sticker_path, delete_mode=False):
        overlay = Gtk.Overlay()
        overlay.set_size_request(100, 100)
        
        event_box = Gtk.EventBox()
        event_box.connect("button-press-event", self.on_sticker_clicked, sticker_path)
        
        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(str(sticker_path), 100, 100)
            image = Gtk.Image.new_from_pixbuf(pixbuf)
        except Exception:
            image = Gtk.Image.new_from_icon_name("image-missing", Gtk.IconSize.DIALOG)
        
        event_box.add(image)
        overlay.add(event_box)
        
        if delete_mode:
            delete_btn = Gtk.Button()
            delete_btn.set_relief(Gtk.ReliefStyle.NONE)
            delete_btn.set_focus_on_click(False)
            delete_btn.set_size_request(28, 28)
            trash_icon = Gtk.Image.new_from_icon_name("user-trash-symbolic", Gtk.IconSize.MENU)
            delete_btn.set_image(trash_icon)
            delete_btn.set_tooltip_text("Delete sticker")
            
            css = """
                .delete-button-sticker {
                    background-color: #e74c3c;
                    border-radius: 14px;
                    padding: 2px;
                    min-width: 28px;
                    min-height: 28px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.3);
                }
                .delete-button-sticker:hover { background-color: #c0392b; }
                .delete-button-sticker:active { background-color: #a93226; }
            """
            css_provider = Gtk.CssProvider()
            css_provider.load_from_data(css.encode())
            delete_btn.get_style_context().add_class("delete-button-sticker")
            delete_btn.get_style_context().add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
            delete_btn.connect("clicked", self.on_delete_sticker_clicked, sticker_path)
            
            overlay.add_overlay(delete_btn)
            delete_btn.set_halign(Gtk.Align.END)
            delete_btn.set_valign(Gtk.Align.START)
            delete_btn.set_margin_top(4)
            delete_btn.set_margin_end(4)
        
        # Hover effect for stickers
        css_provider = Gtk.CssProvider()
        css = """
            .sticker-button:hover {
                background-color: rgba(128, 128, 128, 0.1);
                border-radius: 8px;
            }
            .sticker-button { padding: 8px; transition: all 0.2s ease; }
        """
        css_provider.load_from_data(css.encode())
        context = event_box.get_style_context()
        context.add_class("sticker-button")
        context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        
        overlay.show_all()
        self.flowbox.add(overlay)
    
    def on_sticker_clicked(self, widget, event, sticker_path):
        if event.button == 1:
            self.copy_and_close(sticker_path)
        return True
    
    def on_delete_sticker_clicked(self, widget, sticker_path):
        dialog = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.QUESTION,
                                   buttons=Gtk.ButtonsType.YES_NO, text=f"Delete '{sticker_path.name}'?")
        dialog.format_secondary_text("This action cannot be undone.")
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            try:
                sticker_path.unlink()
                self.load_stickers()
            except Exception as e:
                error_dialog = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.ERROR,
                                                 buttons=Gtk.ButtonsType.OK, text="Error deleting sticker")
                error_dialog.format_secondary_text(str(e))
                error_dialog.run()
                error_dialog.destroy()
    
    def copy_and_close(self, sticker_path):
        try:
            file_uri = Path(sticker_path).resolve().as_uri()
            subprocess.run(['wl-copy', '-t', 'text/uri-list'], input=file_uri, encoding='utf-8', check=True)
        except Exception as e:
            print(f"Error copying: {e}")
        finally:
            Gtk.main_quit()
    
    def on_add_sticker(self, widget):
        dialog = Gtk.FileChooserDialog(title="Add Stickers", parent=self, action=Gtk.FileChooserAction.OPEN,
                                       buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                                Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
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
    print("Sticker Picker started - Dropdown menu with Gtk.Menu")
    app = StickerPicker()
    Gtk.main()

if __name__ == "__main__":
    main()
