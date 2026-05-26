from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
from pathlib import Path
from supabase import create_client, Client

# Definir la ruta exacta del archivo .env (en la carpeta raíz)
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Verificación de seguridad
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise ValueError("¡Error! Asegúrate de tener SUPABASE_URL y SUPABASE_KEY en tu archivo .env")

# Inicializar cliente
supabase: Client = create_client(url, key)

app = FastAPI(title="ScoreNow API")

@app.get("/")
def read_root():
    return {"message": "ScoreNow lista y a tu servicio, Lord Aly!"}

@app.get("/teams")
def get_teams():
    """Endpoint para listar todos los equipos desde Supabase"""
    try:
        response = supabase.table("teams").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al conectar con Supabase: {str(e)}")

@app.post("/add-team")
def add_team(name: str, country: str):
    """Inserta un equipo nuevo en la tabla"""
    try:
        data = {"name": name, "country": country}
        response = supabase.table("teams").insert(data).execute()
        return {"message": "Equipo agregado", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar equipo: {str(e)}")