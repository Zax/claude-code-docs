← [Indice](../README.md) | [← CLAUDE.md](claude-md.md)

# Prompting

Best practice per scrivere prompt efficaci con Claude.

## Regole base

- Essere chiari e dettagliati nella richiesta
- Usare esempi positivi e negativi
- Incoraggiare il ragionamento step-by-step
- Richiedere tag XML specifici per strutturare l'output
- Specificare lunghezza e formato desiderati

Guida completa: https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview

## Struttura delle richieste

- **Contesto e vincoli prima, richiesta operativa dopo**: fornire sempre il contesto necessario *prima* di chiedere l'azione. Se si danno vincoli dopo, Claude potrebbe aver già imboccato una strada sbagliata
- **Una richiesta per messaggio**: evitare di comprimere più richieste non correlate in un singolo messaggio. Ogni richiesta separata ottiene risposte più precise
- **Riportare risultati esatti**: quando si testa qualcosa e si chiede aiuto, includere log, errori e screenshot concreti anziché descrizioni vaghe
- **Mettere in discussione le proposte**: non accettare passivamente — ragionare sulla proposta e obiettare se qualcosa non convince

## Auto-analisi del proprio stile di prompting

Un metodo efficace per migliorare è chiedere all'AI di **analizzare le proprie conversazioni** alla fine di sessioni di lavoro sostanziali:

> *"Analizza come faccio le richieste in questa conversazione, evidenziando sia i punti efficaci che quelli deboli."*

**Quando funziona meglio**: dopo sessioni collaborative complesse (costruzione di codice, documenti, progetti) con errori, correzioni e cambi di direzione — non dopo semplici Q&A.

**Piattaforma ideale**: Claude Code con Opus (1M token di contesto) permette di analizzare sessioni molto lunghe.

**Ripetere periodicamente**: rifare l'analisi a distanza di settimane per monitorare l'evoluzione dei propri pattern comunicativi.

> È importante chiedere sia punti di forza che debolezze: chiedere solo i punti di forza genera elogi generici, solo le debolezze produce critiche decontestualizzate.

---

[← CLAUDE.md](claude-md.md) | [Successivo: Claude API →](api.md)
