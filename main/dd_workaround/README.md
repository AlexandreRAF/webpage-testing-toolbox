# Qt WebEngine dropdown workaround

## Why it is needed

The viewport simulator embeds a `QWebEngineView` inside a `QGraphicsView` so the page can be scaled to fit the application window. In this configuration, Qt WebEngine's native picker for an HTML `<select>` can be positioned outside the simulated viewport or behave inconsistently.

This workaround prevents the native picker from opening and displays a lightweight, in-page replacement menu at the select element's position instead. The replacement stays inside the webpage viewport, so dropdowns remain usable while the page is being simulated.

## How it works

When the page is loaded, `dropdown_injection.js` is injected into it by the application. When a supported `<select>` is opened, the script blocks Qt WebEngine's native picker and creates a temporary popup inside the webpage instead.

The popup:

- Copies the select's options and basic styling.
- Opens above or below the control, depending on available space.
- Stays within the webpage viewport and scrolls when the option list is long.
- Updates the original `<select>` when an option is chosen.
- Sends the usual `input` and `change` events so the page continues to respond normally.

The popup closes when the user makes a selection, presses `Escape` or `Tab`, clicks elsewhere, or the page is scrolled, resized, hidden, or loses focus. Its styles are isolated from the webpage with a closed Shadow DOM, and the script prevents itself from being installed more than once.

This is intentionally a focused compatibility layer rather than a complete reimplementation of every browser-native select behavior. Advanced native-picker features may not be reproduced exactly.

## Files

| File | Purpose |
| --- | --- |
| `dropdown_injection.js` | Creates the replacement popup and handles interaction, positioning, and selection. |
| `popup.css` | Styles the popup, options, active option, groups, and disabled states. |
| `README.md` | Documents the workaround and its intended scope. |

## Integration

The main application loads both workaround files from this directory when it starts. Because an injected page script cannot read a local CSS file directly, `main/view_tester.py` reads `popup.css`, inserts its contents into the `__POPUP_CSS_FILE__` placeholder in `dropdown_injection.js`, and registers the resulting script with `QWebEngineScript`.
