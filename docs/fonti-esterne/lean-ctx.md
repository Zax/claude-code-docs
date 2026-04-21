← [Indice](../../README.md)

# Analisi: lean-ctx

| Campo | Valore |
|-------|--------|
| **Repo** | https://github.com/yvgude/lean-ctx |
| **Autore** | yvgude |
| **Stelle** | ~727 |
| **Licenza** | Apache 2.0 + MIT |
| **Linguaggio** | Rust (~91%) |
| **Data analisi** | 21 aprile 2026 |

## Descrizione

MCP Server e shell hook open-source scritto in Rust, progettato per ridurre il consumo di token degli strumenti di coding AI fino al 99%. Singolo binario, zero telemetria, compatibile con Claude Code, Cursor, GitHub Copilot, Windsurf, Gemini CLI e oltre 24 altri tool.

## Tre strategie di risparmio token

1. **Shell Hook**: comprime trasparentemente l'output dei comandi CLI (90+ pattern supportati) prima che arrivi all'LLM. Risparmio stimato: 60-95%
2. **Context Server (MCP)**: 42 tool MCP con caching, 10 modalità di lettura file e compressione adattiva. Risparmio stimato: 74-99%
3. **AI Tool Hooks**: integrazione one-command via `lean-ctx init --agent <tool>`

## Tool principali (42 totali)

### Core
- `ctx_read` — lettura file con 8 modalità (full, map, signatures, diff, aggressive, lines...)
- `ctx_multi_read` — lettura multipla in una singola richiesta
- `ctx_tree` — listing directory
- `ctx_shell` — comandi shell con compressione output
- `ctx_search` — ricerca nel codice
- `ctx_compress` — checkpoint conversazioni lunghe (90-99% risparmio)

### Intelligenza
- `ctx_smart_read` — selezione automatica della modalità di lettura ottimale
- `ctx_delta` — aggiornamenti incrementali via Myers diff
- `ctx_dedup` — deduplicazione cross-file
- `ctx_intent` — rilevamento semantico dell'intento
- `ctx_graph` — analisi dipendenze del progetto

### Memoria e multi-agente
- `ctx_session` — memoria cross-sessione
- `ctx_knowledge` — knowledge persistente del progetto
- `ctx_agent` — coordinamento multi-agente
- `ctx_task` — orchestrazione task A2A

## Modalità di lettura file (`ctx_read`)

| Modalità | Caso d'uso | Costo token |
|----------|-----------|-------------|
| `full` | File da editare (cached ~13 token) | 100% prima lettura, ~0% cached |
| `map` | Comprensione API | ~5-15% |
| `signatures` | Dettaglio superficie API | ~10-20% |
| `diff` | File modificati | Solo righe cambiate |
| `aggressive` | File grandi con boilerplate | ~30-50% |
| `lines:N-M` | Range specifici | Proporzionale |

## Protocolli di intelligenza

- **CEP** (Cognitive Efficiency Protocol) — comunicazione adattiva LLM con scoring di compliance
- **CCP** (Context Continuity Protocol) — memoria cross-sessione con posizionamento LITM-aware (-99.2% token cold-start)
- **TDD** (Token Dense Dialect) — shorthand a simboli e mapping identificatori (8-25% risparmio extra)

## Installazione

```bash
# Metodi di installazione (sceglierne uno)
curl -fsSL https://leanctx.com/install.sh | sh
brew tap yvgude/lean-ctx && brew install lean-ctx
npm install -g lean-ctx-bin
cargo install lean-ctx

# Setup e verifica
lean-ctx setup
lean-ctx doctor
```

## Shell Hook: comandi supportati

Dopo `lean-ctx init --global`, 23 comandi vengono automaticamente aliasati con compressione:
`git`, `npm`, `pnpm`, `yarn`, `cargo`, `docker`, `docker-compose`, `kubectl`, `gh`, `pip`, `ruff`, `go`, `eslint`, `prettier`, `tsc`, `ls`, `find`, `grep`, `curl`, `wget` e altri.

Copertura totale: 34 categorie di comandi (Git 19, Docker 10, Kubernetes 8, test runner 8, npm/pnpm/yarn 6, ecc.).

## Compatibilità editor/tool AI

Rilevamento automatico via `lean-ctx setup`: Cursor, Claude Code, GitHub Copilot, Windsurf, VS Code, Zed, JetBrains, Continue, Cline, Aider, Amp, AWS Kiro e altri.

## Rilevanza per Claude Code

- **Risparmio token significativo**: la compressione dell'output CLI e il caching delle letture file possono ridurre sensibilmente i costi di utilizzo
- **Integrazione diretta**: `lean-ctx init --agent claude-code` configura automaticamente l'integrazione
- **MCP nativo**: funziona come MCP Server, il protocollo già supportato da Claude Code
- **Complementare a token-efficient**: mentre `claude-token-efficient` riduce la verbosità dell'*output* di Claude, `lean-ctx` comprime l'*input* (output dei tool) — i due approcci sono combinabili

## Valutazione

**Punti di forza:**
- Progetto molto attivo (1052+ commit, ultimo push recente)
- Singolo binario Rust, zero telemetria, nessuna dipendenza runtime
- Compressione trasparente senza cambiare il workflow
- 42 tool MCP con modalità di lettura intelligenti
- Ampia compatibilità (24+ editor/tool AI)

**Aspetti da considerare:**
- Progetto giovane (creato il 23 marzo 2026)
- Aggiunge un layer intermedio che potrebbe complicare il debugging
- Il risparmio effettivo dipende dal tipo di utilizzo
- Dimensione repo elevata (~427 MB)
