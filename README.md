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

