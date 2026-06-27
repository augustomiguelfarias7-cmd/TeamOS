# TeamOS Interface Plan

TeamOS will use a mobile interface inspired by Android's interaction model while keeping the browser-first TeamOS identity.

## Interface goals

- Provide a large, touch-first mobile shell.
- Keep search and web access at the center of the home screen.
- Include normal operating-system areas such as settings, battery, network, display, sound, privacy, assistant, and about.
- Use a top-right gear button on the home screen to open settings.
- Keep the internal system based on Linux while writing the interface in Android-style languages and structure.

## Home screen structure

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
│   YouTube  ChatGusto  GitHub │
│   Wiki     Mail       Pull   │
│                             │
│   ←        ○       □    ≡    │
└─────────────────────────────┘
```

## Settings access

Settings are opened through the gear button in the top-right corner of the home screen. This keeps settings visible like a normal operating system while preserving the search-first home layout.

## Settings sections

The first settings structure should include:

- About TeamOS
- Battery
- Network and Wi-Fi
- Display
- Sound
- Privacy and security
- ChatGusto assistant
- System

## Implementation direction

The interface starts as an Android-style shell blueprint:

```text
interface/
├── src/main/kotlin/teamos/ui/
│   └── TeamOsShell.kt
└── src/main/res/
    ├── layout/
    │   ├── home_screen.xml
    │   └── settings_screen.xml
    └── values/
        └── strings.xml
```

This gives the project a real UI structure without pretending the Linux-based OS internals are already complete.
