# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass


global_style = """
    #centralwidget {
        border-image: url(images/background_lite.png) 0 0 0 0 stretch stretch;
    }

    QToolBar QToolButton {
        background-color: transparent;
        border: 1px solid #555;
        border-radius: 4px;
        padding-right: 18px;
    }

    QToolBar QToolButton:hover {
        background-color: #e8efeb;
    }

    /* Fix for invisible placeholder text on X11 */
    QLineEdit {
        color: #333333; /* Dark text for light backgrounds */
        background-color: #ffffff;
        border: 1px solid #cccccc;
        padding: 4px;
    }

    QLineEdit::placeholder {
        color: #888888; /* Explicitly set gray placeholder */
    }

    QToolButton#tooltip {
        color: grey;
        background-color: rgba(0,0,0,0); /* Explicitly zero alpha */
        background: none;               /* Force no background image/fill */
        border: none;                   /* Remove native borders */
        font-weight: bold;
    }

    QToolButton#tooltip:hover {
        color: blue;
    }

    /* Standardize ToolBar buttons */
    QToolBar QWidget {
        margin: 2px;
    }

    QSplitter::handle {
        background-color: #cccccc; /* Light gray line */
        margin: 2px;
    }

    QSplitter::handle:vertical {
        height: 4px;
        image: url(handle_dots.png); /* Optional: add a grip icon */
    }

    QSplitter::handle:hover {
        background-color: #3498db; /* Blue highlight when hovering */
    }

    /*QListWidget::item {
        padding: 5px;
    }*/

    QListWidget::item:selected {
        background-color: #3498db;
        color: white;
        font-weight: bold;
    }

    QListWidget::item:hover {
        background-color: #99c6fc;
    }
"""
