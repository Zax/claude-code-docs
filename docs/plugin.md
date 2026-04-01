← [Indice](../README.md) | [← Stato del Servizio](status.md)

# Plugin

I plugin estendono le capacità di Claude Code con workflow, skill e automazioni aggiuntive. Si installano tramite il marketplace integrato.

## Installazione plugin

```bash
# Dal marketplace ufficiale
/plugin install <nome>@claude-plugins-official

# Da un marketplace custom
/plugin marketplace add <owner>/<marketplace-repo>
/plugin install <nome>@<marketplace>

# Aggiornamento
/plugin update <nome>
```

## Plugin documentati

| Plugin | Descrizione |
|--------|-------------|
| [Superpowers](plugin/superpowers.md) | Framework agentico con skill per TDD, debugging sistematico, pianificazione e code review |
| [Claude-Mem](plugin/claude-mem.md) | Memoria persistente tra sessioni con compressione AI e ricerca semantica |
| [Claude HUD](plugin/claude-hud.md) | Dashboard visiva nel terminale: contesto, strumenti, agenti, git, usage |

---

[← Link Utili](link-utili.md)
