# This Python file uses the following encoding: utf-8
import sys
import os
# import re
# import shutil
import subprocess
from pathlib import Path
from typing import Dict

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QCheckBox, QPushButton,
    QMessageBox, QSizePolicy, QLabel, QLineEdit, QFormLayout,
    QSplitter, QListWidget, QAbstractItemView, QFileDialog, QProgressBar,
    # QGroupBox,
    # QPushButton,
    QGridLayout,
    QStyleFactory,
    QToolButton,
    # QToolTip,
    QMenu,
    QDialogButtonBox, QDialog,
    QSpacerItem,
    # QGraphicsOpacityEffect,
    # QAbstractScrollArea,
)
from PySide6.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QPoint, QParallelAnimationGroup, QEvent,
    QSettings, QTimer, QThread, QCoreApplication, QMimeDatabase,
    # QRect
    # Signal,
)

from PySide6.QtGui import QPixmap, QIcon, QAction

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_Integrator

# import qdarktheme
from CustomWidgets import MimeGroupWidget, FlowLayout
from Logic import (
    DesktopFileHandler, AppImageParser, MimeWorker,
    InteractiveHelp, IconThumbnail,
    get_resource_path, create_desktop_icon,
)
import config
import stylesheet


# ------------------------------------------------------------------
# AboutDialog
# ------------------------------------------------------------------
class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Application")
        # self.setFixedSize(450, 450)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        layout = QVBoxLayout(self)

        # --- Header Layout (Icon + Title) ---
        header_layout = QHBoxLayout()

        # App Icon
        self.icon_label = QLabel()
        # Path to your icon file
        icon_path = get_resource_path("icons/AppIntegrator.png")
        pixmap = QPixmap(icon_path)
        self.icon_label.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        header_layout.addWidget(self.icon_label)

        # App Title and Version
        title_label = QLabel(f"<h1 style='color: #3daee9; margin-left: 10px;'>"
                           f"{config.AppConfig.APP_NAME} {config.AppConfig.APP_VERSION}</h1>")
        header_layout.addWidget(title_label)
        header_layout.addStretch() # Push everything to the left

        layout.addLayout(header_layout)

        # --- Description Area ---
        self.label = QLabel()
        self.label.setTextFormat(Qt.RichText)
        self.label.setOpenExternalLinks(True)
        self.label.setWordWrap(True)
        self.label.setText("""
            <div style='text-align: left;'>
                <p>Integrates an AppImage with the system by creating a desktop entry.
                Can also be used for editing an existing desktop file.</p>
                <p>Author: Liviu Istrate @ 2025<br>
                License: GPLv3 <br>
                Website: <a href='https://www.programming-electronics-diy.xyz'>programming-electronics-diy.xyz</a> <br>
                Support me: <a href='https://buymeacoffee.com/liviuistrate'>buymeacoffee.com/liviuistrate</a>
                </p>
                <hr>
                <p>Check for updates on <a href='https://github.com/yourprofile/repo'>GitHub</a></p>
            </div>
        """)
        layout.addWidget(self.label)

        # --- Bottom Buttons ---
        button_layout = QHBoxLayout()

        # About Qt Button
        self.btn_about_qt = QPushButton("About Qt")
        self.btn_about_qt.clicked.connect(lambda: QApplication.aboutQt())

        # Standard OK Button
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        self.buttons.accepted.connect(self.accept)

        button_layout.addWidget(self.btn_about_qt)
        button_layout.addStretch() # Push the OK button to the right
        button_layout.addWidget(self.buttons)

        layout.addLayout(button_layout)


# ------------------------------------------------------------------
# MimeFinderDialog
# ------------------------------------------------------------------
class MimeFinderDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Find MIME Type")
        self.setFixedSize(400, 200)
        self.setAcceptDrops(True) # Enable drag and drop

        layout = QVBoxLayout(self)

        self.label = QLabel("Drag and drop a file here to see its MIME type:")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("border: 2px dashed #aaa; padding: 20px; color: #666;")

        self.result_field = QLineEdit()
        self.result_field.setReadOnly(True)
        self.result_field.setPlaceholderText("MIME type will appear here...")

        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.accept)

        layout.addWidget(self.label)
        layout.addWidget(self.result_field)
        layout.addWidget(self.close_btn)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.label.setStyleSheet("border: 2px dashed #3498db; background: #e1f5fe;")

    def dragLeaveEvent(self, event):
        self.label.setStyleSheet("border: 2px dashed #aaa; background: transparent;")

    def dropEvent(self, event):
        self.label.setStyleSheet("border: 2px dashed #aaa; background: transparent;")
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            # Identify the MIME type
            mime = QMimeDatabase().mimeTypeForFile(file_path)
            self.result_field.setText(mime.name())
            self.result_field.selectAll()
            self.result_field.setFocus()


# ------------------------------------------------------------------
# Finds all 'field_' widgets and returns a clean dictionary.
# ------------------------------------------------------------------
class UIparseDesktopFields:
    @staticmethod
    def collect_data(container_widget):
        data = {}
        if not container_widget:
            return data

        # findChildren searches recursively, handling our Icon/Category containers automatically
        fields = container_widget.findChildren(QLineEdit)
        for le in fields:
            name = le.objectName()
            if name.startswith("field_"):
                key = name.replace("field_", "")
                data[key] = le.text().strip()
        return data


# ------------------------------------------------------------------
# Main class
# ------------------------------------------------------------------
class Integrator(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Integrator()
        self.ui.setupUi(self)

        icon_path = get_resource_path("icons/AppIntegrator.png")
        # icon_path = os.path.join(os.getcwd(), "icons/AppIntegrator.png")
        self.setWindowIcon(QIcon(icon_path))
        create_desktop_icon()

        # Variables
        self.action = "Menu"
        self.filePath = None # Path to selected AppImage or desktop file
        self.active_threads = []
        self.mime_list_1 = {}
        self.mime_list_2 = {}

        # ------------ Settings
        # Initialize QSettings (This points to ~/.config/AppIntegrator/settings.conf)
        self.settings = QSettings(config.AppConfig.APP_NAME , "settings")

        # Load the previous state
        self.load_settings()

        # ------------ Menu
        self.setup_toolbar()

        # ------------ Page 1
        # Tooltips for Options group
        help_btn = self.setup_help_button()
        help_btn.setProperty("help_text", "Set as default app for selected MIME types.")
        self.ui.layoutMakeDefault.addWidget(help_btn, Qt.AlignLeft)
        self.ui.layoutMakeDefault.addStretch()
        self.ui.layoutMakeDefault.setSpacing(2) # Controls the gap between text and [?]

        help_btn = self.setup_help_button()
        help_btn.setProperty("help_text", "Uses the app icon in file manager for associated files.")
        self.ui.layoutSetMIMEicon.addWidget(help_btn, Qt.AlignLeft)
        self.ui.layoutSetMIMEicon.addStretch()
        self.ui.layoutSetMIMEicon.setSpacing(2)

        help_btn = self.setup_help_button()
        help_btn.setProperty("help_text", "Creates a shortcut on your desktop folder.")
        self.ui.layoutAddToDesktop.addWidget(help_btn, Qt.AlignLeft)
        self.ui.layoutAddToDesktop.addStretch()
        self.ui.layoutAddToDesktop.setSpacing(2)

        # Set the alignment of the layout on page_1 to center items horizontally
        # This prevents the buttons from stretching to full width
        self.ui.layoutStartMenu.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        # ------------ Page 2
        self.ui.btnDo.setDisabled(True)
        # ------------ Page 3
        self.ui.btnDeintegrate.setDisabled(True)
        self.ui.layoutAppInfo.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        # ------------ Page 4
        # Create the tooltip
        tooltip = self.setup_help_button()
        tooltip.setProperty("help_text", "Clear the icon input to remove the overrides for selected MIME type(s).")

        # Force the form to respect right alignment for all labels
        self.ui.formLayout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        # Set the horizontal layout alignment to prevent internal stretching
        self.ui.layoutIconPath.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.ui.layoutIconPath.insertWidget(0, tooltip)

        # ADD PLACEHOLDER: This keeps the LineEdit starting at the same X-coordinate
        placeholder = QLabel()
        placeholder.setFixedWidth(20) # Match the exact width of the tooltip button
        placeholder2 = QLabel()
        placeholder2.setFixedWidth(20) # Match the exact width of the tooltip button
        self.ui.layoutMimeTypes.insertWidget(0, placeholder)
        self.ui.layoutIconSearch.insertWidget(0, placeholder2)

        # Add a clear action directly into the QLineEdit
        self.search_clear_action = QAction(self.ui.inputIconSearch)
        self.search_clear_action.setIcon(QIcon.fromTheme("edit-clear")) # Standard Linux clear icon
        self.search_clear_action.triggered.connect(self.ui.inputIconSearch.clear)

        # Put it at the end (TrailingPosition)
        self.ui.inputIconSearch.addAction(self.search_clear_action, QLineEdit.TrailingPosition)

        # Initially hide it because the input is empty
        self.search_clear_action.setVisible(False)

        # Connect to textChanged to toggle visibility
        self.ui.inputIconSearch.textChanged.connect(lambda: self.search_clear_action.setVisible(bool(self.ui.inputIconSearch.text())))

        self.generate_mime_list(self.mime_list_2, self.ui.mimeTypes, self.ui.formLayout, "inputMimeTypes")
        # Index 0 is the top widget (iconsBrowser), Index 1 is the bottom (scrollArea)
        self.ui.splitter.setStretchFactor(0, 4)  # Gives 80% of space to icons
        self.ui.splitter.setStretchFactor(1, 1)  # Gives 20% of space to MIME types
        total_height = sum(self.ui.splitter.sizes())
        # If the splitter hasn't rendered yet, use a default like 800
        if total_height == 0:
            total_height = 800

        # Set sizes: 75% for top, 25% for bottom
        self.ui.splitter.setSizes([total_height * 2 // 4, total_height // 4])

        # ------------ Placeholders
        # self.ui.inMimeTypes.setPlaceholderText("e.g. application/x-desktop;application/x-executable")

        # ----------- Listeners
        # Menu
        self.ui.actionHome.triggered.connect(self.setPageHome)
        self.ui.actionSetMimeIcon.triggered.connect(self.setMIMEiconPage)
        dialog = AboutDialog(self)
        self.ui.actionAbout.triggered.connect(dialog.exec)
        self.ui.actionClose.triggered.connect(self.close)
        self.ui.actionFindMimeType.triggered.connect(self.on_find_mime_type_triggered)
        # Startup page
        self.ui.btnMenuCreateDesktop.clicked.connect(self.setPageCreate)
        self.ui.btnMenuEditDesktop.clicked.connect(self.setPageEdit)
        self.ui.btnMenuUninstall.clicked.connect(self.setPageUninstall)
        # Create/edit desktop page
        self.ui.btnBrowse.clicked.connect(self.browse_file)
        self.ui.btnDo.clicked.connect(self.createDesktop)
        # Uninstall page
        self.ui.btnBrowseUninstall.clicked.connect(self.browse_uninstall_file)
        self.ui.btnDeintegrate.clicked.connect(self.perform_uninstall)
        # Set MIME icon page
        self.ui.inputIconSearch.textChanged.connect(self.filter_icons)
        self.ui.btnApplyMimeIcon.clicked.connect(self.changeMIMEicon)

        # Connect the custom signal from the UI widget to the async parser
        self.ui.inputAppPath.fileDropped.connect(self.handle_file_drop)
        QApplication.instance().aboutToQuit.connect(self.cleanup_before_exit)

        # ------------ Init UI
        # Set start-up page to page 1
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_1)
        # Create/change desktop page
        self.generate_mime_list(self.mime_list_1, self.ui.knownMimeTypes, self.ui.scrollAreaLayoutDesktopFields, "field_MimeType")
        self.ui.widgetMimeTypes.hide()

        # Create a progress bar for the status bar
        self.busy_indicator = QProgressBar()
        self.busy_indicator.setMaximumWidth(150)
        self.busy_indicator.setTextVisible(False)
        self.busy_indicator.hide()

        # Add it to the right side of the status bar
        self.ui.statusbar.addPermanentWidget(self.busy_indicator)

        QTimer.singleShot(50, self.force_initial_layout)

        # ----------- Animation setup
        # Opacity
        # self.opacity_effect = QGraphicsOpacityEffect()
        # self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        # self.animation.setDuration(400)  # Time in milliseconds
        # self.animation.setStartValue(0.0)
        # self.animation.setEndValue(1.0)
        # self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Remove the effect when the animation stops
        # self.animation.finished.connect(self.on_animation_finished)


    # ------------------------------------------------------------------
    # setup_toolbar
    # ------------------------------------------------------------------
    def setup_toolbar(self):
        # Add the Home Action to the left
        self.ui.toolBar.addAction(self.ui.actionHome)
        self.ui.actionHome.setVisible(False)

        # Create an expanding spacer widget
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Add the spacer to the toolbar
        self.ui.toolBar.addWidget(spacer)

        # Add Utilities action
        self.ui.toolBar.addAction(self.ui.actionUtilities)

        # Create the menu container
        utils_menu = QMenu(self)

        # Add existing actions to the menu
        utils_menu.addAction(self.ui.actionSetMimeIcon)
        utils_menu.addAction(self.ui.actionFindMimeType)

        # Find the ToolButton widget
        utils_btn = self.ui.toolBar.widgetForAction(self.ui.actionUtilities)

        # Convert the button into a menu button
        if utils_btn:
            utils_btn.setMenu(utils_menu)
            # InstantPopup makes the menu appear immediately on click
            utils_btn.setPopupMode(QToolButton.InstantPopup)
            utils_btn.setStyleSheet("""
                QToolButton::menu-indicator {
                    subcontrol-origin: padding;
                    subcontrol-position: right center;

                }
            """)

        # About action
        self.ui.toolBar.addAction(self.ui.actionAbout)

        # Add the Close button/action (it will be pushed to the right)
        self.ui.toolBar.addAction(self.ui.actionClose)



    # ------------------------------------------------------------------
    # Load Settings
    # ------------------------------------------------------------------
    def load_settings(self):
        geometry = self.settings.value("geometry")
        if geometry:
            # If the user has a saved preference, use it
            self.restoreGeometry(geometry)
        else:
            # FIRST RUN: Apply your screen-based logic
            self.setup_initial_window_size()

    # ------------------------------------------------------------------
    # Save settings
    # ------------------------------------------------------------------
    def save_settings(self):
        # Save the window size and position
        self.settings.setValue("geometry", self.saveGeometry())

    # ------------------------------------------------------------------
    # Set initial window size
    # ------------------------------------------------------------------
    def setup_initial_window_size(self):
        # Get the current screen geometry
        screen = self.screen()
        geom = screen.availableGeometry()
        screen_h = geom.height()

        # Keep the width exactly as it is now
        current_w = self.width()

        # Determine Height based on Screen size
        if screen_h < 800:
            # SMALL SCREEN: Use 95% of height (almost fullscreen vertical)
            # No 15% margins here to avoid the window becoming a tiny sliver
            target_h = int(screen_h * 0.95)
        else:
            # LARGE SCREEN: Apply 15% margins (70% total height)
            target_h = int(screen_h * 0.70)

        # Apply size and constraints
        self.setMinimumHeight(550) # Prevent it from being dragged too small
        self.setMaximumHeight(16777215) # Ensure it remains resizable by user

        self.resize(current_w, target_h)

        # Calculate X to center horizontally
        # (Screen Width - Window Width) / 2
        target_x = geom.left() + (geom.width() - self.width()) // 2

        # Center vertically on the screen
        # We use geom.top() to account for systems where the taskbar is at the top
        y = geom.top() + (screen_h - target_h) // 2
        self.move(target_x, y)


    # ------------------------------------------------------------------
    # Animation: Sliding
    # ------------------------------------------------------------------
    def slide_to_page(self, target_page, direction="forward"):
        current_page = self.ui.stackedWidget.currentWidget()
        if current_page == target_page:
            return

        width = self.ui.stackedWidget.width()

        # Determine offset based on direction
        # Forward: New page comes from right (width), Old page goes to left (-width)
        # Back: New page comes from left (-width), Old page goes to right (width)
        offset = width if direction == "forward" else -width

        # 1. Setup Animation for the Current (Old) Page
        self.anim_old = QPropertyAnimation(current_page, b"pos")
        self.anim_old.setDuration(500)
        self.anim_old.setStartValue(QPoint(0, 0))
        self.anim_old.setEndValue(QPoint(-offset, 0))
        self.anim_old.setEasingCurve(QEasingCurve.Type.OutCubic)
        # self.anim_old.setEasingCurve(QEasingCurve.Type.OutBounce)

        # 2. Setup Animation for the Target (New) Page
        self.anim_new = QPropertyAnimation(target_page, b"pos")
        self.anim_new.setDuration(500)
        self.anim_new.setStartValue(QPoint(offset, 0))
        self.anim_new.setEndValue(QPoint(0, 0))
        self.anim_new.setEasingCurve(QEasingCurve.Type.OutCubic)
        # self.anim_new.setEasingCurve(QEasingCurve.Type.OutBounce)

        # 3. Group and Execute
        self.anim_group = QParallelAnimationGroup()
        self.anim_group.addAnimation(self.anim_old)
        self.anim_group.addAnimation(self.anim_new)

        target_page.show()
        target_page.raise_()
        target_page.move(offset, 0)

        # Clean up and formalize switch on finish
        self.anim_group.finished.connect(lambda: self.on_slide_finished(target_page, current_page))
        self.anim_group.start()

    # ------------------------------------------------------------------
    # Animation: Finished
    # ------------------------------------------------------------------
    def on_slide_finished(self, target_page, old_page):
        self.ui.stackedWidget.setCurrentWidget(target_page)
        old_page.move(0, 0)
        # Important: Always disconnect to prevent multiple triggers next time
        self.anim_group.finished.disconnect()

        if target_page == self.ui.page_1:
            self.ui.actionHome.setVisible(False)
        else:
            self.ui.actionHome.setVisible(True)

        if target_page == self.ui.page_4:
            self.ui.statusbar.showMessage("Searching for icons...", 5000)
            QCoreApplication.processEvents() # force Qt to show statusbar message
            self.load_icons()

    # ------------------------------------------------------------------
    # Animation: Opacity
    # ------------------------------------------------------------------
    # def fade_to_page(self, target_page):
    #     # 1. Create a NEW effect every time to avoid the "already deleted" error
    #     self.opacity_effect = QGraphicsOpacityEffect()
    #     target_page.setGraphicsEffect(self.opacity_effect)

    #     # 2. Re-link the animation to the NEW effect
    #     self.animation.setTargetObject(self.opacity_effect)

    #     # 3. Store reference for cleanup
    #     self.current_animating_page = target_page

    #     # 4. Standard transition logic
    #     self.ui.stackedWidget.setCurrentWidget(target_page)
    #     self.animation.start()

    # def on_animation_finished(self):
    #     # Strip the effect so the widget renders normally again
    #     if hasattr(self, 'current_animating_page'):
    #         self.current_animating_page.setGraphicsEffect(None)


    # ----------------------------------------------------------------------
    # force_initial_layout
    # ----------------------------------------------------------------------
    def force_initial_layout(self):
        # Switch to page 2 (where knownMimeTypes is)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)

        # Force the scroll area to realize how big it is
        self.ui.knownMimeTypes.widget().adjustSize()

        # Return to page 1
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_1)


    # ------------------------------------------------------------------
    # GUI: create Mime list
    # ------------------------------------------------------------------
    def generate_mime_list(self, group_name, container, source, field_name):
        groups_widget = QWidget()
        groups_layout = QVBoxLayout(groups_widget)
        group_name.clear()

        for group, mime_list in config.KNOWN_MIME_GROUPS.items():
            gw = MimeGroupWidget(group, mime_list)
            # Connect the widget to our update logic
            gw.mimeChanged.connect(lambda: self.update_mimetype_field(group_name, source, field_name))
            groups_layout.addWidget(gw)
            group_name[group] = gw
            # Tell the layout system this widget's size hint has changed
            gw.updateGeometry()

        groups_layout.addStretch()
        container.setWidget(groups_widget)


    # ------------------------------------------------------------------
    # Update Mime list when a desktop file is parsed
    # ------------------------------------------------------------------
    def sync_ui_to_text(self, mime_group, mime_string):
        # Checks the UI checkboxes based on a semicolon-separated string.
        mimes = [m.strip() for m in mime_string.split(';') if m.strip()]

        for gw in mime_group.values():
            for cb in gw.checkboxes:
                # If the checkbox text is in our list, check it!
                cb.setChecked(cb.text() in mimes)


    # ------------------------------------------------------------------
    # Update Mime Type desktop field when a checkbox is changed
    # ------------------------------------------------------------------
    def update_mimetype_field(self, group_name, source, field_name):
        # Find the QLineEdit
        if hasattr(source, 'widget') and source.widget():
            container = source.widget()
            mime_line_edit = container.findChild(QLineEdit, "field_MimeType")
        else:
            mime_line_edit = self.ui.inputMimeTypes

        if not mime_line_edit:
            return

        # Get current state from text box
        current_text = mime_line_edit.text()
        current_mimes = set(m.strip() for m in current_text.split(';') if m.strip())

        # Separate "Manual" MIMEs from "Checkbox" MIMEs
        # We identify everything that COULD be a checkbox
        all_known_checkbox_mimes = set()
        currently_checked_mimes = set()

        for gw in group_name.values():
            for cb in gw.checkboxes:
                mime_val = cb.text().strip()
                all_known_checkbox_mimes.add(mime_val)
                if cb.isChecked():
                    currently_checked_mimes.add(mime_val)

        # Filter: Keep only the stuff the user typed that IS NOT in our checkbox lists
        user_custom_mimes = current_mimes - all_known_checkbox_mimes

        # Final Merge: Custom stuff + ONLY what is actually checked right now
        final_set = user_custom_mimes | currently_checked_mimes
        final_list = sorted(list(final_set))

        # Update UI
        mime_line_edit.blockSignals(True)
        new_text = ";".join(final_list) + (";" if final_list else "")
        mime_line_edit.setText(new_text)
        mime_line_edit.blockSignals(False)


    # ------------------------------------------------------------------
    # Set and show home page
    # ------------------------------------------------------------------
    def setPageHome(self):
        self.action = "menu"
        self.slide_to_page(self.ui.page_1, "back")

    # ------------------------------------------------------------------
    # Set and show create desktop page
    # ------------------------------------------------------------------
    def setPageCreate(self):
        self.action = "create"
        self.clear_dynamic_fields()
        self.slide_to_page(self.ui.page_2, "forward")

    # ------------------------------------------------------------------
    # Set and show edit desktop page
    # ------------------------------------------------------------------
    def setPageEdit(self):
        self.action = "edit"
        self.clear_dynamic_fields()
        self.slide_to_page(self.ui.page_2, "forward")

    # ------------------------------------------------------------------
    # Set uninstall page
    # ------------------------------------------------------------------
    def setPageUninstall(self):
        self.action = "uninstall"
        self.slide_to_page(self.ui.page_3, "forward")

    # ------------------------------------------------------------------
    # setMIMEiconPage
    # ------------------------------------------------------------------
    def setMIMEiconPage(self):
        self.slide_to_page(self.ui.page_4, "forward")

    # ------------------------------------------------------------------
    # Handle appimage or desktop file drop
    # ------------------------------------------------------------------
    def handle_file_drop(self, file_path):
        # Triggered when a file is dropped into the Path field.
        # Ensure it's actually the desire file extension before parsing
        if self.action == "create":
            if file_path.lower().endswith(".appimage"):
                self.clear_dynamic_fields()
                self.parse_appimage_async(file_path)
                self.filePath = file_path
            else:
                self.ui.statusbar.showMessage("Error: Please drop a valid .AppImage file.", 10000)

        elif self.action == "edit":
            if file_path.lower().endswith(".desktop"):
                self.clear_dynamic_fields()
                icon_path, desktop_data = self.parse_desktop_file(file_path)
                self.on_parser_finished(icon_path, desktop_data)
            else:
                self.ui.statusbar.showMessage("Error: Please drop a valid .desktop file.", 10000)


    # ------------------------------------------------------------------
    # Browse for an AppImage or an existing .desktop file
    # ------------------------------------------------------------------
    def browse_file(self):
        if "create" in self.action:
            # Default to the standard applications directory
            if self.filePath:
                path = self.filePath
            else:
                path = os.path.expanduser("~")

            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select AppImage File", path, "AppImage Files (*.AppImage)",
                options=QFileDialog.DontUseNativeDialog
            )

        elif "edit" in self.action:
            # Default to the standard applications directory
            path = os.path.expanduser(config.PathConfig.DESKTOP_FILE_DIR)
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select Desktop File", path, "Desktop Files (*.desktop)",
                options=QFileDialog.DontUseNativeDialog
            )

        if file_path:
            self.clear_dynamic_fields()
            if "create" in self.action:
                self.filePath = file_path
                self.parse_appimage_async(file_path)
            elif "edit" in self.action:
                icon_path, desktop_data = self.parse_desktop_file(file_path)
                self.on_parser_finished(icon_path, desktop_data)


    # ------------------------------------------------------------------
    # Parse AppImage async
    # ------------------------------------------------------------------
    def parse_appimage_async(self, app_path):
        # Create the worker thread
        workerAppImageParser = AppImageParser(app_path, config.PathConfig.ICONS_DIR)

        # Connect signals to UI feedback
        workerAppImageParser.started_task.connect(
            lambda: self.ui.statusbar.showMessage("Parsing AppImage... Please wait.", 10000)
        )
        workerAppImageParser.finished.connect(self.on_parser_finished, Qt.UniqueConnection)
        workerAppImageParser.error.connect(
            lambda msg: self.ui.statusbar.showMessage(msg, 10000)
        )

        # Start the thread
        self.active_threads.append(workerAppImageParser)
        workerAppImageParser.start()


    # ------------------------------------------------------------------
    # Update the UI after an AppImage is parsed
    # ------------------------------------------------------------------
    def on_parser_finished(self, icon_path, desktop_data_raw):
        mime_data_field = ""

        # Remove the worker from the list
        sender = self.sender()

        # Only perform thread-cleanup if the sender is actually a QThread
        # This ignores QPushButtons or direct function calls
        if isinstance(sender, QThread):
            if sender in self.active_threads:
                self.active_threads.remove(sender)
            sender.deleteLater()
        #     print("Cleaned up worker thread.")
        # else:
        #     print(f"Method called by non-thread: {sender}")

        self.ui.inputAppPath.setText(self.filePath)
        target_scroll_area = self.ui.scrollAreaLayoutDesktopFields
        self.ui.statusbar.showMessage("Parsing complete.", 10000)
        existing_keys = {item[0] for item in desktop_data_raw}

        final_data = []
        for k, v in desktop_data_raw:
            final_data.append((k, v, False))

        for field in config.NECESSARY_FIELDS:
            if field not in existing_keys:
                final_data.append((field, "Application" if field == "Type" else "", True))

        old_container = target_scroll_area.widget()
        if old_container: old_container.deleteLater()

        new_container = QWidget()
        new_container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        form_layout = QFormLayout(new_container)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        for key, value, is_extra in final_data:
            if "create" in self.action:
                if key == "Exec":
                    value = self.filePath
                elif key == "Icon":
                    value = icon_path
                elif key == "TryExec":
                    value = self.filePath

            le = QLineEdit(value)
            le.setObjectName(f"field_{key}")
            label_text = f"<i>{key}:</i>" if is_extra else f"<b>{key}:</b>"
            le.installEventFilter(self)

            # SPECIAL HANDLING FOR ICON FIELD
            if key == "Icon":
                # Create a horizontal container for the icon + input
                icon_container = QWidget()
                # Force the container to stay compact vertically
                icon_container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
                h_layout = QHBoxLayout(icon_container)
                h_layout.setContentsMargins(0, 0, 0, 0)
                h_layout.setSpacing(5)
                # Align everything to the center-left so it looks consistent
                h_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

                # Create the Image Label
                img_label = QLabel()
                img_label.setFixedSize(32, 32)
                self.update_icon_preview(icon_path, img_label)

                # Create the tooltip
                tooltip = self.setup_help_button()
                tooltip.setProperty("help_text",
                                    "A system icon name can also be used, such as <i>smplayer</i>"
                                    )
                h_layout.addWidget(tooltip)

                h_layout.addWidget(img_label)
                h_layout.addWidget(le) # Add the LineEdit next to it
                # Add the event listener (Signal)
                # Using lambda allows us to pass the specific img_label we want to update
                le.textChanged.connect(lambda text, lbl=img_label: self.update_icon_preview(text, lbl))

                form_layout.addRow(label_text, icon_container)

            else:
                h_layout = QHBoxLayout()
                h_layout.setContentsMargins(0, 0, 0, 0)
                h_layout.setSpacing(5)
                # Align everything to the center-left so it looks consistent
                h_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

                if key == "MimeType" or key == "Keywords":

                    # Create the tooltip
                    tooltip = self.setup_help_button()
                    if key == "MimeType":
                        tooltip.setProperty("help_text",
                                            """MIME types to be associated with the application. The application will
                            appear in <i>Open with</i> menu for this specific file types.
                                            """
                                            )
                    elif key == "Keywords":
                        tooltip.setProperty("help_text",
                                            """In a .desktop file, the Keywords field is designed to help users find
                                            an application using the search function.<br/>
                                            <table border="1" style="border-collapse: collapse; width: 100%;">
                                                <thead>
                                                    <tr>
                                                        <th style="padding: 8px; text-align: left;">App Category</th>
                                                        <th style="padding: 8px; text-align: left;">Suggested Keywords (semicolon-separated)</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    <tr>
                                                        <td style="padding: 8px; font-weight: bold;">Media Players</td>
                                                        <td style="padding: 8px;">Video;Movie;Film;Clip;Player;Media;Streaming;Cinema;VLC;MP4;MKV;</td>
                                                    </tr>
                                                    <tr>
                                                        <td style="padding: 8px; font-weight: bold;">Browsers</td>
                                                        <td style="padding: 8px;">Internet;Web;Explorer;Navigator;WWW;Site;Cloud;Online;</td>
                                                    </tr>
                                                    <tr>
                                                        <td style="padding: 8px; font-weight: bold;">Image Editors</td>
                                                        <td style="padding: 8px;">Photo;Graphic;Design;Draw;Paint;SVG;Vector;Canvas;Retouch;Photoshop;</td>
                                                    </tr>
                                                    <tr>
                                                        <td style="padding: 8px; font-weight: bold;">Office/Text</td>
                                                        <td style="padding: 8px;">Write;Document;Notes;Edit;Editor;Word;Sheet;Presentation;PDF;</td>
                                                    </tr>
                                                    <tr>
                                                        <td style="padding: 8px; font-weight: bold;">Utilities</td>
                                                        <td style="padding: 8px;">Tool;Task;System;Helper;Manager;Config;Setup;</td>
                                                    </tr>
                                                    <tr>
                                                        <td style="padding: 8px; font-weight: bold;">Games</td>
                                                        <td style="padding: 8px;">Play;Entertainment;Simulation;Action;Arcade;Steam;</td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                            """
                                            )

                    h_layout.addWidget(tooltip)
                    h_layout.addWidget(le)
                    form_layout.addRow(label_text, h_layout)
                else:
                    # ADD PLACEHOLDER: This keeps the LineEdit starting at the same X-coordinate
                    spacer = QSpacerItem(24, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)
                    h_layout.addSpacerItem(spacer)
                    h_layout.addWidget(le)
                    # Standard row for all other fields
                    form_layout.addRow(label_text, h_layout)

            # CATEGORIES HANDLING
            if key == "Categories":
                self.category_list = QListWidget()
                self.category_list.addItems(config.CATEGORIES_LIST)
                self.category_list.setSelectionMode(QAbstractItemView.MultiSelection)
                self.category_list.setMaximumHeight(150)

                existing_cats = [c.strip() for c in value.split(';') if c.strip()]
                for i in range(self.category_list.count()):
                    item = self.category_list.item(i)
                    if item.text() in existing_cats:
                        item.setSelected(True)

                self.category_list.hide()
                self.category_input = le
                self.category_list.itemClicked.connect(self.update_category_line_edit)
                form_layout.addRow("", self.category_list)

            if key == "MimeType":
                mime_data_field = value

        target_scroll_area.setWidget(new_container)

        if not hasattr(self, 'main_splitter'):
            self.setup_resizable_layout()

        # Enable elements
        self.sync_ui_to_text(self.mime_list_1, mime_data_field)
        self.ui.btnDo.setDisabled(False)


    # ------------------------------------------------------------------
    # setup_help_button
    # ------------------------------------------------------------------
    def setup_help_button(self):
        # Create the tooltip button
        help_btn = QToolButton(self.ui.centralwidget)
        help_btn.setText("[?]")
        help_btn.setFixedSize(20, 20)
        help_btn.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        help_btn.setObjectName("tooltip")

        # Connect the click to the balloon function
        # We pass the widget itself so we know where to point
        help_btn.clicked.connect(lambda: self.show_balloon_help(help_btn))
        return help_btn


    # ------------------------------------------------------------------
    # show_balloon_help
    # ------------------------------------------------------------------
    def show_balloon_help(self, widget):
        help_text = widget.property("help_text")
        trigering_btn = None

        # Check if we already have a help window open; if so, close it
        if hasattr(self, 'active_help'):
            trigering_btn = self.active_help.btn
            if self.active_help.isVisible():
                self.active_help.hide()
                self.active_help.btn = None

        # Create and show the new interactive help
        if not hasattr(self, 'active_help') or not widget == trigering_btn:
            self.active_help = InteractiveHelp(help_text, widget, self)
            self.active_help.show_at(widget)


    # ------------------------------------------------------------------
    # clear_dynamic_fields
    # ------------------------------------------------------------------
    def clear_dynamic_fields(self):
        self.ui.inputAppPath.setText("")

        # Safely removes all dynamically generated fields from the Scroll Area.
        # Get the current container widget
        old_container = self.ui.scrollAreaLayoutDesktopFields.widget()

        if old_container:
            # Unparent it from the scroll area
            self.ui.scrollAreaLayoutDesktopFields.takeWidget()
            # Mark it for deletion (Qt will clean it up safely)
            old_container.deleteLater()


    # ------------------------------------------------------------------
    # update_icon_preview
    # ------------------------------------------------------------------
    def update_icon_preview(self, icon_name_or_path, label):
        # Try as direct path first
        if os.path.isfile(icon_name_or_path):
            pixmap = QPixmap(icon_name_or_path)
        else:
            # Try as a System Theme icon
            icon = QIcon.fromTheme(icon_name_or_path)
            pixmap = icon.pixmap(32, 32)

        if not pixmap.isNull():
            label.setPixmap(pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            label.setStyleSheet("border: none;")
        else:
            label.setText("?")
            label.setStyleSheet("color: red; border: 1px solid red;")


    # ------------------------------------------------------------------
    # Split the desktop fields and mime list using a splitter
    # ------------------------------------------------------------------
    def setup_resizable_layout(self):
        # Prevent re-creating the splitter if it already exists
        if hasattr(self, 'main_splitter'):
            return

        # Create the Splitter
        self.main_splitter = QSplitter(Qt.Orientation.Vertical)
        self.main_splitter.setObjectName("mainSplitter")

        # Migrate widgets to the splitter
        # Adding them to the splitter automatically removes them from verticalLayout_2
        self.main_splitter.addWidget(self.ui.scrollAreaLayoutDesktopFields)
        self.main_splitter.addWidget(self.ui.widgetMimeTypes)

        # Insert the splitter into the main vertical layout of Page 2
        # According to your form.ui, verticalLayout_2 holds the elements on page_2
        # We use addWidget or insertWidget(1, ...) to place it after the Path field
        self.ui.verticalLayout_2.insertWidget(1, self.main_splitter)

        # Calculate the total current height of the splitter
        total_height = sum(self.main_splitter.sizes())

        # If the splitter hasn't rendered yet, use a default like 800
        if total_height == 0:
            total_height = 800

        # Set sizes: 75% for top, 25% for bottom
        self.main_splitter.setSizes([total_height * 3 // 4, total_height // 4])

        # Set initial sizes and stretch factors
        self.main_splitter.setStretchFactor(0, 1)
        self.main_splitter.setCollapsible(0, False)
        self.main_splitter.setHandleWidth(6)

        # Ensure the splitter itself is visible
        self.main_splitter.show()


    # ------------------------------------------------------------------
    # Update Category field when a drop-down menu entry is clicked
    # ------------------------------------------------------------------
    def update_category_line_edit(self):
        # Get currently selected items from the list
        selected_from_list = [item.text() for item in self.category_list.selectedItems()]

        # Get what is currently typed in the box (to catch custom categories)
        current_text = self.category_input.text()
        current_all = [c.strip() for c in current_text.split(';') if c.strip()]

        # Identify categories that ARE NOT in our standard list (the custom ones)
        custom_cats = [c for c in current_all if c not in config.CATEGORIES_LIST]

        # Combine: Selected Standard + Existing Custom
        # Use a set to prevent duplicates, then convert back to list
        final_list = list(dict.fromkeys(selected_from_list + custom_cats))

        # Update the text field
        if final_list:
            self.category_input.setText(";".join(final_list) + ";")
        else:
            self.category_input.clear()


    # ------------------------------------------------------------------
    # Manages desktop files: create, edit,
    # place to desktop, set as default app
    # ------------------------------------------------------------------
    def createDesktop(self):
        # Extraction (Using the UI Manager)
        container = self.ui.scrollAreaLayoutDesktopFields.widget()
        gui_data = UIparseDesktopFields.collect_data(container)

        required_fields = ["Name", "Exec"]
        for field in required_fields:
            if not gui_data.get(field):
                QMessageBox.warning(self, "Error", f"{field} cannot be empty.")
                return

        # Disable UI
        self.ui.btnDo.setDisabled(True)

        escape = True
        if self.action == "edit":
            escape = False

        # Logic processing
        desktop_handler = DesktopFileHandler(gui_data, escape)
        desktop_handler.set_data(gui_data)

        # Define paths
        filename = f"{gui_data['Name'].replace(' ', '_')}.desktop"
        app_dir = Path.home() / ".local/share/applications"
        full_path = app_dir / filename

        try:
            # Save .desktop file
            desktop_handler.save(full_path)

            # Add desktop file to Desktop
            if self.ui.cbAddToDesktop.isChecked():
                desktop_handler.deploy_to_desktop(full_path, filename)

            # Run update-desktop-database
            ok, err = self.run_update_desktop_database(app_dir)
            if not ok:
                QMessageBox.information(self, "Done", f".desktop file created at:\n{full_path}\n\nBut update-desktop-database failed: {err}")
                if self.ui.statusbar:
                    self.ui.statusbar.showMessage("Created .desktop file (update failed).", 10000)
            else:
                QMessageBox.information(self, "Done", f".desktop file created at:\n{full_path}\n\nupdate-desktop-database ran successfully.")
                if self.ui.statusbar:
                    self.ui.statusbar.showMessage("Created .desktop file and updated database.", 10000)

            # If requested, set as default for selected MIME types
            if self.ui.cbMakeDefault.isChecked() and gui_data.get("MimeType"):
                self.start_mime_registration(filename, gui_data.get("MimeType"))

            if self.ui.cbSetMIMEicon.isChecked() and gui_data.get("MimeType"):
                self.handle_mimetype_icon("create", gui_data.get("MimeType"), gui_data.get("Icon"))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {e}")


    # ----------------------------------------------------------------------
    # Run update-desktop-database
    # ----------------------------------------------------------------------
    def run_update_desktop_database(self, applications_dir: Path):
        try:
            subprocess.run(["update-desktop-database", str(applications_dir)], check=True)
            return True, None
        except FileNotFoundError:
            return False, "update-desktop-database not found"
        except subprocess.CalledProcessError as e:
            return False, str(e)


    # ----------------------------------------------------------------------
    # start_mime_registration
    # ----------------------------------------------------------------------
    def start_mime_registration(self, desktop_name, mime_data):
        # Setup UI for "Busy" mode
        self.busy_indicator.show()
        self.busy_indicator.setRange(0, 0) # This makes it an "Indeterminate" pulsing bar
        self.ui.statusbar.showMessage("Registering MimeTypes...")

        # Initialize Thread
        # Use a local variable to avoid the reassignment bug
        workerMime = MimeWorker(desktop_name, mime_data)

        # Connect signals
        workerMime.progress.connect(self.update_mime_status, Qt.UniqueConnection)
        workerMime.finished.connect(self.on_mime_finished, Qt.UniqueConnection)

        self.active_threads.append(workerMime)
        workerMime.start()

    # ----------------------------------------------------------------------
    # update_mime_status
    # ----------------------------------------------------------------------
    def update_mime_status(self, percent, mt):
        # Switch to determinate progress if you want to show exact %
        self.busy_indicator.setRange(0, 100)
        self.busy_indicator.setValue(percent)
        self.ui.statusbar.showMessage(f"Registering: {mt}")

    # ----------------------------------------------------------------------
    # on_mime_finished
    # ----------------------------------------------------------------------
    def on_mime_finished(self):
        # Use self.sender() to get the specific worker that just finished
        worker = self.sender()

        # Only perform thread-cleanup if the sender is actually a QThread
        # This ignores QPushButtons or direct function calls
        if isinstance(worker, QThread):
            if worker in self.active_threads:
                self.active_threads.remove(worker)

            # Clean up the thread object properly
            worker.deleteLater()

        self.busy_indicator.hide()
        self.ui.statusbar.showMessage("MimeType registration complete.", 5000)
        QMessageBox.information(self, "Success", "Application integrated and file associations updated.")


    # ----------------------------------------------------------------------
    # Changes the default icon for a MIME type that is shown in a file manager.
    # ----------------------------------------------------------------------
    def handle_mimetype_icon(self, action, mime_data, icon_path):
        # Sets a custom icon for a specific mimetype using a local XML override.
        mime_dir = os.path.expanduser("~/.local/share/mime/packages")
        os.makedirs(mime_dir, exist_ok=True)

        mime_list = [mt.strip() for mt in mime_data.split(";") if mt.strip()]

        for mimetype in mime_list:
            file_path = os.path.join(mime_dir, f"{mimetype.replace('/', '-')}.xml")

            if action == "create":
                xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
        <mime-type type="{mimetype}">
            <icon name="{icon_path}"/>
        </mime-type>
    </mime-info>
    """
                with open(file_path, "w") as f:
                    f.write(xml_content)
                    f.close()

            elif action == "delete":
                # Delete the file if it exists
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        print(f"Removed icon override for: {mimetype}")
                    except Exception as e:
                        print(f"Error removing {file_path}: {e}")

        # Refresh the system mime database
        try:
            subprocess.run(
                ["update-mime-database", os.path.expanduser("~/.local/share/mime")],
                check=True,
                capture_output=True
            )
            print("MIME database refreshed.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to refresh MIME database: {e}")


    # ----------------------------------------------------------------------
    # Restore the default app for given mime list
    # or remove the mime types from the mimelist file
    # if there was no previous app associated with them
    # ----------------------------------------------------------------------
    def restore_mimetype_defaults(self, desktop_file_name, mime_list):
        settings = QSettings(config.AppConfig.APP_NAME, "MimeBackups")
        settings.beginGroup(desktop_file_name)
        mimetypes = settings.allKeys()
        if not mimetypes:
            mimetypes = [mt.strip() for mt in mime_list.split(";") if mt.strip()]

        total = len(mimetypes)

        for i, mt in enumerate(mimetypes):
            old_app = settings.value(mt)
            prog = int((i / total) * 100)
            self.update_mime_status(prog, mt)

            if old_app:
                # Case A: We have a backup, restore it
                try:
                    subprocess.run(
                        ["xdg-mime", "default", str(old_app), mt],
                        check=False, stderr=subprocess.DEVNULL
                    )
                except Exception as e:
                    print(f"Failed to restore {mt}: {e}")
            else:
                # Case B: NO backup exists (App was the first to claim this mime)
                # We must force the system to "forget" our uninstalled app
                self.clear_mimetype_association(mt, desktop_file_name)

        settings.endGroup()
        settings.remove(desktop_file_name)


    # ----------------------------------------------------------------------
    # Manually removes the association from ~/.config/mimeapps.list
    # to prevent 'broken' file associations.
    # ----------------------------------------------------------------------
    def clear_mimetype_association(self, mimetype, desktop_file_name):
        mime_path = os.path.expanduser("~/.config/mimeapps.list")

        if not os.path.exists(mime_path):
            return

        try:
            with open(mime_path, "r") as f:
                lines = f.readlines()

            new_lines = []
            for line in lines:
                # If the line contains our mimetype AND our app, we strip our app out
                if mimetype in line and desktop_file_name in line:
                    # Remove the app name and any trailing/leading semicolons
                    line = line.replace(desktop_file_name, "").replace(";;", ";")
                    # If the line now ends in '=', it means no apps are left for this mime
                    if line.strip().endswith("="):
                        continue
                new_lines.append(line)

            with open(mime_path, "w") as f:
                f.writelines(new_lines)
        except Exception as e:
            print(f"Error clearing mime {mimetype}: {e}")
            self.ui.statusbar.showMessage(f"Error clearing mime {mimetype}: {e}", 10000)


    # ----------------------------------------------------------------------
    # eventFilter
    # ----------------------------------------------------------------------
    def eventFilter(self, watched, event):
        # Compare event.type() to the QEvent class constants
        if event.type() == QEvent.FocusIn:
            if watched.objectName() == "field_MimeType":
                self.ui.widgetMimeTypes.show()

                # Delay to ensure the layout has finished expanding
                # Scroll item in view
                QTimer.singleShot(50, lambda: self.ui.scrollAreaLayoutDesktopFields.ensureWidgetVisible(watched))

            elif watched.objectName() == "field_Categories":
                self.category_list.show()

            else:
                self.ui.widgetMimeTypes.hide()
                self.check_category_focus()

        elif event.type() == QEvent.FocusOut:
            # Prevent hiding if the user is clicking a checkbox in the list
            target = QApplication.focusWidget()

            if target:
                # Check if target is a checkbox or a child of the mime container
                if isinstance(target, QCheckBox) or self.ui.knownMimeTypes.isAncestorOf(target):
                    return super().eventFilter(watched, event)

            self.ui.widgetMimeTypes.hide()
            # Short delay to check if user clicked an item in the list
            QTimer.singleShot(150, self.check_category_focus)

        # Always return the base class eventFilter for all other events
        return super().eventFilter(watched, event)


    def check_category_focus(self):
        if not self.category_list.hasFocus() and not self.category_input.hasFocus():
            self.category_list.hide()


    # ----------------------------------------------------------------------
    # parse_desktop_file
    # ----------------------------------------------------------------------
    def parse_desktop_file(self, file_path):
        data_dict = {}
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and section headers like [Desktop Entry]
                    if "=" in line and not line.startswith("#") and not line.startswith("["):
                        k, v = line.split("=", 1)
                        data_dict[k.strip()] = v.strip()

            icon_path = data_dict.get("Icon", "")

            # Convert dict to list of tuples for the parser
            data_list = list(data_dict.items())

            return icon_path, data_list

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not read desktop file: {e}")


    # ----------------------------------------------------------------------
    # browse_uninstall_file
    # ----------------------------------------------------------------------
    def browse_uninstall_file(self):
        # Default to the standard applications directory
        path = os.path.expanduser(config.PathConfig.DESKTOP_FILE_DIR)
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Desktop File", path, "Desktop Files (*.desktop)",
            options=QFileDialog.DontUseNativeDialog
        )

        if file_path:
            self.ui.le_uninstall_path.setText(file_path)
            # Enable elements
            self.ui.btnDeintegrate.setDisabled(False)
            self.preview_uninstall_app(file_path)

    # ----------------------------------------------------------------------
    # preview_uninstall_app
    # ----------------------------------------------------------------------
    def preview_uninstall_app(self, file_path):
        try:
            _, data = self.parse_desktop_file(file_path)
            data = dict(data)

            # Display Name
            app_name = data.get("Name", "Unknown Application")
            self.ui.lbl_uninstall_name.setText(app_name)

            # Mimetype used to unset default app
            self.mime_list = data.get("MimeType", "")

            # Display Icon
            icon_path = data.get("Icon", "")
            if os.path.isfile(icon_path):
                pixmap = QPixmap(icon_path)
            else:
                # Try as a System Theme icon
                icon = QIcon.fromTheme(icon_path)
                pixmap = icon.pixmap(32, 32)

            if not pixmap.isNull():
                self.ui.lbl_uninstall_icon.setPixmap(
                    pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )
                self.current_uninstall_icon = icon_path # Store for deletion
            else:
                self.ui.lbl_uninstall_icon.setText("No Icon Found")
                self.current_uninstall_icon = None

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not read desktop file: {e}")


    # ----------------------------------------------------------------------
    # perform_uninstall
    # ----------------------------------------------------------------------
    def perform_uninstall(self):
        desktop_file_path = self.ui.le_uninstall_path.text().strip()

        if not desktop_file_path or not os.path.exists(desktop_file_path):
            QMessageBox.warning(self, "Error", "Please select a valid .desktop file.")
            return

        # Disable UI
        self.ui.btnDeintegrate.setDisabled(True)

        # Extract the filename (e.g., "myapp.desktop") to find it on the Desktop too
        file_name = os.path.basename(desktop_file_path)
        desktop_folder_path = os.path.join(os.path.expanduser("~"), "Desktop", file_name)

        confirm = QMessageBox.question(
            self, "Confirm",
            f"Are you sure you want to uninstall {file_name}?\n\n"
            "This will remove the shortcut from your Menu and Desktop.",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            try:
                # Setup UI for "Busy" mode
                self.busy_indicator.show()
                self.busy_indicator.setRange(0, 0) # This makes it an "Indeterminate" pulsing bar
                self.ui.statusbar.showMessage("Restoring MimeTypes...")

                # Restore Mime Types BEFORE deleting the desktop file
                self.restore_mimetype_defaults(file_name, self.mime_list)

                # Delete the main .desktop file (from ~/.local/share/applications)
                if os.path.exists(desktop_file_path):
                    os.remove(desktop_file_path)

                # Delete the .desktop file from the Desktop folder (if it exists)
                if os.path.exists(desktop_folder_path):
                    os.remove(desktop_folder_path)

                # Delete the Icon (only if it's in our local icons folder)
                if hasattr(self, 'current_uninstall_icon') and self.current_uninstall_icon:
                    if os.path.exists(self.current_uninstall_icon) and ".local/share/icons" in self.current_uninstall_icon:
                        os.remove(self.current_uninstall_icon)

                self.handle_mimetype_icon("delete", self.mime_list, "")

                # Reset UI
                self.ui.le_uninstall_path.clear()
                self.ui.lbl_uninstall_icon.clear()
                self.ui.lbl_uninstall_name.setText("Uninstalled from Menu and Desktop.")

                # Refresh system database
                os.system("update-desktop-database ~/.local/share/applications")
                os.system("update-mime-database ~/.local/share/mime")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete files: {e}")

            self.busy_indicator.hide()
            self.ui.statusbar.showMessage("")



    # ----------------------------------------------------------------------
    # Override the close event to trigger saving
    # ----------------------------------------------------------------------
    def closeEvent(self, event):
        if self.cleanup_before_exit():
            # Proceed with closing
            self.save_settings()
            super().closeEvent(event)
        else:
            # The user clicked 'Yes' to wait, so cancel the close
            event.ignore()


    # ----------------------------------------------------------------------
    # This covers cases where the app is closed via the task manager
    # or system shutdown, not just the "X" button.
    # ----------------------------------------------------------------------
    def cleanup_before_exit(self):
        # Identify which threads are actually running
        running_threads = [t for t in self.active_threads if t.isRunning()]

        if running_threads:
            # Map the thread objects to human-readable names for the UI
            # We use a helper to identify the worker type
            names = []
            for t in running_threads:
                if isinstance(t, MimeWorker):
                    names.append("MimeType Registration")
                elif isinstance(t, AppImageParser):
                    names.append("AppImage Analysis")
                else:
                    names.append("Background Task")

            worker_list_str = "\n - " + "\n - ".join(names)

            reply = QMessageBox.question(
                self, "Operation in Progress",
                f"The following tasks are still running:{worker_list_str}\n\n"
                "Closing now may cause data corruption. Do you want to wait?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
            )

            if reply == QMessageBox.Yes:
                # Tell the closeEvent to ignore the close request
                return False
            else:
                # Stop and WAIT
                self.stop_all_workers()
                # Crucial: stop_all_workers must call worker.wait()
                # so the thread is dead before we continue

        self.save_settings()
        return True # Tell closeEvent it is safe to proceed


    # ----------------------------------------------------------------------
    # stop_all_workers
    # ----------------------------------------------------------------------
    def stop_all_workers(self):
        # Safely shut down all threads and wait for them to finish.
        for worker in list(self.active_threads):
            if worker.isRunning():
                # Tell the internal loop to stop
                if hasattr(worker, 'stop'):
                    worker.stop()

                # If it's the AppImage parser, kill the --appimage-extract process
                if hasattr(worker, 'process') and worker.process:
                    worker.process.terminate()

                # Stop the Qt event loop for the thread
                worker.quit()

                # BLOCK until the thread is actually finished
                # This is the most important line to prevent the crash
                if not worker.wait(2000): # Wait up to 2 seconds
                    worker.terminate()     # Force kill if still stuck


    # ----------------------------------------------------------------------
    # Update elements in hidden pages when the window is resized
    # to prevent the snapping effect
    # ----------------------------------------------------------------------
    def resizeEvent(self, event):
        # Let the window handle the initial resize
        super().resizeEvent(event)

        # Get the current page so we can return to it
        current_idx = self.ui.stackedWidget.currentIndex()

        # Disable updates temporarily to prevent visual flickering
        self.ui.stackedWidget.setUpdatesEnabled(False)

        # Force a layout pass on every page
        for i in range(self.ui.stackedWidget.count()):
            page = self.ui.stackedWidget.widget(i)
            # Force the widget to recognize its new parent size
            page.setGeometry(self.ui.stackedWidget.rect())
            # Trigger a recursive layout recalculation
            page.layout().activate()

        # Re-enable updates and ensure we are back on the correct page
        self.ui.stackedWidget.setUpdatesEnabled(True)
        self.ui.stackedWidget.setCurrentIndex(current_idx)

        # Specific fix for the ScrollArea internal widget
        if hasattr(self.ui, 'knownMimeTypes'):
            self.ui.knownMimeTypes.widget().adjustSize()


    # ----------------------------------------------------------------------
    # Icon browser for changing the MIME type icon in a file manager
    # ----------------------------------------------------------------------
    def load_icons(self):
        self.icon_data = [] # Stores (path, name, widget)
        if hasattr(self.ui.inputIconPath, 'previous_element'):
            self.ui.inputIconPath.previous_element = None
        self.ui.inputMimeTypes.clear()
        self.ui.inputIconPath.clear()
        self.ui.inputIconSearch.clear()

        # Locations to scan
        search_paths = [
                os.path.expanduser("~/.local/share/icons"),
                # Current Theme Apps (Example: Breeze/Adwaita)
                "/usr/share/icons/hicolor/scalable/apps",
                "/usr/share/icons/breeze/apps/48",
                "/usr/share/icons/adwaita/48x48/apps",
                # Generic fallback for apps
                "/usr/share/icons/hicolor/48x48/apps",
                "/usr/share/pixmaps"
            ]

        # Check if we already initialized the layout
        if not self.ui.scrollAreaWidgetContents_2.layout():
            self.flow_layout = FlowLayout(self.ui.scrollAreaWidgetContents_2)
            self.flow_layout.setSpacing(10)
            self.ui.scrollAreaWidgetContents_2.setSizePolicy(
                QSizePolicy.Preferred, QSizePolicy.Expanding
            )
        else:
            # Use the existing layout
            self.flow_layout = self.ui.scrollAreaWidgetContents_2.layout()
            # Clear old icons before adding new ones
            self.clear_layout(self.flow_layout)
            # Force the layout to recognize it's empty
            self.flow_layout.invalidate()

        for path in search_paths:
            if os.path.exists(path):
                for file in os.listdir(path):
                    if file.endswith((".png", ".svg")):
                        full_path = os.path.join(path, file)
                        thumb = IconThumbnail(full_path, file, self.ui.inputIconPath)

                        self.flow_layout.addWidget(thumb)
                        self.icon_data.append({'name': file.lower(), 'widget': thumb})

        # Tell the layout to reposition everything now that they are added
        # Force the scroll area to re-calculate its scrollbars
        self.ui.scrollAreaWidgetContents_2.adjustSize()
        self.flow_layout.activate()
        self.ui.scrollAreaWidgetContents_2.update()


    # ----------------------------------------------------------------------
    # filter_icons
    # ----------------------------------------------------------------------
    def filter_icons(self, text):
        search_term = text.lower().strip()

        # Optional: Block updates during the loop for smoother performance
        self.ui.scrollAreaWidgetContents_2.setUpdatesEnabled(False)

        for item in self.icon_data:
            if not search_term:
                item['widget'].show()
            else:
                item['widget'].setVisible(search_term in item['name'])

        self.flow_layout.invalidate()
        self.ui.scrollAreaWidgetContents_2.setUpdatesEnabled(True)


    # ----------------------------------------------------------------------
    # clear_layout
    # ----------------------------------------------------------------------
    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    # hide() ensures it stops overlapping immediately
                    # before the next event loop deletes it
                    widget.hide()
                    widget.deleteLater()
                else:
                    # If there are nested layouts, clear them recursively
                    self.clear_layout(item.layout())

    # ----------------------------------------------------------------------
    # changeMIMEicon
    # ----------------------------------------------------------------------
    def changeMIMEicon(self):
        icon = self.ui.inputIconPath.text()
        mime_data = self.ui.inputMimeTypes.text()
        action = "create"
        if not icon:
            action = "delete"

        self.handle_mimetype_icon(action, mime_data, icon)
        if action == "create":
            self.ui.statusbar.showMessage("MIME icon changed successfully!", 5000)
        else:
            self.ui.statusbar.showMessage("Removed icon override for selected MIME", 5000)


    # ----------------------------------------------------------------------
    # on_find_mime_type_triggered
    # ----------------------------------------------------------------------
    def on_find_mime_type_triggered(self):
        dialog = MimeFinderDialog(self)
        dialog.exec() # Use exec() for a modal popup


    # def get_scaled_size(points):
    #     # Get the logical DPI of the primary screen (Standard is 96)
    #     app = QApplication.instance()
    #     dpi = app.primaryScreen().logicalDotsPerInch()
    #     # Calculate pixels: (points * dpi) / 72
    #     return int((points * dpi) / 72)



# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
if __name__ == "__main__":
    # Force the platform theme to ignore system overrides
    os.environ["QT_QPA_PLATFORMTHEME"] = ""

    # Force the app to scale according to the OS display settings
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"

    # Suppress all SVG-related logging categories
    os.environ["QT_LOGGING_RULES"] = "qt.svg*=false;qt.text.*=false"

    # Forces Qt to use its own internal icon engine and avoid GTK icon loaders
    # This prevents crashing on Ubuntu based dist when the file browser is used.
    os.environ["QT_QPA_PLATFORMTHEME"] = "fusion"
    # Prevents Qt from trying to load the system's GTK icon theme which crashes on Zorin
    os.environ["XDG_CURRENT_DESKTOP"] = "KDE"


    app = QApplication(sys.argv)

    # Disable 'Desktop Settings Awareness' so system themes don't fight Fusion
    app.setDesktopSettingsAware(False)

    # Use 'auto' to synchronize with the system theme (default behavior)
    app.setStyle(QStyleFactory.create("Fusion"))
    # app.setStyleSheet(qdarktheme.load_stylesheet("light"))
    app.setStyleSheet(stylesheet.global_style)

    widget = Integrator()
    widget.show()
    sys.exit(app.exec())
