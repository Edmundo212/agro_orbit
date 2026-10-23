# Simulador IoT de AgroOrbit en Wokwi

El ESP32 simula lecturas de humedad del suelo, temperatura y pH, y las envía cada
5 segundos a `POST /api/iot/lectura`. No se necesitan sensores físicos.

## Conectar Wokwi con el dashboard local

1. Arranca AgroOrbit desde la carpeta del proyecto:

   ```powershell
   python -m uvicorn app.main:app --reload --port 8000
   ```

2. Crea un proyecto nuevo de ESP32 con Arduino en Wokwi y copia `sketch.ino` y
   `diagram.json` de esta carpeta.
3. Para enviar datos a tu computadora, activa el **Wokwi IoT Gateway privado**.
   El gateway privado de Wokwi es necesario para conectar con servicios locales;
   el gateway público no puede acceder a `localhost`. Ejecuta el gateway y, en
   el editor de Wokwi, usa `F1` → **Enable Private Wokwi IoT Gateway**.
4. Inicia la simulación y abre el monitor serie. Deberías ver respuestas HTTP
   `200` junto con cada lectura.
5. Abre `http://127.0.0.1:8000/iot`. La tabla se actualiza automáticamente.

El firmware usa `host.wokwi.internal:8000` para alcanzar el servidor local. Si
publicas AgroOrbit en un servidor accesible desde Internet, cambia `API_URL` en
`sketch.ino` por la URL HTTPS pública de ese servidor.
