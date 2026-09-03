// Lightweight select replacement for Qt WebEngine previews. It intentionally
// supports the common interaction path instead of fully reproducing every
// native <select> behavior.

// Script runs in a private scope (using IIFE) to make sure
// it will not conflict with the website.
(() => {
    "use strict";

    //Prevents the script to be loaded more than once into the same context.
    const INSTALL_KEY = "__qtSimpleSelectPopup";
    if (globalThis[INSTALL_KEY]) return;
    globalThis[INSTALL_KEY] = true;

    //-------------------------------------------------------------------------
    // Global Variables
    //-------------------------------------------------------------------------

    const CSS = `__POPUP_CSS_FILE__`;
    const MENU_STYLE = [
        "font-family", "font-size", "font-weight", "font-style", "line-height",
        "letter-spacing", "word-spacing", "text-transform", "direction",
        "color", "color-scheme", "border", "border-radius", "box-shadow",
        "text-shadow",
    ];
    const OPTION_STYLE = [
        "font-family", "font-size", "font-weight", "font-style", "line-height",
        "letter-spacing", "word-spacing", "text-transform", "direction",
        "color", "background-color",
    ];

    // Keep the popup state in one place so opening, closing, and selection
    // changes cannot leave separate variables out of sync.
    const state = { select: null, activeIndex: -1, host: null, menu: null };

    //-------------------------------------------------------------------------
    // Functions
    //-------------------------------------------------------------------------

    const isSelect = (node) => node?.localName === "select";

    const selectFromEvent = (event) => {
        const path = event.composedPath?.() || [event.target];
        return path.find(isSelect) || null;
    };

    function eligible(select) {
        // Leave multi-selects, list boxes, and invisible controls untouched.
        if (!isSelect(select) || select.disabled || select.multiple || select.size > 1) return false;
        const rect = select.getBoundingClientRect();
        const style = getComputedStyle(select);
        return rect.width > 0 && rect.height > 0 && style.display !== "none" &&
            style.visibility !== "hidden" && style.pointerEvents !== "none";
    }

    function ensurePopup() {
        if (state.host?.isConnected) return;

        // A closed shadow root keeps the popup's styles isolated from the page.
        const host = document.createElement("div");
        host.style.cssText = "all:initial;position:fixed;display:none;z-index:2147483647";

        const shadow = host.attachShadow({ mode: "closed" });
        const style = document.createElement("style");
        const menu = document.createElement("div");

        style.textContent = CSS;
        menu.id = "menu";
        menu.setAttribute("role", "listbox");
        menu.addEventListener("click", onMenuClick);
        menu.addEventListener("pointermove", onMenuPointerMove);
        shadow.append(style, menu);
        (document.documentElement || document.body).append(host);
        state.host = host;
        state.menu = menu;
    }

    const optionIndex = (row) => Number.isInteger(Number(row?.dataset.index)) ? Number(row.dataset.index) : -1;

    function validIndex(index) {
        // Disabled options cannot be selected through the custom menu.
        const option = state.select?.options[index];
        return Boolean(option && !option.disabled && !option.hidden && !option.parentElement?.disabled);
    }

    function copyStyles(source, target, properties) {
        const style = getComputedStyle(source);
        properties.forEach((property) => {
            const value = style.getPropertyValue(property);
            if (value && value !== "normal") target.style.setProperty(property, value);
        });
    }

    function effectiveBackground(element) {
        let current = element;
        while (current?.nodeType === Node.ELEMENT_NODE) {
            const color = getComputedStyle(current).backgroundColor;
            if (color && color !== "transparent" && color !== "rgba(0, 0, 0, 0)") return color;
            current = current.parentElement;
        }
        return "Canvas";
    }

    function copyMenuStyle(select) {
        copyStyles(select, state.menu, MENU_STYLE);
        const selectStyle = getComputedStyle(select);
        const background = selectStyle.backgroundColor === "transparent" ||
            selectStyle.backgroundColor === "rgba(0, 0, 0, 0)"
            ? effectiveBackground(select)
            : selectStyle.backgroundColor;
        state.menu.style.backgroundColor = background;
        state.menu.style.padding = selectStyle.padding;
    }

    function setActive(index) {
        if (!validIndex(index)) return;
        state.activeIndex = index;

        // CSS highlights the active row; the real select remains focused.
        state.menu.querySelectorAll(".option").forEach((row) => {
            row.dataset.active = String(optionIndex(row) === index);
        });
    }

    function buildMenu(select) {
        // Flatten options and optgroups into rows while retaining the original
        // option index, which is needed when committing a selection.
        state.menu.replaceChildren();
        Array.from(select.children).forEach((child) => {
            if (child instanceof HTMLOptGroupElement) {
                const group = document.createElement("div");
                group.className = "group";
                group.textContent = child.label;
                copyStyles(child, group, ["font-family", "font-size", "font-weight", "font-style", "color", "direction"]);
                state.menu.append(group);
                Array.from(child.children).forEach((option) => addOption(select, option, child.disabled));
            } else if (child instanceof HTMLOptionElement) {
                addOption(select, child, false);
            }
        });
    }

    function addOption(select, option, groupDisabled) {
        if (!(option instanceof HTMLOptionElement) || option.hidden) return;
        const index = Array.prototype.indexOf.call(select.options, option);
        const row = document.createElement("div");
        const disabled = groupDisabled || option.disabled;

        // Copy the option's appearance, falling back to the select's style.
        const selectStyle = getComputedStyle(select);
        const optionStyle = getComputedStyle(option);

        copyStyles(option, row, OPTION_STYLE);

        if (!row.style.color) row.style.color = selectStyle.color;

        if (!row.style.backgroundColor || row.style.backgroundColor === "rgba(0, 0, 0, 0)") {
            row.style.backgroundColor = "transparent";
        }

        row.className = "option";
        row.dataset.index = String(index);
        row.dataset.active = String(index === state.activeIndex);
        row.textContent = option.label || option.textContent || "";
        row.setAttribute("role", "option");
        row.setAttribute("aria-disabled", String(disabled));
        row.setAttribute("aria-selected", String(option.selected));

        row.style.padding = optionStyle.padding !== "0px"
            ? optionStyle.padding
            : (selectStyle.padding || "4px 8px");

        state.menu.append(row);
    }

    function positionPopup(select) {
        // Place the menu below the select when possible, otherwise above it, and keep it within the web page viewport.
        const rect = select.getBoundingClientRect();
        const margin = 4;
        const viewportWidth = document.documentElement.clientWidth;
        const viewportHeight = document.documentElement.clientHeight;
        const menuRect = state.menu.getBoundingClientRect();
        const below = viewportHeight - rect.bottom;
        const openBelow = below >= menuRect.height || below >= rect.top;
        const top = openBelow ? rect.bottom + 2 : rect.top - menuRect.height - 2;
        const left = Math.min(Math.max(margin, rect.left), viewportWidth - menuRect.width - margin);

        state.menu.style.minWidth = `${Math.max(80, rect.width)}px`;
        state.menu.style.maxWidth = `${viewportWidth - margin * 2}px`;
        state.menu.style.maxHeight = `${Math.max(40, Math.min(320, viewportHeight - margin * 2))}px`;
        state.host.style.display = "block";
        state.host.style.visibility = "hidden";
        state.host.style.left = `${left}px`;
        state.host.style.top = `${Math.max(margin, top)}px`;
        state.host.style.visibility = "visible";
    }

    function open(select) {
        if (!eligible(select)) return;
        ensurePopup();
        state.select = select;
        state.activeIndex = select.selectedIndex;
        copyMenuStyle(select);
        buildMenu(select);
        positionPopup(select);
        if (state.activeIndex >= 0) setActive(state.activeIndex);
    }

    function close(refocus = false) {
        // Closing clears the rows so a later open always reflects current DOM.
        const select = state.select;
        state.select = null;
        state.activeIndex = -1;
        if (state.host) state.host.style.display = "none";
        if (state.menu) state.menu.replaceChildren();
        if (refocus && select?.isConnected) select.focus({ preventScroll: true });
    }

    function commit(index) {
        const select = state.select;
        if (!select || !validIndex(index)) return close(true);
        const previous = select.selectedIndex;

        // Update the real control so the website's existing form logic keeps
        // working, then notify it using the events expected from a select.
        select.selectedIndex = index;
        close(true);
        if (previous !== index) {
            select.dispatchEvent(new Event("input", { bubbles: true }));
            select.dispatchEvent(new Event("change", { bubbles: true }));
        }
    }

    function moveActive(step) {
        if (!state.select) return;
        let index = state.activeIndex;
        do { index += step; } while (index >= 0 && index < state.select.options.length && !validIndex(index));
        if (validIndex(index)) setActive(index);
    }

    function onMenuPointerMove(event) {
        const row = event.target.closest?.(".option");
        if (row && row.getAttribute("aria-disabled") !== "true") setActive(optionIndex(row));
    }

    function onMenuClick(event) {
        const row = event.target.closest?.(".option");
        if (!row || row.getAttribute("aria-disabled") === "true") return;
        event.preventDefault();
        commit(optionIndex(row));
    }

    function onMouseDown(event) {
        // Cancel Qt's native picker and show the HTML popup instead.
        if (state.host?.contains(event.target)) return;
        const select = selectFromEvent(event);
        if (select && eligible(select) && event.button === 0) {
            event.preventDefault();
            queueMicrotask(() => state.select === select ? close(true) : open(select));
        } else if (state.select) {
            close(false);
        }
    }

    function onKeyDown(event) {
        // Keyboard actions mapping
        if (state.select) {
            if (event.key === "Escape" || event.key === "Tab") {
                event.preventDefault();
                return close(true);
            }
            if (event.key === "ArrowDown" || event.key === "ArrowRight") {
                event.preventDefault();
                return moveActive(1);
            }
            if (event.key === "ArrowUp" || event.key === "ArrowLeft") {
                event.preventDefault();
                return moveActive(-1);
            }
            if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                return commit(state.activeIndex);
            }
            return;
        }
        const select = selectFromEvent(event);
        if (select && eligible(select) && ["Enter", " ", "F4"].includes(event.key)) {
            event.preventDefault();
            open(select);
        }
    }

    //-------------------------------------------------------------------------
    // Event Listeners
    //-------------------------------------------------------------------------

    // Capture events before Chromium/Qt opens its native select popup.   
    window.addEventListener("mousedown", onMouseDown, { capture: true, passive: false });
    window.addEventListener("keydown", onKeyDown, { capture: true, passive: false });
    window.addEventListener("resize", () => close(false), true);
    window.addEventListener("blur", () => close(false), true);
    document.addEventListener("scroll", () => close(false), true);
    document.addEventListener("visibilitychange", () => document.hidden && close(false), true);
})();
