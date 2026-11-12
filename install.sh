#!/bin/sh
# Install or update PC Pulse for the current user, then reload it if it is on the panel.
set -e
UUID="pc-pulse@puneet"
SRC="$(cd "$(dirname "$0")" && pwd)/$UUID/files/$UUID"
DEST="$HOME/.local/share/cinnamon/applets/$UUID"
mkdir -p "$DEST"
cp -r "$SRC"/. "$DEST"/
echo "Installed to $DEST"
if command -v dbus-send >/dev/null 2>&1; then
    dbus-send --session --print-reply --dest=org.Cinnamon.LookingGlass /org/Cinnamon/LookingGlass \
        org.Cinnamon.LookingGlass.ReloadExtension string:"$UUID" string:'APPLET' >/dev/null 2>&1 \
        && echo "Reloaded. If it is not on your panel yet: right click the panel > Applets > PC Pulse > +" \
        || echo "Add it: right click the panel > Applets > PC Pulse > +"
fi
