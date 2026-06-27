# TeamOS

TeamOS is a mobile, browser-first operating system concept built on top of the Linux kernel. The project focuses on creating the user-facing experience: a large Android-style interface, a search-centered home screen, Pull Search integration, normal system settings, and ChatGusto as the system assistant.

## Vision

TeamOS is designed around a simple idea: the phone starts at search, not at apps. Instead of a traditional app-store-first launcher, TeamOS uses a home screen with a stylish wallpaper, a search/address bar, recent or pinned websites, and a settings gear for normal operating-system controls.

Core principles:

- **Linux-powered base**: TeamOS uses Linux for the kernel, drivers, processes, networking, filesystem, and low-level system behavior.
- **Android-style interface layer**: the interface is planned around Android-style languages and structure, starting with Kotlin and XML-style layouts.
- **Browser-first shell**: the main user experience is a browser-like system shell.
- **Search-first home**: the initial screen centers on search and direct website access.
- **Settings like a normal OS**: a top-right gear opens settings for about, battery, network, display, sound, privacy, assistant, and system controls.
- **No traditional app store**: websites, tabs, sessions, and pinned/recent pages replace classic mobile apps in the initial design.
- **Pull Search integration**: searches are routed through Pull Search by default.
- **ChatGusto assistant**: ChatGusto is the official assistant, planned to open quickly from the power-button triple press.
- **TeamOS Agent Mode**: ChatGusto may request controlled system-agent permissions through TeamOS security prompts, scanner checks, and user approval.

## Login flow

The first TeamOS account flow is intentionally simple:

```text
e-mail -> hello by e-mail name -> create local PIN -> home
```

The user enters an e-mail address, TeamOS greets the user by a display name derived from that e-mail, then the user creates a numeric local PIN before reaching the home screen.

## Planned home screen

```text
┌─────────────────────────────┐
│  12:45              WiFi 86% │
│                         ⚙   │
│                             │
│      pesquise quanto quiser │
│                             │
│   ┌─────────────────────┐   │
│   │ Pesquisar ou acessar │   │
│   └─────────────────────┘   │
│                             │
│   Sites recentes             │
│                             │
│   ┌─────┐ ┌─────┐ ┌─────┐   │
│   │ YT  │ │ GPT │ │ Git │   │
│   │Tube │ │Chat │ │Hub  │   │
│   └─────┘ └─────┘ └─────┘   │
│                             │
│   ┌─────┐ ┌─────┐ ┌─────┐   │
│   │Wiki │ │Mail │ │Pull │   │
│   └─────┘ └─────┘ └─────┘   │
│                             │
│   ←        ○       □    ≡    │
└─────────────────────────────┘
```

## Search behavior

TeamOS uses Pull Search as the default search provider:

```text
https://pull-search.genmb.com/?q=%s#
```

If the user enters a normal query, TeamOS URL-encodes it and opens Pull Search. If the user enters a valid URL or domain, TeamOS opens that address directly.

## Interface structure

The first interface files live in `interface/`:

```text
interface/
├── README.md
└── src/main/
    ├── kotlin/teamos/ui/TeamOsShell.kt
    └── res/
        ├── layout/login_email_screen.xml
        ├── layout/login_greeting_screen.xml
        ├── layout/pin_creation_screen.xml
        ├── layout/home_screen.xml
        ├── layout/settings_screen.xml
        └── values/strings.xml
```

## Kernel and drivers

TeamOS does not copy the full Linux kernel or full driver source into this repository. Instead, it stores integration files that point to the Linux kernel baseline and describe the driver stacks TeamOS expects to import from Linux.

```text
kernel/
├── linux.toml
├── config/team_mobile.conf
└── patches/

drivers/
├── manifests/mobile.toml
├── wifi/
├── display/
├── input/
├── audio/
└── power/
```

The helper `tools/fetch_linux_kernel.sh` can fetch the configured Linux stable kernel into an external build directory when the project is ready to build kernel images.

## Internal system structure

The first internal TeamOS services live in `system/`:

```text
system/
├── README.md
└── teamos_internal/
    ├── agent_mode.py
    ├── login.py
    ├── models.py
    └── wifi.py
```

These files start the TeamOS internal layer for Agent Mode security review and Linux Wi-Fi integration through NetworkManager. The goal is to import the heavy internal behavior from Linux while implementing TeamOS-specific control, permission, and interface glue in this repository.

## Project status

TeamOS is in the early interface scaffolding phase. The current repository documents the system vision and starts the Android-style interface structure.
