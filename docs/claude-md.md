← [Indice](../README.md) | [← Setup](setup.md)

# CLAUDE.md - Memoria di Progetto

Il file `CLAUDE.md` fornisce a Claude contesto persistente tra sessioni. Viene letto automaticamente all'inizio di ogni sessione.

## Cos'è

Un file Markdown che fornisce a Claude contesto permanente: convenzioni, comandi, architettura, regole. Pensalo come un documento di onboarding per un collega che ogni giorno parte da zero.

**Come funziona tecnicamente**: il contenuto viene iniettato come _user message_ dopo il system prompt, non come parte del system prompt. Claude lo legge e cerca di seguirlo, ma non è un enforcement garantito — istruzioni vaghe o in conflitto possono essere ignorate.

## Gerarchia dei file

I file vengono caricati dal più generico al più specifico (il più specifico ha priorità):

| Scope | Posizione | Condiviso con |
|-------|-----------|---------------|
| Globale personale | `~/.claude/CLAUDE.md` | Solo te (tutti i progetti) |
| Progetto | `./CLAUDE.md` oppure `./.claude/CLAUDE.md` | Team via version control |
| Sotto-directory | `<sottocartella>/CLAUDE.md` | Team, caricato lazy |

I file nella gerarchia di directory sopra la working directory vengono caricati all'avvio. Quelli nelle sottodirectory vengono caricati on demand quando Claude legge file in quelle cartelle.

> Esiste anche un livello **managed policy** per organizzazioni (IT/DevOps centralizato), che non può essere escluso dagli utenti.

## Composizione multi-livello

I file CLAUDE.md si compongono: Claude legge tutti i livelli simultaneamente. Questo permette di separare le preoccupazioni:

- **Globale** (`~/.claude/CLAUDE.md`): preferenze personali (tono, formato, regole ASCII)
- **Progetto** (`./CLAUDE.md` o `./.claude/CLAUDE.md`): standard condivisi col team
- **Sottodirectory**: regole specifiche di area (es. `frontend/CLAUDE.md`, `api/CLAUDE.md`)

Si possono anche creare **profili specializzati** per casi d'uso diversi (coding puro, automazione con agenti, analisi dati) con regole mirate per ciascuno.

## Lingua del file

Claude interpreta il CLAUDE.md con la stessa precisione in qualsiasi lingua. Non c'è differenza tecnica tra scriverlo in italiano o in inglese.

La scelta pratica:
- **Italiano** (o la lingua del team): più leggibile per chi mantiene il file, coerente con il contesto di lavoro
- **Inglese**: preferibile se il progetto è condiviso con persone non italofone o pubblicato open source

## Importare file esterni

Il CLAUDE.md supporta la sintassi `@path/to/file` per includere altri file, che vengono espansi nel contesto all'avvio:

```markdown
Vedi @README per la panoramica del progetto e @package.json per i comandi disponibili.

# Istruzioni aggiuntive
- Git workflow: @docs/git-instructions.md
```

Utile anche per preferenze personali non committate:
```markdown
# Preferenze personali
@~/.claude/my-project-instructions.md
```

La prima volta che Claude Code incontra import esterni mostra un dialog di approvazione.

## Commenti HTML

I commenti `<!-- ... -->` vengono rimossi prima dell'iniezione nel contesto. Utili per lasciare note ai maintainer senza consumare token:

```markdown
<!-- TODO: aggiornare questa sezione dopo la migrazione a v2 -->
## Comandi
- `npm run build`
```

I commenti dentro i code block vengono preservati.

## Organizzare le regole con `.claude/rules/`

Per progetti grandi, le istruzioni possono essere suddivise in file separati sotto `.claude/rules/`. Ogni file dovrebbe coprire un solo argomento:

```
progetto/
├── .claude/
│   ├── CLAUDE.md
│   └── rules/
│       ├── code-style.md
│       ├── testing.md
│       └── security.md
```

### Regole con scope a path specifici

Le regole possono essere limitate a determinati file tramite frontmatter YAML:

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# Regole API
- Tutti gli endpoint devono includere validazione dell'input
- Usa il formato standard di risposta per gli errori
```

Pattern supportati: `**/*.ts`, `src/**/*`, `*.md`, ecc. Le regole senza `paths` si applicano sempre.

### Regole personali globali

Le regole in `~/.claude/rules/` si applicano a tutti i progetti sulla propria macchina.

### Symlink

La directory `.claude/rules/` supporta symlink — utile per condividere regole tra più progetti.

## Best practice

- **Max ~200 righe** per file. File troppo lunghi consumano contesto e riducono l'aderenza alle istruzioni
- **Non duplicare** ciò che Claude può inferire dal codice (es. "questo è un progetto TypeScript" con un `package.json` presente)
- **Istruzioni specifiche e verificabili**, non vaghe ("segui le best practice")
  - Esempio: invece di "sii conciso", meglio "quando uno step fallisce, fermati immediatamente e riporta l'errore completo con traceback prima di tentare qualsiasi fix"
- Usa **header e bullet point** per strutturare — Claude legge la struttura come un lettore umano
- Metti in `CLAUDE.md` solo ciò che serve in **ogni sessione**
- Per documentazione ad-hoc, usa `docs/` e referenzia con `@docs/filename.md`
- Se il file cresce troppo, spezza le istruzioni in file separati sotto `.claude/rules/`
- Controlla periodicamente conflitti tra file CLAUDE.md di livelli diversi

## Cosa includere

- Descrizione breve del progetto (pochi bullet)
- Comandi di build, test, lint usati di frequente
- Convenzioni di naming e struttura cartelle
- Regole immutabili ("MAI fare X", "USA SEMPRE Y")
- Terminologia specifica del progetto
- Principi di ingegneria (es. SOLID)
- Cose che Claude tende a sbagliare (sezione "Gotchas")

## Cosa NON includere

- Informazioni che cambiano spesso (mettile nei prompt)
- Dati sensibili (il file viene spesso committato su git)
- Cose ovvie che Claude può capire dal codice
- Descrizioni dettagliate dell'architettura (meglio un link a `docs/architecture.md`)

## Generazione iniziale

```bash
# Claude Code genera un CLAUDE.md di partenza basato sulla struttura del progetto
claude /init
```

> Consiglio: dopo `/init`, **elimina** la maggior parte del contenuto generato. Tieni solo ciò che aggiunge valore reale.

Con `CLAUDE_CODE_NEW_INIT=true` si attiva una modalità interattiva che guida passo passo nella creazione (esplora il codice, fa domande, propone il file prima di scriverlo).

## CLAUDE.md e `/compact`

Il CLAUDE.md **sopravvive alla compattazione**: dopo `/compact`, Claude ricarica il file da disco e lo reinietta nel contesto. Se un'istruzione sembra sparire dopo `/compact`, significa che era stata data solo nella conversazione, non scritta nel file.

## Compatibilità con AGENTS.md

Se il repo usa già `AGENTS.md` per altri agenti AI, creare un `CLAUDE.md` che lo importa per non duplicare le istruzioni:

```markdown
@AGENTS.md

## Claude Code
- Usa plan mode per modifiche in `src/billing/`.
```

## Auto Memory

Da Claude Code v2.1.59+, Claude può accumulare conoscenza automaticamente tra le sessioni.

**Storage**: `~/.claude/projects/<project>/memory/`

```
memory/
├── MEMORY.md          # Indice conciso, caricato ad ogni sessione
├── debugging.md       # Note sui pattern di debug
├── api-conventions.md # Decisioni di design API
```

**Limiti di caricamento**:
- `MEMORY.md`: prime 200 righe o 25KB — il resto non viene caricato all'avvio
- I file topic (es. `debugging.md`) non vengono caricati all'avvio — Claude li legge on demand

**Gestione**: usa `/memory` per sfogliare, modificare o eliminare i file di memoria. I file sono plain markdown editabili manualmente.

**Disabilitare**: imposta `autoMemoryEnabled: false` nelle impostazioni o la variabile d'ambiente `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.

---

[← Setup](setup.md) | [Successivo: Prompting →](prompting.md)
