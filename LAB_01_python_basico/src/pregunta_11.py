"""
    La cuarta columna (`codes`) contiene letras minúsculas separadas por
    comas. Para cada una de esas letras, sume los valores de la segunda
    columna (`value`) de los registros en los que aparece. Retorne un
    diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"a": 122, "b": 49, "c": 91, ...}
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


def pregunta_11():
    sumas = {}
    for r in _leer_registros():
        for codigo in r["codes"]:
            sumas[codigo] = sumas.get(codigo, 0) + r["value"]
    return dict(sorted(sumas.items()))