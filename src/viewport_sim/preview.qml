import QtQuick
import QtWebEngine

Rectangle {
    id: preview
    color: "#202124"
    clip: true

    property int viewportWidth: 1000
    property int viewportHeight: 700
    property alias pageUrl: browser.url

    signal addressChanged(url address)
    signal pageLoadStarted()
    signal pageLoadFinished(bool success)

    function reloadPage() {
        browser.reloadAndBypassCache()
    }

    WebEngineView {
        id: browser
        objectName: "browser"
        // Scale the rendered item, keeping the page's CSS viewport unchanged.
        width: preview.viewportWidth
        height: preview.viewportHeight
        anchors.centerIn: parent
        scale: Math.min(preview.width / width, preview.height / height)
        transformOrigin: Item.Center
        focus: true

        onUrlChanged: preview.addressChanged(url)
        onLoadingChanged: function(info) {
            if (info.status === WebEngineView.LoadStartedStatus)
                preview.pageLoadStarted()
            else if (info.status === WebEngineView.LoadSucceededStatus)
                preview.pageLoadFinished(true)
            else if (info.status === WebEngineView.LoadFailedStatus
                     || info.status === WebEngineView.LoadStoppedStatus)
                preview.pageLoadFinished(false)
        }
    }
}
