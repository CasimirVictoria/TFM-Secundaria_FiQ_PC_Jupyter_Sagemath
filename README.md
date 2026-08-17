# 🎓 Implementació del Pensament Computacional a Secundària mitjançant Quaderns Interactius de Jupyter i SageMath

> **Treball de Final de Màster (TFM)**  
> *Màster Universitari en Professorat d'Educació Secundària (Especialitat Física i Química)*  
> **Universitat de València (UV)** — Curs 2025/2026  
> **Autor:** Casimir Victòria  

---

## 🎯 Objectiu del Treball

Aquest projecte investiga i desenvolupa una proposta didàctica innovadora sobre com l'ús del **Pensament Computacional (PC)** i la modelització científica interactiva poden transformar l'ensenyament-aprenentatge de la **Física i la Química** a l'Educació Secundària Obligatòria (ESO) i al Batxillerat, d'acord amb el marc curricular de la **LOMLOE** i el **Decret 107/2022 de la Generalitat Valenciana**.

Per a portar a terme aquesta implementació a l'aula, s'utilitzen **quaderns interactius de Jupyter** combinats amb el sistema de computació matemàtica i científica de codi obert **SageMath** (basat en Python).

---

## 🧠 Reflexió Metodològica: Predicar amb l'Exemple del Pensament Computacional

En el desenvolupament d'aquest TFM s'ha aplicat un principi fonamental: **com a futurs docents de ciències, no podem promoure el pensament computacional a l'aula si no som capaços d'aplicar-lo amb rigor a la nostra pròpia feina de recerca**.

Per aquest motiu, la metodologia de recerca d'aquest treball estableix una divisió clara i transparent:

```mermaid
flowchart LR
    A["⚙️ Treball Mecànic i Indexació (Automatitzat)"] --> B["- Cerca sistemàtica en 30 bases de dades (Scopus, WOS, Dialnet, ERIC).\n- Descàrrega autoritzada via VPN institucional.\n- Generació de cites BibTeX oficials i fitxes de lectura Denote.\n- Indexació i recuperació semàntica de la memòria documental a la RAM."]
    
    C["💡 Treball Intel·lectual (100% Humà)"] --> D["- Anàlisi crític de la literatura didàctica i corrents pedagògics.\n- Detecció d'idees alternatives de l'alumnat en física i química.\n- Disseny curricular de la Unitat Didàctica i simulacions a l'aula.\n- Redacció i reflexió pedagògica de la memòria."]
```

1. **Automatització de les tasques mecàniques i gestió de la memòria:** Les tasques repetitives (cerca documental simultània, extracció de metadades editorials, formatat de citacions en APA 7 i indexació semàntica per a la recuperació instantània de fitxes de lectura a la memòria RAM) s'han automatitzat mitjançant el desenvolupament d'eines pròpies de codi obert ([`mcp-server-academic-spain`](https://github.com/CasimirVictoria/mcp-server-academic-spain) i [`mcp-server-segon-cervell-semantic`](https://github.com/CasimirVictoria/segon-cervell-semantic-mcp)). Això assegura una revisió sistemàtica exhaustiva sense biaixos d'omissió ni pèrdua de referències.
2. **Centralitat del treball intel·lectual docent:** Alliberar el temps de les tasques burocràtiques i mecàniques permet dedicar el 100% de l'esforç a la reflexió pedagògica, a la transposició didàctica dels conceptes científics i al disseny d'activitats d'indagació autèntiques per a l'alumnat.

---

## 🌐 Un Aprenentatge Integrat: La Confluència de Quatre Àmbits

L'elaboració d'aquest Treball de Final de Màster ha suposat un procés d'aprenentatge especialment enriquidor: l'oportunitat d'explorar la confluència de **quatre àmbits que sovint es treballen per separat**, però que s'han anat entrellaçant de manera natural al llarg del projecte:

1. 🧪 **La Didàctica de les Ciències Experimentals:** Com a eix central, cercant maneres d'acostar la Física i la Química a l'alumnat a partir de la indagació i la comprensió dels fenòmens naturals.
2. 💻 **El Pensament Computacional:** Entès com una eina d'aprenentatge pràctica mitjançant entorns interactius lliures (`Jupyter`, `SageMath`, `Python`) per a visualitzar i experimentar amb models científics a l'aula.
3. 🧠 **L'Organització del Treball i la Memòria:** L'ús de mètodes d'indexació i gestió de notes en text pla (`Denote`, `Emacs`) per a estructurar les pròpies lectures i la recerca bibliogràfica amb rigor.
4. 🛡️ **El Compromís amb el Programari Lliure:** La decisió de fonamentar tota la proposta en tecnologies obertes i accessibles (Linux, Git, Quarto), assegurant que qualsevol docent i centre públic puga utilitzar i adaptar aquests recursos lliurement.

Aquest camí ha permès enfocar el TFM no sols com un tràmit acadèmic, sinó com una **experiència formativa molt valuosa per a consolidar una visió docent coherent, pràctica i compromesa amb l'escola pública**.


---

## 🛠️ Ecosistema Tecnològic i Ciència Oberta (REA)

Tot el projecte està construït sobre tecnologies lliures, gratuïtes i de text pla, garantint que qualsevol docent o centre educatiu puga auditar, replicar i adaptar el material lliurement:

* **Format:** [Quarto Markdown](https://quarto.org/) (`.qmd`) per a generació reproducible de la memòria en PDF, HTML i LaTeX seguint les normes **APA 7**.
* **Càlcul i Simulació:** [SageMath](https://www.sagemath.org/) (versió 10.10 compilada des del codi font) i [JupyterLab](https://jupyter.org/).
* **Editor i Gestió del Coneixement:** [GNU Emacs](https://www.gnu.org/software/emacs/) amb integració de [Citar](https://github.com/emacs-citar/citar), [Denote](https://protesilaos.com/emacs/denote) i [citar-denote](https://github.com/pprevos/citar-denote) per a fitxes de lectura interconnectades.
* **Control de Versions:** [Git](https://git-scm.com/) i [GitHub](https://github.com/CasimirVictoria/TFM-Secundaria_FiQ_PC_Jupyter_Sagemath).
* **Bases de Dades Consultades:** Scopus, Web of Science (Clarivate), Dialnet, OpenAlex, ERIC, Revista Eureka, RODERIC (Universitat de València), RIUNET, RUA, UJI, SciELO, Redalyc, TESEO, TDR, arXiv i CORE.

---

## 📜 Llicència i Compromís amb el Programari Lliure

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

Aquest projecte s'allibera sota la llicència de domini públic **Creative Commons Zero 1.0 (CC0 1.0)**, alineant-se amb la filosofia dels **Recursos Educatius Oberts (REA)** i de la **Ciència Oberta (Open Science)** impulsada per la UNESCO i les universitats públiques.
