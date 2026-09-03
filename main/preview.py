from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPainter

class Preview(QGraphicsView):
    # Show the web page at its selected resolution, scaled to fit the screen.

    def __init__(self, browser):
        super().__init__()

        # A QGraphicsScene can contain widgets and apply a visual transform to them.
        self.scene = QGraphicsScene(self)
        self.scene.addWidget(browser)
        self.setScene(self.scene)

        # Center the simulated browser and hide scrollbars because it is always scaled to fit inside this view.
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setStyleSheet("background: #202124; border: 0;")

    # resizeEvent is a property that already exists on QGraphicsView. It is overriden here:
    def resizeEvent(self, event): 
        # Recalculate the scale whenever the monitor or window size changes.
        super().resizeEvent(event)
        self.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self.set_scaling_quality()

    def set_size(self, width, height):
        # The scene rectangle represents the browser's real simulated size.
        self.scene.setSceneRect(0, 0, width, height)

        self.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self.set_scaling_quality()

    
    def set_scaling_quality(self):
        # Enable smooth scaling when downscaling the view, to mitigate some scaling artifacts.
        width = self.scene.width()
        scene_width = self.size().width()
        if (width > scene_width):
            self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        else:
            self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, False)