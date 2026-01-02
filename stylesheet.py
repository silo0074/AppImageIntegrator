# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass

from Logic import get_resource_path

# Get the absolute path to the image inside the AppImage
bg_image_path = get_resource_path("images/background_lite.png")

# Using {{ and }} for the CSS blocks so Python treats them as text.
global_style = f"""
    QWidget {{
        font-size: 11pt;
    }}

    #centralwidget {{
        border-image: url({bg_image_path}) 0 0 0 0 stretch stretch;
    }}

    QToolBar QToolButton {{
        background-color: transparent;
        border: 1px solid #555;
        border-radius: 4px;
        padding-right: 18px;
    }}

    QToolBar QToolButton:hover {{
        background-color: #e8efeb;
    }}

    QLineEdit {{
        color: #333333;
        background-color: #ffffff;
        border: 1px solid #cccccc;
        padding: 4px;
    }}

    QLineEdit::placeholder {{
        color: #888888;
    }}

    QToolButton#tooltip {{
        color: grey;
        background-color: rgba(0,0,0,0);
        background: none;
        border: none;
        font-weight: bold;
    }}

    QToolButton#tooltip:hover {{
        color: blue;
    }}

    QToolBar QWidget {{
        margin: 2px;
    }}

    QSplitter::handle {{
        background-color: #cccccc;
        margin: 2px;
    }}

    QSplitter::handle:vertical {{
        height: 4px;
        /*image: url(handle_dots.png);*/
    }}

    QSplitter::handle:hover {{
        background-color: #3498db;
    }}

    QListWidget::item:selected {{
        background-color: #3498db;
        color: white;
        font-weight: bold;
    }}

    QListWidget::item:hover {{
        background-color: #99c6fc;
    }}
"""
