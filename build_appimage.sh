#!/bin/bash
set -e

# Path to config file
CONFIG_FILE="src/config.py"

# Extract the version string
# This looks for the line starting with APP_VERSION,
# then uses sed to grab only the text inside the quotes.
export VERSION=$(grep "APP_VERSION =" "$CONFIG_FILE" | sed -E 's/.*"([^"]+)".*/\1/')

echo "------------------------------------------------"
echo "BUILDING VERSION: $VERSION"
echo "------------------------------------------------"

# Constants
APP_NAME="AppImageIntegrator"
APP_ICON="src/icons/AppImageIntegrator.png"
APP_DESKTOP="AppImageIntegrator.desktop"
APP_DIR="AppDir"
export VERSION=$VERSION

# Define tools directory
TOOLS_DIR="build_tools"
mkdir -p "$TOOLS_DIR"

# Binary paths
LINUXDEPLOY="$TOOLS_DIR/linuxdeploy-x86_64.AppImage"
APPIMAGETOOL="$TOOLS_DIR/appimagetool-x86_64.AppImage"
APPIMAGE_RUNTIME="$TOOLS_DIR/runtime-x86_64"

# Setup & Dependencies
rm -rf dist build $APP_DIR

if [ -f AppImageIntegrator.spec ]; then
    rm AppImageIntegrator.spec
fi

python3 -m venv venv
source venv/bin/activate

# Use requirements.txt instead of manual pip install
if [ -f requirements.txt ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install pyinstaller  # Ensure pyinstaller is available in venv
else
    echo "requirements.txt not found! Falling back to manual install..."
    pip install PySide6 pyinstaller
fi

# PyInstaller Build
# Creates the bundled folder in dist/AppImageIntegrator/
pyinstaller --noconfirm --onedir --windowed \
    --name ${APP_NAME} \
    --add-data "src/images:images" \
    --add-data "src/icons:icons" \
    src/main.py

# Fetch appimagetool (if missing)
if [ ! -f "$APPIMAGETOOL" ]; then
    wget -q -N https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage -O "$APPIMAGETOOL"
    chmod +x "$APPIMAGETOOL"
fi

# Download linuxdeploy
if [ ! -f "$LINUXDEPLOY" ]; then
    wget -q -N https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage -O "$LINUXDEPLOY"
    chmod +x "$LINUXDEPLOY"
fi

# Download runtime-x86_64
if [ ! -f "$APPIMAGE_RUNTIME" ]; then
    wget -q -N https://github.com/AppImage/type2-runtime/releases/download/continuous/runtime-x86_64 -O "$APPIMAGE_RUNTIME"
    chmod +x "$APPIMAGE_RUNTIME"
fi


# Structure AppDir MANUALLY to preserve PyInstaller's layout
echo "Structuring AppDir..."
mkdir -p $APP_DIR/usr/bin
mkdir -p $APP_DIR/usr/share/applications
mkdir -p $APP_DIR/usr/share/icons/hicolor/256x256/apps/

# Copy EVERYTHING from PyInstaller's output folder into usr/bin
# This keeps the '_internal' folder relative to the executable
cp -r dist/${APP_NAME}/* $APP_DIR/usr/bin/

# Use linuxdeploy ONLY for Desktop/Icon/Metadata
# We point --executable to the file ALREADY in the AppDir
export EXTRA_QT_PLUGINS="platforms;styles"

"$LINUXDEPLOY" \
    --appdir $APP_DIR \
    --executable $APP_DIR/usr/bin/${APP_NAME} \
    --icon-file $APP_ICON \
    --desktop-file $APP_DESKTOP \

# Manual Packaging with appimagetool
# This uses the local runtime file to avoid the download error.
"$APPIMAGETOOL" \
    --runtime-file "$APPIMAGE_RUNTIME" \
    $APP_DIR \
    ${APP_NAME}-x86_64.AppImage


# Post-Build Verification
echo "VERIFYING LIBRARIES..."
# Check the files in AppDir before we turn it into an AppImage. No execution needed!
ldd $APP_DIR/usr/bin/${APP_NAME} | grep "not found" || echo "All libraries resolved."

echo "STARTING TEST EXECUTION..."
timeout 3s ./${APP_NAME}-x86_64.AppImage || {
    if [ $? -eq 124 ]; then
        echo "SUCCESS: AppImage launched correctly."
    else
        echo "ERROR: AppImage failed to launch."
        exit 1
    fi
}
