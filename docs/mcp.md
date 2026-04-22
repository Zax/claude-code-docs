← [Indice](../README.md) | [← Claude API](api.md)

# MCP - Model Context Protocol

Configurazione e uso dei server MCP per connettere Claude a servizi esterni.

MCP estende Claude Code con accesso a strumenti esterni, database, API e servizi tramite un protocollo standardizzato. Oltre 300 integrazioni disponibili (GitHub, Slack, PostgreSQL, ecc.).

## Aggiungere un server MCP

```bash
# Wizard interattivo
claude mcp add

# Oppure direttamente
claude mcp add <nome-server> -- <comando>
```

Senza MCP, Claude Code può solo leggere file ed eseguire comandi bash. Con MCP può interrogare database, creare ticket Jira, fare review su GitHub, controllare errori su Sentry, ecc.

## Tool search e lazy loading

Solo i tool essenziali vengono caricati nel prompt iniziale. I tool MCP sono **differiti di default**: nel contesto entra solo il nome (~token minimi), e lo schema completo viene caricato on-demand quando Claude decide di usarli. Questo significa zero costo per i server MCP configurati ma non usati nella sessione.

Per vedere cosa sta occupando contesto, usare il comando `/context`.

## Computer-use MCP Server

`computer-use` è un server MCP **built-in** che permette a Claude di controllare il computer tramite GUI: aprire app, cliccare, digitare, scorrere e fare screenshot dello schermo.

### Requisiti

| Requisito | Dettaglio |
|-----------|-----------|
| Piattaforma | Solo macOS (su Windows disponibile solo in Desktop app) |
| Piano | Pro o Max (non disponibile su Team/Enterprise) |
| Versione | Claude Code v2.1.85 o successiva |
| Sessione | Solo interattiva (non funziona con flag `-p`) |
| Permessi macOS | Accessibility + Screen Recording |

### Abilitazione

Il server è disattivato di default. Per attivarlo:

1. Eseguire `/mcp` nella sessione
2. Selezionare `computer-use` dalla lista
3. Scegliere **Enable** (l'impostazione persiste per progetto)
4. Al primo uso, concedere i permessi macOS richiesti (Accessibility e Screen Recording)

### Come funziona

Claude sceglie automaticamente lo strumento più preciso disponibile, in ordine di priorità:

1. **MCP server dedicato** per il servizio → lo usa
2. **Comando shell** → usa Bash
3. **Task nel browser** con [Chrome](https://code.claude.com/docs/en/chrome) configurato → usa Chrome
4. **Nessuno dei precedenti** → usa computer-use

Quando computer-use è attivo:

- Le app da controllare vanno **approvate singolarmente** per sessione
- Le altre app vengono **nascoste** (ripristinate a fine turno)
- Il **terminale è escluso** dagli screenshot (sicurezza)
- Un **lock esclusivo** impedisce l'uso da più sessioni simultanee
- Gli screenshot vengono **ridimensionati automaticamente** (es. 3456×2234 → ~1372×887 su Retina)

### Sicurezza

| Guardrail | Descrizione |
|-----------|-------------|
| Approvazione per-app | Claude controlla solo le app approvate nella sessione corrente |
| Warning per app sensibili | Terminali → "equivalente a shell access", Finder → "accesso a qualsiasi file", System Settings → "può modificare impostazioni di sistema" |
| Terminale escluso | Claude non vede mai il proprio output nei screenshot |
| Escape globale | Premere **Esc** ovunque per interrompere immediatamente |
| Lock file | Una sola sessione alla volta può usare il computer |

Le app vengono classificate in livelli di controllo:

- **Solo visualizzazione**: browser e piattaforme di trading
- **Solo click**: terminali e IDE
- **Controllo completo**: tutte le altre app

### Casi d'uso

- **Build e validazione app native**: compilare un target Swift/macOS, lanciare l'app, cliccare sui controlli, fare screenshot dei risultati
- **Test UI end-to-end**: aprire un'app Electron, navigare il flusso di onboarding, catturare ogni step — senza configurare Playwright
- **Debug visuale**: ridimensionare finestre per riprodurre bug di layout, fare screenshot, correggere il CSS, verificare la fix
- **iOS Simulator**: controllare il simulatore senza scrivere XCTest
- **App GUI-only**: interagire con design tool, pannelli hardware, app proprietarie senza CLI/API

Esempio di prompt:

```
Build the MenuBarStats target, launch it, open the preferences window,
and verify the interval slider updates the label. Screenshot the
preferences window when you're done.
```

### Troubleshooting

| Problema | Soluzione |
|----------|-----------|
| "Computer use is in use by another session" | Chiudere l'altra sessione; se crashata, il lock si rilascia automaticamente |
| Permessi macOS richiesti di continuo | Riavviare Claude Code; verificare in Impostazioni di Sistema → Privacy → Screen Recording |
| `computer-use` non appare in `/mcp` | Verificare: macOS, v2.1.85+, piano Pro/Max, autenticazione claude.ai, sessione interattiva |

---

[← Claude API](api.md) | [Successivo: Limiti e Pricing →](limiti-e-pricing.md)
