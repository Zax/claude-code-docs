← [Indice](../README.md) | [← MCP](mcp.md)

# Limiti e Pricing

Rate limit, costi per token, differenze tra piani e modelli.

| Piano | Costo | Include Claude Code |
|-------|-------|---------------------|
| Free | $0 | No |
| Pro | $20/mese | Sì |
| Max | $100/mese | Sì, con limiti più alti |
| Max 20x | $200/mese | Sì, limiti massimi |
| API (Console) | Pay-per-use | Sì, tramite API key |

> Per uso frequente di Claude Code, un abbonamento Max è generalmente più economico rispetto al pay-per-use via API.

## Ottimizzazione dei token

Un file `CLAUDE.md` ben strutturato con regole anti-verbosità può ridurre i token di output di circa il 63% (benchmark su 5 prompt con Sonnet).

**Proiezione a scala**: con 1000 prompt/giorno si risparmiano circa 96.000 token e ~$8.64/mese (Sonnet).

> **Nota**: il file CLAUDE.md stesso consuma token di input ad ogni messaggio. Il risparmio netto è positivo solo con volumi sufficienti. Per uso occasionale può costare più di quanto fa risparmiare.

---

[← MCP](mcp.md) | [Successivo: Tips & Tricks →](tips-e-tricks.md)
