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

---

[← Claude API](api.md) | [Successivo: Limiti e Pricing →](limiti-e-pricing.md)
