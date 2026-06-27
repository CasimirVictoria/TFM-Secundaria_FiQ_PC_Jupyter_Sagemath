# 🎓 Academic Spain MCP: Estat del Projecte (v2.4.0)

Estat actual del servidor d'investigació acadèmica i legal optimitzat per a la recerca educativa a Espanya i la Comunitat Valenciana.

## 🚀 Funcionalitats Principals

| Eina               | Descripció                                                       | Fonts Suportades                                                          |
| :----------------- | :--------------------------------------------------------------- | :------------------------------------------------------------------------ |
| `search_works`     | Cerca bibliogràfica i legal detallada.                           | `all`, `dialnet`, `openalex`, `boe`, `scielo`, `teseo`, `procomun`, `gva`, `wos`, `roderic` |
| `suggest`          | Expansió de consultes amb terminologia LOMLOE i GVA.             | N/A (Motor intern)                                                        |
| `discover`         | Cerca ràpida multi-font amb deducció automàtica de terminologia. | Totes                                                                     |
| `get_fulltext_boe` | Extracció de text complet de disposicions del BOE.               | BOE (Legislació Nacional)                                                 |

## 📚 Fonts Integrades (22 fonts en total)

### 🇪🇸 Fonts Nacionals i Autonòmiques
- **BOE (Agència Estatal BOE)**: Legislació nacional, decrets i ordres estatals.
- **DOGV (Generalitat Valenciana)**: Normativa autonòmica valenciana (incorporada v2.4.0).
- **TESEO**: Tesis doctorals defensades a universitats espanyoles (via scraping Playwright).
- **INTEF / Procomún**: Recursos educatius oberts i objectes d'aprenentatge (via scraping).

### 🔬 Fonts Acadèmiques i Científiques
- **Dialnet**: La major base de dades de literatura científica en espanyol.
- **Web of Science (WOS)**: Referent global en cites i impacte científic (via API Starter).
- **RODERIC (UV)**: Repositori institucional de la Universitat de València (tesis, articles localitzats) (incorporada v2.4.1).
- **OpenAlex**: Index global d'articles, autors i institucions.
- **SciELO**: Publicacions d'accés obert (Iberoamèrica i Espanya) (via scraping).

## 🛠 Millores Tecnològiques Recents

- **Scrapers Robusts**: Migració a Playwright amb `evaluate` per superar bloquejos 403 i gestionar SPAs (SciELO, TESEO, GVA).
- **Motor d'Expansió Bilingüe**: Suport per a terminologia educativa en català/valencià i castellà (LOMLOE).
- **Generador de Referències APA 7**: Conversió automàtica de metadades a format bibliogràfic estàndard.
- **Enllaços Directes DOGV**: Generació dinàmica d'URLs a partir de la signatura de la norma.

## 📋 Millores Pendents i Futur

> [!TIP]
> **Optimització de Rendiment**: Implementar un sistema de cache (SQLite o JSON) per evitar scraping repetit de la mateixa consulta.

> [!NOTE]
> **Integració ERIC**: Explorar l'API de ProQuest/ERIC per a literatura educativa internacional en anglès.

> [!IMPORTANT]
> **Anàlisi de Text Complet GVA**: Desenvolupar un connector per extreure el text de les ordres de la GVA (similar al que ja fa el BOE) per permetre anàlisi de NotebookLM.

---
**Estat de l'Entorn**: `/home/casi/Documents/Segon_Cervell/03_ESTUDI/03.1_TFM/MCP_Academic_Spain/`
**Versió de Python**: 3.10+ (Venv actiu)
**Dependències Clau**: `mcp`, `playwright`, `httpx`, `beautifulsoup4`
