"""Conexión a Supabase. Si no hay credenciales, funciona en modo demo (memoria)."""
import os
import uuid
from datetime import datetime, timezone

from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        from supabase import create_client
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:  # noqa: BLE001
        print(f"[database] No se pudo conectar a Supabase: {e}")

def _now():
    return datetime.now(timezone.utc).isoformat()

DEMO = {
    "parcelas": [
        {"id": "demo-1", "nombre": "Parcela Norte", "cultivo_actual": "Papa",
         "hectareas": 2.5, "latitud": -9.93, "longitud": -76.24, "created_at": _now()},
    ],
    "lecturas": [],
}

def modo() -> str:
    return "Supabase" if client else "Demo (memoria)"

def listar_parcelas():
    if client:
        return client.table("parcelas").select("*").order("created_at", desc=True).execute().data
    return DEMO["parcelas"]

def crear_parcela(datos: dict):
    if client:
        return client.table("parcelas").insert(datos).execute().data[0]
    fila = {**datos, "id": str(uuid.uuid4()), "created_at": _now()}
    DEMO["parcelas"].insert(0, fila)
    return fila

def guardar_lectura(datos: dict):
    if client:
        return client.table("lecturas_iot").insert(datos).execute().data[0]
    fila = {**datos, "id": str(uuid.uuid4()), "created_at": _now()}
    DEMO["lecturas"].insert(0, fila)
    return fila

def listar_lecturas(limite: int = 50):
    if client:
        return (client.table("lecturas_iot").select("*")
                .order("created_at", desc=True).limit(limite).execute().data)
    return DEMO["lecturas"][:limite]
