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

---

## 📚 Bases de Dades i Fonts Indexades

El servidor `tfm-search` realitza consultes en paral·lel en un catàleg de **24 fonts d'informació** de primer nivell, estructurades segons el seu àmbit:

### 🌐 Bases de Dades Acadèmiques Internacionals (Globals)
* **Scopus** *(requereix UV eduVPN)*: L'estàndard d'or en indexació i resums de revistes científiques.
* **Web of Science (WOS)** *(requereix UV eduVPN)*: Plataforma d'informació científica d'alt impacte mundial.
* **PubMed**: Base de dades del govern dels EUA líder en ciències de la vida, medicina i assajos clínics.
* **EuropePMC**: Accés a milions d'articles de recerca biomèdica de repositoris europeus.
* **arXiv**: Dipòsit d'accés obert per a preprints de Física, Matemàtiques i Computació.
* **CORE**: El major agregador de publicacions de recerca en accés obert de milers de repositoris institucionals del món.
* **Zenodo**: Dipòsit multidisciplinar de codi i dades científiques obert, operat pel CERN.
* **CrossRef**: Registre oficial de metadades i resolució de DOIs acadèmics.
* **Semantic Scholar**: Cercador acadèmic amb anàlisi d'impacte i rellevància basat en IA.
* **OpenAlex**: Catàleg massiu, global i obert de publicacions, autors i institucions científiques.
* **Google Scholar**: Motor de cerca general de literatura acadèmica en qualsevol àmbit.

### 🏫 Àmbit Educatiu i Didàctica de les Ciències
* **ERIC (Education Resources Information Center)**: La base de dades sobre educació i pedagogia més gran del món (EUA).
* **Revista Eureka**: Revista científica espanyola de referència en Didàctica de les Ciències Experimentals (Física i Química).

### 🇪🇸 Repositoris de Tesis i Literatura Espanyola / Iberoamericana
* **Dialnet**: El portal de referència i major repositori de literatura científica en espanyol i català.
* **TESEO**: Base de dades oficial del Ministeri d'Educació d'Espanya de tesis doctorals llegides.
* **TDR (Tesis Doctorals en Xarxa)**: Repositori cooperatiu de tesis de les universitats catalanes i altres comunitats.
* **RODERIC**: Repositori institucional de la **Universitat de València (UV)**.
* **SciELO**: Biblioteca digital cooperativa de revistes científiques de la península ibèrica i Llatinoamèrica.
* **Redalyc**: Xarxa de revistes de ciències socials i humanitats d'accés obert.
* **HAL**: Repositori nacional francès de publicacions científiques en obert.
* **IACR**: Repositori especialitzat de recerca en criptografia i seguretat de la informació.

### ⚖️ Legislació Educativa i Recursos Docents (REA / OER)
* **Redined**: Xarxa de bases de dades d'informació educativa, recursos d'aula i recerca espanyola.
* **Procomún**: Xarxa intel·ligent de Recursos Educatius Oberts (REA/OER) del Ministeri d'Educació d'Espanya.
* **BOE (Boletín Oficial del Estado)**: Diari oficial nacional per a lleis de referència educativa (LOMLOE, Reials Decrets, etc.).
* **GVA DOGV (Diari Oficial de la Generalitat Valenciana)**: Publicacions legislatives educatives de la Comunitat Valenciana.
