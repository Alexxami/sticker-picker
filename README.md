# Sticker Picker - Documentation

Floating application for Wayland that allows selecting and copying stickers (images and animated GIFs) from a local folder to the clipboard, for later pasting into any application.

## Features

- Fixed-size floating window (400×600 pixels) that always stays on top.
- Compatible formats: **PNG, JPG, JPEG, GIF, WEBP** (including animation).
- Preview of each sticker in reduced size.
- Copy to clipboard preserving the original format (animated GIFs are copied as files, preserving animation).
- Auto-closes after copying a sticker.
- Close with the `Escape` key.
- `+` button to add new stickers from the file system.
- Centralized storage in `~/.config/stickers/`.

## Installation

### 1. Install dependencies

#### Ubuntu / Debian
```bash
sudo apt update
sudo apt install python3 python3-gi python3-gi-cairo gir1.2-gtk-3.0 wl-clipboard
```

#### Arch Linux / Manjaro
```bash
sudo pacman -S python python-gobject gtk3 wl-clipboard
```

#### Fedora
```bash
sudo dnf install python3 python3-gobject gtk3 wl-clipboard
```

#### OpenSUSE
```bash
sudo zypper in python3 python3-gobject gtk3 wl-clipboard
```

### 2. Make it executable

```bash
mv sticker-picker/stickers.py /path/of/your/config/stickers.py
```

### 3. Create the stickers folder

```bash
mkdir -p ~/.config/stickers
```

## Usage

### Run the application

```bash
python3 ~/bin/sticker_picker.py
```

### Interaction

1. **Select a sticker**: Left-click on any sticker in the grid.
   - The sticker is copied to the clipboard.
   - The window closes automatically.
2. **Paste the sticker**: In the target application (editor, chat, etc.) use `Ctrl+V` or the paste option from the menu.
3. **Add new stickers**: Press the `+` button (top right).
   - A file picker opens.
   - You can select one or more files (PNG, JPG, GIF).
   - Files are copied to `~/.config/stickers/` and the grid updates instantly.
4. **Cancel / Close without copying**: Press the `Escape` key or close the window with the `X` button.

## Keyboard Shortcuts

| Key       | Action                         |
|-----------|--------------------------------|
| `Escape`  | Closes the window without copying. |
| `Ctrl+W`  | Closes the window (standard GTK). |
| `Ctrl+Q`  | Quits the application.        |

## Customization

### Change the window size

Edit these lines in the script:

```python
self.set_default_size(400, 600)  # Width, Height
self.set_size_request(400, 600)  # Minimum and maximum
```

### Change the number of columns

Modify the value in:

```python
self.flowbox.set_max_children_per_line(3)
```

### Change the thumbnail size

Look for the line:

```python
pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(str(sticker_path), 100, 100)
```

and adjust the two numbers (thumbnail width and height).
