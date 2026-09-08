from pathlib import Path

from PySide6.QtCore import Qt, QUrl, Signal
from PySide6.QtQuickWidgets import QQuickWidget


class Preview(QQuickWidget):
    # Host a Qt Quick browser with an independently sized CSS viewport.

    urlChanged = Signal(QUrl)
    loadStarted = Signal()
    loadFinished = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        directory = Path(__file__).resolve().parent
        self.setSource(QUrl.fromLocalFile(str(directory / "preview.qml")))
        if self.status() == QQuickWidget.Status.Error:
            raise RuntimeError("Unable to load browser preview:\n" +
                               "\n".join(error.toString() for error in self.errors()))

        self.rootObject().addressChanged.connect(self.urlChanged.emit)
        self.rootObject().pageLoadStarted.connect(self.loadStarted.emit)
        self.rootObject().pageLoadFinished.connect(self.loadFinished.emit)

    def set_url(self, url):
        self.rootObject().setProperty("pageUrl", url)

    def reload_bypassing_cache(self):
        self.rootObject().reloadPage()

    def set_size(self, width, height):
        self.rootObject().setProperty("viewportWidth", width)
        self.rootObject().setProperty("viewportHeight", height)
