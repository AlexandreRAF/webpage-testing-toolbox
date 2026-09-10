# Viewport simulator

Preview webpages at their real target viewport resolution in an embedded Chromium-based browser.

The webpage renders at the selected width and height in CSS pixels, so its layout and responsive breakpoints use those exact dimensions. For example, selecting 1920 × 1080 gives the page a 1920 × 1080 CSS viewport, even when the preview is scaled down to fit the application window.

![Viewport simulator](../../assets/view_tester.PNG)

## Setup

Follow the [root setup instructions](../../README.md#setup-and-running) to create the virtual environment and install dependencies. The simulator requires a desktop display environment capable of running PySide6 and Qt WebEngine.

## Running

Start from the repository root in a new terminal.

Windows (Command Prompt):

```bat
cd src\viewport_sim
run_windows.bat
```

Linux:

```bash
cd src/viewport_sim
bash run_linux.sh
```

The launcher activates the project's virtual environment and applies the platform-specific launch configuration.

## Usage

1. Enter a webpage URL and press **Enter** to load it.
2. Choose a preset, or select **Custom** and enter the width (**W**) and height (**H**).
3. Click **Rotate** to swap the width and height.
4. Click **Refresh** to reload the page while bypassing the cache.

The preview stays centered and scales to fit the window while preserving the selected viewport resolution.

## Presets

| Preset | Width × height (CSS pixels) |
| --- | --- |
| Mobile | 390 × 844 |
| Tablet | 768 × 1024 |
| Laptop | 1366 × 768 |
| Desktop | 1920 × 1080 |

The initial custom viewport is 1000 × 700. Each custom dimension can range from 100 to 10000 CSS pixels.
