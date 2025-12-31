# AppImage Integrator

**AppImage Integrator** is a lightweight utility designed for Linux users (optimized for KDE Plasma) to "install" standalone AppImages into the desktop environment by creating desktop entries and associating MIME types, so your portable applications feel like native system installs.

---

## 🚀 Features

* **Native Desktop Integration**: Automatically generates `.desktop` files in your local applications folder.
* **Icon Browser & Management**: Features a built-in icon browser with search functionality to help you find and change the icon for desired MIME types that shows in file managers.
* **MIME Type Association**: Link specific file extensions to your AppImages so they appear in "Open With" menus.
* **MIME Finder Tool**: Includes a dedicated drag-and-drop utility to identify file types using the system's `QMimeDatabase`.
* **Clean Uninstall**: Safely removes desktop files and associated icons while restoring original MIME associations.

---

## 🛠️ Installation

### Prerequisites
Ensure you have Python 3.10+ installed on your Linux system.

### Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/silo0074/AppImageIntegrator.git
   cd appimage-integrator

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate

3. **Install dependencies**:
   ```bash
   pip install PySide6

## 📖 How to Use

1. **Integrate a New App**

* Launch the application and select "Create desktop file".
* Browse for your AppImage file.

* The tool will automatically parse the AppImage for metadata.

* Adjust the Name, Icon, and MIME Types in the dynamic form.

* Click Apply.
