"""AgroOrbit – Backend FastAPI + Dashboard HTML + Supabase."""
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from . import database, iot, nasa_data, rotation_engine

BASE = Path(__file__).parent
app = FastAPI(title="AgroOrbit")
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")
templates = Jinja2Templates(directory=BASE / "templates")
app.include_router(iot.router)

def ctx(**kw):
    return {"modo": database.modo(), **kw}

# ---------- Páginas ----------
@app.get("/")
def inicio(request: Request):
    return templates.TemplateResponse(request, "index.html", ctx(
        n_parcelas=len(database.listar_parcelas()),
        n_lecturas=len(database.listar_lecturas(500)),
        pagina="inicio"))

@app.get("/nasa")
def pagina_nasa(request: Request):
    return templates.TemplateResponse(request, "nasa.html", ctx(pagina="nasa"))

@app.get("/rotaciones")
def pagina_rot(request: Request):
    return templates.TemplateResponse(request, "rotaciones.html", ctx(
        cultivos=list(rotation_engine.CULTIVOS), pagina="rotaciones"))

@app.get("/iot")
def pagina_iot(request: Request):
    return templates.TemplateResponse(request, "iot.html", ctx(pagina="iot"))

@app.get("/parcelas")
def pagina_parcelas(request: Request):
    return templates.TemplateResponse(request, "parcelas.html", ctx(
        parcelas=database.listar_parcelas(),
        cultivos=list(rotation_engine.CULTIVOS), pagina="parcelas"))

@app.post("/parcelas")
def crear_parcela(nombre: str = Form(...), cultivo_actual: str = Form(""),
                  hectareas: float = Form(1), latitud: float = Form(-9.93),
                  longitud: float = Form(-76.24)):
    database.crear_parcela({"nombre": nombre, "cultivo_actual": cultivo_actual,
                            "hectareas": hectareas, "latitud": latitud, "longitud": longitud})
    return RedirectResponse("/parcelas", status_code=303)

# ---------- APIs ----------
@app.get("/api/nasa")
async def api_nasa(lat: float = -9.93, lon: float = -76.24, dias: int = 14):
    return await nasa_data.obtener_clima(lat, lon, dias)

class PedidoRotacion(BaseModel):
    anterior: Optional[str] = ""
    humedad: float = 0.5

@app.post("/api/rotaciones")
def api_rotaciones(p: PedidoRotacion):
    return rotation_engine.generar_escenarios(p.anterior or "", p.humedad)
