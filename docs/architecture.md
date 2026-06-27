# TeamOS Architecture

TeamOS is planned as a mobile operating system experience built on Linux. The project avoids writing a kernel from scratch and instead concentrates on the shell, browser-first workflow, assistant integration, and security model.

## High-level stack

```text
┌─────────────────────────────────────┐
│ TeamOS interface                     │
│ Home, navigation, tabs, recent sites │
├─────────────────────────────────────┤
│ Browser runtime                      │
│ Web pages, Pull Search, ChatGusto    │
├─────────────────────────────────────┤
│ TeamOS services                      │
│ agent guard, scanner, permissions    │
├─────────────────────────────────────┤
│ Linux userland                       │
│ networking, audio, display, power    │
├─────────────────────────────────────┤
│ Linux kernel                         │
│ drivers, memory, processes, devices  │
└─────────────────────────────────────┘
```

## Home screen

The TeamOS home screen is not a regular web page. It is the system shell. It contains:

- status information such as time, Wi-Fi, and battery;
- the slogan `pesquise quanto quiser`;
- a search/address bar;
- recent or pinned websites;
- navigation controls for back, home, tabs, and menu.

## Pull Search

Pull Search is the default search provider. The URL template is:

```text
https://pull-search.genmb.com/?q=%s#
```

The shell should detect whether user input is a URL/domain or a search query:

- URL/domain input opens directly in the browser runtime.
- Search input is URL-encoded and inserted into the Pull Search template.

## Recent sites instead of app store

TeamOS does not start with a traditional app store. The home screen acts as a launcher for websites through:

- recent sites;
- pinned sites;
- active tabs/sessions;
- browser history.

This keeps TeamOS aligned with a browser-first model while still feeling familiar to mobile users.

## ChatGusto assistant

ChatGusto is the official TeamOS assistant:

```text
https://chatgusto-ai.genmb.com
```

Planned activation:

```text
three quick power-button presses -> ChatGusto assistant panel
```

The assistant should open as a system panel or bottom sheet above the current screen, not merely as a normal browser tab.

## TeamOS Agent Mode

TeamOS should not expose broad system control to arbitrary websites. Instead, it should use a controlled Agent Mode flow:

```text
ChatGusto requests system access
↓
TeamOS detects the request
↓
TeamOS shows a security warning
↓
TeamOS runs scanner/security checks
↓
TeamOS shows requested permissions
↓
User allows or denies access
↓
ChatGusto becomes an approved agent only within granted limits
```

The security prompt should warn users that system access can be risky and may allow malicious behavior if the origin is not trusted.

Initial checks should include:

- trusted origin check for `https://chatgusto-ai.genmb.com`;
- HTTPS/certificate validation;
- requested permission review;
- suspicious behavior detection where possible.

Scanner results must not be presented as a perfect guarantee. They are an additional safety layer before explicit user consent.

## Initial Agent Mode permissions

The first TeamOS Agent Mode should be narrow and reversible. Possible early permissions:

- open a website;
- search with Pull Search;
- open TeamOS settings;
- read the current page title;
- read the current page URL.

Sensitive permissions such as files, camera, microphone, location, credentials, cookies, and system-wide changes should require separate explicit prompts or remain unsupported until the security model is mature.
