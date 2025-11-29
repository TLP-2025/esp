from __future__ import annotations

from typing import Dict, List

# Prefijos que usamos en el código fuente "interno" del parser:
#   det:  -> DETERMINANTE
#   sus:  -> SUSTANTIVO
#   adj:  -> ADJETIVO
#   nom:  -> NOMBRE_PROPIO
#   pre:  -> PREPOSICION
#   vrs:  -> VERBO
#   adv:  -> ADVERBIO

_PREFIXES = ("det:", "sus:", "adj:", "nom:", "pre:", "vrs:", "adv:")


# Diccionario base extraído de los ejemplos aceptados.
# clave: palabra en minúsculas (sin punto final), valor: prefijo (det/sus/adj/nom/pre/vrs/adv)
_BASE_LEXICON: Dict[str, str] = {'ana': 'nom',
 'carlos': 'nom',
 'ciudad': 'sus',
 'come': 'vrs',
 'comen': 'vrs',
 'el': 'det',
 'en': 'pre',
 'la': 'det',
 'lee': 'vrs',
 'libro': 'sus',
 'los': 'det',
 'maestra': 'sus',
 'manzana': 'sus',
 'manzanas': 'sus',
 'niño': 'sus',
 'niños': 'sus',
 'visitan': 'vrs'}


# Listas ampliadas muy simples para etiquetar frases nuevas.
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
    return any(word.startswith(p) for p in _PREFIXES) or word.startswith("vrp:")


def _normalize_annotated_token(token: str) -> str:
    """Normaliza tokens ya anotados.

    - Cambiamos cualquier verbo 'vrp:palabra' a 'vrs:palabra' para
      eliminar la distinción singular/plural.
    - Dejamos el resto igual.
    """
    if ":" not in token:
        return token

    pref, word = token.split(":", 1)
    if pref == "vrp":
        pref = "vrs"

    return f"{pref}:{word}"


def _classify_word(word: str) -> str:
    """Devuelve el prefijo (sin ':') para una palabra NO anotada.

    Orden de decisión (muy simple por ser un lenguaje restringido):
    - Si está en el léxico base extraído de los ejemplos, usamos ese.
    - Si es un determinante conocido, usamos 'det'.
    - Si es una preposición conocida, usamos 'pre'.
    - Si es un adverbio conocido, usamos 'adv'.
    - Si está en la lista de verbos comunes, usamos 'vrs' (VERBO).
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
        return "vrs"

    # 5) Nombre propio por mayúscula inicial
    if word and word[0].isupper():
        return "nom"

    # 6) Por defecto, sustantivo
    return "sus"


def annotate_source(source: str) -> str:
    """Devuelve una versión del `source` donde cada palabra lleva su tipo de token como prefijo.

    Comportamiento:
    - Si el texto ya viene anotado (det:/sus:/adj:/nom:/pre:/vrs:/adv:/vrp:),
      se normaliza solo para que cualquier 'vrp:' pase a 'vrs:' y se respeta lo demás.
    - Si el texto NO viene anotado:
        - El punto '.' y las palabras 'y' y 'no' se dejan sin prefijo (las reconoce el lexer).
        - El resto se clasifica automáticamente con `_classify_word`.
    """
    # ¿Hay al menos un token anotado?
    has_annotated = False
    for line in source.splitlines():
        for raw in line.split():
            if _is_already_annotated(raw):
                has_annotated = True
                break
        if has_annotated:
            break

    annotated_lines: List[str] = []

    for line in source.splitlines():
        words = line.split()
        annotated_words: List[str] = []

        for raw in words:
            word = raw
            trailing_punto = ""

            # Separar un punto final pegado: "ciudad." -> "ciudad" + "."
            if word.endswith(".") and word != ".":
                word = word[:-1]
                trailing_punto = "."

            if has_annotated:
                # Texto ya anotado: solo normalizamos verbos en plural (vrp: -> vrs:)
                if _is_already_annotated(word):
                    annotated_words.append(_normalize_annotated_token(word))
                else:
                    annotated_words.append(word)
            else:
                low = word.lower()

                # Palabras que el lexer ya conoce sin prefijo
                if low in ("y", "no", "."):
                    annotated_words.append(low)
                else:
                    if word == "":
                        pass
                    else:
                        pref = _classify_word(word)
                        annotated_words.append(f"{pref}:{word}")

            # Agregar el punto como token separado, si existía
            if trailing_punto:
                annotated_words.append(trailing_punto)

        annotated_lines.append(" ".join(annotated_words))

    return "\n".join(annotated_lines)
