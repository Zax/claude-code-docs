← [Indice](../README.md) | [← Prompting](prompting.md)

# Claude API e Modelli

## Modelli attuali (generazione 4.x)

| Modello | ID API | Contesto | Output max | Prezzo (input/output per MTok) |
|---------|--------|----------|------------|-------------------------------|
| Claude Opus 4.6 | `claude-opus-4-6` | 1M token | 128k | $5 / $25 |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 1M token | 64k | $3 / $15 |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | 200k token | 64k | $1 / $5 |

> Knowledge cutoff: Opus 4.6 → mag 2025, Sonnet 4.6 → ago 2025, Haiku 4.5 → feb 2025

---

## Casi d'uso consigliati

### Claude Opus 4.6 — Massima intelligenza
Il modello più capace. Da usare quando la qualità del risultato conta più del costo o della velocità.

- Ragionamento multi-step complesso (matematica, logica, strategia)
- Analisi approfondita di documenti lunghi (fino a 1M token di contesto)
- Scrittura creativa di alta qualità
- Ricerca e sintesi su argomenti tecnici complessi
- Agentic tasks con pianificazione autonoma e uso di strumenti
- Coding su codebase grandi con molte dipendenze da tenere a mente
- Revisione critica di architetture e decisioni di design

**Quando NON usarlo**: task semplici e ripetitivi, elaborazioni in batch ad alto volume, applicazioni real-time dove la latenza è critica.

---

### Claude Sonnet 4.6 — Miglior rapporto qualità/costo
Il punto di equilibrio ideale per la maggior parte dei casi d'uso professionali.

- Coding quotidiano: scrittura, refactoring, debug, code review
- Generazione e analisi di testi professionali
- Risposta a domande tecniche con contesto esteso
- Integrazione in applicazioni con volumi medi
- Automazioni e pipeline agentic di media complessità
- Assistente per ricerca e summarization
- Ideale per Claude Code nell'uso quotidiano

**Nota**: supporta *adaptive thinking* (ragionamento adattivo) insieme a Opus 4.6.

---

### Claude Haiku 4.5 — Velocità e basso costo
Il modello più rapido ed economico. Ottimo per task ad alto volume o con latenza critica.

- Classificazione e tagging di testi
- Estrazione di entità e dati strutturati
- Risposte brevi in chatbot e assistenti leggeri
- Moderazione contenuti
- Pipeline batch ad alto volume
- Riassunti rapidi di testi brevi
- Primo stadio in pipeline multi-modello (filtraggio prima di passare a modelli più grandi)

---

## Funzionalità per modello

| Funzionalità | Opus 4.6 | Sonnet 4.6 | Haiku 4.5 |
|--------------|:--------:|:----------:|:---------:|
| Extended thinking | ✓ | ✓ | ✓ |
| Adaptive thinking | ✓ | ✓ | — |
| Contesto 1M token | ✓ | ✓ | — |
| Batch API 300k output | ✓ | ✓ | — |

**Extended thinking**: il modello ragiona passo per passo prima di rispondere (visibile nel "thinking block"). Migliora le prestazioni su task complessi.

**Adaptive thinking**: il modello decide autonomamente quanto pensare in base alla difficoltà del task.

---

## Modelli legacy

Disponibili ma non consigliati per nuovi progetti. Usa le versioni 4.x sopra.

| Modello | ID API | Note |
|---------|--------|------|
| Claude Opus 4.5 | `claude-opus-4-5-20251101` | Predecessore di Opus 4.6 |
| Claude Sonnet 4.5 | `claude-sonnet-4-5-20250929` | Predecessore di Sonnet 4.6 |
| Claude Opus 4.1 | `claude-opus-4-1-20250805` | — |
| Claude Sonnet 4 | `claude-sonnet-4-20250514` | — |
| Claude Opus 4 | `claude-opus-4-20250514` | — |
| Claude Haiku 3 | `claude-3-haiku-20240307` | Deprecated |

---

## Extended Thinking (Ragionamento esteso)

Alcuni modelli possono "pensare" prima di rispondere, mostrando il ragionamento passo per passo in blocchi separati (`thinking` blocks). Utile per task complessi; da evitare per domande semplici (spreco di token).

### Modalità disponibili

**Adattiva** — consigliata per Opus 4.6 e Sonnet 4.6
Il modello decide autonomamente quanto pensare in base alla complessità del task. Si controlla con il parametro `effort`:

```python
thinking={"type": "adaptive", "effort": "high"}  # low | medium | high
```

**Manuale** — disponibile su tutti i modelli con extended thinking, deprecata su Opus/Sonnet 4.6
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
| Opus 4.6 | ✓ | ✓ |
| Sonnet 4.6 | ✓ | ✓ |
| Haiku 4.5 | ✓ | — |

> Con tool use e thinking abilitato, il modello può ragionare tra una chiamata e l'altra (interleaved thinking). I blocchi di thinking vanno passati invariati nelle richieste successive per mantenere la continuità del ragionamento.

---

## Note pratiche

- I modelli sono disponibili su **Anthropic API**, **AWS Bedrock** e **Google Vertex AI** con ID leggermente diversi
- Per interrogare capabilities e limiti token via API: endpoint `/v1/models`
- La **Batch API** riduce i costi del 50% per elaborazioni asincrone (risultati entro 24h)

---

[← Prompting](prompting.md) | [Successivo: MCP →](mcp.md)
