# Accessibility checker

Scan webpages for potential accessibility issues using WCAG 2.2 as the target
standard and save the results to CSV. Supports Chromium and Firefox.
Coverage is being expanded; the current version implements only the checks listed below.

## Usage

Follow the [root setup instructions](../../README.md#setup-and-running) and activate
the virtual environment. Run these commands from the repository root.

Create the output folder and scan one page:

```bash
mkdir reports
python src/accessibility_checker/cli.py --urls https://example.com -o reports --headless
```

Scan several pages:

```bash
python src/accessibility_checker/cli.py --urls https://example.com https://example.org -o reports --headless
```

Scan a text file using Firefox:

```bash
python src/accessibility_checker/cli.py --url-file urls.txt --browser firefox -o reports --headless
```

Example `urls.txt`:

```text
https://example.com
https://example.org
```

Scan a sitemap:

```bash
python src/accessibility_checker/cli.py --url-file https://example.com/sitemap.xml -o reports --headless
```

Use either `--urls` or `--url-file`. Files can be local or remote; XML paths must
end in `.xml`. Sitemap indexes are not expanded into child sitemaps.

| Option | Purpose |
| --- | --- |
| `--urls URL [URL ...]` | Pages to scan, starting with `http://` or `https://`. |
| `--url-file PATH_OR_URL` | TXT URL list or XML sitemap. |
| `-o`, `--output-path` | Existing directory for the CSV report. Required. |
| `--browser` | `chromium` (default) or `firefox`. |
| `-hl`, `--headless` | Run without a visible browser window. |
| `-h`, `--help` | Show help. |

## Output

Each run creates a file such as `reports/2026-09-23-14-30-00.csv`.

The report columns are `time`, `page`, `criterion`, `message_type`, `tag`,
`message`, and `code`. `code` contains the original opening tag.
For example, `<img src="photo.jpg">` produces a finding like this (timestamp and
page URL omitted here):

| criterion | message_type | tag | message | code |
| --- | --- | --- | --- | --- |
| 1.1.1 | REVIEW_REQUIRED | img | Missing alt text attribute | `<img src="photo.jpg">` |

- `REVIEW_REQUIRED`: a potential issue to review.
- `PAGE_ERROR`: the page could not be scanned; processing continues.
- `LOADING_TIMED_OUT`: network activity did not settle; the loaded HTML is still checked.

An empty report contains only column headers.

## Current checks

`WCAG22_1_1` reports candidates for review under WCAG 2.2 criterion 1.1.1 (Non-text Content):

- `<img>` missing `alt`.
- `<svg>`, `<canvas>`, `<audio>`, and `<video>` missing both `aria-label` and `aria-labelledby`.
- Other elements with `role="img"` missing both ARIA label attributes.

Examples:

```html
<!-- Reported -->
<img src="photo.jpg">
<svg></svg>
<span role="img">:)</span>

<!-- Not reported by the current checks -->
<img src="photo.jpg" alt="A mountain lake">
<svg aria-label="Company logo"></svg>
<span role="img" aria-label="Smile">:)</span>
```

These checks only detect missing attributes. Empty values count as present, and
label references and descriptions are not validated. Valid alternatives such as
SVG titles or decorative graphics may still be flagged. CSS imagery, unmarked
character graphics, iframe contents, and shadow DOM are not checked.
A report with no findings does not establish WCAG compliance.

## Code structure

- `cli.py`: arguments and pipeline startup.
- `validators.py`: URL sources and output directory validation.
- `checkers.py`: WCAG checker classes and the `CHECKERS` list.
- `logger.py`: page loading, checker execution, DataFrame, and CSV export.
