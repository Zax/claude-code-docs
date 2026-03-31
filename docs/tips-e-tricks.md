← [Indice](../README.md) | [← Limiti e Pricing](limiti-e-pricing.md)

# Tips & Tricks

## Comandi utili

- Usa `ultrathink` nel prompt per attivare il livello massimo di extended thinking
- Usa `/clear` per iniziare un task nuovo con contesto pulito
- Usa `/compact` con cautela: compatta la sessione ma è lento e può perdere dettagli
- Per task lunghi, chiedi a Claude di salvare la sessione corrente in un file `.md` in `docs/`
- Usa le checkbox markdown `[ ]` nei file di piano per tracciare il progresso — Claude può spuntarle
- Metti il repo `~/.claude/` sotto git per versionare la tua configurazione globale

## Ridurre la verbosità dell'output

Claude Code tende ad essere verboso per default. È possibile ridurre l'output di circa il 63% con regole nel `CLAUDE.md`:

- **Eliminare aperture adulatorie** ("Sure!", "Great question!") e chiusure vuote ("I hope this helps!")
- **Evitare la riformulazione della domanda** prima di rispondere
- **Richiedere solo ASCII**: em dash, smart quotes e caratteri Unicode possono rompere i parser
- **No disclaimer non necessari** e frasi tipo "As an AI..."

> **Attenzione**: il file CLAUDE.md stesso consuma token di input ad ogni messaggio. Il risparmio netto è positivo solo con un volume di output sufficiente a compensare. Per query brevi e uso occasionale, può costare più di quanto fa risparmiare.

## Workflow efficace per il codice

- **Prima di scrivere**: leggere tutti i file rilevanti e capire il requisito completo
- **Durante la scrittura**: preferire edit mirate a riscritture complete, puntare alla soluzione più semplice possibile
- **Prima di dichiarare "fatto"**: eseguire il codice un'ultima volta — mai dichiarare fatto senza un test che passa
- **"Tre righe simili sono meglio di un'astrazione prematura"**: evitare over-engineering

<!-- Aggiungi qui le tue scoperte -->

---

[← Limiti e Pricing](limiti-e-pricing.md) | [Successivo: Link Utili →](link-utili.md)
