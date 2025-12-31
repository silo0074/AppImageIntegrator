# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QCheckBox, QFormLayout,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QMainWindow,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QSplitter, QStackedWidget, QStatusBar, QToolBar,
    QVBoxLayout, QWidget)

from CustomWidgets import FileDropLineEdit

class Ui_Integrator(object):
    def setupUi(self, Integrator):
        if not Integrator.objectName():
            Integrator.setObjectName(u"Integrator")
        Integrator.resize(703, 799)
        self.actionHome = QAction(Integrator)
        self.actionHome.setObjectName(u"actionHome")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoPrevious))
        self.actionHome.setIcon(icon)
        self.actionClose = QAction(Integrator)
        self.actionClose.setObjectName(u"actionClose")
        self.actionClose.setMenuRole(QAction.MenuRole.QuitRole)
        self.actionAbout = QAction(Integrator)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionAbout.setMenuRole(QAction.MenuRole.AboutRole)
        self.actionSetMimeIcon = QAction(Integrator)
        self.actionSetMimeIcon.setObjectName(u"actionSetMimeIcon")
        self.actionSetMimeIcon.setMenuRole(QAction.MenuRole.NoRole)
        self.actionFindMimeType = QAction(Integrator)
        self.actionFindMimeType.setObjectName(u"actionFindMimeType")
        self.actionFindMimeType.setMenuRole(QAction.MenuRole.NoRole)
        self.actionUtilities = QAction(Integrator)
        self.actionUtilities.setObjectName(u"actionUtilities")
        self.actionUtilities.setMenuRole(QAction.MenuRole.NoRole)
        self.centralwidget = QWidget(Integrator)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setAutoFillBackground(True)
        self.verticalLayout_4 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        sizePolicy.setHeightForWidth(self.page_1.sizePolicy().hasHeightForWidth())
        self.page_1.setSizePolicy(sizePolicy)
        self.verticalLayout_8 = QVBoxLayout(self.page_1)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.layoutStartMenu = QVBoxLayout()
        self.layoutStartMenu.setSpacing(20)
        self.layoutStartMenu.setObjectName(u"layoutStartMenu")
        self.layoutStartMenu.setContentsMargins(-1, 0, -1, -1)
        self.frameCreateDesktop = QFrame(self.page_1)
        self.frameCreateDesktop.setObjectName(u"frameCreateDesktop")
        self.frameCreateDesktop.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameCreateDesktop.setFrameShadow(QFrame.Shadow.Raised)
        self.frameCreateDesktop.setLineWidth(4)
        self.frameCreateDesktop.setMidLineWidth(0)
        self.verticalLayout_9 = QVBoxLayout(self.frameCreateDesktop)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label = QLabel(self.frameCreateDesktop)
        self.label.setObjectName(u"label")

        self.verticalLayout_9.addWidget(self.label)

        self.btnMenuCreateDesktop = QPushButton(self.frameCreateDesktop)
        self.btnMenuCreateDesktop.setObjectName(u"btnMenuCreateDesktop")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btnMenuCreateDesktop.sizePolicy().hasHeightForWidth())
        self.btnMenuCreateDesktop.setSizePolicy(sizePolicy1)
        self.btnMenuCreateDesktop.setMinimumSize(QSize(0, 0))

        self.verticalLayout_9.addWidget(self.btnMenuCreateDesktop)

        self.verticalLayout_9.setStretch(0, 1)

        self.layoutStartMenu.addWidget(self.frameCreateDesktop)

        self.frameEditDesktop = QFrame(self.page_1)
        self.frameEditDesktop.setObjectName(u"frameEditDesktop")
        self.frameEditDesktop.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameEditDesktop.setFrameShadow(QFrame.Shadow.Raised)
        self.frameEditDesktop.setLineWidth(4)
        self.verticalLayout_7 = QVBoxLayout(self.frameEditDesktop)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(-1, 6, -1, -1)
        self.label_3 = QLabel(self.frameEditDesktop)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_7.addWidget(self.label_3)

        self.btnMenuEditDesktop = QPushButton(self.frameEditDesktop)
        self.btnMenuEditDesktop.setObjectName(u"btnMenuEditDesktop")
        sizePolicy1.setHeightForWidth(self.btnMenuEditDesktop.sizePolicy().hasHeightForWidth())
        self.btnMenuEditDesktop.setSizePolicy(sizePolicy1)
        self.btnMenuEditDesktop.setMinimumSize(QSize(0, 0))
        self.btnMenuEditDesktop.setBaseSize(QSize(0, 0))

        self.verticalLayout_7.addWidget(self.btnMenuEditDesktop)

        self.verticalLayout_7.setStretch(0, 1)

        self.layoutStartMenu.addWidget(self.frameEditDesktop)

        self.frameUninstall = QFrame(self.page_1)
        self.frameUninstall.setObjectName(u"frameUninstall")
        self.frameUninstall.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameUninstall.setFrameShadow(QFrame.Shadow.Raised)
        self.frameUninstall.setLineWidth(4)
        self.verticalLayout_5 = QVBoxLayout(self.frameUninstall)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(-1, 6, -1, -1)
        self.label_2 = QLabel(self.frameUninstall)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_5.addWidget(self.label_2)

        self.btnMenuUninstall = QPushButton(self.frameUninstall)
        self.btnMenuUninstall.setObjectName(u"btnMenuUninstall")

        self.verticalLayout_5.addWidget(self.btnMenuUninstall)

        self.verticalLayout_5.setStretch(0, 1)

        self.layoutStartMenu.addWidget(self.frameUninstall)


        self.verticalLayout_8.addLayout(self.layoutStartMenu)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer)

        self.stackedWidget.addWidget(self.page_1)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        sizePolicy.setHeightForWidth(self.page_2.sizePolicy().hasHeightForWidth())
        self.page_2.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.page_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.layoutSelectApp = QHBoxLayout()
        self.layoutSelectApp.setObjectName(u"layoutSelectApp")
        self.label_10 = QLabel(self.page_2)
        self.label_10.setObjectName(u"label_10")

        self.layoutSelectApp.addWidget(self.label_10)

        self.inputAppPath = FileDropLineEdit(self.page_2)
        self.inputAppPath.setObjectName(u"inputAppPath")
        self.inputAppPath.setReadOnly(True)

        self.layoutSelectApp.addWidget(self.inputAppPath)

        self.btnBrowse = QPushButton(self.page_2)
        self.btnBrowse.setObjectName(u"btnBrowse")

        self.layoutSelectApp.addWidget(self.btnBrowse)


        self.verticalLayout_2.addLayout(self.layoutSelectApp)

        self.layoutDesktopFields = QVBoxLayout()
        self.layoutDesktopFields.setSpacing(6)
        self.layoutDesktopFields.setObjectName(u"layoutDesktopFields")
        self.scrollAreaLayoutDesktopFields = QScrollArea(self.page_2)
        self.scrollAreaLayoutDesktopFields.setObjectName(u"scrollAreaLayoutDesktopFields")
        self.scrollAreaLayoutDesktopFields.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 65, 16))
        self.scrollAreaLayoutDesktopFields.setWidget(self.scrollAreaWidgetContents_3)

        self.layoutDesktopFields.addWidget(self.scrollAreaLayoutDesktopFields)


        self.verticalLayout_2.addLayout(self.layoutDesktopFields)

        self.layoutMimeTypesList = QVBoxLayout()
        self.layoutMimeTypesList.setObjectName(u"layoutMimeTypesList")
        self.layoutMimeTypesList.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.widgetMimeTypes = QWidget(self.page_2)
        self.widgetMimeTypes.setObjectName(u"widgetMimeTypes")
        self.verticalLayout = QVBoxLayout(self.widgetMimeTypes)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_11 = QLabel(self.widgetMimeTypes)
        self.label_11.setObjectName(u"label_11")

        self.verticalLayout.addWidget(self.label_11)

        self.knownMimeTypes = QScrollArea(self.widgetMimeTypes)
        self.knownMimeTypes.setObjectName(u"knownMimeTypes")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.knownMimeTypes.sizePolicy().hasHeightForWidth())
        self.knownMimeTypes.setSizePolicy(sizePolicy2)
        self.knownMimeTypes.setMinimumSize(QSize(0, 0))
        self.knownMimeTypes.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.knownMimeTypes.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 49, 16))
        sizePolicy2.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy2)
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.knownMimeTypes.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.knownMimeTypes)


        self.layoutMimeTypesList.addWidget(self.widgetMimeTypes)


        self.verticalLayout_2.addLayout(self.layoutMimeTypesList)

        self.layoutOptions = QGroupBox(self.page_2)
        self.layoutOptions.setObjectName(u"layoutOptions")
        self.gridLayout = QGridLayout(self.layoutOptions)
        self.gridLayout.setObjectName(u"gridLayout")
        self.layoutMakeDefault = QHBoxLayout()
        self.layoutMakeDefault.setObjectName(u"layoutMakeDefault")
        self.cbMakeDefault = QCheckBox(self.layoutOptions)
        self.cbMakeDefault.setObjectName(u"cbMakeDefault")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.cbMakeDefault.sizePolicy().hasHeightForWidth())
        self.cbMakeDefault.setSizePolicy(sizePolicy3)

        self.layoutMakeDefault.addWidget(self.cbMakeDefault)


        self.gridLayout.addLayout(self.layoutMakeDefault, 1, 0, 1, 1)

        self.layoutSetMIMEicon = QHBoxLayout()
        self.layoutSetMIMEicon.setObjectName(u"layoutSetMIMEicon")
        self.cbSetMIMEicon = QCheckBox(self.layoutOptions)
        self.cbSetMIMEicon.setObjectName(u"cbSetMIMEicon")

        self.layoutSetMIMEicon.addWidget(self.cbSetMIMEicon)


        self.gridLayout.addLayout(self.layoutSetMIMEicon, 1, 2, 1, 1)

        self.line = QFrame(self.layoutOptions)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 1, 1, 1, 1)

        self.layoutAddToDesktop = QHBoxLayout()
        self.layoutAddToDesktop.setObjectName(u"layoutAddToDesktop")
        self.cbAddToDesktop = QCheckBox(self.layoutOptions)
        self.cbAddToDesktop.setObjectName(u"cbAddToDesktop")
        sizePolicy3.setHeightForWidth(self.cbAddToDesktop.sizePolicy().hasHeightForWidth())
        self.cbAddToDesktop.setSizePolicy(sizePolicy3)

        self.layoutAddToDesktop.addWidget(self.cbAddToDesktop)


        self.gridLayout.addLayout(self.layoutAddToDesktop, 1, 5, 1, 1)

        self.line_2 = QFrame(self.layoutOptions)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_2, 1, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 6, 1, 1)


        self.verticalLayout_2.addWidget(self.layoutOptions)

        self.layoutButton = QGridLayout()
        self.layoutButton.setObjectName(u"layoutButton")
        self.btnDo = QPushButton(self.page_2)
        self.btnDo.setObjectName(u"btnDo")

        self.layoutButton.addWidget(self.btnDo, 5, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.layoutButton)

        self.verticalLayout_2.setStretch(1, 2)
        self.verticalLayout_2.setStretch(2, 1)
        self.stackedWidget.addWidget(self.page_2)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.verticalLayout_6 = QVBoxLayout(self.page_4)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFormAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignTrailing)
        self.layoutIconPath = QHBoxLayout()
        self.layoutIconPath.setObjectName(u"layoutIconPath")
        self.inputIconPath = QLineEdit(self.page_4)
        self.inputIconPath.setObjectName(u"inputIconPath")

        self.layoutIconPath.addWidget(self.inputIconPath)


        self.formLayout.setLayout(3, QFormLayout.ItemRole.FieldRole, self.layoutIconPath)

        self.label_5 = QLabel(self.page_4)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_5)

        self.layoutMimeTypes = QHBoxLayout()
        self.layoutMimeTypes.setObjectName(u"layoutMimeTypes")
        self.inputMimeTypes = QLineEdit(self.page_4)
        self.inputMimeTypes.setObjectName(u"inputMimeTypes")

        self.layoutMimeTypes.addWidget(self.inputMimeTypes)


        self.formLayout.setLayout(2, QFormLayout.ItemRole.FieldRole, self.layoutMimeTypes)

        self.label_6 = QLabel(self.page_4)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_6)

        self.layoutIconSearch = QHBoxLayout()
        self.layoutIconSearch.setObjectName(u"layoutIconSearch")
        self.inputIconSearch = QLineEdit(self.page_4)
        self.inputIconSearch.setObjectName(u"inputIconSearch")

        self.layoutIconSearch.addWidget(self.inputIconSearch)


        self.formLayout.setLayout(4, QFormLayout.ItemRole.FieldRole, self.layoutIconSearch)

        self.label_4 = QLabel(self.page_4)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_4)


        self.verticalLayout_6.addLayout(self.formLayout)

        self.splitter = QSplitter(self.page_4)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setLineWidth(1)
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.splitter.setHandleWidth(4)
        self.iconsBrowser = QScrollArea(self.splitter)
        self.iconsBrowser.setObjectName(u"iconsBrowser")
        self.iconsBrowser.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 679, 427))
        self.iconsBrowser.setWidget(self.scrollAreaWidgetContents_2)
        self.splitter.addWidget(self.iconsBrowser)
        self.mimeTypes = QScrollArea(self.splitter)
        self.mimeTypes.setObjectName(u"mimeTypes")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(1)
        sizePolicy4.setHeightForWidth(self.mimeTypes.sizePolicy().hasHeightForWidth())
        self.mimeTypes.setSizePolicy(sizePolicy4)
        self.mimeTypes.setWidgetResizable(True)
        self.scrollAreaWidgetContents_4 = QWidget()
        self.scrollAreaWidgetContents_4.setObjectName(u"scrollAreaWidgetContents_4")
        self.scrollAreaWidgetContents_4.setGeometry(QRect(0, 0, 679, 16))
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.scrollAreaWidgetContents_4.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_4.setSizePolicy(sizePolicy5)
        self.mimeTypes.setWidget(self.scrollAreaWidgetContents_4)
        self.splitter.addWidget(self.mimeTypes)

        self.verticalLayout_6.addWidget(self.splitter)

        self.btnApplyMimeIcon = QPushButton(self.page_4)
        self.btnApplyMimeIcon.setObjectName(u"btnApplyMimeIcon")

        self.verticalLayout_6.addWidget(self.btnApplyMimeIcon)

        self.verticalLayout_6.setStretch(1, 1)
        self.stackedWidget.addWidget(self.page_4)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.verticalLayout_11 = QVBoxLayout(self.page_3)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.layoutBrowse = QHBoxLayout()
        self.layoutBrowse.setObjectName(u"layoutBrowse")
        self.label_12 = QLabel(self.page_3)
        self.label_12.setObjectName(u"label_12")

        self.layoutBrowse.addWidget(self.label_12)

        self.le_uninstall_path = QLineEdit(self.page_3)
        self.le_uninstall_path.setObjectName(u"le_uninstall_path")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.le_uninstall_path.sizePolicy().hasHeightForWidth())
        self.le_uninstall_path.setSizePolicy(sizePolicy6)
        self.le_uninstall_path.setReadOnly(True)

        self.layoutBrowse.addWidget(self.le_uninstall_path)

        self.btnBrowseUninstall = QPushButton(self.page_3)
        self.btnBrowseUninstall.setObjectName(u"btnBrowseUninstall")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.btnBrowseUninstall.sizePolicy().hasHeightForWidth())
        self.btnBrowseUninstall.setSizePolicy(sizePolicy7)

        self.layoutBrowse.addWidget(self.btnBrowseUninstall)


        self.verticalLayout_11.addLayout(self.layoutBrowse)

        self.layoutAppInfo = QVBoxLayout()
        self.layoutAppInfo.setObjectName(u"layoutAppInfo")
        self.layoutAppInfo.setContentsMargins(-1, 25, -1, 25)
        self.lbl_uninstall_icon = QLabel(self.page_3)
        self.lbl_uninstall_icon.setObjectName(u"lbl_uninstall_icon")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.lbl_uninstall_icon.sizePolicy().hasHeightForWidth())
        self.lbl_uninstall_icon.setSizePolicy(sizePolicy8)
        self.lbl_uninstall_icon.setMinimumSize(QSize(64, 64))
        self.lbl_uninstall_icon.setFrameShape(QFrame.Shape.NoFrame)
        self.lbl_uninstall_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layoutAppInfo.addWidget(self.lbl_uninstall_icon)

        self.lbl_uninstall_name = QLabel(self.page_3)
        self.lbl_uninstall_name.setObjectName(u"lbl_uninstall_name")

        self.layoutAppInfo.addWidget(self.lbl_uninstall_name)


        self.verticalLayout_11.addLayout(self.layoutAppInfo)

        self.btnDeintegrate = QPushButton(self.page_3)
        self.btnDeintegrate.setObjectName(u"btnDeintegrate")

        self.verticalLayout_11.addWidget(self.btnDeintegrate)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_11.addItem(self.verticalSpacer_2)

        self.stackedWidget.addWidget(self.page_3)

        self.verticalLayout_4.addWidget(self.stackedWidget)

        Integrator.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(Integrator)
        self.statusbar.setObjectName(u"statusbar")
        Integrator.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(Integrator)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setMovable(False)
        self.toolBar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toolBar.setFloatable(False)
        Integrator.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.toolBar.addAction(self.actionHome)

        self.retranslateUi(Integrator)

        self.stackedWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(Integrator)
    # setupUi

    def retranslateUi(self, Integrator):
        Integrator.setWindowTitle(QCoreApplication.translate("Integrator", u"App Integrator", None))
        self.actionHome.setText(QCoreApplication.translate("Integrator", u"Back", None))
        self.actionClose.setText(QCoreApplication.translate("Integrator", u"Close", None))
        self.actionAbout.setText(QCoreApplication.translate("Integrator", u"About", None))
        self.actionSetMimeIcon.setText(QCoreApplication.translate("Integrator", u"Set MIME Icon", None))
        self.actionFindMimeType.setText(QCoreApplication.translate("Integrator", u"Find MIME Type", None))
        self.actionUtilities.setText(QCoreApplication.translate("Integrator", u"Utilities", None))
        self.label.setText(QCoreApplication.translate("Integrator", u"Create a desktop file based on an AppImage", None))
        self.btnMenuCreateDesktop.setText(QCoreApplication.translate("Integrator", u"Create desktop file", None))
        self.label_3.setText(QCoreApplication.translate("Integrator", u"Edit an existing desktop file", None))
        self.btnMenuEditDesktop.setText(QCoreApplication.translate("Integrator", u"Edit desktop file", None))
        self.label_2.setText(QCoreApplication.translate("Integrator", u"Uninstall using a desktop file. Removes the .desktop file, the icon and restores the MIME types.", None))
        self.btnMenuUninstall.setText(QCoreApplication.translate("Integrator", u"Uninstall", None))
        self.label_10.setText(QCoreApplication.translate("Integrator", u"Select App:", None))
        self.btnBrowse.setText(QCoreApplication.translate("Integrator", u"Browse", None))
        self.label_11.setText(QCoreApplication.translate("Integrator", u"Known mime types (select any):", None))
        self.layoutOptions.setTitle(QCoreApplication.translate("Integrator", u"Options", None))
        self.cbMakeDefault.setText(QCoreApplication.translate("Integrator", u"Make default", None))
        self.cbSetMIMEicon.setText(QCoreApplication.translate("Integrator", u"Set MIME Icon", None))
        self.cbAddToDesktop.setText(QCoreApplication.translate("Integrator", u"Add to Desktop", None))
        self.btnDo.setText(QCoreApplication.translate("Integrator", u"Apply", None))
        self.label_5.setText(QCoreApplication.translate("Integrator", u"Icon:", None))
        self.label_6.setText(QCoreApplication.translate("Integrator", u"MIME types:", None))
        self.label_4.setText(QCoreApplication.translate("Integrator", u"Search:", None))
        self.btnApplyMimeIcon.setText(QCoreApplication.translate("Integrator", u"Apply", None))
        self.label_12.setText(QCoreApplication.translate("Integrator", u"Select App:", None))
        self.btnBrowseUninstall.setText(QCoreApplication.translate("Integrator", u"Browse", None))
        self.lbl_uninstall_icon.setText("")
        self.lbl_uninstall_name.setText("")
        self.btnDeintegrate.setText(QCoreApplication.translate("Integrator", u"Deintegrate", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("Integrator", u"toolBar", None))
    # retranslateUi

