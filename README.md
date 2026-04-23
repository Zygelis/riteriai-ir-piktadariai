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

## Kaip ištestuoti pasirinktą atviro kodo LLM, esantį HuggingFace platformoje

Pridėjome <code>evaluate_model.py</code> programinį kodą, kad galima būtų palyginti atviro kodo LLM modelius.

Example usage:
```
python evaluate_model.py --model Qwen/Qwen3.5-4B --benchmark aime25 --max-samples 10 --batch-size 1
```

Arba mažesnį modelį:
```
python evaluate_model.py --model meta-llama/Llama-3.2-1B-Instruct --benchmark gpqa:diamond --max-samples 10 --batch-size 2
```
