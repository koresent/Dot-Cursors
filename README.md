# ⚫ Dot Cursors

Minimalist dot cursor pack for Windows and Linux.
Created for personal use, shared for anyone who needs it.

Includes **Black** and **White** versions.

## 🖼️ Previews

### ⚫ Black
<img alt="Dot Black Preview" src=".github/showcase/black.png" />

### ⚪ White
<img alt="Dot White Preview" src=".github/showcase/white.png" />

-----

## 🛠️ Installation

### 🪟 Windows

1. Clone or download the repository.
2. Open `Windows/Dot-Black` or `Windows/Dot-White`.
3. Right-click on `install.inf` and select **Install**.
4. Press `Win + R`, type `main.cpl` and hit **Enter**.
5. Go to the **Pointers** tab and select the new scheme (`Dot-Black` or `Dot-White`) from the dropdown.

### 🐧 Linux

#### Quick Install (via script)

```bash
git clone https://github.com/koresent/Dot-Cursors.git
cd Dot-Cursors
chmod +x install.sh
./install.sh
```

For system-wide installation, run with `sudo`:
```bash
sudo ./install.sh --system
```

#### Manual Install

Copy the theme folders to your user icons directory:

```bash
mkdir -p ~/.local/share/icons
cp -r Linux/Dot-Black Linux/Dot-White ~/.local/share/icons/
```

#### Applying the Cursor Theme

- **GNOME / Tweaks:** Open **GNOME Tweaks** → **Appearance** → **Cursor** → select `Dot-Black` or `Dot-White` (or run `gsettings set org.gnome.desktop.interface cursor-theme 'Dot-Black'`).
- **KDE Plasma:** Open **System Settings** → **Colors & Themes** → **Cursors** → select `Dot-Black` or `Dot-White` (or run `plasma-apply-cursortheme Dot-Black`).
- **XFCE:** Open **Settings** → **Mouse and Touchpad** → **Theme** tab → select `Dot-Black` or `Dot-White`.
- **Wayland (Hyprland / Sway):** Set environment variables in your compositor config:
  ```ini
  env = XCURSOR_THEME,Dot-Black
  env = XCURSOR_SIZE,32
  ```
