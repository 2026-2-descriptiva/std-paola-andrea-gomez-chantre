"""
    Para cada valor distinto de la segunda columna (`value`), construya la
    lista de letras de la primera columna (`letter`) que aparecen con ese
    valor. Conserve las letras repetidas y el orden en que aparecen en el
    archivo. Retorne una lista de tuplas `(valor, letras)` ordenada por el
    valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["E", "B", "E"]), (2, ["A", "E"]), ...]
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


def pregunta_07():
    letras = {}
    for r in _leer_registros():
        letras.setdefault(r["value"], []).append(r["letter"])
    return sorted(letras.items())