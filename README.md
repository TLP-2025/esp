# esp
Parser descendente recursivo para un subconjunto del idioma español

## Gramática del lenguaje

```text
parrafo     -> oracion* EOF
oracion     -> oracion_svo
oracion_svo -> sujetos verbo adverbios? complemento? .

sujetos     -> sujeto ("Y" sujeto)*
sujeto      -> sujeto_det | nombre
nombre      -> "NOMBRE_PROPIO" "ADJETIVO"?
sujeto_det  -> "DETERMINANTE"? "SUSTANTIVO" "ADJETIVO"?

verbo       -> "NO"? "VERBO" objeto?
objeto      -> sujetos

adverbios   -> "ADVERBIO"+

complemento -> "PREPOSICION" sujeto
```



## Impresión del árbol de análisis con librería (`rich`)

Primero debes instalar (una sola vez) en tu entorno de Python:

```bash
pip install rich
```

Al ejecutar el programa, si la oración es aceptada, se imprimirá el árbol
usando `rich.tree.Tree`, por ejemplo:

```bash
python esp.py
esp> Los niños comen manzanas rápidamente en la ciudad.
Oración(es) aceptada(s).
Árbol de análisis sintáctico <list>
└── [0]: OracionSVO
    ├── sujeto: Sujetos
    │   └── sujetos[0]: SujetoDet
    ├── verbo: Verbo
    │   ├── negacion: None
    │   ├── verbo: VERBO(vrs:comen)
    │   ├── objeto: Sujetos
    │   └── adverbio[0]: ADVERBIO(adv:rápidamente)
    └── complemento: ComplementoPre
```

El formato exacto puede variar un poco según el tamaño de la consola.