from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routes.tarea_ruta import tareas


app = FastAPI(
    title="To Do list web app",
    description="Aplicación similar al primer proyecto del curso, con la diferencia de que este proyecto contiene IA para vectorizar las palabras a un lenguaje más entendible y pueda contestar de vuelta.",
    version="0.0.2",
    openapi_tags=[{
        "name": "tareas",
        "description": "Grupo de administración de tareas."
    }]
)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def server_index():
    return FileResponse("static/index.html")

app.include_router(tareas)