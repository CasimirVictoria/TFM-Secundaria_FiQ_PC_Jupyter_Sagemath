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
  * Abast real mesurat: $x_{\text{final}} = 1{,}190\text{ m}$ (a $y_{\text{final}} = -0{,}606\text{ m}$).
  * Abast previst per Galileu: $x_{\text{ideal}} = 1{,}234\text{ m}$ (discrepància mínima de només el $3{,}6\%$).
* **Funció didàctica:** Demostra que a xicoteta escala de laboratori ($x \sim 1\text{ m}$) i baixes velocitats, el model ideal de buit de Galileu és una excel·lent primera aproximació.
* **Font i descàrrega directa per a comprovació:**
  * Projecte oficial Open Source Physics (OSP): [https://physlets.org/tracker/](https://physlets.org/tracker/)
  * Descàrrega directa del paquet original `.TRZ` (amb el vídeo `.mp4` i el fitxer `.trk`): [https://github.com/OpenSourcePhysics/tracker/raw/master/examples/BallToss.trz](https://github.com/OpenSourcePhysics/tracker/raw/master/examples/BallToss.trz)

---

## 2. `exp_02_nba_sportvu_shot.csv`: Tir de 3 Punts NBA (Seguiment Òptic Multicàmera SportVU)
* **Descripció:** Tir de 3 punts real d'un partit oficial de l'NBA (*Chicago Bulls vs Cleveland Cavaliers*, partit inaugural de temporada, 27 d'octubre de 2015 al United Center de Chicago).
* **Aparell experimental:** Sistema oficial multicàmera estereoscòpica **SportVU** instal·lat a la coberta del pavelló (6 càmeres d'alta definició a $25\text{ fps}$, $\Delta t = 0{,}040\text{ s}$, calibrades a les dimensions de la pista).
* **Mòbil:** Pilota reglamentària de l'NBA Spalding mida 7: massa $m = 0{,}624\text{ kg}$, diàmetre $D = 0{,}240\text{ m}$.
* **Condicions inicials reals:**
  * Alçada d'eixida: $y_0 = 2{,}57\text{ m}$ (llançament en suspensió sobre el cap d'un jugador professional).
  * Velocitat inicial: $v_0 = 8{,}72\text{ m/s}$, $\alpha = 54{,}5^\circ$.
  * Àpex màxim assolit: $y_{\text{màx}} = 4{,}80\text{ m}$.
  * Abast real mesurat fins a l'anella: $x_{\text{final}} = 7{,}20\text{ m}$ (a l'alçada reglamentària de cistella $y = 3{,}10\text{ m} \approx 10\text{ ft}$).
* **Funció didàctica:** Mostra a gran escala esportiva la desviació real provocada per l'aire en una pilota gran i veloç, explicant per què els jugadors apliquen paràmetres diferents dels teòrics de buit.
* **Font i descàrrega directa per a comprovació:**
  * Publicació científica: Rob Romijnders (2016), *Applying Deep Learning to Basketball Trajectories*, Large-Scale Sports Analytics / [arXiv:1608.03793](https://arxiv.org/abs/1608.03793).
  * Repositori GitHub oficial amb les dades brutes (`seq_all.csv.tar.gz`): [https://github.com/RobRomijnders/RNN_basketball/blob/master/data/seq_all.csv.tar.gz](https://github.com/RobRomijnders/RNN_basketball/blob/master/data/seq_all.csv.tar.gz)

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
