![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?logo=python)
![Qt Version](https://img.shields.io/badge/Qt-6.x-green?logo=qt)
![PySide6](https://img.shields.io/badge/Framework-PySide6-blue?logo=qt)
![Release](https://img.shields.io/github/v/release/silo0074/AppImageIntegrator)
![Build Status](https://github.com/silo0074/AppImageIntegrator/actions/workflows/build-appimage.yml/badge.svg)

# AppImage Integrator

**AppImage Integrator** is a lightweight utility designed for Linux users (optimized for KDE Plasma) to "install" standalone AppImages into the desktop environment by creating desktop entries and associating MIME types, so your portable applications feel like native system installs.

---

## 🚀 Features

* **Native Desktop Integration**: Automatically generates `.desktop` files in your local applications folder.
* **Icon Browser & Management**: Features a built-in icon browser with search functionality to help you find and change the icon for desired MIME types that shows in file managers.
* **MIME Type Association**: Link specific file extensions to your AppImages so they appear in "Open With" menus.
* **Desktop file editor**: Existing .desktop files can be edited, useful for Wine apps.
* **MIME Finder Tool**: Includes a dedicated drag-and-drop utility to identify file types using the system's `QMimeDatabase`.
* **Clean Uninstall**: Safely removes desktop files and associated icons while restoring original MIME associations.

---

## 🛠️ Installation

### Prerequisites
* **Python 3.10 or higher**: Required for PySide6 compatibility.
* **Qt6 Libraries**: Typically included when installing PySide6 via pip, but required for the UI to render correctly on Linux.

### Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/silo0074/AppImageIntegrator.git
   cd AppImageIntegrator

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate

3. **Install dependencies**:
   ```bash
   pip install PySide6

## 📖 How to Use

**Integrate a New App**

* Launch the application and select "Create desktop file".
* Browse for your AppImage file.
* The tool will automatically parse the AppImage for metadata.
* Adjust the Name, Icon, and MIME Types in the dynamic form.
* Click Apply.

## 🛠️ Built With

* **[Python 3.10+](https://www.python.org/)** - The core programming language.
* **[Qt 6 / PySide6](https://doc.qt.io/qtforpython-6/)** - Used for the graphical user interface and system integration logic.
* **[Qt Designer](https://doc.qt.io/qt-6/qtdesigner-manual.html)** - Used for crafting the XML-based UI layouts (`form.ui`).

  
