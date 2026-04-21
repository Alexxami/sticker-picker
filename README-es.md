# Sticker Picker - Documentación

Aplicación flotante para Wayland que permite seleccionar y copiar stickers (imágenes y GIFs animados) desde una carpeta local al portapapeles, para pegarlos posteriormente en cualquier aplicación.

## Características

- Ventana flotante de tamaño fijo (400×600 píxeles) que siempre se mantiene encima.
- Compatible con formatos: **PNG, JPG, JPEG, GIF** (incluyendo animación).
- Vista previa de cada sticker en tamaño reducido.
- Copia al portapapeles manteniendo el formato original (el GIF animado se copia como archivo, preservando la animación).
- Cierre automático tras copiar un sticker.
- Cierre con la tecla `Escape`.
- Botón `+` para añadir nuevos stickers desde el sistema de archivos.
- Almacenamiento centralizado en `~/.config/stickers/`.

## Instalación

### 1. Instalar dependencias

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

### 2. Crear el script

Crea el archivo `sticker_picker.py` en la ubicación que prefieras (por ejemplo `~/bin/sticker_picker.py`) con el contenido del script (ver abajo).

### 3. Dar permisos de ejecución

```bash
chmod +x ~/bin/sticker_picker.py
```

### 4. Crear la carpeta de stickers

```bash
mkdir -p ~/.config/stickers
```

## Uso

### Ejecutar la aplicación

```bash
~/bin/sticker_picker.py
```

O con Python:

```bash
python3 ~/bin/sticker_picker.py
```

### Interacción

1. **Seleccionar un sticker**: Haz clic izquierdo sobre cualquier sticker de la cuadrícula.
   - El sticker se copia al portapapeles.
   - La ventana se cierra automáticamente.
2. **Pegar el sticker**: En la aplicación destino (editor, chat, etc.) usa `Ctrl+V` o la opción de pegar del menú.
3. **Añadir nuevos stickers**: Pulsa el botón `+` (arriba a la derecha).
   - Se abre un selector de archivos.
   - Puedes seleccionar uno o varios archivos (PNG, JPG, GIF).
   - Los archivos se copian a `~/.config/stickers/` y la cuadrícula se actualiza al instante.
4. **Cancelar / Cerrar sin copiar**: Presiona la tecla `Escape` o cierra la ventana con el botón `X`.

## Atajos de teclado

| Tecla     | Acción                         |
|-----------|--------------------------------|
| `Escape`  | Cierra la ventana sin copiar.  |
| `Ctrl+W`  | Cierra la ventana (estándar GTK). |
| `Ctrl+Q`  | Salir de la aplicación.        |

## Personalización

### Cambiar el tamaño de la ventana

Edita estas líneas en el script:

```python
self.set_default_size(400, 600)  # Ancho, Alto
self.set_size_request(400, 600)  # Mínimo y máximo
```

### Cambiar el número de columnas

Modifica el valor en:

```python
self.flowbox.set_max_children_per_line(3)
```

### Cambiar el tamaño de las miniaturas

Busca la línea:

```python
pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(str(sticker_path), 100, 100)
```

y ajusta los dos números (ancho y alto de la miniatura).

```

Este documento asume que todo funciona correctamente, omitiendo cualquier sección de errores o solución de problemas.
