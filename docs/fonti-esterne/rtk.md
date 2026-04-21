← [Indice](../../README.md)

# Analisi: RTK (Rust Token Killer)

| Campo | Valore |
|-------|--------|
| **Sito** | https://www.rtk-ai.app/ |
| **Repo** | https://github.com/rtk-ai/rtk |
| **Stelle** | ~31.355 |
| **Fork** | ~1.831 |
| **Licenza** | Apache 2.0 |
| **Linguaggio** | Rust (~92%) |
| **Versione** | v0.15.2 |
| **Data analisi** | 21 aprile 2026 |

## Descrizione

RTK è un proxy CLI ad alte prestazioni scritto in Rust che comprime l'output dei comandi shell prima che raggiungano la context window degli assistenti AI. Singolo binario, zero dipendenze, ~10ms di overhead per comando. Riduzione media dichiarata: 60-90% dei token, con picchi fino al 99% su output molto verbosi (es. `cargo test`).

## Come funziona

1. Intercetta i comandi CLI tramite hook trasparente
2. Applica filtri contestuali: rimozione rumore, raggruppamento intelligente, troncamento, deduplicazione
3. Restituisce output compresso all'agent AI
4. L'agent riceve meno rumore e contesto più rilevante

Il meccanismo chiave è l'**auto-rewrite hook**: dopo `rtk init -g`, un hook PreToolUse riscrive automaticamente i comandi idonei come `rtk <comando>` prima dell'esecuzione, garantendo adozione al 100% senza overhead di token.

**Nota**: l'hook intercetta solo le chiamate Bash. I tool built-in di Claude Code (`Read`, `Grep`, `Glob`) non vengono intercettati — per quelli serve usare esplicitamente `rtk` o gli equivalenti shell.

## Comandi supportati (100+)

### Operazioni file
`ls`, `read`, `find`, `grep`, `diff`, `smart` (code summary), `cat`, `head`, `tail`

### Version control
`git status`, `git log`, `git diff`, `git add`, `git commit`, `git push`, `git pull`

### GitHub
`gh pr list`, `gh pr view`, `gh issue list`, `gh run list`

### Testing
`jest`, `vitest`, `playwright`, `pytest`, `go test`, `cargo test`, `rake test`, `rspec`

### Build e linting
`eslint`, `biome`, `tsc`, `next build`, `prettier`, `cargo build`, `cargo clippy`, `ruff`, `golangci-lint`, `rubocop`

### Package manager
`pnpm list`, `pip list`, `pip outdated`, `bundle install`, `prisma generate`

### Container e orchestrazione
`docker ps`, `docker images`, `docker logs`, `docker compose`, `kubectl pods`, `kubectl logs`, `kubectl services`

### AWS
EC2, Lambda, CloudFormation, DynamoDB, IAM, S3, logs, STS

## Esempio di risparmio token (sessione 30 min)

| Operazione | Frequenza | Standard | Con RTK | Risparmio |
|------------|-----------|----------|---------|-----------|
| `ls`/`tree` | 10x | 2.000 | 400 | -80% |
| `cat`/`read` | 20x | 40.000 | 12.000 | -70% |
| `grep`/`rg` | 8x | 16.000 | 3.200 | -80% |
| `git status` | 10x | 3.000 | 600 | -80% |
| `git diff` | 5x | 10.000 | 2.500 | -75% |
| `cargo test` | 5x | 25.000 | 2.500 | -90% |
| **Totale** | | **~118.000** | **~23.900** | **-80%** |

## Comandi meta (analytics)

- `rtk gain` — statistiche di risparmio (token totali, percentuale, comandi processati)
- `rtk gain --graph` — visualizzazione ASCII a 30 giorni
- `rtk gain --history` — storico comandi con risparmi
- `rtk discover` — analizza la cronologia Claude Code per opportunità di ottimizzazione mancate
- `rtk session` — tracking di adozione
- `rtk proxy <cmd>` — esecuzione raw senza filtri (per debugging)

## Installazione

```bash
# Metodi (sceglierne uno)
brew install rtk
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh
cargo install --git https://github.com/rtk-ai/rtk

# Attivazione hook automatico
rtk init -g                    # Claude Code / GitHub Copilot
rtk init -g --gemini           # Gemini CLI
rtk init -g --codex            # OpenAI Codex
rtk init -g --agent cursor     # Cursor
rtk init --agent windsurf      # Windsurf
rtk init --agent cline         # Cline / Roo Code
```

## Compatibilità

| Tool AI | Comando | Metodo |
|---------|---------|--------|
| Claude Code | `rtk init -g` | PreToolUse hook (bash) |
| GitHub Copilot (VS Code) | `rtk init -g --copilot` | Transparent rewrite |
| Cursor | `rtk init -g --agent cursor` | hooks.json preToolUse |
| Gemini CLI | `rtk init -g --gemini` | BeforeTool hook |
| Windsurf | `rtk init --agent windsurf` | .windsurfrules |
| Cline / Roo Code | `rtk init --agent cline` | .clinerules |
| OpenCode | `rtk init -g --opencode` | Plugin TypeScript |

**OS**: macOS, Linux, WSL (supporto Windows nativo limitato: filtri funzionano, hook no)

## Confronto con lean-ctx

| Aspetto | RTK | lean-ctx |
|---------|-----|----------|
| **Approccio** | Proxy CLI (solo shell hook) | Shell hook + MCP Server (42 tool) |
| **Stelle** | ~31.355 | ~727 |
| **Focus** | Compressione output comandi | Compressione + caching + memoria |
| **Integrazione** | Hook PreToolUse (solo Bash) | Hook + MCP nativo |
| **Tool aggiuntivi** | No (solo compressione) | Sì (lettura intelligente, delta, knowledge) |
| **Maturità** | Più maturo (gen 2026, ampia adozione) | Più giovane (mar 2026) |
| **Complessità** | Minimale, fa una cosa sola | Più ricco ma più complesso |

RTK è più focalizzato e leggero: fa una sola cosa (comprimere output CLI) e la fa bene. lean-ctx è più ambizioso, con MCP server, tool intelligenti e memoria cross-sessione.

## Rilevanza per Claude Code

- **Impatto diretto**: comprime l'output dei comandi Bash prima che entrino nella context window, riducendo il consumo di token del piano
- **Integrazione nativa**: hook PreToolUse dedicato per Claude Code (`rtk init -g`)
- **Zero friction**: dopo l'init, la compressione è completamente trasparente
- **Analytics utili**: `rtk gain` e `rtk discover` permettono di monitorare e ottimizzare il risparmio
- **Complementare ad altri approcci**: combinabile con `claude-token-efficient` (riduce verbosità output Claude) e con il caching MCP di lean-ctx

## Valutazione

**Punti di forza:**
- Progetto molto popolare e attivo (31k+ stelle, aggiornato quotidianamente)
- Filosofia Unix: fa una cosa sola, la fa bene
- Overhead minimo (~10ms per comando)
- 100+ comandi supportati con filtri specifici
- Installazione e attivazione semplicissime

**Aspetti da considerare:**
- Non intercetta i tool built-in di Claude Code (Read, Grep, Glob) — solo Bash
- Non offre caching o memoria, solo compressione stateless
- Molte issue aperte (648) per un progetto relativamente giovane
- Il risparmio su piani flat-rate (non pay-per-token) è indiretto: più contesto disponibile per sessione
