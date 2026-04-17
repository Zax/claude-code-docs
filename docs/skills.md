← [Indice](../README.md) | [← Plugin](plugin.md)

# Skill

Le skill sono istruzioni modulari che estendono le capacità di Claude Code. Seguono lo standard aperto **Agent Skills** (adottato anche da OpenAI, GitHub Copilot, Cursor, Figma) e funzionano con un meccanismo di **progressive disclosure**: solo il nome e la descrizione (~100 token) vengono caricati all'avvio; il contenuto completo si carica solo quando la skill viene invocata.

## Dove si salvano

Le skill si possono definire a tre livelli:

| Livello | Percorso | Ambito |
|---------|----------|--------|
| Personale | `~/.claude/skills/<nome>/SKILL.md` | Tutti i progetti |
| Progetto | `.claude/skills/<nome>/SKILL.md` | Solo il progetto corrente |
| Enterprise | Managed settings | Tutta l'organizzazione |

Struttura tipica di una skill:

```
~/.claude/skills/my-skill/
├── SKILL.md              # Obbligatorio: frontmatter + istruzioni
├── scripts/              # Opzionale: script eseguibili
├── references/           # Opzionale: documentazione di supporto
└── assets/               # Opzionale: template, risorse
```

> **Nota**: il nome della cartella deve corrispondere al campo `name` nel frontmatter. Solo lettere minuscole, numeri e trattini (max 64 caratteri).

Claude Code rileva automaticamente le modifiche ai file skill senza dover riavviare la sessione. In monorepo, le skill vengono scoperte anche nelle sottodirectory (es. `packages/frontend/.claude/skills/`).

## Formato di SKILL.md

Il file è composto da frontmatter YAML + corpo markdown:

```yaml
---
name: explain-code
description: Spiega il codice con diagrammi e analogie. Usalo quando chiedi "come funziona questo codice?"
---

Quando spieghi del codice, includi sempre:

1. **Analogia**: paragona il codice a qualcosa di quotidiano
2. **Diagramma**: usa ASCII art per mostrare il flusso
3. **Walkthrough**: spiega passo per passo cosa succede
4. **Gotcha**: qual è l'errore comune o il malinteso tipico?
```

### Campi frontmatter obbligatori

| Campo | Descrizione |
|-------|-------------|
| `name` | Nome della skill (diventa il comando `/nome`). Solo minuscole, numeri, trattini. |
| `description` | Cosa fa e quando usarla (1-1024 caratteri). Claude lo usa per decidere se invocare la skill automaticamente. **Deve stare su una sola riga.** |

### Campi opzionali

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `when_to_use` | string | Contesto aggiuntivo su quando invocare la skill |
| `argument-hint` | string | Hint nell'autocomplete (es. `[issue-number]`) |
| `disable-model-invocation` | boolean | Se `true`, solo l'utente può invocarla (non Claude) |
| `user-invocable` | boolean | Se `false`, nasconde dal menu `/` (solo Claude la invoca) |
| `allowed-tools` | string/list | Tool permessi senza chiedere conferma (es. `Read Grep Bash(git *)`) |
| `model` | string | Modello da usare quando la skill è attiva |
| `effort` | string | Livello di effort: `low`, `medium`, `high`, `xhigh`, `max` |
| `context` | string | `fork` per eseguire in un subagent isolato |
| `agent` | string | Tipo di subagent: `Explore`, `Plan`, `general-purpose` |
| `paths` | string/list | Glob pattern per limitare quando la skill si attiva (es. `src/**/*.ts`) |

### Variabili disponibili nel contenuto

| Variabile | Descrizione |
|-----------|-------------|
| `$ARGUMENTS` | Tutti gli argomenti passati all'invocazione |
| `$0`, `$1`, `$2`... | Argomento specifico per indice |
| `${CLAUDE_SESSION_ID}` | ID della sessione corrente |
| `${CLAUDE_SKILL_DIR}` | Directory della skill |

### Comandi shell dinamici

Con la sintassi `` !`<comando>` `` si possono eseguire comandi shell il cui output viene iniettato nel contenuto della skill prima di inviarlo a Claude (preprocessing, non esecuzione da parte di Claude).

## Come si invocano

**Manualmente**: digitare `/nome-skill` nella chat, con argomenti opzionali (es. `/fix-issue 123`). Il menu autocomplete mostra tutte le skill disponibili.

**Automaticamente**: Claude può invocare una skill quando la richiesta corrisponde alla sua `description`, senza che l'utente la chiami esplicitamente.

### Controllare chi invoca

| Configurazione | Effetto |
|----------------|---------|
| Default | Sia l'utente che Claude possono invocare |
| `disable-model-invocation: true` | Solo l'utente (utile per `/deploy`, `/commit`) |
| `user-invocable: false` | Solo Claude (conoscenza di background, non un comando) |

## Skill built-in vs custom

Claude Code include alcune skill predefinite:

| Skill | Descrizione |
|-------|-------------|
| `/simplify` | Rivede il codice per qualità, riuso ed efficienza |
| `/loop` | Esegue un prompt/comando a intervalli regolari |
| `/claude-api` | Aiuto per costruire app con Claude API |

> **Differenza con i comandi**: comandi come `/help`, `/compact`, `/clear` sono logica integrata nel CLI. Le skill sono basate su prompt e Claude le orchestra usando i tool disponibili.

> **Legacy**: i file in `.claude/commands/` continuano a funzionare ma le skill sono preferite perché supportano frontmatter, file di supporto e invocazione automatica.

## Gestione del contesto

- Le descrizioni delle skill condividono un budget di contesto (1% della finestra, minimo 8.000 caratteri)
- Quando ci sono molte skill, le descrizioni vengono accorciate automaticamente
- Il contenuto completo di una skill, una volta invocata, resta nella conversazione per il resto della sessione
- Durante la compattazione automatica, le prime 5.000 token per skill vengono preservate (max 25.000 token totali tra tutte le skill)
- Per aumentare il budget: variabile d'ambiente `SLASH_COMMAND_TOOL_CHAR_BUDGET`

## Skill documentate

| Skill | Descrizione |
|-------|-------------|
| [Claude Config Audit](fonti-esterne/claude-config-audit.md) | Audit sistematico della configurazione Claude: MCP duplicati, plugin inutilizzati, conflitti, spreco token e RAM |

## Risorse

- [Documentazione ufficiale](https://code.claude.com/docs/en/skills)
- [Agent Skills Specification](https://agentskills.io/specification)
- [Repository skill ufficiali Anthropic](https://github.com/anthropics/skills)
- [Awesome Claude Skills](https://github.com/travisvn/awesome-claude-skills) (community)

---

[← Plugin](plugin.md)
