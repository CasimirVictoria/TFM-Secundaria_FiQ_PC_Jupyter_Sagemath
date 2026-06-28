# 🛠️ Metodologia i Transparència: Automatització de la Cerca Bibliogràfica amb `tfm-search`

Aquest document descriu la integració d'intel·ligència artificial i desenvolupament propi en la metodologia de recerca d'aquest TFM. S'exposa de manera transparent com s'ha dissenyat i emprat una eina de programari per optimitzar les tasques documentals.

---

## 📋 Declaració de Transparència i Rigor Metodològic

En l'elaboració d'aquest treball, s'ha aplicat una divisió clara entre les tasques mecàniques de gestió de dades i el intel·lectual propi d'una recerca acadèmica:

*   **El Treball Mecànic (Automatitzat):** La cerca repetitiva en múltiples portals, la introducció manual de paraules clau a 29 motors de cerca diferents, la descàrrega de documents, la filtració de resultats duplicats i la importació manual de fitxers de citació a Zotero. Tota aquesta tasca —que és de caràcter rutinari i no requereix reflexió pedagògica— s'ha automatitzat mitjançant el servidor customitzat **`tfm-search`** (Model Context Protocol). Això garanteix un rigor molt superior en la revisió sistemàtica i evita l'omissió de referències clau.
*   **El Treball Intel·lectual (Exclusivament Humà):** El filtratge crític de la bibliografia obtinguda, la lectura comprensiva dels articles, l'anàlisi pedagògica dels corrents didàctics, la síntesi teòrica de l'estat de l'art, i la redacció intel·lectual de la memòria, així com el disseny original de la unitat didàctica de Física i Química per a secundària.

Aquest exercici de disseny de programari és, a la vegada, un **exemple pràctic del Pensament Computacional** que es defensa en aquest TFM: davant un problema real de recerca (cerca d'informació fragmentada), s'ha realitzat una descomposició del problema, dissenyat un algorisme de cerca i desduplicació, i s'ha automatitzat la solució.

---

## 💬 1. Exemple de Consulta en Llenguatge Natural

En lloc de realitzar cerques individuals a cadascuna de les 29 plataformes, l'usuari interacciona en llenguatge natural amb l'assistent de IA integrat a l'IDE:

> **"Busca articles de didàctica en espanyol sobre com ensenyar química o física de secundària emprant programació o pensament computacional."**

---

## ⚙️ 2. Execució i Ruteig del Servidor MCP

La IA tradueix la intenció i fa la crida a l'eina **`unified_search`** del servidor local. El flux de treball s'executa automàticament en paral·lel:

```mermaid
graph TD
    UserQuery["Consulta de l'Usuari"] --> |Llenguatge natural| Client["Client IA (IDE / Claude)"]
    Client --> |Eina unified_search| MCP["Servidor tfm-search"]
    
    MCP --> |Classificació Semàntica| Router{"Rutejador Intel·ligent"}
    
    Router -->|Detecta educació/espanyol| CatEdu["Categoria: spanish_education"]
    
    CatEdu --> |Consultes en Paral·lel| Dialnet["Dialnet"]
    CatEdu --> |Consultes en Paral·lel| Redined["Redined"]
    CatEdu --> |Consultes en Paral·lel| Eureka["Revista Eureka"]
    CatEdu --> |Consultes en Paral·lel| Roderic["RODERIC (UV)"]
    CatEdu --> |Consultes en Paral·lel| Riunet["RIUNET (UPV)"]
    CatEdu --> |Consultes en Paral·lel| Rua["RUA (UA)"]
    CatEdu --> |Consultes en Paral·lel| Uji["UJI Repositori"]
    CatEdu --> |Consultes en Paral·lel| OpenAlex["OpenAlex (Globals)"]
    CatEdu --> |Consultes en Paral·lel| ERIC["ERIC (Internacional)"]
    
    Dialnet & Redined & Eureka & Roderic & Riunet & Rua & Uji & OpenAlex & ERIC --> |Resultats Acadèmics| Dedup{"Filtre & Desduplicació"}
    
    Dedup --> |Jaccard & Lexical| Format["Formatat en Markdown/JSON"]
    Format --> |Taula de referències| User["Visualització per a l'Usuari"]
```

### Detall dels passos interns:
1. **Classificació de Categoria:** En detectar conceptes com *"secundària"*, *"didàctica"* o *"espanyol"*, el rutejador classifica la cerca com a `spanish_education` i selecciona automàticament les 9 fonts corresponents.
2. **Cerca Paral·lela:** Es llança una consulta asíncrona a les bases de dades generals i als repositoris institucionals valencians.
3. **Desduplicació:** Si un mateix article es troba indexat alhora a *Dialnet*, *OpenAlex* i *RODERIC*, el sistema calcula la distància de Jaccard dels títols i unifica els registres en un de sol, prioritzant la font de més qualitat acadèmica.

---

## 📊 3. Resultats Retornats a l'IDE (Exemple Real d'Alta Potència)

El servidor MCP unifica les respostes de les bases de dades locals i internacionals, descartant duplicats i aplicant un rànquing de rellevància basat en la qualitat de la font i el nombre de citacions. La IA rep i mostra a l'IDE una taula com la següent:

### 🔬 Resultats de Cerca Acadèmica (`tfm-search`)
**Consulta:** *"computational thinking secondary education"* | **Categoria:** `education` / `spanish_education`

| # | Puntuació | Títol de l'Article | Autors | Font (Pes) | Any | Cit. | Accés / DOI |
|---|---|---|---|---|---|---|---|
| 1 | **77.00** | [Research Trends in K-5 Computational Thinking Education: A Bibliometric Analysis and Ideas to Move Forward](https://eric.ed.gov/?id=EJ1414321) | G. Afacan Adanir, I. Delen & Y. Gulbahar | ERIC (9) | 2024 | 0 | 🔗 [ERIC](https://eric.ed.gov/?id=EJ1414321) |
| 2 | **75.00** | [Developing and Assessing Computational Thinking in Secondary Education Using a TPACK Guided Scratch Visual Execution Environment](https://eric.ed.gov/?id=EJ1298018) | R. Hijón Neira, M. García-Iruela & C. Connolly | ERIC (9) | 2021 | 0 | 🔗 [ERIC](https://eric.ed.gov/?id=EJ1298018) |
| 3 | **73.09** | [El debate sobre el pensamiento computacional en educación](https://doi.org/10.5944/ried.22.1.22303) | J. Adell Segura, M. Á. Llopis Nebot, F. M. Esteve-Mon & M. G. Valdeolivas Novella | OpenAlex (8) / RIED | 2019 | 77 | 🔓 [PDF](http://revistas.uned.es/index.php/ried/article/download/22303/18673) / 🔗 [DOI](https://doi.org/10.5944/ried.22.1.22303) |
| 4 | **72.00** | [Computational Thinking in Secondary Education: Where Does It Fit? A Systematic Literary Review](https://eric.ed.gov/?id=ED581487) | J. Lockwood & A. Mooney | ERIC (9) | 2018 | 0 | 🔗 [ERIC](https://eric.ed.gov/?id=ED581487) |
| 5 | **67.46** | [Análisis observacional del desarrollo del pensamiento computacional en Educación Infantil-3 años...](https://doi.org/10.6018/red.480411) | M. Terroba, J. M. Ribera Puchades, D. Lapresa & M. T. Anguera | OpenAlex (8) / RED | 2021 | 8 | 🔓 [PDF](https://revistas.um.es/red/article/download/480411/313691) / 🔗 [DOI](https://doi.org/10.6018/red.480411) |
| 6 | **65.10** | [Estrategias Educativas para la Enseñanza del Pensamiento Computacional: Una Revisión Sistemática](https://doi.org/10.37811/cl_rcm.v7i4.7590) | Erwin León Castillo | OpenAlex (8) | 2023 | 4 | 🔓 [PDF](https://ciencialatina.org/index.php/cienciala/article/download/7590/11509) / 🔗 [DOI](https://doi.org/10.37811/cl_rcm.v7i4.7590) |
| 7 | **61.67** | [A Systematic Review of Computational Thinking in Science Classrooms](https://eric.ed.gov/?id=EJ1365633) | A. A. Ogegbo & U. Ramnarain | ERIC (9) | 2022 | 0 | 🔗 [ERIC](https://eric.ed.gov/?id=EJ1365633) |
| 8 | **54.12** | [El pensamiento algorítmico como estrategia didáctica para el desarrollo de habilidades de resolución de problemas en el contexto de la educación básica secundaria](https://doi.org/10.6018/red.542111) | D. F. Pinzón Pérez, M. Román-González & E. V. González Palacio | OpenAlex (8) / RED | 2023 | 8 | 🔓 [PDF](https://revistas.um.es/red/article/download/542111/336771) / 🔗 [DOI](https://doi.org/10.6018/red.542111) |
| 9 | **45.00** | [Aplicación del pensamiento computacional en el aula. Una unidad didáctica con alumnado de ESO](https://dialnet.unirioja.es/servlet/articulo?codigo=9259647) | Pablo Antonio Gargallo Jaquotot | Dialnet (8) | 2023 | 0 | 🔗 [Dialnet](https://dialnet.unirioja.es/servlet/articulo?codigo=9259647) |
| 10 | **45.00** | [Creatividad y pensamiento computacional. Una secuencia didáctica para explorar su intersección dentro del marco STEM](https://dialnet.unirioja.es/servlet/articulo?codigo=10281230) | I. Pont Niclòs, E. Izquierdo Sanchis & Y. Echegoyen Sanz | Dialnet (8) | 2023 | 0 | 🔗 [Dialnet](https://dialnet.unirioja.es/servlet/articulo?codigo=10281230) |

*Nota: La puntuació final reflecteix la concurrència lexicogràfica combinada amb el pes específic de la indexació de la revista (com Dialnet, ERIC o segells de qualitat FECYT).*

---

## 💡 4. Integració amb altres Eines del TFM

Una vegada filtrada la taula i escollits els articles més rellevants, el procés documental s'enllaça amb la resta de l'ecosistema local:
* **Ingesta automàtica a Zotero:** Executant la instrucció `mcp_zotero_zotero_add_by_doi(doi="10.5944/ried.22.1.22303")` des del terminal, l'article es registra instantàniament en la col·lecció del gestor bibliogràfic amb totes les seves metadades (any, autors, abstract, pàgines).
* **Descàrrega intel·ligent amb bypass VPN:** Si es vol descarregar el PDF d'accés tancat (o de subscripció institucional), l'MCP connecta autònomament la VPN de la Universitat de València (`eduVPN` UV), realitza el túnel segur, descarrega el fitxer de la revista i el guarda a la carpeta de descàrregues de la recerca.
