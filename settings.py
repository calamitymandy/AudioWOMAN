# settings.py for dmgbuild

# Volume name
volume_name = "AudioWOMAN"

# Path to the application to include in the DMG
files = [
    "dist/AudioWOMAN.app"  # Adjust the path if your .app is located elsewhere
]

# Disk image format (default is "UDZO")
format = "UDZO"

# Default icon size
dmg_icon_size = 128

# Do not hide extensions (empty list, no boolean)
hide_extensions = []

# Volume size (optional: dmgbuild will calculate this automatically)
# volume_size = "200M"
