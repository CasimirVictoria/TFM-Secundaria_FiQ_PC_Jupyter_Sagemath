---
name: tfm-research-pipeline
description: >-
  End-to-end automated research, simulation, and drafting pipeline for the Master's Thesis (TFM)
  in Physics and Chemistry Didactics. Searches 30 academic databases (Scopus, WOS, Dialnet, OpenAlex, ERIC, Roderic),
  manages EduVPN for paywalled PDFs, populates BibTeX (references.bib), compiles SageMath simulations,
  and drafts APA 7 compliant Quarto (.qmd) thesis chapters.
---

# 🎓 Pipeline de Recerca i Redacció del TFM (Física i Química - UV)

Aquesta skill automatitza el flux complet de recerca, simulació i redacció per al Treball de Final de Màster en Didàctica de les Ciències Experimentals.

---

## 🔄 Flux de Treball en 5 Fases:

### Fase 1: Cerca Acadèmica Exhaustiva (30 Bases de Dades)
- Executar  o  per a cercar simultàniament a **Scopus**, **Web of Science (WOS)**, **Dialnet**, **OpenAlex**, **ERIC**, **Revista Eureka** i **RODERIC**.
- Classificar per rellevància pedagògica i puntuació de citacions.

### Fase 2: Ingesta Bibliogràfica en Text Pur (BibTeX)
- Extreure el DOI oficial i generar l'entrada BibTeX en format APA 7.
- Afegir l'entrada automàticament a .

### Fase 3: Accés a Text Complet i EduVPN
- Si un article seleccionat requereix subscripció institucional, utilitzar  per a activar la VPN de la Universitat de València.
- Descarregar el PDF autoritzat i desconnectar la VPN automàticament ().

### Fase 4: Modelització i Simulació amb SageMath
- Executar codi de simulació de Física i Química (cinemàtica, termodinàmica, orbitals, estequiometria) mitjançant  o SageMath 10.10 local.
- Exportar gràfics 2D/3D i animacions a la carpeta .

### Fase 5: Redacció i Compilació en Quarto (.qmd)
- Redactar els capítols en valencià seguint l'estructura formal de la Universitat de València.
- Compilar automàticament a HTML/PDF amb .
