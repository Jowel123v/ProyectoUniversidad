from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import SQLModel, Session, create_engine

# MODELOS
from data.models import Estudiante, Curso

# OPERACIONES (con soft delete, restaurar, búsquedas y filtros)

from operations.operations_db import (
    # ESTUDIANTES
    crear_estudiante, listar_estudiantes, listar_estudiantes_eliminados, restaurar_estudiante,
    buscar_estudiante_por_nombre, obtener_estudiante, actualizar_estudiante, eliminar_estudiante,

    # CURSOS
    crear_curso, listar_cursos, listar_cursos_eliminados, restaurar_curso,
    buscar_curso_por_nombre, obtener_curso, actualizar_curso, eliminar_curso,

    # MATRÍCULAS
    matricular, desmatricular, cursos_de_estudiante, estudiantes_de_curso
)

# CONFIGURACIÓN BASE DE DATOS

DATABASE_URL = "sqlite:///database_universidad.db"
engine = create_engine(DATABASE_URL, echo=False)

def crear_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI(
    title="Sistema de Gestión Universitaria",
    description="API para gestionar estudiantes, cursos y matrículas (N:M) en una universidad",
    version="1.0.0",
)

@app.on_event("startup")
def on_startup():
    crear_db()

# ROOT

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Bienvenido al Sistema de Gestión Universitaria",
        "docs": "/docs",
        "endpoints": [
            "/estudiantes",
            "/cursos",
            "/matriculas",
        ],
    }

@app.get("/health", tags=["Root"])
def health():
    return {"status": "ok"}

# ESTUDIANTES

@app.post("/estudiantes/", response_model=Estudiante, tags=["Estudiantes"])
def crear_nuevo_estudiante(obj: Estudiante, session: Session = Depends(get_session)):
    return crear_estudiante(session, obj)

@app.get("/estudiantes/", response_model=List[Estudiante], tags=["Estudiantes"])
def listar_todos_los_estudiantes(
    skip: int = 0,
    limit: int = Query(10, le=100),
    include_deleted: bool = Query(False, description="Incluir eliminados lógicamente"),
    semestre: Optional[int] = Query(None, ge=1, le=10),
    nombre: Optional[str] = None,
    session: Session = Depends(get_session)
):
    return listar_estudiantes(session, skip, limit, include_deleted, semestre, nombre)

@app.get("/estudiantes/deleted", response_model=List[Estudiante], tags=["Estudiantes"])
def listar_estudiantes_borrados(session: Session = Depends(get_session)):
    return listar_estudiantes_eliminados(session)

@app.post("/estudiantes/{estudiante_id}/restore", tags=["Estudiantes"])
def restaurar_estudiante_por_id(estudiante_id: int, session: Session = Depends(get_session)):
    if restaurar_estudiante(session, estudiante_id):
        return {"message": "Estudiante restaurado correctamente"}
    raise HTTPException(status_code=404, detail="No fue posible restaurar el estudiante")

@app.get("/estudiantes/search/", response_model=List[Estudiante], tags=["Estudiantes"])
def buscar_estudiante(nombre: str = Query(..., min_length=1), session: Session = Depends(get_session)):
    return buscar_estudiante_por_nombre(session, nombre)

@app.get("/estudiantes/{estudiante_id}", response_model=Estudiante, tags=["Estudiantes"])
def obtener_estudiante_por_id(estudiante_id: int, session: Session = Depends(get_session)):
    return obtener_estudiante(session, estudiante_id)

@app.put("/estudiantes/{estudiante_id}", response_model=Estudiante, tags=["Estudiantes"])
def actualizar_datos_estudiante(estudiante_id: int, obj: Estudiante, session: Session = Depends(get_session)):
    return actualizar_estudiante(session, estudiante_id, obj)

@app.delete("/estudiantes/{estudiante_id}", tags=["Estudiantes"])
def eliminar_estudiante_por_id(estudiante_id: int, session: Session = Depends(get_session)):
    if eliminar_estudiante(session, estudiante_id):
        return {"message": "Estudiante eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Estudiante no encontrado")