← [Indice](../README.md)

# Setup Claude Code

## Requisiti

- Account Claude **Pro** ($20/mese), **Max** ($100-200/mese), oppure crediti API su Console
- Il piano gratuito di Claude.ai **non** include Claude Code
- Connessione internet attiva
- Shell: Bash, Zsh, PowerShell o CMD

## Installazione - Metodo consigliato (Native Installer)

Non richiede Node.js. Si aggiorna automaticamente in background.

**macOS / Linux:**
```bash
curl -fsSL https://claude.ai/install.sh | bash
claude --version
```

**Windows (PowerShell):**
```powershell
irm https://claude.ai/install.sh | iex
claude --version
```

> Su Windows è necessario **Git for Windows**. Claude Code usa Git Bash internamente per eseguire comandi. Non serve avviare PowerShell come amministratore.

## Installazione alternativa (npm)

Richiede Node.js 18+.

```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

> **MAI** usare `sudo npm install -g` — causa problemi di permessi e sicurezza.

## Installazione su Windows con WSL

```powershell
# PowerShell come Amministratore
wsl --install -d Ubuntu
```

Dopo il riavvio, dentro il terminale Ubuntu:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install git -y
curl -fsSL https://claude.ai/install.sh | bash
claude --version
```

## Autenticazione

Al primo avvio, `claude` apre il browser per il login OAuth con il tuo account Claude (Pro/Max) o Console API.

In alternativa puoi impostare la chiave API come variabile d'ambiente:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Verifica e diagnostica

```bash
claude --version      # Verifica installazione
claude doctor         # Diagnostica automatica dei problemi
```

## Integrazione con VS Code

Claude Code rileva automaticamente VS Code. In alternativa:
1. Avvia Claude Code dal terminale integrato di VS Code
2. Usa il comando `/ide` per abilitare l'integrazione

Funziona anche con Cursor e altri editor moderni.

## Desktop App

Esiste anche un'app desktop per usare Claude Code senza terminale, disponibile per macOS e Windows dalla documentazione ufficiale.

---

[Successivo: CLAUDE.md - Memoria di Progetto →](claude-md.md)
