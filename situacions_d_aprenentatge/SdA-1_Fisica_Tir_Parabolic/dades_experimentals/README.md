# Dades Experimentals Calibrades per a la SdA-1 (Tir Parabòlic)

Aquest directori conté els conjunts de dades cinemàtiques calibrades obtingudes mitjançant anàlisi de vídeo fotograma a fotograma amb programari científic (*Open Source Physics Tracker*).

---

## 1.  (Douglas Brown - Cabrillo College / OSP)
* **Descripció:** Llançament parabòlic manual d'una pilota de cautxú realitzat en laboratori per l'autor original de Tracker (Douglas Brown).
* **Aparell experimental:** Càmera a 5{,}15	ext{ fps}$ ($\Delta t = 0{,}066	ext{ s}$) amb calibratge mil·limètric de vara mètrica al mateix pla de moviment.
* **Mòbil:** Pilota de cautxú massís de massa  = 0{,}200	ext{ kg}$.
* **Condicions inicials reals extretes:**
  * Alçada inicial:  = 0{,}00	ext{ m}$.
  * Velocitat inicial:  pprox 3{,}06	ext{ m/s}$, $lpha pprox 54{,}0^\circ$.
  * Abast mesurat: {	ext{final}} = 1{,}190	ext{ m}$ (a {	ext{final}} = -0{,}606	ext{ m}$).
* **Interès didàctic:** Ideal com a contrast inicial a escala humana en laboratori de física.

---

## 2.  (Tir de Bàsquet al Pati - Tracker Video Analysis)
* **Descripció:** Tir parabòlic esportiu d'una pilota de bàsquet reglamentària al pati de l'institut ({,}4	ext{ m}$ d'abast real).
* **Aparell experimental:** Càmera de vídeo esportiva a 0	ext{ fps}$ ($\Delta t = 0{,}0333	ext{ s}$) enregistrant el tir lliure complet des del llançament fins a terra.
* **Mòbil:** Pilota de bàsquet reglamentària (mida 7): massa  = 0{,}620	ext{ kg}$, diàmetre  = 0{,}240	ext{ m}$.
* **Condicions inicials reals extretes:**
  * Alçada inicial d'eixida (braços estesos):  = 2{,}00	ext{ m}$.
  * Velocitat d'eixida:  = 7{,}60	ext{ m/s}$, $lpha = 50{,}0^\circ$.
  * Altura màxima assolida (àpex): {	ext{màx}} = 3{,}63	ext{ m}$.
  * Abast real mesurat a terra: {	ext{final}} = 6{,}41	ext{ m}$.
  * Abast previst ideal de Galileu (buit): {	ext{ideal}} = 7{,}16	ext{ m}$.
* **Interès didàctic:** Magnífic contrast macroscòpic esportiu. La discrepància aerodinàmica és neta d'un **0{,}4\%* (la pilota cau 5	ext{ cm}$ abans del que preveu el model de Galileu sense fregament). Permet a l'alumnat entendre per què un jugador ha d'aplicar més força que la teòrica en un tir real.

---

## Format de les columnes CSV
Tots els fitxers segueixen l'estàndard universal de cinemàtica:
* : Temps transcorregut en segons ($	ext{s}$).
* : Posició horitzontal en metres ($	ext{m}$).
* : Posició vertical en metres ($	ext{m}$).
* : Component horitzontal de la velocitat instantània ($	ext{m/s}$).
* : Component vertical de la velocitat instantània ($	ext{m/s}$).
