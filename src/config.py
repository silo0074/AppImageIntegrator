# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass

from pathlib import Path
from typing import Dict, List

# Necessary Desktop Fields
NECESSARY_FIELDS = ["Name", "Exec", "MimeType", "Type", "Icon", "Categories", "Keywords"]

# ---------- Configuration: known mime groups ----------
KNOWN_MIME_GROUPS: Dict[str, List[str]] = {
    "Images": [
        "image/png", "image/jpeg", "image/gif", "image/bmp", "image/svg+xml"
    ],
    "Audio": [
        "audio/mpeg", "audio/ogg", "audio/wav", "audio/flac"
    ],
    "Video": [
        "video/mp4", "video/x-matroska", "video/webm", "video/quicktime",
        "video/mpeg", "video/x-mpeg", "video/x-m4v", "video/3gp",
        "video/mkv", "video/flv", "video/x-flv", "video/dv", "video/x-msvideo",
        "video/x-ms-wmv", "video/x-ms-asf", "video/x-anim"
    ],
    "Documents": [
        "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "text/plain", "text/html"
    ],
    "Archives": [
        "application/zip", "application/x-tar", "application/x-7z-compressed", "application/x-rar"
    ]
}

# application/illustrator;application/pdf;application/postscript;application/visio;application/visio.drawing;application/vnd.corel-draw;application/vnd.ms-visio.viewer;application/vnd.visio;application/vsd;application/x-visio;application/x-vsd;application/x-xccx;application/x-xcdt;application/x-xcmx;image/svg+xml;image/svg+xml-compressed;image/x-emf;image/x-eps;image/x-vsd;image/x-wmf;image/x-xcdr;


CATEGORIES_LIST = [
    "AudioVideo", "Audio", "Video", "Development", "Education", "Game",
    "Graphics", "Network", "Office", "Science", "Settings", "System", "Utility"
]

# Keywords
"""
In a .desktop file, the Keywords field is designed to help users find your application
through the application launcher's search bar (like KRunner in KDE or the Activities search in GNOME).

Categories and Suggestions

App Category        Suggested Keywords (semicolon-separated)
--------------------------------------------------------------
Media Players       Video;Movie;Film;Clip;Player;Media;Streaming;Cinema;VLC;MP4;MKV;
Browsers            Internet;Web;Explorer;Navigator;WWW;Site;Cloud;Online;
Image Editors       Photo;Graphic;Design;Draw;Paint;SVG;Vector;Canvas;Retouch;Photoshop;
Office/Text         Write;Document;Notes;Edit;Editor;Word;Sheet;Presentation;PDF;
Utilities           Tool;Task;System;Helper;Manager;Config;Setup;
Games               Play;Entertainment;Simulation;Action;Arcade;Steam;
"""


class AppConfig:
    APP_NAME = "AppImageIntegrator"
    APP_VERSION = "1.0.2"

class PathConfig:
    APP_ICON_PATH = "icons/AppImageIntegrator.png"
    ICONS_DIR = Path.home() / ".local/share/icons/"
    DESKTOP_FILE_DIR = Path.home() / ".local/share/applications"

class UIConfig:
    PRIMARY_COLOR = "#3498db"
    FONT_SIZE = 12
