← [Indice](../../README.md)

# Analisi: claude-config-audit

| Campo | Valore |
|-------|--------|
| **Repo** | https://github.com/paolodalprato/claude-config-audit |
| **Autore** | Paolo Dal Prato |
| **Articolo** | https://www.ai-know.pro/claude-config-audit/ |
| **Data analisi** | 17 aprile 2026 |

## Descrizione

Skill open source per Claude Code che esegue un audit sistematico della configurazione Claude su tutti i livelli, individuando ridondanze, conflitti, sprechi di token e RAM, e incoerenze cross-layer.

## Problema affrontato

Nel tempo gli utenti accumulano server MCP, plugin, skill e istruzioni senza mai verificare l'insieme nel suo complesso. Questo causa:

- **Consumo RAM**: ogni server MCP aggiunge memoria (~40-50 MB per processo Node.js, 200-500 MB per container Docker)
- **Spreco token**: istruzioni duplicate consumano token di contesto ad ogni messaggio
- **Degradazione qualità**: istruzioni in conflitto e ambiguità non producono errori espliciti ma riducono invisibilmente la qualità delle risposte

## Aree controllate

### 1. Server MCP
- Duplicati funzionali (due strumenti che coprono la stessa area)
- Stima impatto su risorse (RAM per processo/container)
- Server che dipendono da servizi esterni non più attivi
- Sovrapposizioni note tra server diversi

### 2. Plugin
- Duplicazione da fonti diverse (stesso plugin da marketplace multipli)
- Sovrapposizione tra plugin marketplace e skill locali
- Plugin di setup/onboarding rimasti attivi dopo configurazione iniziale

### 3. Skill locali
- Anomalie strutturali (file orfani, cartelle di backup)
- Versioni superate coesistenti (skill e varianti "-v2")
- Sovrapposizioni con skill generiche dai plugin
- Coerenza: skill che referenziano server MCP rimossi

### 4. Prompt di sistema
- Sovrapposizioni tra User Preferences e CLAUDE.md (similarità >70%)
- Contraddizioni tra i due livelli
- Istruzioni che referenziano strumenti non più presenti
- Stima del costo in token dell'intero prompt di sistema
- Analisi cross-progetto di duplicate e regole mispiazzate

### 5. Hook e permessi (Claude Code)
- Hook duplicati sullo stesso evento
- Hook che referenziano script inesistenti
- Permessi troppo ampi (accesso shell senza restrizioni)
- Regole che menzionano tool di server MCP rimossi

### 6. File di memoria (Claude Code)
- File non aggiornati da oltre 3 mesi
- File orfani non indicizzati in MEMORY.md
- Indici che superano 200 righe (soglia di troncamento)
- Directory di memoria per progetti rimossi dal disco

## Workflow (6 fasi)

1. **Raccolta dati** — rileva piattaforma e legge i file di configurazione (o chiede all'utente se non ha accesso al filesystem)
2. **Analisi** — applica tutti i controlli ai dati raccolti
3. **Report strutturato** — stato attuale, problemi per gravità, azioni correttive con razionale
4. **Validazione interattiva** — ogni raccomandazione richiede conferma esplicita dell'utente
5. **Applicazione modifiche** — esegue le modifiche approvate con backup preventivo, una categoria alla volta
6. **Report finale** — documenta modifiche, azioni manuali residue, impatto stimato, istruzioni per ripristino

> **Principio chiave**: la skill non rimuove nulla autonomamente e non applica modifiche senza conferma esplicita.

## Compatibilità multi-piattaforma

| Piattaforma | Cosa analizza | Limitazioni |
|-------------|---------------|-------------|
| claude.ai | Connettori MCP, skill di progetto, prompt di progetto, istruzioni personalizzate | No file locali |
| Claude Desktop | Con Desktop Commander: `claude_desktop_config.json` + `settings.json` di Code | No configurazione server-side |
| Claude Code (terminale) | Propria configurazione completa + `claude_desktop_config.json` di Desktop | No accesso a claude.ai |

Il report dichiara esplicitamente quali piattaforme sono state analizzate.

## Installazione

```bash
# Git clone (consigliato per aggiornamenti con git pull)
cd ~/.claude/skills && git clone https://github.com/paolodalprato/claude-config-audit

# Oppure: download ZIP da GitHub, estrarre in ~/.claude/skills/
```

Dopo l'installazione la skill è riconosciuta automaticamente. Per eseguire l'audit basta chiedere a Claude "controlla la mia configurazione" o "esegui un audit del mio setup".

## Caratteristiche principali

- **Conservativa**: richiede sempre conferma esplicita, non rimuove nulla in autonomia
- **Cross-layer**: considera le dipendenze tra componenti, non analizza ogni strato in isolamento
- **Interattiva**: l'utente decide per ogni raccomandazione
- **Estensibile**: i pattern di analisi sono in file di riferimento separati, estensibili dalla community
- **Multi-ambiente**: funziona da tutte le interfacce Claude con adattamenti per ciò che può accedere

## Informazioni integrate nella documentazione

- → [skills.md](../skills.md): aggiunta come skill documentata nella sezione dedicata
