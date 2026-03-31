← [Indice](../../README.md)

# Analisi: claude-token-efficient

| Campo | Valore |
|-------|--------|
| **Repo** | https://github.com/drona23/claude-token-efficient |
| **Autore** | Drona Gangarapu |
| **Stelle** | ~988 |
| **Data analisi** | 31 marzo 2026 |

## Descrizione

Repository che fornisce un file `CLAUDE.md` "drop-in" da inserire nella root di qualsiasi progetto per ridurre la verbosità dell'output di Claude Code di circa il 63%, senza modifiche al codice.

## Problema affrontato

Claude Code, per default, ha diversi comportamenti che sprecano token in output:

1. **Aperture adulatorie** ("Sure!", "Great question!", "Absolutely!")
2. **Chiusure vuote** ("I hope this helps!", "Let me know if you need anything!")
3. **Riformulazione della domanda** prima di rispondere
4. **Em dash, smart quotes, caratteri Unicode** che rompono i parser
5. **Frasi tipo "As an AI..."**
6. **Disclaimer non necessari**
7. **Suggerimenti non richiesti** che vanno oltre lo scope della domanda
8. **Over-engineering del codice** con astrazioni inutili
9. **Allucinazioni** su fatti incerti invece di ammettere di non sapere
10. **Ignorare correzioni dell'utente** (sycophancy: "You're absolutely right!")
11. **Letture ridondanti di file** già letti
12. **Scope creep** (modificare codice fuori dall'ambito della richiesta)

## Soluzione proposta: CLAUDE.md universale

Il file CLAUDE.md del repo è estremamente conciso (~15 righe) con queste regole:

- **Prima di scrivere codice**: leggere tutti i file rilevanti, capire il requisito completo
- **Durante la scrittura**: testare, correggere errori subito, preferire edit a riscritture, soluzione più semplice possibile
- **Prima di dichiarare "fatto"**: eseguire il codice un'ultima volta, mai dichiarare fatto senza un test che passa
- **Output**: niente aperture adulatorie, niente chiusure vuote, niente em dash/smart quotes/Unicode (solo ASCII), essere concisi, dire "non lo so" se incerti
- **Regola override**: le istruzioni esplicite dell'utente vincono sempre su questo file

## Benchmark

Testato su 5 prompt identici con e senza CLAUDE.md:

| Test | Senza | Con | Riduzione |
|------|-------|-----|-----------|
| Spiegare async/await | 180 parole | 65 parole | 64% |
| Code review | 120 parole | 30 parole | 75% |
| Cos'è una REST API | 110 parole | 55 parole | 50% |
| Correzione allucinazione | 55 parole | 20 parole | 64% |
| **Media** | | | **~63%** |

**Proiezione a scala**: con 1000 prompt/giorno si risparmiano circa 96.000 token e ~$8.64/mese (Sonnet).

**Nota importante**: il file CLAUDE.md stesso consuma token di input ad ogni messaggio. Il risparmio netto è positivo solo quando il volume di output è sufficientemente alto da compensare il costo di input persistente.

## Profili specializzati

Il repo include 3 profili aggiuntivi:

### Profilo Coding (`profiles/CLAUDE.coding.md`)
- Codice prima, spiegazione dopo (solo se non ovvia)
- Niente boilerplate, niente astrazioni premature
- Niente docstring o type annotation su codice non modificato
- Review: indica il bug, mostra il fix, stop
- Debug: mai speculare senza leggere il codice, ammettere se la causa è incerta
- "Tre righe simili sono meglio di un'astrazione prematura"

### Profilo Agents (`profiles/CLAUDE.agents.md`)
- Output solo strutturato: JSON, bullet, tabelle
- Nessuna narrazione ("Now I will...", "I have completed...")
- Nessuna richiesta di conferma su task chiaramente definiti
- Mai inventare path, endpoint, nomi di funzioni
- Se un valore è sconosciuto: restituire null o "UNKNOWN"

### Profilo Analysis (`profiles/CLAUDE.analysis.md`)
- Risultato principale prima, contesto e metodologia dopo
- Numeri sempre con unità di misura e fonte
- Distinguere chiaramente tra dati e inferenze
- Formato report: sommario (max 3 bullet), dati di supporto, limiti/caveat

## Consigli dalla community

1. **Regole specifiche battono regole generiche**: invece di "sii conciso", meglio "quando uno step fallisce, fermati immediatamente e riporta l'errore completo con traceback prima di tentare qualsiasi fix"
2. **I file CLAUDE.md si compongono**: Claude legge file a più livelli simultaneamente (globale + progetto + sottodirectory)

## Quando usarlo e quando no

**Utile per**:
- Pipeline di automazione con alto volume di output
- Task strutturati ripetuti (bot, agent loop, generazione codice)
- Team che necessitano output consistente e parsabile

**Non utile per**:
- Query singole e brevi (il file in input costa più del risparmio in output)
- Uso casuale occasionale
- Lavoro esplorativo dove alternative e discussione sono il punto

## Informazioni integrate nella documentazione

- → [tips-e-tricks.md](../tips-e-tricks.md): regole anti-verbosità, workflow efficace, nota sul costo del CLAUDE.md
- → [claude-md.md](../claude-md.md): composizione multi-livello, regole specifiche vs generiche, profili specializzati
- → [limiti-e-pricing.md](../limiti-e-pricing.md): benchmark risparmio token
