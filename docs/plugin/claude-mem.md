← [Indice](../../README.md) | [← Plugin](../plugin.md)

# Claude-Mem

| Campo | Valore |
|-------|--------|
| **Repo** | https://github.com/thedotmack/claude-mem |
| **Autore** | Alex Newman (@thedotmack) |
| **Licenza** | AGPL-3.0 |
| **Stelle** | ~44k |
| **Versione** | 6.5.0 |
| **Piattaforme** | Claude Code, Claude Desktop |

## Cos'è

Claude-Mem è un plugin per Claude Code che implementa un sistema di **memoria persistente e compressione del contesto** tra sessioni. Cattura automaticamente ciò che Claude fa durante le sessioni di codifica, comprime le informazioni con AI e inietta il contesto rilevante nelle sessioni future.

In pratica: mantiene la continuità della conoscenza progettuale anche dopo la chiusura delle sessioni.

## Installazione

```bash
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem
```

Dopo il riavvio di Claude Code, il contesto delle sessioni precedenti apparirà automaticamente.

> **Nota**: `npm install -g claude-mem` installa solo la libreria SDK, non il plugin completo con hook system e worker service.

## Requisiti

- Node.js >= 18.0.0
- Claude Code con supporto plugin
- Bun (auto-installato se mancante)
- uv — Python package manager per ricerca vettoriale (auto-installato)
- SQLite 3 (incluso)

## Come funziona

### Lifecycle hooks

Il plugin si aggancia a 5 eventi del ciclo di vita di Claude Code:
- **SessionStart** — Inietta contesto dalle sessioni precedenti
- **UserPromptSubmit** — Cattura le richieste dell'utente
- **PostToolUse** — Osserva l'uso degli strumenti
- **Stop** — Gestisce la fine dell'elaborazione
- **SessionEnd** — Salva e comprime le osservazioni della sessione

### Worker service

Un servizio HTTP in background (porta 37777, gestito da Bun) con:
- Database SQLite per sessioni, osservazioni, riassunti
- Database vettoriale Chroma per ricerca semantica + keyword
- Interfaccia web viewer su `localhost:37777`
- 10 endpoint di ricerca

### Ricerca a 3 livelli (token-efficiente)

Il sistema usa una strategia di **progressive disclosure** per risparmiare token (~10x):

1. **`search`** — Indice compatto con ID (~50-100 token per risultato)
2. **`timeline`** — Contesto cronologico attorno ai risultati
3. **`get_observations`** — Dettagli completi per ID filtrati (~500-1.000 token)

Si filtra prima di recuperare i dettagli, evitando di caricare tutto in contesto.

## Funzionalità principali

- **Memoria persistente** tra sessioni con compressione AI
- **Ricerca in linguaggio naturale** tramite la skill `mem-search`
- **Ricerca ibrida** semantica + keyword (Chroma vector DB)
- **Controllo privacy**: il tag `<private>` esclude contenuti sensibili dalla memorizzazione
- **Sistema di citazioni** con ID osservazioni per tracciabilità
- **Configurazione granulare** del contesto iniettato (`~/.claude-mem/settings.json`)
- **Interfaccia web** per consultare la memoria su `localhost:37777`

## Risorse

- Documentazione: https://docs.claude-mem.ai
- Discord: https://discord.com/invite/J4wttp9vDu

<!-- Aggiungi qui le tue scoperte -->
