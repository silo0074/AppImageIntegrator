<<<<<<< HEAD
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?logo=python)
![Qt Version](https://img.shields.io/badge/Qt-6.x-green?logo=qt)
![PySide6](https://img.shields.io/badge/Framework-PySide6-blue?logo=qt)
![Release](https://img.shields.io/github/v/release/silo0074/AppImageIntegrator)
=======
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)
![Qt Version](https://img.shields.io/badge/Qt-6.x-41CD52?logo=qt&logoColor=white)
![PySide6](https://img.shields.io/badge/Framework-PySide6-blue?logo=qt&logoColor=white)
[![Hosted on Codeberg](https://img.shields.io/badge/Hosted_on-Codeberg-7091AD?logo=codeberg&logoColor=white)](https://codeberg.org/silo0074/AppImageIntegrator)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](./LICENSE)
[![Release](https://img.shields.io/gitea/v/release/silo0074/AppImageIntegrator?gitea_url=https://codeberg.org)](https://codeberg.org/silo0074/AppImageIntegrator/releases)
>>>>>>> main-codeberg

# AppImage Integrator

**AppImage Integrator** is a lightweight utility designed for Linux users to "install" standalone AppImages into the desktop environment by creating desktop entries and associating MIME types, so your portable applications feel like native system installs.

---

## 🚀 Features

* **Native Desktop Integration**: Automatically generates `.desktop` files in your local applications folder.
* **Icon Browser & Management**: Features a built-in icon browser with search functionality to help you find and change the icon for desired MIME types that shows in file managers.
* **MIME Type Association**: Link specific file extensions to your AppImages so they appear in "Open With" menus.
* **Desktop file editor**: Existing .desktop files can be edited, useful for Wine apps.
* **MIME Finder Tool**: Includes a dedicated drag-and-drop utility to identify file types using the system's `QMimeDatabase`.
* **Clean Uninstall**: Safely removes desktop files and associated icons while restoring original MIME associations.

---

<br>

<<<<<<< HEAD
## 📸 Screenshots

| Main Interface | App Install |
| :---: | :---: |
| ![Main UI](./assets/AppIntegrator_screenshoot_01_Menu.png) | ![Create .desktop](./assets/AppIntegrator_screenshoot_02_Create.png) |

<br>

<details>
  <summary>🔍 Click to view more screenshots</summary>
  
  ![Set MIME icon](./assets/AppIntegrator_screenshoot_03_Mime_Icon.png)
  ![About page](./assets/AppIntegrator_screenshoot_04_About.png)
</details>

<br>
=======
| Menu Screen | Install AppImage |
| :---: | :---: |
| ![Menu](./assets/AppIntegrator_screenshoot_01_Menu.png) | ![Create](./assets/AppIntegrator_screenshoot_02_Create.png) |

<details>
<summary><b>Click to see more screenshots</b></summary>

#### Mime Icon
![Mime Icon](./assets/AppIntegrator_screenshoot_03_Mime_Icon.png)

#### About Screen
![About](./assets/AppIntegrator_screenshoot_04_About.png)

</details>


>>>>>>> main-codeberg

## 💡 Usage

After downloading the AppImage, right-click it and under **Properties -> Permissions**, check the **Execute** right. You can integrate the app itself the same way you would with other AppImages.
> [!TIP]
> To easily find your AppImage apps, I recommend placing them under `/home/youruser/Apps`.

<<<<<<< HEAD
<br>

## 📥 Download

The application binary can be downloaded as an AppImage from the [Releases](https://github.com/silo0074/AppImageIntegrator/releases) section.
The AppImage is automatically built by GitHub Actions using this workflow: [.github/workflows/build-appimage.yml](./.github/workflows/build-appimage.yml).

<br>
=======


## 📥 Download

The application binary can be downloaded as an AppImage from the [Releases](https://codeberg.org/silo0074/AppImageIntegrator/releases) section.

To verify the integrity of the download, run:

```bash
sha256sum -c AppImageIntegrator-x86_64.AppImage.sha256
```

Make it executable:
```bash
chmod +x AppImageIntegrator-x86_64.AppImage
```

>>>>>>> main-codeberg

## 🔨 Compiling

If you prefer to build the AppImage yourself, you can use the provided automation script: [build_appimage.sh](./build_appimage.sh).

1. **Clone the repository**:
   ```bash
<<<<<<< HEAD
   git clone https://github.com/silo0074/AppImageIntegrator.git
   cd AppImageIntegrator
=======
   git clone https://codeberg.org/silo0074/AppImageIntegrator.git
   cd AppImageIntegrator
   ```
>>>>>>> main-codeberg

2. **Run the script**:
   ```bash
   ./build_appimage.sh
<<<<<<< HEAD

<br>
=======
   ```


>>>>>>> main-codeberg

## 📖 How to Use

**Integrate a New App**

* Launch the application and select "Create desktop file".
* Browse for your AppImage file.
* The tool will automatically parse the AppImage for metadata.
* Adjust the Name, Icon, and MIME Types in the dynamic form.
* Click Apply.

<br>

<<<<<<< HEAD
## How does it work

The user can select an AppImage which will be temporarly unpacked to extract the icon and the desktop file. The icon will be copied in `.local/share/icons/` and a .desktop file will be created in `.local/share/applications`. The user can modify the desktop fields such as the application name or pick another icon. The MIME types can be selected using a list of check boxes. These tells the system what file types the application can handle so it can appear in the Open With menu.

Based on the settings inside the Options section, a desktop file can be created, the installed app can be set as default, the app icon can be used for selected MIME types to appear in the KDE file manager instead of the default ones. 

<br>

=======
>>>>>>> main-codeberg
## 🛠️ Built With

* **[Python 3.10+](https://www.python.org/)** - The core programming language.
* **[Qt 6 / PySide6](https://doc.qt.io/qtforpython-6/)** - Used for the graphical user interface and system integration logic.
* **[Qt Designer](https://doc.qt.io/qt-6/qtdesigner-manual.html)** - Used for crafting the XML-based UI layouts (`form.ui`).

<br>

## ❤️ Donations

<a href="https://www.buymeacoffee.com/liviuistrate" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="60px" width="217px">
</a>
  
