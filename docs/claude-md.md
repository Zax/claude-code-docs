← [Indice](../README.md) | [← Setup](setup.md)

# CLAUDE.md - Memoria di Progetto

Il file `CLAUDE.md` è il cuore della memoria persistente di Claude Code. Viene letto automaticamente all'inizio di ogni sessione.

## Cos'è

Un file Markdown nella root del progetto che fornisce a Claude contesto permanente: convenzioni, comandi, architettura, regole. Pensalo come un documento di onboarding per un collega che ogni giorno parte da zero.

## Gerarchia dei file di memoria

I file vengono caricati in ordine, dal più generico al più specifico (il più specifico ha priorità):

| File | Scope | Note |
|------|-------|------|
| `~/.claude/CLAUDE.md` | Globale (tutti i progetti) | Preferenze personali |
| `<root-progetto>/CLAUDE.md` | Progetto | Convenzioni del repo |
| `<root-progetto>/CLAUDE.local.md` | Personale progetto | Da mettere in `.gitignore` |
| `<sottocartella>/CLAUDE.md` | Sotto-directory | Caricato lazy, solo se si lavora lì |

## Composizione multi-livello

I file CLAUDE.md si compongono: Claude legge tutti i livelli simultaneamente. Questo permette di separare le preoccupazioni:

- **Globale** (`~/.claude/CLAUDE.md`): preferenze personali (tono, formato, regole ASCII)
- **Progetto** (root del repo): vincoli specifici del progetto
- **Sottodirectory**: regole specifiche di area (es. `frontend/CLAUDE.md`, `api/CLAUDE.md`)

Si possono anche creare **profili specializzati** per casi d'uso diversi (coding puro, automazione con agenti, analisi dati) con regole mirate per ciascuno.

## Best practice

- **Max ~200 righe** per file. File troppo lunghi consumano contesto e riducono l'aderenza alle istruzioni
- **Non duplicare** ciò che Claude può inferire dal codice (es. "questo è un progetto TypeScript" con un `package.json` presente)
- **Istruzioni specifiche e verificabili**, non vaghe ("segui le best practice")
  - Esempio: invece di "sii conciso", meglio "quando uno step fallisce, fermati immediatamente e riporta l'errore completo con traceback prima di tentare qualsiasi fix"
- Usa **header e bullet point** per strutturare — Claude legge la struttura come un lettore umano
- Metti in `CLAUDE.md` solo ciò che serve in **ogni sessione**
- Per documentazione ad-hoc, usa `docs/` e referenzia con `@docs/filename.md`
- Se il file cresce troppo, spezza le istruzioni in file separati sotto `.claude/rules/`

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

## Auto Memory

Da Claude Code v2.1.59+, Claude può accumulare conoscenza automaticamente tra le sessioni, salvando note su comandi di build, insight di debug, preferenze di stile. È attivabile/disattivabile con `/memory`.

## Esempio per un progetto C# + AngularJS

```markdown
# CLAUDE.md

## Progetto
App gestionale con backend C# (.NET 8 Web API) e frontend AngularJS 1.x.

## Comandi
- `dotnet build` — Build del backend
- `dotnet test` — Esegui test
- `npm start` — Avvia frontend dev server

## Convenzioni
- Backend: C# con naming PascalCase, architettura a layer (Controllers → Services → Repositories)
- Frontend: AngularJS 1.x, controller con suffisso `Ctrl`, servizi con suffisso `Service`
- API RESTful con rotte in kebab-case

## Regole
- MAI usare `var` in C# quando il tipo non è evidente
- SEMPRE aggiungere XML doc comments sui metodi pubblici
- SEMPRE usare `$http` tramite service dedicati, mai direttamente nei controller

## Gotchas
- Il progetto usa AngularJS 1.x, NON Angular 2+. Non suggerire sintassi Angular moderna.
```

<!-- Aggiungi qui le tue scoperte -->

---

[← Setup](setup.md) | [Successivo: Prompting →](prompting.md)
