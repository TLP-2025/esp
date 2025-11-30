# esp
Parser descendente recursivo para un subconjunto del idioma español

## Gramática del lenguaje
```
parrafo     -> oracion* EOF
oracion     -> oracion_svo
oracion_svo -> sujetos verbo complemento? .

sujetos     -> sujeto ("y" sujeto)*
sujeto      -> sujeto_det | nombre
nombre      -> "nombre_propio" "adjetivo"?
sujeto_det  -> "determinante"? "sustantivo" "adjetivo"?

verbo       -> "no"? "verbo" objeto?
objeto      -> sujetos  

complemento -> "preposicion" sujeto
```