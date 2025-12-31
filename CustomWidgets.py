# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass

from PySide6.QtWidgets import (
    QLineEdit, QGroupBox, QVBoxLayout, QPushButton, QHBoxLayout, QCheckBox,
    QLayout,
)

from PySide6.QtCore import (
    Signal, QPoint, QRect, QSize
)

from typing import List


# ----------------------------------------------------------------------
# FileDropLineEdit
# ----------------------------------------------------------------------
class FileDropLineEdit(QLineEdit):
    # Define a custom signal that sends the file path as a string
    fileDropped = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)  # Enable drop capabilities
        self.setPlaceholderText("Drag and drop a file here...")

    def dragEnterEvent(self, event):
        # Check if the dragged object contains URLs (files)
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        # Extract the local file path from the URL
        urls = event.mimeData().urls()
        self.setFocus()
        if urls:
            file_path = urls[0].toLocalFile()
            # Emit the signal so the main window knows a file arrived
            self.fileDropped.emit(file_path)
            event.acceptProposedAction()


# ----------------------------------------------------------------------
# MimeGroupWidget
# ----------------------------------------------------------------------
class MimeGroupWidget(QGroupBox):
    # Custom signal to notify when any checkbox is clicked
    mimeChanged = Signal()

    def __init__(self, title: str, mime_list: List[str], parent=None):
        super().__init__(title, parent)
        self.setLayout(QVBoxLayout())
        self.check_all_btn = QPushButton("Select all")
        self.check_all_btn.setMaximumWidth(120)
        self.check_all_btn.clicked.connect(self.toggle_all)
        header_layout = QHBoxLayout()
        header_layout.addWidget(self.check_all_btn)
        header_layout.addStretch()
        self.layout().addLayout(header_layout)
        self.checkboxes: List[QCheckBox] = []
        for m in mime_list:
            cb = QCheckBox(m)
            self.layout().addWidget(cb)
            self.checkboxes.append(cb)
            # Connect each checkbox to emit our custom signal
            cb.toggled.connect(lambda: self.mimeChanged.emit())
        self._all_selected = False

    def toggle_all(self):
        self._all_selected = not self._all_selected
        text = "Deselect all" if self._all_selected else "Select all"
        self.check_all_btn.setText(text)
        for cb in self.checkboxes:
            cb.setChecked(self._all_selected)

    def selected_mimes(self) -> List[str]:
            return [cb.text() for cb in self.checkboxes if cb.isChecked()]


# ----------------------------------------------------------------------
# FlowLayout
# ----------------------------------------------------------------------
class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)
        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)
        self.items = []

    def addItem(self, item):
        self.items.append(item)

    def count(self):
        return len(self.items)

    def itemAt(self, index):
        return self.items[index] if 0 <= index < len(self.items) else None

    def takeAt(self, index):
        return self.items.pop(index) if 0 <= index < len(self.items) else None

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self._do_layout(rect, False)

    def sizeHint(self):
        # Returns the preferred size of the layout.
        return self.minimumSize()

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        # Passes True to tell the layout engine: "Just calculate, don't move anything"
        return self._do_layout(QRect(0, 0, width, 0), True)

    def minimumSize(self):
        # Calculates the minimum size needed to fit all visible items.
        size = QSize()
        for item in self.items:
            # We use expandedTo to find the bounding box of all items
            size = size.expandedTo(item.minimumSize())

        # Add margins to the calculation
        margins = self.contentsMargins()
        size += QSize(margins.left() + margins.right(),
                      margins.top() + margins.bottom())
        return size

    def _do_layout(self, rect, test_only):
        x = rect.x()
        y = rect.y()
        line_height = 0
        spacing = self.spacing()

        for item in self.items:
            wid = item.widget()
            if wid and not wid.isVisible():
                continue

            # Calculate where the next item should go
            next_x = x + item.sizeHint().width() + spacing

            # If we hit the right edge, wrap to the next line
            if next_x - spacing > rect.right() and line_height > 0:
                x = rect.x()
                y = y + line_height + spacing
                next_x = x + item.sizeHint().width() + spacing
                line_height = 0

            # CRITICAL: Only set the geometry if we aren't just testing the height
            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = next_x
            line_height = max(line_height, item.sizeHint().height())

        return y + line_height - rect.y()
