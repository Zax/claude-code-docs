← [Indice](../README.md) | [← Stato del Servizio](status.md)

# Plugin

I plugin sono pacchetti di componenti che estendono Claude Code con skill, agent, hook, server MCP, server LSP e monitor. Si distribuiscono tramite marketplace e si installano con un comando.

## Plugin vs configurazione standalone

| Approccio | Nomi skill | Ideale per |
|-----------|------------|------------|
| **Standalone** (`.claude/`) | `/hello` | Workflow personali, personalizzazioni progetto, esperimenti |
| **Plugin** (con `.claude-plugin/plugin.json`) | `/plugin-name:hello` | Condivisione team/community, versioning, riuso tra progetti |

> **Consiglio**: parti con configurazione standalone in `.claude/` per iterare velocemente, poi converti in plugin quando vuoi condividere.

## Struttura di un plugin

```
my-plugin/
├── .claude-plugin/           # Metadati (opzionale)
│   └── plugin.json             # Manifest del plugin
├── skills/                   # Skill come <nome>/SKILL.md
├── commands/                 # Skill come file .md piatti (legacy)
├── agents/                   # Definizioni subagent
├── hooks/                    # Hook in hooks.json
│   └── hooks.json
├── monitors/                 # Monitor in background
│   └── monitors.json
├── output-styles/            # Stili di output personalizzati
├── bin/                      # Eseguibili aggiunti al PATH del tool Bash
├── scripts/                  # Script di utilità per hook e altro
├── .mcp.json                 # Server MCP
├── .lsp.json                 # Server LSP
└── settings.json             # Impostazioni default del plugin
```

> **Errore comune**: non mettere `skills/`, `agents/`, `hooks/` dentro `.claude-plugin/`. Solo `plugin.json` va li. Tutto il resto alla root del plugin.

### Manifest (`plugin.json`)

Il manifest è opzionale. Se omesso, Claude Code scopre i componenti nelle posizioni default e usa il nome della directory.

```json
{
  "name": "my-plugin",
  "description": "Descrizione del plugin",
  "version": "1.0.0",
  "author": { "name": "Nome Autore" },
  "homepage": "https://docs.example.com",
  "repository": "https://github.com/user/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"]
}
```

Il campo `name` è l'unico obbligatorio e definisce il namespace delle skill (es. `/my-plugin:hello`).

### Versioning

Formato **semver** `MAJOR.MINOR.PATCH`. Claude Code usa la versione per decidere se aggiornare: se cambi il codice senza incrementare la versione, gli utenti non vedranno le modifiche.

## Installazione e gestione

### Marketplace

Un marketplace è un catalogo di plugin. Il marketplace **ufficiale Anthropic** (`claude-plugins-official`) è disponibile automaticamente.

```bash
# Installare un plugin dal marketplace ufficiale
/plugin install github@claude-plugins-official

# Aggiungere un marketplace custom
/plugin marketplace add owner/repo                     # GitHub
/plugin marketplace add https://gitlab.com/org/repo.git  # Git URL
/plugin marketplace add ./my-marketplace               # Locale

# Aggiornare il catalogo
/plugin marketplace update marketplace-name

# Rimuovere un marketplace (rimuove anche i plugin installati da esso)
/plugin marketplace remove marketplace-name
```

### Installare, aggiornare, gestire

```bash
# Installare (default: scope user)
/plugin install plugin-name@marketplace-name

# Con scope specifico
claude plugin install formatter@my-marketplace --scope project

# Aggiornare
/plugin update plugin-name

# Disabilitare senza rimuovere
/plugin disable plugin-name@marketplace-name

# Riabilitare
/plugin enable plugin-name@marketplace-name

# Rimuovere completamente
/plugin uninstall plugin-name@marketplace-name

# Ricaricare dopo modifiche (senza riavviare)
/reload-plugins
```

### Scope di installazione

| Scope | File settings | Effetto |
|-------|---------------|---------|
| `user` (default) | `~/.claude/settings.json` | Personale, tutti i progetti |
| `project` | `.claude/settings.json` | Condiviso via version control |
| `local` | `.claude/settings.local.json` | Solo per te, in questo progetto (gitignored) |
| `managed` | Managed settings | Installato dall'admin, read-only |

### Auto-update

Il marketplace ufficiale ha l'auto-update abilitato di default. Per i marketplace custom è disabilitato. Si gestisce dal menu `/plugin` → **Marketplaces**.

Per disabilitare tutti gli aggiornamenti: `DISABLE_AUTOUPDATER=1`. Per mantenere solo gli aggiornamenti plugin: `FORCE_AUTOUPDATE_PLUGINS=1`.

### Interfaccia interattiva

`/plugin` apre un'interfaccia con 4 tab navigabili con Tab/Shift+Tab:

- **Discover**: sfoglia i plugin disponibili
- **Installed**: gestisci plugin installati (premi `f` per preferiti)
- **Marketplaces**: aggiungi, aggiorna, rimuovi marketplace
- **Errors**: errori di caricamento plugin

## Componenti di un plugin

### Skill

Le skill del plugin seguono lo stesso formato delle skill standalone (vedi [Skill](skills.md)) ma sono namespaced: `/plugin-name:skill-name`.

### Agent

Subagent specializzati in `agents/` come file markdown con frontmatter:

```yaml
---
name: security-reviewer
description: Rivede il codice per vulnerabilità di sicurezza
model: sonnet
effort: medium
maxTurns: 20
disallowedTools: Write, Edit
---

Prompt di sistema dell'agent...
```

Campi supportati: `name`, `description`, `model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, `memory`, `background`, `isolation` (solo `"worktree"`).

Un plugin può impostare un agent come thread principale tramite `settings.json`:

```json
{ "agent": "security-reviewer" }
```

### Hook

Gestori di eventi in `hooks/hooks.json`. Stessi eventi della configurazione standalone:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{ "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh" }]
      }
    ]
  }
}
```

**Tipi di hook**: `command` (shell), `http` (POST a URL), `prompt` (valutazione LLM), `agent` (verifica agentica).

**Eventi principali**: `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`, `Stop`, `PreCompact`, `PostCompact`, `SubagentStart`, `SubagentStop`, `TaskCreated`, `TaskCompleted`, `FileChanged`, `CwdChanged`, `ConfigChange`, e altri.

### Server MCP

Server MCP bundled in `.mcp.json`:

```json
{
  "mcpServers": {
    "plugin-api": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
    }
  }
}
```

Si avviano automaticamente quando il plugin è abilitato.

### Server LSP (Code Intelligence)

I plugin LSP danno a Claude **intelligence sul codice in tempo reale**:

- **Diagnostica automatica**: dopo ogni modifica, il language server analizza e riporta errori/warning. Claude vede type error, import mancanti, errori di sintassi senza compilare
- **Navigazione codice**: go to definition, find references, hover info, list symbols

Configurazione in `.lsp.json`:

```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": { ".go": "go" }
  }
}
```

> Il binario del language server va installato separatamente. Il plugin configura solo la connessione.

**Plugin LSP disponibili nel marketplace ufficiale**:

| Linguaggio | Plugin | Binario richiesto |
|-----------|--------|-------------------|
| C/C++ | `clangd-lsp` | `clangd` |
| C# | `csharp-lsp` | `csharp-ls` |
| Go | `gopls-lsp` | `gopls` |
| Java | `jdtls-lsp` | `jdtls` |
| Kotlin | `kotlin-lsp` | `kotlin-language-server` |
| Lua | `lua-lsp` | `lua-language-server` |
| PHP | `php-lsp` | `intelephense` |
| Python | `pyright-lsp` | `pyright-langserver` |
| Rust | `rust-analyzer-lsp` | `rust-analyzer` |
| Swift | `swift-lsp` | `sourcekit-lsp` |
| TypeScript | `typescript-lsp` | `typescript-language-server` |

### Monitor

Processi in background che osservano log, file o stati esterni e notificano Claude ad ogni riga stdout:

```json
[
  {
    "name": "error-log",
    "command": "tail -F ./logs/error.log",
    "description": "Application error log",
    "when": "always"
  }
]
```

Il campo `when` controlla quando parte: `"always"` (default, all'avvio sessione) o `"on-skill-invoke:<nome-skill>"` (alla prima invocazione della skill).

### Directory `bin/`

File eseguibili in `bin/` vengono aggiunti al `PATH` del tool Bash quando il plugin è attivo. Utile per rendere disponibili comandi custom senza path assoluti.

## Plugin nel marketplace ufficiale

### Integrazioni esterne

| Plugin | Servizio |
|--------|----------|
| `github` | GitHub |
| `gitlab` | GitLab |
| `atlassian` | Jira / Confluence |
| `asana` | Asana |
| `linear` | Linear |
| `notion` | Notion |
| `figma` | Figma |
| `vercel` | Vercel |
| `firebase` | Firebase |
| `supabase` | Supabase |
| `slack` | Slack |
| `sentry` | Sentry |

### Workflow di sviluppo

| Plugin | Descrizione |
|--------|-------------|
| `commit-commands` | Workflow git: commit, push, PR |
| `pr-review-toolkit` | Agent specializzati per review PR |
| `agent-sdk-dev` | Strumenti per sviluppo con Agent SDK |
| `plugin-dev` | Toolkit per creare plugin |

### Stili di output

| Plugin | Descrizione |
|--------|-------------|
| `explanatory-output-style` | Insight educativi sulle scelte implementative |
| `learning-output-style` | Modalità apprendimento interattivo |

## Variabili d'ambiente

Due variabili disponibili ovunque nel plugin (skill, hook, MCP, LSP, monitor):

| Variabile | Descrizione |
|-----------|-------------|
| `${CLAUDE_PLUGIN_ROOT}` | Path assoluto della directory di installazione del plugin. Cambia ad ogni update. |
| `${CLAUDE_PLUGIN_DATA}` | Directory persistente per dati del plugin che sopravvivono agli aggiornamenti (`~/.claude/plugins/data/{id}/`) |

### User config

Il campo `userConfig` nel manifest permette di chiedere valori all'utente quando il plugin è abilitato:

```json
{
  "userConfig": {
    "api_endpoint": { "description": "API endpoint", "sensitive": false },
    "api_token": { "description": "Token di autenticazione", "sensitive": true }
  }
}
```

I valori sono disponibili come `${user_config.KEY}` nelle configurazioni e come `CLAUDE_PLUGIN_OPTION_<KEY>` nelle variabili d'ambiente. I valori sensibili vanno nel keychain di sistema.

## Sviluppo e testing

```bash
# Testare un plugin locale senza installarlo
claude --plugin-dir ./my-plugin

# Caricare più plugin contemporaneamente
claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two

# Debug dettagliato del caricamento
claude --debug

# Validare manifest e componenti
/plugin validate

# Ricaricare dopo modifiche
/reload-plugins
```

### Convertire configurazione standalone in plugin

1. Creare la struttura: `mkdir -p my-plugin/.claude-plugin`
2. Creare `plugin.json` con nome e descrizione
3. Copiare `skills/`, `agents/`, `commands/` dalla `.claude/` del progetto
4. Migrare gli hook da `settings.json` a `hooks/hooks.json`
5. Testare con `claude --plugin-dir ./my-plugin`

### Sottomettere al marketplace ufficiale

- **Claude.ai**: [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)
- **Console**: [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)

## Plugin documentati

| Plugin | Descrizione |
|--------|-------------|
| [Superpowers](plugin/superpowers.md) | Framework agentico con skill per TDD, debugging sistematico, pianificazione e code review |
| [Claude-Mem](plugin/claude-mem.md) | Memoria persistente tra sessioni con compressione AI e ricerca semantica |
| [Claude HUD](plugin/claude-hud.md) | Dashboard visiva nel terminale: contesto, strumenti, agenti, git, usage |

## Risorse

- [Documentazione ufficiale — Creare plugin](https://code.claude.com/docs/en/plugins)
- [Documentazione ufficiale — Scoprire e installare plugin](https://code.claude.com/docs/en/discover-plugins)
- [Documentazione ufficiale — Reference tecnico](https://code.claude.com/docs/en/plugins-reference)
- [Documentazione ufficiale — Marketplace](https://code.claude.com/docs/en/plugin-marketplaces)
- [Catalogo plugin ufficiale](https://claude.com/plugins)

---

[← Link Utili](link-utili.md) | [Successivo: Skill →](skills.md)
