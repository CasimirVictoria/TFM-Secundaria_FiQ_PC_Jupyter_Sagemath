# 🎓 Pensament Computacional i Modelització en Física i Química de Batxillerat

> **Treball de Final de Màster (TFM) — Modalitat d'Innovació Docent**  
> *Màster Universitari en Professorat d'Educació Secundària (Especialitat Física i Química)*  
> **Universitat de València (UV)** — Convocatòria de Setembre 2026  
> **Autor:** Casimiro Victoria Castillo  
> **Tutora:** Dra. Paula Tuzón Marco  
> **Llicència:** Domini Públic / Codi Obert ([CC0 1.0](LICENSE))

---

## 🌐 Recursos en Obert (Accés Web)

El projecte ha estat desplegat com a **Recurs Educatiu Obert (REA)** accessible públicament:

* 📖 **[Llibre Web del TFM (Quarto)](https://casimirvictoria.github.io/TFM-Secundaria_FiQ_PC_Jupyter_Sagemath/)**: Text complet de la memòria organitzat per capítols, navegable i amb motor de cerca integrat.
* 📥 **[Memòria Oficial en PDF (Descarregar)](https://casimirvictoria.github.io/TFM-Secundaria_FiQ_PC_Jupyter_Sagemath/Pensament-Computacional-i-Modelitzaci%C3%B3-en-F%C3%ADsica-i-Qu%C3%ADmica-de-Batxillerat.pdf)**: Document oficial maquetat en LaTeX (normativa acadèmica UV).
* 🚀 **[Simulació Interactiva WebAssembly (SdA)](https://casimirvictoria.github.io/TFM-Secundaria_FiQ_PC_Jupyter_Sagemath/simulacio/)**: Entorn interactiu de càlcul simbòlic i ajust empíric (Pyodide, SymPy, SciPy i Plotly), operable des de qualsevol dispositiu mòbil o ordinador d'aula sense instal·lacions prèvies.

---

## 🎯 Síntesi de la Proposta d'Innovació Docent

Aquest treball presenta una **proposta d'innovació didàctica** per a la matèria de **Física i Química de 1r de Batxillerat**, articulada d'acord amb el marc curricular de la **LOMLOE** (Decret 108/2022 de la Comunitat Valenciana).

La proposta aborda un problema diagnòstic àmpliament documentat en la recerca didàctica: la desafecció de l'alumnat envers la física, provocada per un enfocament transmissiu basat en la resolució mecànica d'exercicis algorítmics en un «buit ideal» desconnectat de la realitat observable.

### 🌟 Els Quatre Pilars de la Innovació:

1. **Modelització de «Caixa Blanca» (White-Box Modeling):**  
   Superació dels simuladors tancats de «caixa negra». L'alumnat interactua directament amb les lleis dinàmiques de Newton expressades en càlcul simbòlic (`SymPy`), connectant la física de la pissarra amb el codi executable.
2. **Cicle d'Indagació Empírica Autèntica:**  
   Enregistrament de llançaments reals al pati de l'institut $\rightarrow$ Captura de dades de posició-temps mitjançant vídeo-anàlisi (`Tracker`) $\rightarrow$ Contrast amb el model ideal de Galileu $\rightarrow$ Detecció del conflicte cognitiu per la frenada de l'aire $\rightarrow$ Refinament del model físic afegint el fregament aerodinàmic (`SciPy`).
3. **Pensament Computacional Integrat (*Use-Modify-Create*):**  
   Seguint la taxonomia de Brennan, Resnick i Weintrop, l'alumnat mai programa des de zero: comença utilitzant quaderns estructurats (*Use*), modifica paràmetres i hipòtesis físiques (*Modify*) i finalment construeix l'ajust a les seues pròpies dades experimentals (*Create*).
4. **Disseny Universal per a l'Aprenentatge (DUA) i Aprenentatge Cooperatiu:**  
   Bastida socioemocional per a prevenir la frustració tecnològica: rols cooperatius basats en el programa CA/AC (Pujolàs), assistència formativa en la depuració d'errors i interfície neta amb codi plegat per defecte.

---

## 📂 Estructura del Repositori

```text
├── memoria/                     📚 Codi font Quarto de la memòria escrita
│   ├── 00_portada.tex           Portada oficial
│   ├── 01_introduccio.qmd       Capítol 1: Context i objectius
│   ├── 02_marc_teoric.qmd       Capítol 2: Marc teòric i estat de l'art
│   ├── 03_metodologia_disseny.qmd Capítol 3: Proposta d'innovació docent
│   ├── 04_resultats_proposta.qmd Capítol 4: Articulació de la SdA
│   ├── 05_conclusions.qmd       Capítol 5: Conclusions i línies de futur
│   ├── 06_annexos.qmd           Capítol 6: Annexos de codi i materials
│   ├── _quarto.yml              Configuració del llibre Quarto
│   └── references.bib           Bibliografia en format APA 7
│
├── situacions_d_aprenentatge/   🚀 Recursos Educatius Oberts (REAs)
│   ├── SdA-1_Fisica_Tir_Parabolic/  Simulació cinemàtica i dinàmica (Pyodide)
│   └── SdA-2_Quimica_Gasos_Ideals/  Simulacions termodinàmiques (Python/SciPy)
│
├── docs/                        🌐 Eixida estàtica per a GitHub Pages
│   ├── index.html               Portada del llibre web
│   ├── Pensament-...pdf         PDF oficial per a descàrrega directa
│   └── simulacio/               Aplicació web de la SdA
│
├── LICENSE                      Llicència pública Creative Commons (CC0 1.0)
└── README.md                    Descripció del repositori
```

---

## 🛠️ Tecnologies i Estàndards Emprats

* **Escriptura i Documentació Científica:** [Quarto](https://quarto.org/), Pandoc, LaTeX (XeLaTeX), BibLaTeX / APA 7.
* **Computació Científica i Càlcul Simbòlic:** Python 3, [SymPy](https://www.sympy.org/), [NumPy](https://numpy.org/), [SciPy](https://scipy.org/), [SageMath](https://www.sagemath.org/).
* **Execució Client-Side al Navegador:** [Pyodide](https://pyodide.org/) (WebAssembly), [Plotly.js](https://plotly.com/javascript/), [MathJax 3](https://www.mathjax.org/), [CodeMirror](https://codemirror.net/).
* **Vídeo-Anàlisi Experimental:** [Tracker Video Analysis and Modeling Tool](https://physlets.org/tracker/).
