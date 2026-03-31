← [Indice](../../README.md) | [← Plugin](../plugin.md)

# Claude HUD

| Campo | Valore |
|-------|--------|
| **Repo** | https://github.com/jarrodwatts/claude-hud |
| **Autore** | Jarrod Watts (@jarrodwatts) |
| **Licenza** | MIT |
| **Stelle** | ~15.7k |
| **Piattaforme** | Claude Code (v1.0.80+) |

## Cos'è

Claude HUD è un plugin che aggiunge un'**interfaccia visiva nella riga di stato del terminale**, sempre visibile sotto l'input dell'utente. Mostra in tempo reale: utilizzo del contesto, strumenti attivi, agenti in esecuzione, progresso dei task, stato git e limiti di utilizzo dell'abbonamento.

## Installazione

```bash
# 1. Aggiungere il marketplace
/plugin marketplace add jarrodwatts/claude-hud

# 2. Installare il plugin
/plugin install claude-hud

# 3. Configurare la statusline
/claude-hud:setup
```

Dopo il setup, riavviare completamente Claude Code.

> **Linux**: se `/tmp` è un filesystem separato, impostare prima `mkdir -p ~/.cache/tmp && TMPDIR=~/.cache/tmp claude`
>
> **Windows**: se manca un runtime JS, installare Node.js LTS con `winget install OpenJS.NodeJS.LTS`

## Requisiti

- Claude Code v1.0.80+
- Node.js 18+ o Bun

## Cosa mostra

### Layout predefinito (2 righe)

```
[Opus] │ my-project git:(main*)
Context █████░░░░░ 45% │ Usage ██░░░░░░░░ 25% (1h 30m / 5h)
```

- **Riga 1**: modello, provider (Bedrock/API), percorso progetto, branch git
- **Riga 2**: barra contesto (verde → giallo → rosso) e limiti utilizzo

### Linee opzionali (disabilitate di default)

```
◐ Edit: auth.ts | ✓ Read ×3 | ✓ Grep ×2        ← Attività strumenti
◐ explore [haiku]: Finding auth code (2m 15s)    ← Stato agenti
▸ Fix authentication bug (2/5)                    ← Progresso todo
```

L'aggiornamento avviene ogni ~300ms. I dati sul contesto sono token nativi di Claude Code (non stimati), con supporto fino a 1M di contesto.

## Configurazione

### Configurazione guidata

```bash
/claude-hud:configure
```

Avvia un flusso interattivo per scegliere un preset e regolare i singoli elementi.

### Preset disponibili

| Preset | Descrizione |
|--------|-------------|
| **Full** | Tutti gli elementi abilitati (strumenti, agenti, todo, git, utilizzo, durata) |
| **Essential** | Attività + stato git, minimo rumore visivo |
| **Minimal** | Solo modello e barra contesto |

### Opzioni principali

| Opzione | Default | Descrizione |
|---------|---------|-------------|
| `display.showModel` | true | Nome modello `[Opus]` |
| `display.showContextBar` | true | Barra visuale contesto |
| `display.showTools` | false | Attività strumenti |
| `display.showAgents` | false | Stato agenti |
| `display.showTodos` | false | Progresso todo |
| `display.showDuration` | false | Durata sessione |
| `display.showUsage` | true | Limiti utilizzo abbonamento |
| `display.showMemoryUsage` | false | RAM approssimativa |
| `gitStatus.enabled` | true | Branch git |
| `gitStatus.showDirty` | true | `*` per cambiamenti non committed |
| `gitStatus.showAheadBehind` | false | `↑N ↓N` per commits ahead/behind |

Il file di configurazione manuale si trova in `~/.claude/plugins/claude-hud/config.json`.

## Note e limitazioni

- **Usage**: visibile solo per abbonati Claude (Pro/Max), non per utenti API-only
- **Memory usage**: mostra RAM approssimativa della macchina, non l'uso preciso di Claude Code
- **Git status**: funziona solo dentro repository git
- **Strumenti/agenti/todo**: disabilitati di default, vanno abilitati nella configurazione
- Quando il contesto supera l'85% mostra un breakdown dettagliato dei token
