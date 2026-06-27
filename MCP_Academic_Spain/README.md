# 🔬 Server MCP: `tfm-search` (MCP Academic Spain & Education)

Aquest és un servidor MCP (Model Context Protocol) dissenyat específicament per a la investigació acadèmica en l'àmbit de la **didàctica de les ciències (Física i Química)** i la **legislació educativa espanyola/valenciana** per al Treball de Fi de Màster (TFM).

Permet que qualsevol assistent de Intel·ligència Artificial (com Claude, Cursor o Antigravity) cerqui articles acadèmics, controli la connexió VPN de la Universitat per a accedir a revistes subscrites, i descarregui directament documents de text complet.

---

## 🛠️ Requisits del Sistema

* **Sistema Operatiu:** Linux (Debian/Ubuntu recomanat per a la integració amb NetworkManager i la VPN).
* **Python:** Versió 3.10 o superior.
* **NetworkManager (nmcli):** Requerit per al control automatitzat de la VPN institucional de la UV (`eduVPN`).
* **Zotero & Scite:** (Opcional) Per a la integració del guardat de referències automàtic.

---

## 🚀 Guia d'Instal·lació i Configuració

### 1. Clonar o copiar la carpeta de l'MCP
Assegura't de tenir aquesta carpeta (`MCP_Academic_Spain`) desada al teu ordinador (per exemple, dins del mateix repositori del teu TFM).

### 2. Crear l'entorn virtual de Python
Des de la terminal, accedeix a la carpeta de l'MCP i crea un entorn virtual:

```bash
cd MCP_Academic_Spain
python3 -m venv venv
```

### 3. Instal·lar les dependències de Python
Activa l'entorn virtual i instal·la els paquets necessaris de l'MCP i web scraping:

```bash
source venv/bin/activate
pip install mcp python-dotenv httpx playwright beautifulsoup4 pypdf
```

### 4. Instal·lar el navegador per a Playwright
El motor de cerca de Dialnet, Redined i BOE requereix Playwright per a navegar asíncronament. Descarrega el navegador Chromium:

```bash
playwright install chromium
```

---

## ⚙️ Configuració de les Claus d'Accés (APIs)

Crea un fitxer ocult a la teva carpeta personal anomenat `~/.mcp_academic_keys` i afegeix-hi les teves credencials (per exemple, per a Scopus, Web of Science o Unpaywall si en tens):

```env
SCOPUS_API_KEY="la_teva_clau_api_de_scopus"
# Afegeix altres claus necessàries per als cercadors indexats...
```

---

## 🔌 Integració amb el teu Client d'IA

Perquè la teva IA (com Claude Desktop o Antigravity) pugui utilitzar aquestes eines, has d'afegir el servidor al fitxer de configuració de servidors MCP (per a Claude Desktop és a `~/.config/Claude/claude_desktop_config.json` i per a Antigravity a `~/.gemini/antigravity-cli/mcp_config.json`):

```json
{
  "mcpServers": {
    "tfm-search": {
      "command": "/ABSOLUTE/PATH/TO/MCP_Academic_Spain/venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/MCP_Academic_Spain/server.py",
        "--transport",
        "stdio"
      ],
      "env": {
        "PYTHONPATH": "/ABSOLUTE/PATH/TO/MCP_Academic_Spain"
      }
    }
  }
}
```
*⚠️ Recorda canviar `/ABSOLUTE/PATH/TO/` per la ruta absoluta real de la carpeta del teu ordinador.*

---

## 🔍 Eines Disponibles per a la IA

Un cop configurat, la IA tindrà accés automàtic a les següents funcions:

1. **`unified_search`**: Cerca acadèmica unificada amb enrutament automàtic de consultes (classifica si la teva pregunta és de tipus general, educatiu, espanyol o biomèdic i només consulta les bases de dades rellevants).
2. **`search_academic_spain`**: Cerca detallada en fonts estatals espanyoles com **Dialnet**, **Redined**, **BOE**, **Procomún**, **Roderic (UV)** i bases de dades globals.
3. **`vpn_control`**: Controla programàticament la connexió WireGuard de la UV (`eduVPN`) per comprovar l'estat, connectar-se o desconnectar-se de la xarxa universitària.
4. **`download_paper`**: Descàrrega directa del document complet de l'article amb auto-connexió intel·ligent a la VPN si el recurs és de pagament i requereix accés institucional de la UV.
