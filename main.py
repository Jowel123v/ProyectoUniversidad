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

