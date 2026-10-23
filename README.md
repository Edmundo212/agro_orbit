# AgroOrbit 🛰️
Python (FastAPI) + Dashboard HTML/CSS/JS + Supabase.

## Correr local
```bash
pip install -r requirements.txt
cp .env.example .env     # opcional: pega tu URL y KEY de Supabase
uvicorn app.main:app --reload --port 8000
```
Abre http://localhost:8000 (sin Supabase funciona en modo demo).

## Supabase
1. Crea un proyecto en https://supabase.com
2. SQL Editor -> pega `supabase_schema.sql` -> Run
3. Settings -> API -> copia `Project URL` y `anon key` al `.env`

## Render
- Build: `pip install -r requirements.txt`
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Variables de entorno: `SUPABASE_URL`, `SUPABASE_KEY`

## Enviar datos desde un sensor
```bash
curl -X POST http://localhost:8000/api/iot/lectura \
  -H "Content-Type: application/json" \
  -d '{"dispositivo":"esp32-01","humedad_suelo":42,"temperatura":17.5,"ph":6.4}'
```
