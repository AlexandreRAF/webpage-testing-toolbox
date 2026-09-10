# Bulk console logger

Visit multiple webpages with Chromium or Firefox and save browser console messages and page loading times to a CSV report. This is the initial CLI version; pages are visited sequentially.

## Setup

Follow the [root setup instructions](../../README.md#setup-and-running) to create the virtual environment and install dependencies, including Chromium and Firefox. Then activate the environment from the repository root:

Windows (Command Prompt):

```bat
venv\Scripts\activate.bat
```

Linux:

```bash
source venv/bin/activate
```

## Usage

Run the following commands from the repository root with the virtual environment active. Create the output directory before running the logger:

```bash
mkdir reports
```

Scan URLs without opening a visible browser window:

```bash
python src/console_logger/cli.py --urls https://example.com https://example.org -o reports --headless
```

Scan URLs from a text file:

```bash
python src/console_logger/cli.py --url-file urls.txt -o reports --headless
```

Example `urls.txt`:

```text
https://example.com
https://example.org
```

Scan a sitemap using Firefox:

```bash
python src/console_logger/cli.py --url-file https://example.com/sitemap.xml --browser firefox -o reports --headless
```

`--url-file` accepts a local path or an HTTP(S) URL. XML paths must end in `.xml`; other paths are treated as whitespace-separated text lists. XML input should contain page URLs in `<loc>` elements. Sitemap indexes are not expanded into their child sitemaps.

### Alternative: run without activating the environment

After setup, you can use the virtual environment's Python directly. Run from the repository root with the `reports` directory already created.

Windows:

```bat
venv\Scripts\python.exe src\console_logger\cli.py --urls https://example.com -o reports --headless
```

Linux:

```bash
./venv/bin/python src/console_logger/cli.py --urls https://example.com -o reports --headless
```

All CLI options work the same way with either approach.

## Options

| Option | Description |
| --- | --- |
| `--urls URL [URL ...]` | Page URLs starting with `http://` or `https://`. |
| `--url-file PATH_OR_URL` | Text URL list or XML sitemap. Use either this or `--urls`. |
| `-o`, `--output-path DIRECTORY` | Required existing output directory, not a CSV filename. |
| `--browser {chromium,firefox}` | Browser to use. Default: `chromium`. |
| `-hl`, `--headless` | Run without a visible browser window. By default, the browser is visible. |
| `-h`, `--help` | Show help. |

Provide exactly one URL source and an output directory. URLs without an HTTP(S) prefix are skipped.

## Output

Each run saves a timestamped file such as `reports/2026-09-10-14-30-00.csv` with these columns:

| Column | Contents |
| --- | --- |
| `time` | Timestamp recorded by the logger. |
| `page` | Page URL. |
| `message_type` | Browser console message type, `PAGE_LOADING_TIME`, or `LOADING_TIMED_OUT`. |
| `message` | Console text, loading duration in seconds, or timeout message. |

Loading time includes waiting for network activity to settle. The report includes console messages of all types, not just errors. It is saved after all pages have been processed; a navigation failure can stop the run before the CSV is written.
