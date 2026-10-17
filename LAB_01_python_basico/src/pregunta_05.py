"""
    Para cada letra de la primera columna (`letter`), encuentre el valor
    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 9, 2), ("B", 9, 1), ...]
         
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


def pregunta_05():
    valores = {}
    for r in _leer_registros():
        valores.setdefault(r["letter"], []).append(r["value"])
    return [(letra, max(v), min(v)) for letra, v in sorted(valores.items())]