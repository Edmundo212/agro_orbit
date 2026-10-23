"""Datos NASA POWER (gratis, sin API key): precipitación, humedad de suelo y temperatura.
NDVI se estima a partir de la humedad (para NDVI real de MODIS usa NASA AppEEARS)."""
import random
from datetime import date, timedelta

import httpx

URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

def _limpiar(v):
    return None if v is None or v <= -900 else v

def _demo(lat, lon, dias):
    random.seed(int(abs(lat * 100 + lon * 100)))
    hoy = date.today()
    filas = []
    for i in range(dias):
        h = round(min(1, max(0.1, 0.5 + random.uniform(-0.2, 0.2))), 2)
        filas.append({
            "fecha": (hoy - timedelta(days=dias - i)).isoformat(),
            "humedad": h,
            "precipitacion": round(max(0, random.gauss(4, 4)), 1),
            "temperatura": round(random.uniform(12, 20), 1),
            "ndvi": round(min(0.9, 0.2 + 0.6 * h), 2),
        })
    return {"fuente": "Datos de demostración (NASA no disponible)", "datos": filas}

async def obtener_clima(lat: float, lon: float, dias: int = 14):
    fin = date.today() - timedelta(days=3)  # POWER tiene ~2-3 días de retraso
    ini = fin - timedelta(days=dias - 1)
    params = {
        "parameters": "PRECTOTCORR,GWETROOT,T2M",
        "community": "AG", "latitude": lat, "longitude": lon,
        "start": ini.strftime("%Y%m%d"), "end": fin.strftime("%Y%m%d"), "format": "JSON",
    }
    try:
        async with httpx.AsyncClient(timeout=25) as c:
            r = await c.get(URL, params=params)
            r.raise_for_status()
        p = r.json()["properties"]["parameter"]
        filas = []
        for f in sorted(p["T2M"].keys()):
            h = _limpiar(p["GWETROOT"].get(f))
            pr = _limpiar(p["PRECTOTCORR"].get(f))
            t = _limpiar(p["T2M"].get(f))
            if h is None:
                continue
            filas.append({
                "fecha": f"{f[:4]}-{f[4:6]}-{f[6:]}",
                "humedad": round(h, 2),
                "precipitacion": round(pr or 0, 1),
                "temperatura": round(t or 0, 1),
                "ndvi": round(min(0.9, 0.2 + 0.6 * h), 2),
            })
        if not filas:
            return _demo(lat, lon, dias)
        return {"fuente": "NASA POWER (NDVI estimado)", "datos": filas}
    except Exception:  # noqa: BLE001
        return _demo(lat, lon, dias)
