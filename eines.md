# Eines i Entorn de Treball

## Format
Per a realitzar tot el material emprat en el TFM, així com la mateixa memòria del treball, he emprat el format Quarto Markdown (que vaig emprar per primera vegada en la part d'estadística, conjuntament amb R, de l'assignatura d'Innovació docent del màster). Els motius per a emprar aquest format són:

* Es tracta d'un format de text pla, el que permet editar tot el material en qualsevol editor i facilita emprar un sistema de control de versions com Git.
* Permet crear quaderns de Jupyter de forma nativa.
* Facilita enormement l'exportació a altres formats, com HTML (i crear al seu torn de manera senzilla pàgines web), **LaTeX**, PDF, DOCX, etc.
* Donat que la memòria del màster ha de seguir les normes APA 7, emprar Quarto facilita molt la tasca de formatar les cites bibliogràfiques i la bibliografia final. Simplement cal afegir una línia en la capçalera del document indicant l'estil desitjat, i Quarto s'encarrega de processar-ho de forma automàtica.

## Editor
El fet que es treballe simplement amb text permet editar el contingut amb qualsevol editor o IDE (RStudio, VSCode, Vim, Emacs...). Jo en particular he decidit desenvolupar i redactar tot el projecte de manera exclusivament local des de la consola de Linux, utilitzant **Neovim** com a editor principal, sense necessitat d'IDE tipus VS Code o similars. 

Encara que he considerat emprar **[VSCodium](https://vscodium.com/)** en el futur (el qual permet emprar extensions de Quarto, LTeX per a correcció gramatical o complements de Zotero), per ara tot el meu flux de treball es gestiona de manera eficient directament des de la línia de comandes.



## Jupyter i SageMath
He emprat JupyterLab per a treballar de manera interactiva amb els quaderns elaborats, així com **SageMath** com a nucli (*kernel*) de càlcul. Per a treballar còmodament amb Quarto en JupyterLab, s'ha instal·lat l'extensió *JupyterLab Quarto* i *Jupytext*, que manté sincronitzat el quadern (en format `.ipynb`) amb el fitxer de text en format `.qmd`.

Els càlculs analítics, numèrics, gràfiques i animacions es realitzaran íntegrament emprant SageMath.

### Instal·lació local de SageMath
Si bé SageMath es pot instal·lar fàcilment en gairebé qualsevol sistema operatiu, he optat per compilar-lo manualment des del codi font. Això em permet disposar de la versió de desenvolupament més recent (versió 10.10) i completament optimitzada per al meu entorn.

El procés ha consistit en clonar el repositori oficial mitjançant Git, instal·lar les dependències des dels repositoris de Debian (seguint les [instruccions oficials](https://doc.sagemath.org/html/en/installation/source-distro.html), així com les de [sagemanifolds](https://sagemanifolds.obspm.fr/install_ubuntu.html)) i compilar el codi aprofitant el multiprocés (`make -jN`).
En el meu cas he clonat el repositori git de Sagemath i compilat emprant:

```sh
make configure
./configure SAGE_CONFIGURE_ARGS="-Dbuild-docs=false"
export MAKE="make -j16"
time make
```
He hagut de passar eixa opció al *configure* perquè si no fallava la compilació per culpa de *Meson*
Al meu portatil, un Ryzen 7 5700u amb uns 18 GB de RAM ha trigat 42 minuts:

```sh
 make[2]: Leaving directory '/home/casimir/Programes/sage/build/make'

Sage build/upgrade complete!

real 42m23.862s user 460m41.630s sys 20m15.811s
```


### Execució dels quaderns al núvol
Per a facilitar que els estudiants (o qualsevol usuari, ja que el repositori és públic) puguen executar els quaderns sense haver d'instal·lar res als seus ordinadors, el projecte està preparat per a llançar-se a **MyBinder**. 

M'he basat en el repositori oficial de `sage-binder-env` (un fitxer Dockerfile que configura un entorn aïllat amb l'última versió estable del nucli Sage i carrega els quaderns directament al navegador).

### Accés remot segur (Tailscale)
Per a poder treballar amb aquest entorn de recerca i computació des de qualsevol lloc, he configurat una xarxa privada virtual (VPN) utilitzant **Tailscale**. Això em permet connectar-me de manera segura a la instància de JupyterLab i als serveis de càlcul de SageMath de l'ordinador principal des de qualsevol dispositiu mòbil o portàtil, sense haver d'exposar ports directament a internet.

## Gestor Bibliogràfic

Com a gestor bibliogràfic empre **Zotero**, conjuntament amb el complement *Better BibTeX*. Aquesta integració automatitza tota la feina relacionada amb la citació. Zotero exporta de forma contínua la base de dades a un fitxer en format `.bib`, i l'editor de text té la capacitat de llegir-lo en temps real.

## Raonament Pedagògic i Transparència
Una de les principals motivacions per a emprar aquesta arquitectura (Quarto, Jupyter i SageMath) és la convicció que s'ha de promocionar l'elaboració de **Recursos Educatius Oberts (REA)** i l'ús de programari lliure a l'aula.

A més, considere que hui dia és fonamental que els futurs docents tinguen una bona formació en programació i en l'ús d'eines computacionals. Aquestes habilitats són estructurals en qualsevol àmbit relacionat amb les disciplines STEM i, per tant, els nostres alumnes també les necessitaran i les empraran en el seu futur acadèmic i professional.

### Intel·ligència artificial

Finalment, vull fer notar que empraré la **intel·ligència artificial** per a l'assistència en la cerca bibliogràfica (com ja detallaré més endavant) i per a l'elaboració de codi. Aquest fet no implica que el treball no siga genuí i elaborat completament per mi. L'estic integrant com una eina actual, un exemple pràctic del que descric en el paràgraf anterior, que facilita enormement tasques com, per exemple, *elaborar un programa per a realitzar cerques en diferents bases de dades de manera unificada* des del mateix IDE, emprant llenguatge natural en comptes d'operadors lògics. Estic convençut que assistents similars seran eines habituals en la tasca docent dels professors de física i química a curt termini, així com per a tots els estudiants i investigadors en general.

De fet, he creat, amb l'ajuda de la pròpia IA, el servidor [MCP_Academic_Spain](MCP_Academic_Spain/README.md) per a realitzar cerques en 29 bases de dades de manera unificada i paral·lela, basant-me en projectes com [https://biomcp.org/](https://biomcp.org/). També crearé i empraré un MCP per a treballar des del mateix IDE amb SageMath, enviant el codi a una instància de JupyterLab corrent com a servei de *systemctl* al meu ordinador. Tot això sense eixir de l'entorn de treball.

#### Reflexió sobre la co-creació de programari
Cal reconèixer de manera transparent que, sense l'assistència activa de la IA en la co-programació, el desenvolupament d'un servidor MCP d'aquestes característiques (que implica programació asíncrona, control de navegadors en segon pla amb Playwright, desduplicació de dades i connexions VPN automatitzades) hauria requerit una dedicació de temps superior a la redacció de la mateixa memòria del TFM, fent-lo del tot inviable.

Això il·lustra un canvi de paradigma fonamental: la democratització de la creació de programari. Els usuaris no tècnics poden crear les seues pròpies eines, en este cas una eina de recerca, adaptada completament a les seues necessitats. En aquest apartat el rol de l'investigador o docent ha sigut el d'un *arquitecte del sistema* (qui té la visió, defineix la lògica del problema i valida els resultats), mentre que la IA actua com a *ajudant tècnic/programador*. Aquest procés és un model pràctic de pensament computacional aplicat a l'aula que es vol promoure.

#### Nota de transparència sobre les eines de IA
Com a part del compromís amb la transparència metodològica, cal remarcar que, a diferència de la resta de l'entorn de treball (que és completament lliure i de codi obert), els assistents de IA emprats per a la co-programació i l'assistència en la cerca no són programari lliure. S'ha fet ús del model comercial de llenguatge Gemini de Google, inicialment a través de l'eina `gemini-cli` en la línia de comandes i, posteriorment, mitjançant el client de terminal `antigravity-cli`. Tot i que l'ús d'estes eines propietàries i tancades ha facilitat enormement el procés de desenvolupament, s'estableix com a línia futura del projecte l'exploració de models de llenguatge de codi obert i lliures (com ara Llama o similars) per a aconseguir un ecosistema totalment lliure.

#### Antecedents personals

L'ús d'eines com BioMCP en particular és el que m'ha acabat de convèncer que la IA ens pot ajudar moltíssim a aprendre. Ens permet aprendre de manera autònoma si ens ensenyen com **aprendre a aprendre**, d'una manera immensament més fàcil, filtrant la informació, democratitzant l'accés al coneixement i empoderant-nos en el procés d'aprenentatge.

Hem de saber, això sí, emprar les **fonts d'informació correctes** i tindre en compte les **limitacions** (en particular les al·lucinacions, cada vegada menors) d'aquestes eines. A nivell personal, ha sigut una revelació veure com, davant d'un problema de la vida real, un repte de salut molt específic, el fet de fer les preguntes correctes i aplicar amb rigor el mètode científic ens permet, gràcies a la IA i a l'ús del MCP BioMCP, formular una hipòtesi sòlida i traçar una via clara cap a la solució. Indagar de manera autònoma en estudis d'avantguarda i assajos clínics m'ha permés experimentar —sempre sota una estricta supervisió mèdica— una solució simple i segura, comprovant l'eficàcia de primera mà. Aquest procés genera un empoderament profund sobre la pròpia vida i la salut que fa només dos anys hauria sigut inimaginable, facilitant l'accés a un corpus de coneixement que sovint triga a ser incorporat per la medicina convencional. És precisament aquest mateix potencial de resolució proactiva de problemes reals el que vull traslladar a l'aula.

> **Nota:** Quan acabe la redacció del TFM publicaré també l'estudi particular que he realitzat en el meu àmbit personal (el que en l'argot científic coneixem com un assaig clínic de màxim rigor empíric amb una mostra de n=1, on l'investigador principal, el pacient i el conillet d'Índies soc exclusivament jo mateix 🐹🧪 😅). Aquest tracta bàsicament sobre com es pot millorar la salut cardiovascular amb precursors d'òxid nítric (NO), en particular la L-citrulina. També analitza com un gran percentatge de la població presenta polimorfismes genètics que impedeixen una assimilació òptima de vitamines del complex B metilat, i les implicacions per al sistema nerviós, tant perifèric com central, d'aquesta condició. D'aquesta manera, amb simples intervencions com prendre suplements de L-citrulina, NAC (n-acetilcisteina), glicina, i un complex B metilat, es pot afavorir la remielinització de nervis perifèrics, optimitzar la salut cardiovascular reduint l'homocisteïna i com efecte secundari optimitzar la producció de neurotransmissors.

## Compromís amb el Codi Obert i la Ciència Oberta

Totes les eines ací descrites són de codi obert, lliures i gratuïtes. Aquesta elecció respon a un compromís ètic i pedagògic amb la **democratització del coneixement**. 
En conformar un entorn altament integrat exclusivament amb programari lliure, s'eliminen les barreres d'entrada (com el pagament de llicències privatives) per a qualsevol estudiant, docent o centre educatiu que desitge replicar, auditar o adaptar aquest mètode de treball.

A més, tot el material elaborat en aquest projecte serà alliberat com a codi obert i estarà disponible per a tothom. Aquesta decisió s'alinea amb la filosofia de la Ciència Oberta ([Open Science](https://www.unesco.org/en/open-science)) i l'impuls dels Recursos Educatius Oberts ([REA](https://www.rebiun.org/kit-rea/sobre-rea)). 

