"""
    Repita la pregunta 7, pero ahora cada lista de letras debe contener cada
    letra una sola vez y estar ordenada alfabéticamente. Retorne una lista de
    tuplas `(valor, letras)` ordenada por el valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["B", "E"]), (2, ["A", "E"]), ...]
"""

import gzip


def _leer_registros(ruta="data/data.csv.gz"):
    registros = []
    with gzip.open(ruta, "rt", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            letter, value, date, codes, metrics = linea.split("\t")
            registros.append(
                {
                    "letter": letter,
                    "value": int(value),
                    "date": date,
                    "codes": codes.split(","),
                    "metrics": [
                        (clave, int(valor))
                        for clave, valor in (par.split(":") for par in metrics.split(","))
                    ],
                }
            )
    return registros


def pregunta_08():
    letras = {}
    for r in _leer_registros():
        letras.setdefault(r["value"], set()).add(r["letter"])
    return [(valor, sorted(l)) for valor, l in sorted(letras.items())]