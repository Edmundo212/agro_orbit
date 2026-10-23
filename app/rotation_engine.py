"""Motor de rotación de cultivos multiobjetivo (suelo, agua, ingreso)."""
from itertools import product

# n: efecto en nitrógeno (-1 extrae, 0 neutro, 2 fija) | agua: 1-3 | ingreso: 1-4
CULTIVOS = {
    "Papa":     {"familia": "Solanáceas",    "n": -1, "agua": 3, "ingreso": 4},
    "Maíz":     {"familia": "Poáceas",       "n": -1, "agua": 3, "ingreso": 3},
    "Frijol":   {"familia": "Fabáceas",      "n": 2,  "agua": 2, "ingreso": 3},
    "Arveja":   {"familia": "Fabáceas",      "n": 2,  "agua": 2, "ingreso": 2},
    "Haba":     {"familia": "Fabáceas",      "n": 2,  "agua": 2, "ingreso": 2},
    "Quinua":   {"familia": "Amarantáceas",  "n": 0,  "agua": 1, "ingreso": 4},
    "Cebada":   {"familia": "Poáceas",       "n": -1, "agua": 1, "ingreso": 2},
    "Zanahoria": {"familia": "Apiáceas",     "n": 0,  "agua": 2, "ingreso": 3},
}

PERFILES = {
    "Equilibrado":      {"suelo": 0.34, "agua": 0.33, "ingreso": 0.33},
    "Salud del suelo":  {"suelo": 0.60, "agua": 0.20, "ingreso": 0.20},
    "Ahorro de agua":   {"suelo": 0.20, "agua": 0.60, "ingreso": 0.20},
    "Máximo ingreso":   {"suelo": 0.15, "agua": 0.15, "ingreso": 0.70},
}

def _puntajes(seq, humedad):
    c = [CULTIVOS[x] for x in seq]
    suelo = sum((x["n"] + 1) / 3 for x in c) / len(c)
    agua = sum(1 - ((x["agua"] - 1) / 2) * (1 - humedad) for x in c) / len(c)
    ingreso = sum((x["ingreso"] - 1) / 3 for x in c) / len(c)
    return {"suelo": suelo, "agua": agua, "ingreso": ingreso}

def _valida(seq, anterior):
    familias = [CULTIVOS[x]["familia"] for x in seq]
    if anterior in CULTIVOS and CULTIVOS[anterior]["familia"] == familias[0]:
        return False
    return all(familias[i] != familias[i + 1] for i in range(len(familias) - 1))

def generar_escenarios(anterior: str = "", humedad: float = 0.5, temporadas: int = 3):
    humedad = min(1.0, max(0.0, humedad))
    candidatas = [s for s in product(CULTIVOS, repeat=temporadas) if _valida(s, anterior)]
    resultado = []
    for nombre, pesos in PERFILES.items():
        mejor, mejor_total, mejor_p = None, -1, None
        for seq in candidatas:
            p = _puntajes(seq, humedad)
            total = sum(p[k] * pesos[k] for k in pesos)
            if total > mejor_total:
                mejor, mejor_total, mejor_p = seq, total, p
        resultado.append({
            "escenario": nombre,
            "secuencia": list(mejor),
            "total": round(mejor_total * 100),
            "suelo": round(mejor_p["suelo"] * 100),
            "agua": round(mejor_p["agua"] * 100),
            "ingreso": round(mejor_p["ingreso"] * 100),
        })
    return resultado
