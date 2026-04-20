← [Indice](../README.md) | [← Modelli](modelli.md)

# Claude API

Parametri, funzionalità e utilizzo dell'API Anthropic.

## Extended Thinking (Ragionamento esteso)

Alcuni modelli possono "pensare" prima di rispondere, mostrando il ragionamento passo per passo in blocchi separati (`thinking` blocks). Utile per task complessi; da evitare per domande semplici (spreco di token).

> **Nota**: Opus 4.7 **non supporta** extended thinking. Usa solo adaptive thinking.

### Modalità disponibili

**Adattiva** — disponibile su Opus 4.7, Sonnet 4.6
Il modello decide autonomamente quanto pensare in base alla complessità del task. Si controlla con il parametro `effort`:

```python
thinking={"type": "adaptive", "effort": "high"}  # low | medium | high
```

**Manuale** — disponibile su Sonnet 4.6 e Haiku 4.5, non su Opus 4.7
Si specifica un budget fisso di token per il ragionamento:

```python
thinking={"type": "enabled", "budget_tokens": 10000}
```

Il `budget_tokens` deve essere inferiore a `max_tokens`.

### Visualizzazione del thinking

| Opzione `display` | Effetto |
|-------------------|---------|
| `"summarized"` (default) | Restituisce un riassunto del ragionamento |
| `"omitted"` | Nasconde il thinking, streaming più veloce |

In entrambi i casi vieni addebitato per i **token di thinking completi**.

### Quando usarlo

| Scenario | Consiglio |
|----------|-----------|
| Matematica, logica, algoritmi complessi | `effort: "high"` o budget alto |
| Coding con molte dipendenze | `effort: "medium"` |
| Domande semplici, chat, classificazione | Non usarlo |

### Supporto per modello

| Modello | Extended thinking | Adaptive thinking |
|---------|:-----------------:|:-----------------:|
| Opus 4.7 | — | ✓ |
| Sonnet 4.6 | ✓ | ✓ |
| Haiku 4.5 | ✓ | — |

> Con tool use e thinking abilitato, il modello può ragionare tra una chiamata e l'altra (interleaved thinking). I blocchi di thinking vanno passati invariati nelle richieste successive per mantenere la continuità del ragionamento.

---

## Ottimizzazione del contesto

L'API Anthropic offre strategie native per gestire il contesto senza tagliare lato client:

- **`clear_tool_uses`**: rimuove i blocchi tool_use/tool_result vecchi dai messaggi, preservando i metadati. Riduce il contesto senza perdere il filo del ragionamento.
- **`clear_thinking`**: toglie i thinking block vecchi mantenendo solo i più recenti. Utile con extended thinking attivo su sessioni lunghe.

Queste strategie sono più precise del troncamento generico perché operano a livello semantico (rimuovono parti specifiche) anziché tagliare per posizione.

---

## Note pratiche

- I modelli sono disponibili su **Anthropic API**, **AWS Bedrock** e **Google Vertex AI** con ID leggermente diversi
- Per interrogare capabilities e limiti token via API: endpoint `/v1/models`
- La **Batch API** riduce i costi del 50% per elaborazioni asincrone (risultati entro 24h)

---

[← Modelli](modelli.md) | [Successivo: MCP →](mcp.md)
