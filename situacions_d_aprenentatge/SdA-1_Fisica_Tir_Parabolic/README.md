# SdA 1 (Física): Més enllà del buit — Modelització del tir parabòlic amb resistència aerodinàmica

**Nivell:** 1r de Batxillerat (Física i Química / Física)  
**Marc Curricular:** Decret 108/2022 de la Comunitat Valenciana (LOMLOE)  
**Competències Específiques:** CE1, CE2, CE3, CE4, CE5, CE6  
**Durada estimada:** 6 sessions de 55 minuts (expandible a 10-12 segons la diversitat del grup)

---

## 🎯 Objectiu Didàctic
Superar el model clàssic del «buit ideal» de Galileu ($k=0$) mitjançant la formulació de les lleis de Newton amb resistència aerodinàmica (models de Stokes i Rayleigh), emprant el pensament computacional com a eina epistèmica per alliberar l'alumnat de la sobrecàrrega d'àlgebra manual.

## 📂 Continguts d'aquesta carpeta
* **`index.html`**: **Entorn d'Aprenentatge Integral WebAssembly (Pyodide + SymPy + SciPy + Plotly + CodeMirror)**. Executa Python natiu al navegador de l'alumne sense dependre de servidors ni instal·lacions, integrant:
  * Les 4 fases de modelització d'Hestenes (*Use-Modify-Create*).
  * Editor de codi interactiu amb execució en temps real.
  * Contrast de dades experimentals reals de *Physics Tracker* (`.csv`).
  * Bastida socioemocional amb targetes de depuració d'errors en valencià.
* **`simulador_simple.html`**: Versió lleugera orientada a l'exploració directa mitjançant controls lliscants (*sliders*).

## 🔄 Seqüenciació d'Aula (*Use-Modify-Create*)
1. **Sessió 1 (USE / Herron 1):** Enregistrament de llançaments reals al pati amb mòbils i vídeo-anàlisi amb *Physics Tracker* (`.csv`).
2. **Sessió 2 (USE / Herron 1):** Exploració qualitativa de la simulació interactiva amb controls lliscants.
3. **Sessió 3 (MODIFY / Herron 2):** Resolució simbòlica ideal a *SageMath* / *SymPy* mitjançant `solve()` i `diff()`.
4. **Sessió 4 (MODIFY / Herron 2):** El Conflicte Cognitiu: contrast del tir ideal de Galileu enfront de les dades reals de *Tracker*. Activació del model dinàmic de fricció aerodinàmica.
5. **Sessió 5 (CREATE / Herron 3):** Anàlisi de residuals, estimació de l'error relatiu percentual de l'abast i discussió de casos límit.
6. **Sessió 6 (CREATE / Herron 3):** Comunicació científica, coavaluació cooperativa (Programa CA/AC) i reflexió metacognitiva.
