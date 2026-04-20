← [Indice](../../README.md)

# Analisi: Cambiamo Paradigma

| Campo | Valore |
|-------|--------|
| **Articolo** | https://pinperepette.github.io/signal.pirate/articoli/cambiamo-paradigma.html |
| **Autore** | Pinperepette (Andrea Amani) |
| **Sito** | Signal Pirate |
| **Data analisi** | 20 aprile 2026 |

## Descrizione

Analisi approfondita dell'architettura interna di Claude Code (512K righe TypeScript), presentata come caso studio dello stato dell'arte negli agent system. La tesi centrale: nel 2026 il valore non e piu nello scrivere codice ma nell'**orchestrazione di agenti autonomi**.

## Pattern architetturali analizzati

### 1. Pattern ReAct (Reason + Act)

Il cuore del loop agente: prepara contesto → chiama LLM → LLM risponde con testo e/o tool_use → esegui tool → valuta se continuare o terminare. Implementato come `AsyncGenerator` per streaming non bloccante (l'utente vede progressi mentre i tool girano).

### 2. Tool come contratto tipizzato

Un tool non e una funzione, e un'**interfaccia con metadati di orchestrazione**:

| Proprieta | Funzione |
|-----------|----------|
| `name` | Identificatore unico |
| `inputSchema` | Validazione runtime (Zod) |
| `description()` | Asincrona, calibrata sul contesto |
| `call(args, context)` | Esecuzione effettiva |
| `checkPermissions()` | Controllo autorizzazioni |
| `isReadOnly(input)` | Discriminante per parallelismo |
| `isConcurrencySafe(input)` | Esecuzione parallela? |
| `isDestructive?(input)` | Operazione irreversibile? |
| `maxResultSizeChars` | Limite output |

### 3. Orchestrazione tool (parallelismo intelligente)

Non e l'LLM a decidere l'ordine di esecuzione. L'orchestratore decide basandosi sui metadati:

- **Tool read-only** → eseguiti in parallelo (max 10)
- **Tool non-read-only** → eseguiti in serie
- **Concorrenza massima**: 10 (configurabile via `CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY`)

### 4. Catena permessi a 4 livelli

1. **Regole statiche** (`settings.json`): allow/deny per tool e pattern
2. **Hook pre-tool-use**: script shell che ispezionano input (JSON stdin → JSON stdout)
3. **Classificatore ML**: valuta rischio semantico (non pattern matching). Es: `rm -rf node_modules` ≠ `rm -rf /`
4. **Prompt utente**: ultima risorsa, chiede conferma

Conservativo per default. Opt-in per fiducia, opt-out per controllo.

### 5. Sub-agent (ricorsione)

Un agent crea altri agent tramite il tool `Agent`:

- **History separata** (nessun inquinamento del padre)
- **File state clonato** (fotografia al momento dello spawn)
- **Permessi ereditati monotoni** (solo restrizione, mai espansione)
- **Worktree opzionale** (`git worktree add` per modifiche isolate)
- **Fork semantics** (`fork=true`): eredita intera history del padre, diverge da li

### 6. Comunicazione inter-agent (Actor Model)

Mailbox basate su file JSON (`~/.claude/teams/{team}/inboxes/{agent}.json`):

- Messaggi strutturati con timestamp
- File locking con retry/backoff
- Tipi: `shutdown_request/response`, `plan_approval_response`, `broadcast`
- Se mandi a un agent fermo, si risveglia automaticamente
- Debuggabile con `cat`

### 7. Gestione memoria (3 livelli)

| Livello | Meccanismo | Dettaglio |
|---------|-----------|-----------|
| Compaction | A 70% della finestra, agent separato riassume messaggi vecchi | Lossy intelligente: preserva decisioni chiave, non taglia per posizione cronologica |
| File state cache | LRU dei file letti | Secondo accesso = cache hit (zero token), invalidata su modifica |
| Persistenza | CLAUDE.md nel progetto | Caricato nel system prompt a ogni sessione |

API native per microcompact: `clear_tool_uses` (rimuove tool_use vecchi), `clear_thinking` (toglie thinking block vecchi).

### 8. Retry differenziato

| Errore | Retry | Strategia |
|--------|-------|-----------|
| 429 (rate limit) | Fino a 10 | Backoff esponenziale (500ms → raddoppia) |
| 529 (server saturato) | Max 3, solo foreground | Zero retry per background (ogni retry amplifica carico 3-10x) |
| Errori connessione | 1 singolo | — |

### 9. Tool search (lazy loading)

Solo tool essenziali (`alwaysLoad: true`) nel prompt iniziale. Il resto e differito (`shouldDefer: true`) con `searchHint` (3-10 parole). L'LLM cerca via meta-tool `ToolSearch`, riceve schema completo, lo invoca. Zero token per tool inutili nella sessione.

## Problemi strutturali evidenziati

1. **Hallucination sui tool**: LLM invoca con input plausibile ma sbagliato. Zod cattura formato, non semantica. Puo loopare ripetendo errore con variazioni
2. **Error propagation nei sub-agent**: figlio fallisce silenziosamente, padre usa risultato parziale come fatto
3. **Loop fuori controllo**: senza `maxTurns` continua forever; con limite, lavoro incompleto
4. **Cost explosion**: costo scala con (turni × sub-agent × tool call), non con righe di codice
5. **Perdita contesto post-compaction**: dopo 3-4 compaction, vincoli lontani diventano rumore

> **Regola pratica**: affidabilita proporzionale alla specificita del task. "Leggi file, aggiungi test" funziona. "Riscrivi modulo autenticazione" e una scommessa.

## Innovazioni uniche di Claude Code

- **Tool loading lazy**: nessun framework lo fa, deferito + on-demand discovery
- **Microcompact nativa API**: integrazione col provider, non hackery client-side
- **Content replacement + prompt cache parity**: sub-agent vedono stesse anteprime per mantenere cache
- **Classificatore ML per permessi**: capisce rischio semantico, non regex
- **Hook system estensibile**: pre/post tool, pre/post compact (bash, HTTP, LLM)
- **AsyncLocalStorage**: multi-agent nello stesso processo senza race condition

## Informazioni integrate nella documentazione

- → [tips-e-tricks.md](../tips-e-tricks.md): compaction, concorrenza tool, retry, tool lazy loading
- → [api.md](../api.md): microcompact API native
