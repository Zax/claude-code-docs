← [Indice](../../README.md) | [← Plugin](../plugin.md)

# Superpowers

| Campo | Valore |
|-------|--------|
| **Repo** | https://github.com/obra/superpowers |
| **Autore** | Jesse Vincent (Prime Radiant) |
| **Licenza** | MIT |
| **Stelle** | ~128k |
| **Piattaforme** | Claude Code, Cursor, Codex, OpenCode, Gemini CLI |

## Cos'è

Superpowers è un framework agentico che fornisce un flusso di lavoro completo per agenti di codifica. È costruito su un insieme di **skill componibili** che automatizzano metodologie di sviluppo software.

La filosofia di fondo: l'agente non salta direttamente alla codifica, ma segue un processo strutturato — chiede chiarimenti, presenta il design, crea un piano di implementazione e applica TDD rigoroso.

## Installazione

**Claude Code (Official Marketplace):**
```bash
/plugin install superpowers@claude-plugins-official
```

**Claude Code (Custom Marketplace):**
```bash
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

**Cursor:**
```
/add-plugin superpowers
```

**Aggiornamento:**
```bash
/plugin update superpowers
```

## Come funziona

Le skill si attivano automaticamente quando Claude rileva determinati contesti (es. "aiutami a pianificare questa feature"). Non serve configurazione manuale post-installazione.

Il workflow tipico:
1. L'agente chiede chiarimenti prima di procedere
2. Presenta il design in sezioni leggibili per validazione
3. Crea un piano di implementazione dettagliato
4. Avvia lo sviluppo guidato da subagenti con revisioni automatiche
5. Applica TDD (Test-Driven Development) rigoroso

## Skill disponibili

### Testing
- **test-driven-development** — Ciclo RED-GREEN-REFACTOR automatizzato

### Debugging
- **systematic-debugging** — Processo a 4 fasi per root cause analysis
- **verification-before-completion** — Verifica che il problema sia effettivamente risolto prima di dichiarare "fatto"

### Collaborazione e pianificazione
- **brainstorming** — Raffinamento del design con approccio socratico
- **writing-plans** — Piani di implementazione dettagliati
- **executing-plans** — Esecuzione in batch con checkpoint
- **dispatching-parallel-agents** — Flussi paralleli di subagenti
- **requesting-code-review** e **receiving-code-review** — Review del codice strutturate

### Git workflow
- **using-git-worktrees** — Branch di sviluppo paralleli isolati
- **finishing-a-development-branch** — Workflow decisionale per merge/PR
- **subagent-driven-development** — Revisione a due stadi (conformità spec + qualità codice)

### Meta
- **writing-skills** — Creazione di nuove skill personalizzate
- **using-superpowers** — Introduzione al sistema

## Principi guida

- **Test-Driven Development**: test prima di tutto
- **Approccio sistematico** rispetto ad ad-hoc
- **Riduzione della complessità**: soluzioni semplici
- **Evidenza empirica**: verificare sempre con dati concreti

## Risorse

- Discord: https://discord.gg/Jd8Vphy9jq
- Issues: https://github.com/obra/superpowers/issues
