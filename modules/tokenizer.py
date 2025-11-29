from __future__ import annotations

from typing import Dict, List

# Prefijos usados en los ejemplos/lexer:
#   det:  -> DETERMINANTE
#   sus:  -> SUSTANTIVO
#   adj:  -> ADJETIVO
#   nom:  -> NOMBRE_PROPIO
#   pre:  -> PREPOSICION
#   vrs:  -> VERBO (usaremos solo "verbo", sin distinguir singular/plural)

_PREFIXES = ("det:", "sus:", "adj:", "nom:", "pre:", "vrs:")

# Diccionario base extraído de los ejemplos aceptados.
# clave: palabra en minúsculas (sin punto final), valor: prefijo (det/sus/adj/nom/pre/vrs)
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
_GENERIC_DETS = {"el", "la", "los", "las", "un", "una", "unos", "unas", "este", "esta", "estos", "estas", "ese", "esa", "esos", "esas"}
_GENERIC_PRES = {"a", "ante", "bajo", "con", "contra", "de", "desde", "en", "entre", "hacia", "hasta", "para", "por", "según", "sin", "sobre", "tras"}

# Verbos comunes que queremos reconocer explícitamente (todos como VERBO "vrs")
_V_COMMON = {"come", "comen", "lee", "leen", "juega", "juegan", "corre", "corren", "piensa", "piensan", "visita", "visitan"}


def _is_already_annotated(word: str) -> bool:
    return any(word.startswith(p) for p in _PREFIXES) or word in (".", "y", "no")


def _classify_word(word: str) -> str:
    """Devuelve el prefijo (sin ':') para una palabra NO anotada.

    La lógica es sencilla:
    - Si está en el léxico base extraído de los ejemplos, usamos ese.
    - Si es un determinante/preposición conocida, usamos det/pre.
    - Si es un verbo común, usamos siempre vrs (ya no distinguimos plural).
    - Si empieza con mayúscula y no entra en otro caso, la tratamos como nombre propio (nom).
    - En cualquier otro caso, la consideramos sustantivo (sus).
    """
    low = word.lower()

    # 1) Léxico base de ejemplos
    pref = _BASE_LEXICON.get(low)
    if pref is not None:
        return pref

    # 2) Listas genéricas
    if low in _GENERIC_DETS:
        return "det"
    if low in _GENERIC_PRES:
        return "pre"

    # 3) Verbos comunes (sin distinguir número)
    if low in _V_COMMON:
        return "vrs"

    # 4) Nombres propios por mayúscula inicial
    if word and word[0].isupper():
        return "nom"

    # 5) Por defecto, sustantivo
    return "sus"


def _normalize_annotated_token(token: str) -> str:
    """Normaliza tokens ya anotados.

    - Cambiamos cualquier verbo 'vrp:palabra' a 'vrs:palabra' para
      eliminar la distinción singular/plural a nivel de tokens.
    - Dejamos el resto igual.
    """
    if ":" not in token:
        return token

    pref, word = token.split(":", 1)
    if pref == "vrp":
        pref = "vrs"

    return f"{pref}:{word}"


def annotate_source(source: str) -> str:
    """Devuelve una versión del `source` donde cada palabra lleva su tipo de token como prefijo.

    Comportamiento:
    - Si el texto ya viene anotado (det:/sus:/adj:/nom:/pre:/vrs:/vrp:),
      se normaliza solo para que cualquier 'vrp:' pase a 'vrs:' y se respeta lo demás.
    - Si el texto NO viene anotado:
        - El punto '.' y las palabras 'y' y 'no' se dejan sin prefijo (las reconoce el lexer).
        - El resto se clasifica automáticamente con _classify_word.
    """
    # Primero verificamos si hay al menos un token anotado
    has_annotated = False
    for line in source.splitlines():
        for raw in line.split():
            if any(raw.startswith(p) for p in _PREFIXES) or raw.startswith("vrp:"):
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

            if has_annotated and (word.startswith("vrp:") or word.startswith("vrs:") or any(word.startswith(p) for p in ("det:", "sus:", "adj:", "nom:", "pre:"))):
                # Normalizamos solo prefijo si es verbo plural
                normalized = _normalize_annotated_token(word)
                annotated_words.append(normalized)
            else:
                low = word.lower()

                # Palabras que el lexer ya conoce sin prefijo
                if low in ("y", "no", "."):
                    annotated_words.append(low)
                elif has_annotated and ":" in word:
                    # Otro token anotado que no cae en los prefijos conocidos,
                    # lo dejamos tal cual por seguridad.
                    annotated_words.append(word)
                else:
                    # Clasificación automática
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
