## Qt Web Engine Dropdown Menu Workaround
When QWebEngineView is passed inside a QGraphicsView widget, it may lead to unexpected behaviors on dropdown menus inside the webpages, as these components are not originally designed to work together.
In this dropdown menu case, it originally opens outside of the QGraphicsView widget most of the times. With this workaround, the original dropdown menu is intercepted, then a patched one is created in its place.
This implementation avoids code overcomplication and keeps it lightweight.  