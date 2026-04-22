← [Indice](../README.md) | [← Limiti e Pricing](limiti-e-pricing.md)

# Tips & Tricks

## Comandi utili

- Usa `ultrathink` nel prompt per attivare il livello massimo di extended thinking
- Usa `/clear` per iniziare un task nuovo con contesto pulito
- Usa `/compact` con cautela: compatta la sessione ma è lento e può perdere dettagli
- Per task lunghi, chiedi a Claude di salvare la sessione corrente in un file `.md` in `docs/`
- Usa le checkbox markdown `[ ]` nei file di piano per tracciare il progresso — Claude può spuntarle
- Metti il repo `~/.claude/` sotto git per versionare la tua configurazione globale

## Ridurre la verbosità dell'output

Claude Code tende ad essere verboso per default. È possibile ridurre l'output di circa il 63% con regole nel `CLAUDE.md`:

- **Eliminare aperture adulatorie** ("Sure!", "Great question!") e chiusure vuote ("I hope this helps!")
- **Evitare la riformulazione della domanda** prima di rispondere
- **Richiedere solo ASCII**: em dash, smart quotes e caratteri Unicode possono rompere i parser
- **No disclaimer non necessari** e frasi tipo "As an AI..."

> **Attenzione**: il file CLAUDE.md stesso consuma token di input ad ogni messaggio. Il risparmio netto è positivo solo con un volume di output sufficiente a compensare. Per query brevi e uso occasionale, può costare più di quanto fa risparmiare.

## Analisi dell'uso: `/insights`, `/stats` e `/cost`

Claude Code offre tre comandi built-in per analizzare il proprio utilizzo, a diversi livelli di dettaglio.

### `/insights` — Report approfondito delle sessioni

Genera un report che analizza le sessioni Claude Code degli ultimi **30 giorni**, producendo un file HTML interattivo salvato localmente.

```
/insights
```

Il report include:

- **Aree di progetto**: su quali parti del codice hai lavorato di più
- **Pattern di interazione**: come usi Claude Code (tool preferiti, comandi frequenti, stile di prompting)
- **Punti di attrito**: dove il workflow si blocca o rallenta
- **Suggerimenti personalizzati**: raccomandazioni concrete per migliorare l'efficienza

**Caratteristiche chiave**:

| Aspetto | Dettaglio |
|---------|-----------|
| Fonte dati | Cronologia sessioni locale (~30 giorni) |
| Output | File HTML interattivo in `~/.claude/usage-data/report.html` |
| Privacy | Elaborazione completamente locale, nessun upload |
| Frequenza consigliata | Una volta al mese |

> **Tip**: Esegui `/insights` periodicamente per scoprire skill e istruzioni che potrebbero velocizzare il tuo workflow. Man mano che le tue abitudini cambiano, i suggerimenti si aggiornano di conseguenza.

Il comando è disponibile anche da terminale:

```bash
claude /insights
```

### `/stats` — Panoramica dell'attività

Mostra statistiche visuali sull'utilizzo quotidiano:

```
/stats
```

Include:

- **Uso giornaliero**: frequenza e intensità d'uso nel tempo
- **Cronologia sessioni**: lista delle sessioni recenti
- **Streak**: giorni consecutivi di utilizzo
- **Preferenze modello**: distribuzione dei modelli usati (Opus, Sonnet, Haiku)

Utile per avere un colpo d'occhio rapido sulla propria attività, senza la profondità di analisi di `/insights`.

### `/cost` — Consumo token e costi

Mostra le statistiche di consumo token della sessione corrente:

```
/cost
```

Output tipico:

```
Total cost:            $0.55
Total duration (API):  6m 19.7s
Total duration (wall): 6h 33m 10.2s
Total code changes:    0 lines added, 0 lines removed
```

> **Nota**: `/cost` mostra stime locali basate sul conteggio token. Per la fatturazione effettiva, consultare la [Console](https://platform.claude.com/usage). Per utenti Pro/Max con abbonamento, `/cost` è meno rilevante — usare `/stats` per monitorare i pattern d'uso.

### Confronto rapido

| Comando | Cosa mostra | Periodo | Output |
|---------|-------------|---------|--------|
| `/insights` | Analisi approfondita workflow e suggerimenti | ~30 giorni | HTML interattivo |
| `/stats` | Attività, streak, modelli preferiti | Storico | Visualizzazione nel terminale |
| `/cost` | Token consumati e costo stimato | Sessione corrente | Testo nel terminale |

### Analytics di team

Per organizzazioni (Team/Enterprise), esistono dashboard web separate:

- **claude.ai**: [claude.ai/analytics/claude-code](https://claude.ai/analytics/claude-code) — metriche d'uso, contributo PR con integrazione GitHub, leaderboard
- **API Console**: [platform.claude.com/claude-code](https://platform.claude.com/claude-code) — metriche d'uso, tracking spesa

Queste dashboard sono complementari ai comandi locali: i comandi analizzano il tuo uso personale, le dashboard mostrano metriche aggregate del team.

## Workflow efficace per il codice

- **Prima di scrivere**: leggere tutti i file rilevanti e capire il requisito completo
- **Durante la scrittura**: preferire edit mirate a riscritture complete, puntare alla soluzione più semplice possibile
- **Prima di dichiarare "fatto"**: eseguire il codice un'ultima volta — mai dichiarare fatto senza un test che passa
- **"Tre righe simili sono meglio di un'astrazione prematura"**: evitare over-engineering

## Come funziona il motore interno

Capire come funziona Claude Code sotto il cofano aiuta a usarlo meglio.

### Compaction automatica

Quando il contesto raggiunge il **70% della finestra**, un agent separato riassume i messaggi vecchi preservando le decisioni chiave. Non taglia per posizione cronologica ma per rilevanza.

- Dopo 3-4 compaction successive, vincoli lontani possono diventare rumore
- Per task lunghi, chiedi a Claude di salvare decisioni importanti in un file prima che vengano compattate
- CLAUDE.md e la memoria persistente non sono soggetti a compaction

### Orchestrazione dei tool

Claude Code classifica ogni tool con metadati (`isReadOnly`, `isConcurrencySafe`, `isDestructive`) e decide automaticamente come eseguirli:

- **Tool read-only** (Read, Grep, Glob): eseguiti in **parallelo** (max 10 simultanei)
- **Tool non-read-only** (Edit, Write, Bash): eseguiti in **serie**
- Concorrenza massima configurabile: `CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY=10`

Questo spiega perché le ricerche sono veloci (parallele) mentre le scritture sono sequenziali.

### Catena dei permessi

Quando Claude vuole eseguire un tool, la richiesta passa per 4 livelli:

1. **Regole statiche** in `settings.json` (allow/deny per tool e pattern)
2. **Hook pre-tool-use** (script shell che possono bloccare/modificare/approvare)
3. **Classificatore ML** che valuta il rischio semantico (non semplice pattern matching)
4. **Prompt utente** (conferma manuale, ultima risorsa)

### Tool lazy loading

Solo i tool essenziali sono caricati nel prompt iniziale. Gli altri sono differiti e scoperti on-demand tramite `ToolSearch` quando servono. Questo risparmia token di contesto: zero costo per tool non usati nella sessione.

### Retry differenziato

Claude Code gestisce gli errori API in modo diverso:

| Errore | Retry | Strategia |
|--------|-------|-----------|
| 429 (rate limit) | Fino a 10 | Backoff esponenziale (500ms → raddoppia) |
| 529 (server saturato) | Max 3, solo foreground | Zero retry per sub-agent in background |
| Errori connessione | 1 singolo | — |

I sub-agent in background non fanno retry su 529 per non amplificare il carico sul server (ogni retry moltiplica il carico 3-10x).

---

[← Limiti e Pricing](limiti-e-pricing.md) | [Successivo: Link Utili →](link-utili.md)
