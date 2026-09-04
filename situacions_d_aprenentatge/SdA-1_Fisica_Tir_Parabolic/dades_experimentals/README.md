# Conjunts de Dades Experimentals Reals de Tir Parabòlic (SdA Física)

Aquest directori conté fitxers de dades experimentals reals obtinguts mitjançant seguiment per vídeo (*video-tracking*) i visió per computador, calibrats en espai i temps per a l'anàlisi cinemàtica i dinàmica a l'aula de Batxillerat i Didàctica de les Ciències Experimentals.

---

## 1. `exp_01_tracker_osp_balltoss.csv` (Open Source Physics - Douglas Brown)
* **Descripció:** Experiment de referència oficial de la suite *Tracker* d'Open Source Physics (OSP), creat pel Prof. Douglas Brown (Cabrillo College).
* **Aparell experimental:** Llançament manual d'una pilota en laboratori, enregistrat amb càmera calibrada espacialment amb un patró mètric vertical i eixos de coordenades orientats.
* **Mòbil:** Pilota de cautxú massissa de massa $m = 0{,}200\text{ kg}$.
* **Freqüència temporal:** $15{,}15\text{ fps}$ ($\Delta t = 0{,}066\text{ s}$).
* **Condicions inicials reals extretes:**
  * Posició inicial: $(x_0, y_0) = (0{,}0, 0{,}0)\text{ m}$.
  * Velocitat inicial: $v_{0x} \approx 1{,}80\text{ m/s}$, $v_{0y} \approx 2{,}47\text{ m/s}$ $\rightarrow$ $v_0 \approx 3{,}06\text{ m/s}$, $\alpha \approx 54{,}0^\circ$.
  * Gravetat experimental ajustada: $g_{\text{exp}} = 10{,}25\text{ m/s}^2$.
* **Interès didàctic:** Ideal com a primer contacte per a verificar les equacions de Galileu en un rang d'abast reduït ($1{,}2\text{ m}$) amb baixíssima fricció aerodinàmica.

---

## 2. `exp_02_tracker_llancament_esfera.csv` (Chalk-Snacker Project)
* **Descripció:** Sèrie temporal d'alta resolució obtinguda per seguiment fotograma a fotograma amb *Physics Tracker* d'un projectil esfèric llançat a velocitat moderada.
* **Aparell experimental:** Càmera de $60\text{ fps}$ ($\Delta t = 0{,}0167\text{ s}$) amb 49 fotogrames consecutius d'arc parabòlic complet.
* **Mòbil:** Esfera de massa $m = 0{,}0698\text{ kg}$ i radi $r = 0{,}0275\text{ m}$ ($D = 0{,}055\text{ m}$).
* **Condicions inicials reals extretes:**
  * Alçada inicial de llançament: $y_0 = 0{,}680\text{ m}$.
  * Velocitat inicial: $v_{0x} \approx 2{,}65\text{ m/s}$, $v_{0y} \approx 4{,}24\text{ m/s}$ $\rightarrow$ $v_0 \approx 5{,}00\text{ m/s}$, $\alpha \approx 58{,}0^\circ$.
  * Altura màxima assolida: $y_{\text{màx}} = 1{,}395\text{ m}$.
  * Abast total: $x_{\text{final}} = 2{,}113\text{ m}$.
* **Interès didàctic:** Mostra un llançament complet amb alçada inicial $y_0 \ne 0$, ideal per treballar la resolució d'equacions de segon grau generals i l'ajust de corbes parabòliques amb terme independent.

---

## 3. `exp_03_rebot_pilota_pingpong.csv` (Yassinini / BallsTracker Project)
* **Descripció:** Dades reals obtingudes mitjançant visió per computador (OpenCV) i seguiment automatitzat del centre de masses després d'un rebot.
* **Mòbil:** Pilota de tennis de taula (ping-pong) reglamentària: $m = 0{,}0027\text{ kg}$, diàmetre $D = 0{,}040\text{ m}$.
* **Freqüència temporal:** $60\text{ fps}$ ($\Delta t = 0{,}0168\text{ s}$).
* **Condicions inicials reals extretes:**
  * Llançament/rebot quasi vertical: $\alpha \approx 85{,}5^\circ$, $v_0 \approx 3{,}60\text{ m/s}$.
  * Altura màxima: $y_{\text{màx}} \approx 0{,}634\text{ m}$.
* **Interès didàctic:** Com que la massa d'una pilota de ping-pong és extremadament baixa ($2{,}7\text{ g}$) respecte a la seua secció transversal, el nombre de Reynolds i la relació àrea/massa fan que la resistència de l'aire siga molt pronunciada, permetent contrastar de forma evident la fricció enfront del model ideal.

---

## Format de les columnes CSV
Tots els fitxers segueixen l'estàndard universal de cinemàtica:
* `t`: Temps transcorregut en segons ($\text{s}$).
* `x`: Posició horitzontal en metres ($\text{m}$).
* `y`: Posició vertical en metres ($\text{m}$).
* `vx`: Component horitzontal de la velocitat instantània ($\text{m/s}$).
* `vy`: Component vertical de la velocitat instantània ($\text{m/s}$).
