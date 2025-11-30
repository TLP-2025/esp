# Prefijos que usamos en el código fuente "interno" del parser:
#   det:  -> DETERMINANTE
#   sus:  -> SUSTANTIVO
#   adj:  -> ADJETIVO
#   nom:  -> NOMBRE_PROPIO
#   pre:  -> PREPOSICION
#   ver:  -> VERBO
#   adv:  -> ADVERBIO

_PREFIXES = ("det:", "sus:", "adj:", "nom:", "pre:", "ver:", "adv:")


# Diccionario base extraído de los ejemplos aceptados.
# clave: palabra en minúsculas (sin punto final), valor: prefijo (det/sus/adj/nom/pre/ver/adv)
_BASE_LEXICON: dict[str, str] = {'ana': 'nom',
 'carlos': 'nom',
 'ciudad': 'sus',
 'come': 'ver',
 'comen': 'ver',
 'el': 'det',
 'en': 'pre',
 'la': 'det',
 'lee': 'ver',
 'libro': 'sus',
 'los': 'det',
 'maestra': 'sus',
 'manzana': 'sus',
 'manzanas': 'sus',
 'niño': 'sus',
 'niños': 'sus',
 'visitan': 'ver'}


# listas ampliadas muy simples para etiquetar frases nuevas.
_GENERIC_DETS = {"el", "la", "los", "las", "un", "una", "unos", "unas",
                  "este", "esta", "estos", "estas", "ese", "esa", "esos", "esas"}

_GENERIC_PRES = {"a", "ante", "bajo", "con", "contra", "de", "desde",
                  "en", "entre", "hacia", "hasta", "para", "por", "según",
                  "sin", "sobre", "tras"}

# Verbos comunes (todos se etiquetan como VERBO, sin distinguir singular/plural)
_V_COMMON = {"come", "comen", "lee", "leen", "juega", "juegan",
              "corre", "corren", "piensa", "piensan", "visita", "visitan"}

# Algunos adverbios frecuentes
_ADV_COMMON = {"rápido", "rapido", "rápidamente", "lentamente",
                "ayer", "hoy", "mañana", "siempre", "nunca"}


def _is_already_annotated(word: str) -> bool:
    """Indica si la palabra ya viene con algún prefijo conocido (o es y/no/.)."""
    if word in (".", "y", "no"):
        return True
    return any(word.startswith(p) for p in _PREFIXES)



def _classify_word(word: str) -> str:
    """Devuelve el prefijo (sin ':') para una palabra NO anotada.

    Orden de decisión (muy simple por ser un lenguaje restringido):
    - Si está en el léxico base extraído de los ejemplos, usamos ese.
    - Si es un determinante conocido, usamos 'det'.
    - Si es una preposición conocida, usamos 'pre'.
    - Si es un adverbio conocido, usamos 'adv'.
    - Si está en la lista de verbos comunes, usamos 'ver' (VERBO).
    - Si empieza con mayúscula y no entra en otro caso, la tratamos como nombre propio 'nom'.
    - En cualquier otro caso, la consideramos sustantivo 'sus'.
    """
    low = word.lower()

    # 1) Léxico base
    pref = _BASE_LEXICON.get(low)
    if pref is not None:
        return pref

    # 2) Determinantes / preposiciones
    if low in _GENERIC_DETS:
        return "det"
    if low in _GENERIC_PRES:
        return "pre"

    # 3) Adverbios
    if low in _ADV_COMMON:
        return "adv"

    # 4) Verbos comunes
    if low in _V_COMMON:
        return "ver"

    # 5) Nombre propio por mayúscula inicial
    if word and word[0].isupper():
        return "nom"

    # 6) Por defecto, sustantivo
    return "sus"


def annotate_source(source: str) -> str:
    """Devuelve una versión del `source` donde cada palabra lleva su tipo de token como prefijo.

    Comportamiento:
    
    - El punto '.' y las palabras 'y' y 'no' se dejan sin prefijo (las reconoce el lexer).
    - El resto se clasifica con `_classify_word`.
    """
    
    annotated_lines: list[str] = []

    for line in source.split('\n'):
        words = line.split()
        annotated_words: list[str] = []

        while len(words) > 0:
            
            word = words.pop(0)
            if (word == ""): continue

            # Separar un punto final pegado: "ciudad." -> "ciudad" + "."
            if len(word) > 1 and word.endswith("."):
                word = word[:-1]
                words.append(".")

            
            if (not _is_already_annotated(word)):
                pref = _classify_word(word)
                word = f"{pref}:{word}"
            
            annotated_words.append(word)

        annotated_lines.append(" ".join(annotated_words))

    return "\n".join(annotated_lines)
