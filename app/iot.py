"""Recepción de lecturas de sensores IoT (ESP32, Arduino, etc.)."""
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from . import database

router = APIRouter(prefix="/api/iot", tags=["IoT"])

class Lectura(BaseModel):
    dispositivo: str
    humedad_suelo: float
    temperatura: Optional[float] = None
    ph: Optional[float] = None
    parcela_id: Optional[str] = None

@router.post("/lectura")
def recibir(l: Lectura):
    datos = l.model_dump(exclude_none=True)
    return database.guardar_lectura(datos)

@router.get("/lecturas")
def listar(limite: int = 50):
    return database.listar_lecturas(limite)
