# Webpage Testing Toolbox

Webpage Testing Toolbox is a growing collection of focused utilities for inspecting, testing, and troubleshooting websites. It is intended for web developers, testers, and anyone who needs practical ways to identify responsive layout issues, browser console messages, loading problems, and other behavior that may be difficult to spot when checking pages manually.

The tools support different parts of the website testing process, from previewing a page at exact viewport dimensions to collecting diagnostics across many URLs. Each utility is designed to solve a specific problem and can be used independently, without requiring the rest of the toolbox.

Current tools:

- **[Viewport simulator](src/viewport_sim/README.md):** preview responsive layouts at their real target viewport resolution, using common presets or custom dimensions.
- **[Bulk console logger](src/console_logger/README.md):** visit multiple URLs with Chromium or Firefox and save browser console messages and page loading times to CSV.

## Requirements

- Python 3
- Windows or Linux
- A display environment capable of running PySide6 and Qt WebEngine for the viewport simulator

The setup script creates the project's local `venv` virtual environment, installs Python dependencies from [`venv_creation_components/requirements.txt`](venv_creation_components/requirements.txt), and installs Chromium and Firefox for the console logger through Playwright.

## Setup and running

Start each command block from the repository root. Run setup once, or when recreating the environment.

### Windows

Create the environment and install dependencies:

```bat
cd venv_creation_components
create_venv_windows.bat
```

### Linux

Create the environment and install dependencies:

```bash
cd venv_creation_components
bash create_venv_linux.sh
```

After setup, follow the [viewport simulator guide](src/viewport_sim/README.md#running) or the [console logger guide](src/console_logger/README.md#setup) to run a tool.

## Viewport simulator

The webpage renders at the exact selected width and height in CSS pixels. A 1920 × 1080 viewport keeps that resolution even when the preview scales down to fit the application window.

![Webpage Testing Toolbox showing a simulated webpage viewport](assets/view_tester.PNG)

See [launch instructions, presets, and usage](src/viewport_sim/README.md).

## Bulk console logger

The initial CLI version supports direct URLs, text URL lists, and XML sitemaps. It visits pages sequentially and exports a CSV report.

See [setup, examples, and CLI options](src/console_logger/README.md).

## To do

### Bulk console logger

- [ ] Create a graphical user interface (GUI).
- [ ] Implement parallel workers to scan multiple pages at once.

### Planned tools

- [ ] **Network throttling and performance logger:** test multiple pages under configurable bandwidth and latency limits, then export loading performance metrics.
- [ ] **Bulk accessibility checker:** scan multiple pages for common accessibility issues and export findings for each URL.
- [ ] **Bulk metadata and SEO checker:** inspect page titles, meta descriptions, canonical URLs, robots directives, and heading structure, then flag missing or inconsistent values.

## Project structure

```text
src/
|-- viewport_sim/
|   |-- README.md          # Viewport simulator documentation
|   |-- viewport_sim.py    # Desktop application
|   |-- preview.py         # Qt Quick host and Python signal bridge
|   `-- preview.qml        # WebEngineView and viewport scaling
`-- console_logger/
    |-- README.md          # CLI documentation
    |-- cli.py             # Command-line entry point
    |-- logger.py          # Browser console capture and CSV export
    `-- validators.py      # URL and output directory validation
assets/
`-- view_tester.PNG        # Viewport simulator preview
```

## License

This project is open source and distributed under the terms of the [MIT License](LICENSE).
