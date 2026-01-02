# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass


import os
import re
import sys
import shutil
import subprocess
import tempfile
from pathlib import Path

from PySide6.QtWidgets import (
    QLabel, QSizePolicy, QFrame,
    QVBoxLayout,
)

from PySide6.QtCore import (
    QThread, Signal, QSettings, Qt, QPoint,
)

from PySide6.QtGui import (
    QPixmap,
    # QFontMetrics
)

import config


# ------------------------------------------------------------------
# Get absolute path to resource, works for dev and for PyInstaller
# ------------------------------------------------------------------
def get_resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# ------------------------------------------------------------------
# Build and save a .desktop file
# ------------------------------------------------------------------
class DesktopFileHandler:
    def __init__(self, data_dict=None, escape_exec=True):
        self.data = data_dict or {}
        self.escape = escape_exec

    def set_data(self, data_dict):
        self.data = data_dict

    def build_content(self):
        """Generates the string content for a .desktop file."""
        lines = ["[Desktop Entry]"]
        for key, value in self.data.items():
            if not value:
                continue  # Skip empty fields

            # Add special formatting for specific keys if needed
            if self.escape and key == "Exec":
                # Ensure the path is quoted if it contains spaces and add %F
                lines.append(f'{key}="{value}" %F')
            elif key == "Terminal" or key == "StartupNotify":
                # These are usually booleans; ensure they are lowercase
                lines.append(f"{key}={str(value).lower()}")
            else:
                # Standard key=value pair
                lines.append(f"{key}={value}")
        return "\n".join(lines)

    def save(self, destination_path):
        """Writes the content to disk and sets executable permissions."""
        dest_dir = os.path.dirname(destination_path)
        if not os.path.exists(dest_dir):
            # Create the directory if it doesn't exist (~/.local/share/applications)
            os.makedirs(dest_dir, exist_ok=True)

        content = self.build_content()
        with open(destination_path, 'w') as f:
            f.write(content)

        # Ensure executable permissions (chmod +x)
        mode = os.stat(destination_path).st_mode
        os.chmod(destination_path, mode | 0o111)

    @staticmethod
    def deploy_to_desktop(source_file, desktop_filename):
        """Copies the generated file to the user's Desktop folder."""
        desktop_path = Path.home() / "Desktop" / desktop_filename
        shutil.copy2(source_file, desktop_path)


# ------------------------------------------------------------------
# Extract AppImage, find icon and desktop file
# Copy icon to ~/.local/share/icons
# Return icon path and contents of desktop file
# ------------------------------------------------------------------
class AppImageParser(QThread):
    # Signals: (icon_path, desktop_entries_dict)
    started_task = Signal() # Notification that work has begun
    finished = Signal(str, list)
    error = Signal(str)

    def __init__(self, appimage_path, destination_folder):
        super().__init__()
        self.appimage_path = os.path.abspath(appimage_path)
        self.destination_folder = os.path.abspath(destination_folder)
        # Force the extraction directory to be an absolute path near the AppImage
        # self.extract_dir = os.path.join(os.path.dirname(self.appimage_path), "squashfs-root")
        self.temp_dir = tempfile.mkdtemp()
        self.extract_dir = os.path.join(self.temp_dir, "squashfs-root")

        self.process = None  # Reference to the subprocess
        self._is_killed = False

    def stop(self):
        # Called from the main thread to kill the process.
        self._is_killed = True
        if self.process and self.process.poll() is None:
            # Send termination signal
            self.process.terminate()
            # Or self.process.kill() for a forced exit

            # Cleanup old extraction if exists
            if os.path.exists(self.extract_dir):
                shutil.rmtree(self.extract_dir)

    def run(self):
        self.started_task.emit()
        try:
            # Cleanup old extraction if exists
            if os.path.exists(self.extract_dir):
                shutil.rmtree(self.extract_dir)

            # Use Popen instead of run()
            self.process = subprocess.Popen(
                [self.appimage_path, "--appimage-extract"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.temp_dir
            )

            # Wait for completion while checking if we should abort
            stdout, stderr = self.process.communicate()

            if self._is_killed:
               return # Exit silently if we killed it intentionally

            if self.process.returncode != 0:
               self.error.emit(f"Extraction failed: {stderr}")
               return

            # Find Icon and Desktop
            icon_path = self.get_appimage_icon()
            desktop_data = self.get_appimage_desktop()

            # Cleanup
            if os.path.exists(self.extract_dir):
                shutil.rmtree(self.extract_dir)

            self.finished.emit(icon_path or "", desktop_data)

        except Exception as e:
            if not self._is_killed:
                self.error.emit(str(e))

    def get_appimage_icon(self):
        base_name = os.path.splitext(os.path.basename(self.appimage_path))[0].lower()
        search_key = re.split(r'[\s\-]', base_name)[0]
        valid_exts = ('.svg', '.png', '.ico')

        for filename in os.listdir(self.extract_dir):
            if filename.lower().endswith(valid_exts) and search_key in filename.lower():
                src = os.path.join(self.extract_dir, filename)
                dst = os.path.join(self.destination_folder, filename)
                os.makedirs(self.destination_folder, exist_ok=True)
                shutil.copy2(src, dst)
                return dst
        return None

    def get_appimage_desktop(self):
        entries = []  # Use a list to hold tuples
        desktop_files = [f for f in os.listdir(self.extract_dir) if f.lower().endswith(".desktop")]
        if not desktop_files:
            return entries

        path = os.path.join(self.extract_dir, desktop_files[0])
        with open(path, 'r', encoding='utf-8') as f:
            found_keys = set()
            for line in f:
                line = line.strip()
                if not line or line.startswith('[') or line.startswith('#'):
                    continue

                if '=' in line:
                    key, val = line.split('=', 1)
                    key = key.strip()
                    if key not in found_keys:
                        entries.append((key, val.strip()))  # Store as a tuple
                        found_keys.add(key)
        return entries



# ----------------------------------------------------------------------
# Save current default app for each mime in a config file
# Set new default app for each mime
# ----------------------------------------------------------------------
class MimeWorker(QThread):
    progress = Signal(int, str)  # Sends percentage and current mime name
    finished = Signal()

    def __init__(self, desktop_name, mime_data):
        super().__init__()
        self.desktop_name = desktop_name
        self.mime_data = mime_data
        self._is_running = True # Control flag

    def stop(self):
        self._is_running = False

    def run(self):
        mime_types = [mt.strip() for mt in self.mime_data.split(";") if mt.strip()]
        total = len(mime_types)

        settings = QSettings(config.AppConfig.APP_NAME, "MimeBackups")

        for i, mt in enumerate(mime_types):
            if not self._is_running: # Check if we should abort
                break

            # Update UI
            self.progress.emit(int((i / total) * 100), mt)

            # Query the CURRENT default app for this mimetype
            result = subprocess.run(["xdg-mime", "query", "default", mt], capture_output=True, text=True)
            current = result.stdout.strip()

            # Save the backup only if it's not already our own app
            if current and current != self.desktop_name:
                settings.setValue(f"{self.desktop_name}/{mt}", current)

            # Set the new default
            subprocess.run(["xdg-mime", "default", self.desktop_name, mt], stderr=subprocess.DEVNULL)

        # Qt will automatically emit the signal
        # Comment this to prevent the signal to be emitted twice
        # self.finished.emit()



# ----------------------------------------------------------------------
# Creates a custom tooltip
# ----------------------------------------------------------------------
class InteractiveHelp(QLabel):
    def __init__(self, text, btn, parent=None):
        super().__init__(parent)
        # Set to RichText to render HTML
        self.setTextFormat(Qt.RichText)
        # Setup window flags to look like a tooltip but stay active
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint)
        self.btn = btn

        self.setStyleSheet("""
            QLabel {
                color: black;
                border: 1px solid #555555;
                padding: 8px;
                border-radius: 4px;
            }
        """)

        self.setText(text)
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.setWordWrap(True)
        # self.setMinimumWidth(500)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Install event filter to detect when the mouse leaves the POPUP
        self.installEventFilter(self)

    # def eventFilter(self, watched, event):
    #     if event.type() == QEvent.Leave:
    #         self.hide()
    #     return super().eventFilter(watched, event)

    def show_at(self, widget):
        # Position it to the right of the button
        pos = widget.mapToGlobal(QPoint(widget.width() + 5, 0))
        self.move(pos)
        self.show()


# ----------------------------------------------------------------------
# Icon browser.
# A custom clickable widget for each icon thumbnail.
# ----------------------------------------------------------------------
class IconThumbnail(QFrame):
    def __init__(self, icon_path, icon_name, parent_input):
        super().__init__()
        self.icon_path = icon_path
        self.icon_name = icon_name
        self.parent_input = parent_input

        self.setFixedSize(100, 80)
        self.setFrameShape(QFrame.StyledPanel)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(2, 5, 2, 5) # Left, Top, Right, Bottom
        self.layout.setSpacing(2)

        # Thumbnail Image
        self.img_label = QLabel()
        pixmap = QPixmap(icon_path).scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.img_label.setPixmap(pixmap)
        self.img_label.setAlignment(Qt.AlignCenter)

        # Icon Name
        self.name_label = QLabel(icon_name)
        self.name_label.setStyleSheet("font-size: 8pt;")
        self.name_label.setWordWrap(True)
        self.name_label.setAlignment(Qt.AlignCenter)

        # Get font metrics to calculate text width
        # metrics = QFontMetrics(self.name_label.font())
        # Elide the text if it's wider than 80px (90px frame minus margins)
        # elided_text = metrics.elidedText(icon_name, Qt.ElideMiddle, 80)
        # self.name_label.setText(elided_text)

        # Add a tooltip so the user can still see the full name on hover
        self.setToolTip(icon_name)

        self.layout.addWidget(self.img_label)
        self.layout.addWidget(self.name_label)

    def mousePressEvent(self, event):
        # When clicked, set the parent input field to this icon's path/name
        self.parent_input.setText(self.icon_path)
        self.setStyleSheet("background-color: #3daee9;")

        # Check if the attribute exists AND is not None
        prev = getattr(self.parent_input, 'previous_element', None)
        if prev is not None:
            try:
                prev.setStyleSheet("background-color: white;")
            except RuntimeError:
                # This handles cases where the previous widget was deleted by C++
                pass
        self.parent_input.previous_element = self


# ----------------------------------------------------------------------
# create_desktop_icon
# ----------------------------------------------------------------------
def create_desktop_icon():
    # Get the current AppImage path
    app_path = os.path.realpath(sys.argv[0])

    # Get the localized Desktop path using xdg-user-dir
    try:
        import subprocess
        desktop_path = subprocess.check_output(['xdg-user-dir', 'DESKTOP']).decode('utf-8').strip()
    except:
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    shortcut_path = os.path.join(desktop_path, f"{config.AppConfig.APP_NAME}.desktop")
    if os.path.exists(shortcut_path):
        return

    # Define the desktop entry content
    desktop_entry = f"""[Desktop Entry]
Type=Application
Name={config.AppConfig.APP_NAME}
Comment=Manage your AppImages and edit existing desktop files
Exec={app_path}
Icon=system-software-install
Terminal=false
StartupWMClass=AppImageIntegrator-x86_64.AppImage
Categories=Utility;
"""

    with open(shortcut_path, "w") as f:
        f.write(desktop_entry)

    # Make the shortcut executable (required by GNOME to trust it)
    os.chmod(shortcut_path, 0o755)
