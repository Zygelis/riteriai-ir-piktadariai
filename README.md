# Lietuviškų riterių ir melagių loginių puzlių generatorius

Genetravimo logika paremta https://github.com/dmackinnon1/knaves repozitorija.

## Kaip susigeneruoti riterių ir melagių loginių puzlių duomenis
```
python riteriu_dataset/generate_rp_dataset.py
```

Papildomai galima keisti generavimo parametrus:
- lengvų, vidutinių ir sunkių puzlių kiekį duomenų rinkinmyje su <code>--easy</code>, <code>--medium</code> ir <code>--hard</code> parametrais.
- <code>--seed</code> skaitinę reikšmę, naudojamą pseudoatsitiktinių skaičių generatoriaus inicializavimui.
- <code>--language</code> keičia generuojamo duomenų rinkinio kalbą. Palaikomos lietuvių ("lt") ir anglų ("en") kalbos.
- <code>--output</code> keičia kur išsaugomas duomenų rinkinys.
- <code>--system-prompt-file</code> keičia sistemos nurodymo failą.