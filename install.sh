#!/usr/bin/env bash
# Dot Cursors Linux Installer

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
THEMES_SRC="$SCRIPT_DIR/Linux"

# Determine target directory
if [ "$EUID" -eq 0 ]; then
    TARGET_DIR="/usr/share/icons"
    MODE="system-wide"
else
    TARGET_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/icons"
    MODE="user"
fi

show_help() {
    echo "Dot Cursors Installer for Linux"
    echo ""
    echo "Usage: ./install.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -u, --user       Install for current user only ($TARGET_DIR)"
    echo "  -s, --system     Install system-wide (/usr/share/icons, requires root)"
    echo "  --uninstall      Remove installed themes"
    echo "  -h, --help       Show this help message"
    echo ""
}

uninstall_themes() {
    echo "Removing Dot Cursors from $TARGET_DIR..."
    rm -rf "$TARGET_DIR/Dot-Black"
    rm -rf "$TARGET_DIR/Dot-White"
    if [ "$MODE" = "user" ] && [ -d "$HOME/.icons" ]; then
        rm -rf "$HOME/.icons/Dot-Black"
        rm -rf "$HOME/.icons/Dot-White"
    fi
    echo "Dot Cursors uninstalled successfully."
    exit 0
}

# Parse options
while [ "$#" -gt 0 ]; do
    case "$1" in
        -u|--user)
            TARGET_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/icons"
            MODE="user"
            shift
            ;;
        -s|--system)
            TARGET_DIR="/usr/share/icons"
            MODE="system-wide"
            if [ "$EUID" -ne 0 ]; then
                echo "Error: System-wide installation requires root privileges. Please run with sudo."
                exit 1
            fi
            shift
            ;;
        --uninstall)
            uninstall_themes
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

if [ ! -d "$THEMES_SRC" ]; then
    echo "Error: Source themes directory '$THEMES_SRC' not found."
    exit 1
fi

echo "=========================================="
echo " Installing Dot Cursors ($MODE)"
echo " Destination: $TARGET_DIR"
echo "=========================================="

mkdir -p "$TARGET_DIR"

for THEME in Dot-Black Dot-White; do
    if [ -d "$THEMES_SRC/$THEME" ]; then
        echo "Installing $THEME..."
        rm -rf "$TARGET_DIR/$THEME"
        cp -r "$THEMES_SRC/$THEME" "$TARGET_DIR/"

        # Also create symlink in ~/.icons for legacy compatibility if user mode
        if [ "$MODE" = "user" ]; then
            mkdir -p "$HOME/.icons"
            ln -sf "$TARGET_DIR/$THEME" "$HOME/.icons/$THEME" 2>/dev/null || true
        fi
    fi
done

# Update icon caches if gtk-update-icon-cache is available
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    echo "Updating icon caches..."
    gtk-update-icon-cache -q -t "$TARGET_DIR/Dot-Black" 2>/dev/null || true
    gtk-update-icon-cache -q -t "$TARGET_DIR/Dot-White" 2>/dev/null || true
fi

echo ""
echo "Installation complete!"
echo ""
echo "How to apply the cursor theme:"
echo "------------------------------------------"
echo "  * GNOME / Tweaks: Open 'GNOME Tweaks' -> Appearance -> Cursor -> Select 'Dot-Black' or 'Dot-White'"
echo "    or run: gsettings set org.gnome.desktop.interface cursor-theme 'Dot-Black'"
echo ""
echo "  * KDE Plasma: System Settings -> Colors & Themes -> Cursors -> Select 'Dot-Black' or 'Dot-White'"
echo "    or run: plasma-apply-cursortheme Dot-Black"
echo ""
echo "  * XFCE: Settings -> Mouse and Touchpad -> Theme tab -> Select 'Dot-Black' or 'Dot-White'"
echo ""
echo "  * Wayland (Hyprland / Sway):"
echo "    Set in your config: env = XCURSOR_THEME,Dot-Black"
echo "                        env = XCURSOR_SIZE,32"
echo "=========================================="
