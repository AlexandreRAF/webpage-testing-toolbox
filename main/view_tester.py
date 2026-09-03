import sys
import os

from PySide6.QtCore import QUrl

from PySide6.QtWidgets import *

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineScript, QWebEnginePage

from preview import Preview

# TODO: Move the settings into an external json or cfg file
PRESETS = {
    "Mobile": (390, 844),
    "Tablet": (768, 1024),
    "Laptop": (1366, 768),
    "Desktop": (1920, 1080),
}

DEFAULT_SIZING = {"width": 1000, "height": 700}

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
WORKAROUND_JS_PATH = ('%s/dd_workaround/dropdown_injection.js' % CURRENT_DIR)
WORKAROUND_CSS_PATH = ('%s/dd_workaround/popup.css' % CURRENT_DIR)

page_loaded = False


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
        self.browser = QWebEngineView()
        self.browser.urlChanged.connect(self.url_updater)
        self.browser.loadFinished.connect(self.load_finished)
        self.browser.loadStarted.connect(self.load_started)
        self.install_dropdown_script()
        self.preview = Preview(self.browser)

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
        self.browser.setUrl(QUrl(self.url.text()))
        self.resize_preview()

    # Page loading status handling.
    def load_started(self):
        global page_loaded 
        page_loaded = False
        self.status_label_updater()

    def load_finished(self):
        global page_loaded 
        page_loaded = True
        self.status_label_updater()

    def status_label_updater(self):
        global page_loaded
        self.status.setText("LOADED" if page_loaded == True else "LOADING...")
        self.status.setStyleSheet("font-weight: bold; color: %s;" % ('lime' if page_loaded == True else 'red'))

    def refresh_page(self):
        # Simulate "Ctrl + Shift + R" behavior.
        self.browser.page().triggerAction(QWebEnginePage.WebAction.ReloadAndBypassCache)

    def url_updater(self):
        # Updates the url if the page is redirected 
        # (this function is activated by a URL change listener).
        self.url.setText(self.browser.url().url())

    def install_dropdown_script(self):
        # Dropdown menu behavior patch via js injection
        script = QWebEngineScript()
        script.setName("Dropdown menu workaround")

        script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentReady)
        script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)

        # Also apply the patches inside iframes.
        script.setRunsOnSubFrames(True)

        # Opens the patch files and imports the css inside the js before injection, 
        # as the injected script cannot read it directly.
        js = open(WORKAROUND_JS_PATH).read().strip()
        css = open(WORKAROUND_CSS_PATH).read().strip()
        final_js = js.replace("__POPUP_CSS_FILE__", css, 1)

        script.setSourceCode(final_js)
        self.browser.page().scripts().insert(script)

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
        # Set the real browser size first, then tell the graphics view to
        # scale that browser to fit the current screen.
        width, height = self.width_box.value(), self.height_box.value()
        self.browser.setFixedSize(width, height)
        self.preview.set_size(width, height)

    def load_page(self):
        # QUrl needs a complete URL, so add https:// when the user omits it.
        address = self.url.text().strip()

        if address and not address.startswith(("http://", "https://")):
            address = "https://" + address
            self.url.setText(address)

        self.browser.setUrl(QUrl(address))

    def rotate_page(self):
        # Gets current width and height and invert them,
        width, height = self.width_box.value(), self.height_box.value()

        self.browser.setFixedSize(height, width)
        self.preview.set_size(height, width)

        self.width_box.setValue(height)
        self.height_box.setValue(width)


def main():
    app = QApplication(sys.argv)
    window = ViewportTool()
    window.showMaximized()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
