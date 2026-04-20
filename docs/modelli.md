← [Indice](../README.md) | [← Prompting](prompting.md)

# Modelli Claude

## Modelli attuali (generazione 4.x)

| Modello | ID API | Contesto | Output max | Prezzo (input/output per MTok) |
|---------|--------|----------|------------|-------------------------------|
| Claude Opus 4.7 | `claude-opus-4-7` | 1M token | 128k | $5 / $25 |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 1M token | 64k | $3 / $15 |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | 200k token | 64k | $1 / $5 |

| | Opus 4.7 | Sonnet 4.6 | Haiku 4.5 |
|--|----------|------------|-----------|
| **Knowledge cutoff** | gen 2026 | ago 2025 | feb 2025 |
| **Training data cutoff** | gen 2026 | gen 2026 | lug 2025 |

---

## Opus 4.7 — Novità rispetto a Opus 4.6

Claude Opus 4.7 è il modello più capace attualmente disponibile, con un **miglioramento significativo nell'agentic coding** rispetto a Opus 4.6.

### Cosa cambia

| Aspetto | Opus 4.6 | Opus 4.7 |
|---------|----------|----------|
| Agentic coding | Buono | **Step-change improvement** |
| Extended thinking | Sì | **No** (rimosso) |
| Adaptive thinking | Sì | Sì |
| Knowledge cutoff | mag 2025 | **gen 2026** |
| Training data cutoff | ago 2025 | **gen 2026** |
| Tokenizer | Standard (~750k parole/1M token) | **Nuovo** (~555k parole/1M token) |
| Prezzo | $5 / $25 | $5 / $25 (invariato) |

### Punti chiave

- **Agentic coding**: Opus 4.7 ha un salto qualitativo nella capacità di pianificare, eseguire e iterare autonomamente su task di coding complessi. È progettato per l'uso con Claude Code e workflow agentici.
- **Extended thinking rimosso**: Opus 4.7 **non supporta** più extended thinking (`type: "enabled"` con `budget_tokens`). Usa solo adaptive thinking, dove il modello decide autonomamente quanto ragionare.
- **Nuovo tokenizer**: il tokenizer di Opus 4.7 è diverso dai modelli precedenti. A parità di 1M token di contesto, copre ~555k parole anziché ~750k. Questo significa che lo stesso testo occupa più token rispetto a Opus 4.6/Sonnet 4.6.
- **Opus 4.6 è ora legacy**: resta disponibile ma non consigliato per nuovi progetti.

---

## Casi d'uso consigliati

### Claude Opus 4.7 — Massima intelligenza e agentic coding

Il modello più capace. Da usare quando la qualità del risultato conta più del costo o della velocità, specialmente per task agentici.

- Agentic coding con pianificazione autonoma e iterazione su task complessi
- Ragionamento multi-step complesso (matematica, logica, strategia)
- Analisi approfondita di documenti lunghi (fino a 1M token di contesto)
- Coding su codebase grandi con molte dipendenze da tenere a mente
- Revisione critica di architetture e decisioni di design
- Scrittura creativa di alta qualità
- Ricerca e sintesi su argomenti tecnici complessi

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

**Nota**: supporta sia *extended thinking* che *adaptive thinking*.

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

| Funzionalità | Opus 4.7 | Sonnet 4.6 | Haiku 4.5 |
|--------------|:--------:|:----------:|:---------:|
| Extended thinking | — | ✓ | ✓ |
| Adaptive thinking | ✓ | ✓ | — |
| Contesto 1M token | ✓ | ✓ | — |
| Batch API 300k output | ✓ | ✓ | — |

**Extended thinking**: il modello ragiona passo per passo prima di rispondere (visibile nel "thinking block"). Migliora le prestazioni su task complessi. **Non disponibile su Opus 4.7**.

**Adaptive thinking**: il modello decide autonomamente quanto pensare in base alla difficoltà del task.

---

## Modelli legacy

Disponibili ma non consigliati per nuovi progetti. Usa i modelli attuali sopra.

| Modello | ID API | Note |
|---------|--------|------|
| Claude Opus 4.6 | `claude-opus-4-6` | Predecessore di Opus 4.7 |
| Claude Opus 4.5 | `claude-opus-4-5-20251101` | — |
| Claude Sonnet 4.5 | `claude-sonnet-4-5-20250929` | Predecessore di Sonnet 4.6 |
| Claude Opus 4.1 | `claude-opus-4-1-20250805` | — |
| Claude Sonnet 4 | `claude-sonnet-4-20250514` | Deprecated, ritiro 15 giu 2026 |
| Claude Opus 4 | `claude-opus-4-20250514` | Deprecated, ritiro 15 giu 2026 |
| Claude Haiku 3 | `claude-3-haiku-20240307` | Deprecated, ritiro 19 apr 2026 |

---

[← Prompting](prompting.md) | [Successivo: Claude API →](api.md)
