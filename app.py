from fastapi import FastAPI
from routes.tareas import tareas_api


# Inicializando el servidor FastAPI
app = FastAPI(
    title="To-Do webapp ChromaDB",
    description="Aplicación construída únicamente en Python, para un sistema administrador de tareas basado en la web.",
    version="0.0.3",
    openapi_tags=[{
        "name": "tareas",
        "description": "Grupo de administración de tareas."
    }]
)


app.include_router(tareas_api)