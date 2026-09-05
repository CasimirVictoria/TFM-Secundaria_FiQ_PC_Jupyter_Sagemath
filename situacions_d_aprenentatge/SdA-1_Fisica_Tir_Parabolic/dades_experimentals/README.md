# Dades Experimentals Calibrades per a la SdA-1 (Tir Parabòlic)

Aquest directori conté **tres conjunts de dades empíriques 100% reals**, obtingudes mitjançant enregistraments reals amb càmeres de vídeo i sistemes de seguiment òptic calibrats. **Cap d'aquestes dades és simulada o generada artificialment.**

Els tres conjunts estan seqüenciats didàcticament per guiar l'alumnat de 1r de Batxillerat des de la validació del model ideal de Galileu fins a la necessitat d'incorporar la dinàmica de fluids de Newton-Rayleigh.

---

## 1. `exp_01_tracker_osp_balltoss.csv`: Pilota de Cautxú de Laboratori (OSP Tracker)
* **Descripció:** Llançament parabòlic manual d'una pilota de cautxú realitzat en laboratori pel creador original de Tracker, Douglas Brown.
* **Aparell experimental:** Càmera de laboratori a $15{,}15\text{ fps}$ ($\Delta t = 0{,}066\text{ s}$) amb calibratge mil·limètric de vara mètrica al mateix pla focal del moviment.
* **Mòbil:** Pilota de cautxú massís de massa $m = 0{,}200\text{ kg}$.
* **Condicions inicials reals:**
  * Alçada inicial: $y_0 = 0{,}00\text{ m}$.
  * Velocitat inicial: $v_0 = 3{,}06\text{ m/s}$, $\alpha = 54{,}0^\circ$.
  * Abast real mesurat (retorn al pla $y = 0{,}00\text{ m}$): $x_{\text{final}} = 0{,}836\text{ m}$ ($t_{\text{vol}} = 0{,}481\text{ s}$).
  * Abast ideal previst per Galileu (buit): $x_{\text{ideal}} = 0{,}908\text{ m}$ (discrepància mínima de només $+0{,}072\text{ m}$, $7{,}9\%$).
* **Funció didàctica:** Demostra que a xicoteta escala de laboratori ($x \sim 1\text{ m}$) i baixes velocitats, el model ideal de buit de Galileu és una excel·lent primera aproximació.
* **Font i descàrrega directa per a comprovació:**
  * Projecte oficial Open Source Physics (OSP): [https://physlets.org/tracker/](https://physlets.org/tracker/)
  * Descàrrega directa del paquet original `.TRZ` (amb el vídeo `.mp4` i el fitxer `.trk`): [https://github.com/OpenSourcePhysics/tracker/raw/master/examples/BallToss.trz](https://github.com/OpenSourcePhysics/tracker/raw/master/examples/BallToss.trz)

---

## 2. `exp_02_pingpong_tt3d.csv`: Pilota de Tennis de Taula (Univ. Tübingen TT3D)
* **Descripció:** Llançament parabòlic net d'una pilota reglamentària de tennis de taula (ping-pong) amb seguiment òptic tridimensional multi-càmera d'alta precisió (sense gir / *no-spin*, evitant forces de sustentació de Magnus).
* **Aparell experimental:** Sistema de calibratge de càmeres sincronitzades a $60\text{ fps}$ ($\Delta t = 0{,}0167\text{ s}$) desenvolupat pel Laboratori de Sistemes Cognitius de la Universitat de Tubinga (*Cognitive Systems Lab*, Alemanya).
* **Mòbil:** Pilota oficial de tennis de taula ITTF: massa $m = 0{,}0027\text{ kg}$ ($2{,}7\text{ g}$), diàmetre $D = 0{,}040\text{ m}$ ($40\text{ mm}$), relació superfície/massa molt elevada.
* **Condicions inicials reals:**
  * Alçada d'eixida: $y_0 = 0{,}269\text{ m}$.
  * Velocitat inicial: $v_0 = 3{,}75\text{ m/s}$, $\alpha = 34{,}7^\circ$.
  * Abast real mesurat fins al contacte amb la taula ($y_{\text{contacte}} = 0{,}020\text{ m}$ pel radi de $2\text{ cm}$): $x_{\text{final}} = 1{,}490\text{ m}$ ($t_{\text{vol}} = 0{,}584\text{ s}$).
  * Abast ideal previst per Galileu (buit): $x_{\text{ideal}} = 1{,}639\text{ m}$ (pèrdua del $9{,}1\%$ de l'abast per pura resistència quadràtica de l'aire).
* **Funció didàctica:** Constitueix el règim intermedi perfecte de fregament quadràtic pur: en ser un llançament pla sense gir manual, la trajectòria segueix al $100\%$ el sistema diferencial de Newton-Rayleigh ($F_d = -c v^2 \hat{v}$) amb un coeficient $k_{\text{drag}} \approx 0{,}11\text{--}0{,}13\text{ m}^{-1}$, verificant la llei física sense les complicacions de gir esportiu.
* **Font i descàrrega directa per a comprovació:**
  * Publicació científica: University of Tübingen, *TT3D: Table Tennis Match 3D Reconstruction* ([arXiv:2504.10035](https://arxiv.org/abs/2504.10035)).
  * Repositori oficial GitHub amb el conjunt *ground truth* (`023.csv`): [https://github.com/cogsys-tuebingen/tt3d/blob/main/data/evaluation/3D_gt/023.csv](https://github.com/cogsys-tuebingen/tt3d/blob/main/data/evaluation/3D_gt/023.csv)

---

## 3. `exp_03_badminton_tracker.csv`: Volant de Bàdminton (ComPADRE / AAPT Tracker OSP)
* **Descripció:** Llançament d'un volant de bàdminton enregistrat en vídeo i processat amb Tracker per l'*American Association of Physics Teachers* (AAPT).
* **Aparell experimental:** Càmera a $29{,}97\text{ fps}$ ($\Delta t = 0{,}03337\text{ s}$) amb cinta vertical de calibratge d'$1{,}80\text{ m}$ al fons.
* **Mòbil:** Volant de bàdminton estàndard de plomes: massa $m \approx 0{,}005\text{ kg}$, diàmetre de faldilla $D \approx 0{,}066\text{ m}$ ($k_{\text{drag}} \approx 0{,}28\text{ m}^{-1}$).
* **Condicions inicials reals:**
  * Alçada inicial: $y_0 = 0{,}65\text{ m}$.
  * Velocitat inicial d'eixida: $v_0 = 17{,}83\text{ m/s}$, $\alpha = 56{,}9^\circ$.
  * Abast real mesurat: $x_{\text{final}} = 4{,}48\text{ m}$ ($t_{\text{vol}} = 1{,}60\text{ s}$).
  * Abast teòric en el buit (Galileu): $x_{\text{ideal}} \approx 29{,}6\text{ m}$!
* **Funció didàctica:** És l'exemple suprem del col·lapse del model de buit: el volant perd més del $85\%$ del seu abast a causa de l'enorme secció cònica aerodinàmica. En els primers $0{,}2\text{ s}$ viatja a $v_x = 9{,}75\text{ m/s}$, però al final del vol ha sigut frenat fins a $v_x \approx 0{,}75\text{ m/s}$, caient pràcticament en vertical i trencant completament la simetria parabòlica.
* **Font i descàrrega directa per a comprovació:**
  * Fitxa oficial ComPADRE OSP (Projecte ID 12086): [https://www.compadre.org/osp/items/detail.cfm?ID=12086](https://www.compadre.org/osp/items/detail.cfm?ID=12086)
  * Descàrrega directa del paquet complet `.TRZ` (amb vídeo `shuttlecock_model.mp4` i projecte Tracker `shuttlecock_model.trk`): [https://www.compadre.org/osp/document/ServeFile.cfm?ID=12086&DocID=2976&TrackerSet=1](https://www.compadre.org/osp/document/ServeFile.cfm?ID=12086&DocID=2976&TrackerSet=1)

---

## Format de les columnes CSV
Tots els fitxers segueixen l'estàndard universal de cinemàtica:
* `t`: Temps transcorregut en segons ($\text{s}$).
* `x`: Posició horitzontal en metres ($\text{m}$).
* `y`: Posició vertical en metres ($\text{m}$).
* `vx`: Component horitzontal de la velocitat instantània ($\text{m/s}$).
* `vy`: Component vertical de la velocitat instantània ($\text{m/s}$).
