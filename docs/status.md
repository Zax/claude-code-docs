← [Indice](../README.md) | [← Link Utili](link-utili.md) | [Successivo: Plugin →](plugin.md)

# Stato del Servizio

La pagina ufficiale **[status.claude.com](https://status.claude.com/)** mostra in tempo reale lo stato operativo di tutti i servizi Anthropic/Claude.

## Servizi monitorati

| Servizio | URL | Uptime (90gg) |
|----------|-----|---------------|
| claude.ai | Piattaforma web | ~98.9% |
| platform.claude.com | Console e gestione API | ~99.3% |
| Claude API | api.anthropic.com | ~99.0% |
| Claude Code | Editor integrato | ~99.3% |
| Claude for Government | Versione governativa | ~99.9% |

## Stati possibili

| Stato | Significato |
|-------|-------------|
| **Operational** | Funzionamento normale |
| **Degraded Performance** | Rallentamenti o latenza elevata |
| **Partial Outage** | Interruzione parziale del servizio |
| **Major Outage** | Disservizio significativo |

## Storico e uptime

La pagina mostra un grafico degli ultimi 90 giorni (selezionabile a 30/60/90 giorni) con indicazione visiva dei periodi di downtime. Ogni incidente è documentato con:
- Data e durata
- Livello di impatto (critico, maggiore, minore, manutenzione programmata)
- Aggiornamenti cronologici durante l'evento

## Notifiche

È possibile iscriversi agli aggiornamenti di stato tramite:
- **Email** (verifica OTP)
- **SMS** (verifica OTP)
- **Slack** (integrazione workspace)
- **Microsoft Teams** (webhook)
- **Webhook personalizzato**
- **Atom/RSS feed** — utile per integrazioni custom o monitoraggio automatico

## Quando usarla

- Se Claude Code non risponde o si comporta in modo anomalo, verifica prima lo stato del servizio
- Prima di aprire un ticket di supporto, controlla se è già un incident noto
- Per monitorare l'affidabilità nel tempo prima di integrare l'API in produzione

---

[← Link Utili](link-utili.md) | [Successivo: Plugin →](plugin.md)
