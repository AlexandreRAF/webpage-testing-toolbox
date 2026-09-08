import sys

from PySide6.QtCore import Qt, QUrl

from PySide6.QtWidgets import *

from PySide6.QtWebEngineQuick import QtWebEngineQuick

from preview import Preview

# TODO: Move the settings into an external json or cfg file
PRESETS = {
    "Mobile": (390, 844),
    "Tablet": (768, 1024),
    "Laptop": (1366, 768),
    "Desktop": (1920, 1080),
}

DEFAULT_SIZING = {"width": 1000, "height": 700}


class ViewportTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Viewport Simulator")

        # URL input.
        self.url = QLineEdit("https://example.com")
        self.url.returnPressed.connect(self.load_page)

        # "Ctrl + Shift + R" function button.
        refresh = QPushButton("Refresh")
        refresh.clicked.connect(self.refresh_page)

        # Orientation change button.
        rotate = QPushButton("Rotate")
        rotate.clicked.connect(self.rotate_page)

        # Status label.
        self.status = QLabel("LOADING...")
        self.status.setStyleSheet("font-weight: bold; color: red;")

        # Store the preset dimensions as item data on each combo-box item.
        self.preset = QComboBox()
        self.preset.addItem("Custom")
        for name, size in PRESETS.items():
            self.preset.addItem(name, size)
        self.preset.currentIndexChanged.connect(self.use_preset)

        # Starting viewport dimensions.
        self.width_box = self.number_box(DEFAULT_SIZING["width"])
        self.height_box = self.number_box(DEFAULT_SIZING["height"])

        self.width_box.valueChanged.connect(self.resize_preview)
        self.height_box.valueChanged.connect(self.resize_preview)

        # Initialize the browser.
        self.preview = Preview()
        self.preview.urlChanged.connect(self.url_updater)
        self.preview.loadFinished.connect(self.load_finished)
        self.preview.loadStarted.connect(self.load_started)

        # Configure the controls bar.
        controls = QHBoxLayout()
        controls.addWidget(QLabel("URL"))
        controls.addWidget(self.url, 1)
        controls.addWidget(self.status)
        controls.addWidget(refresh)
        controls.addWidget(self.preset)
        controls.addWidget(QLabel("W"))
        controls.addWidget(self.width_box)
        controls.addWidget(QLabel("H"))
        controls.addWidget(self.height_box)
        controls.addWidget(rotate)

        # Configure the browser view placement and add the controls bar bellow it.
        central = QWidget()
        layout = QVBoxLayout(central)   
        layout.addWidget(self.preview, 1)
        layout.addLayout(controls)

        # QMainWindow uses one central widget as the main content area.
        self.setCentralWidget(central)

        # Load the initial page and apply the initial viewport.
        self.resize_preview()
        self.preview.set_url(QUrl(self.url.text()))

    # Page loading status handling.
    def load_started(self):
        self.status.setText("LOADING...")
        self.status.setStyleSheet("font-weight: bold; color: red;")

    def load_finished(self, success):
        self.status.setText("LOADED" if success else "LOAD FAILED")
        self.status.setStyleSheet("font-weight: bold; color: %s;" % ('lime' if success else 'red'))

    def refresh_page(self):
        # Simulate "Ctrl + Shift + R" behavior.
        self.preview.reload_bypassing_cache()

    def url_updater(self, address):
        # Updates the url if the page is redirected 
        # (this function is activated by a URL change listener).
        self.url.setText(address.toString())

    @staticmethod
    def number_box(value):
        # This helper avoids repeating the same QSpinBox setup twice.
        box = QSpinBox()
        box.setRange(100, 10000) # Dimension limits can be overriden by changing this line
        box.setValue(value)
        box.setSuffix(" px")

        return box

    def use_preset(self, index):
        # itemData returns the (width, height) tuple stored on the combo box.
        size = self.preset.itemData(index)
        if size:
            self.width_box.setValue(size[0])
            self.height_box.setValue(size[1])

    def resize_preview(self):
        # Qt Quick scales the browser without changing its CSS viewport.
        width, height = self.width_box.value(), self.height_box.value()
        self.preview.set_size(width, height)

    def load_page(self):
        # QUrl needs a complete URL, so add https:// when the user omits it.
        address = self.url.text().strip()

        if address and not address.startswith(("http://", "https://")):
            address = "https://" + address
            self.url.setText(address)

        self.preview.set_url(QUrl(address))

    def rotate_page(self):
        # Gets current width and height and invert them,
        width, height = self.width_box.value(), self.height_box.value()

        self.width_box.setValue(height)
        self.height_box.setValue(width)


def main():
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
    QtWebEngineQuick.initialize()
    app = QApplication(sys.argv)
    window = ViewportTool()
    window.showMaximized()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
