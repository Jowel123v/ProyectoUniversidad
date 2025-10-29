from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import SQLModel, Session, create_engine

# MODELOS (ORM) y SCHEMAS (Pydantic)
from data.models import Estudiante, Curso
from data.schemas import (
    EstudianteCreate, EstudianteUpdate, EstudianteRead,
    CursoCreate, CursoUpdate, CursoRead,
)

# OPERACIONES
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

# FASTAPI
app = FastAPI(
    title="Sistema de Gestión Universitaria",
    description="API para gestionar estudiantes, cursos y matrículas (N:M) en una universidad",
    version="1.0.0",
)

@app.on_event("startup")
def on_startup():
    crear_db()

# ROOT / HEALTH
@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Bienvenido al Sistema de Gestión Universitaria",
        "docs": "/docs",
        "endpoints": ["/estudiantes", "/cursos", "/matriculas"],
    }

@app.get("/health", tags=["Root"])
def health():
    return {"status": "ok"}

# ESTUDIANTES

@app.post("/estudiantes/", response_model=EstudianteRead, status_code=201, tags=["Estudiantes"])

@app.post("/estudiantes/", response_model=EstudianteRead, status_code=201, tags=["Estudiantes"])
def crear_nuevo_estudiante(obj: EstudianteCreate, session: Session = Depends(get_session)):
    est = crear_estudiante(session, obj)  # ahora retorna el objeto con id
    return est


@app.get("/estudiantes/", response_model=List[EstudianteRead], tags=["Estudiantes"])
def listar_todos_los_estudiantes(
    skip: int = 0,
    limit: int = Query(10, le=100),
    include_deleted: bool = Query(False, description="Incluir eliminados lógicamente"),
    semestre: Optional[int] = Query(None, ge=1, le=10),
    nombre: Optional[str] = None,
    session: Session = Depends(get_session)
):
    return listar_estudiantes(session, skip, limit, include_deleted, semestre, nombre)

@app.get("/estudiantes/deleted", response_model=List[EstudianteRead], tags=["Estudiantes"])
def listar_estudiantes_borrados(session: Session = Depends(get_session)):
    return listar_estudiantes_eliminados(session)

@app.post("/estudiantes/{estudiante_id}/restore", tags=["Estudiantes"])
def restaurar_estudiante_por_id(estudiante_id: int, session: Session = Depends(get_session)):
    if restaurar_estudiante(session, estudiante_id):
        return {"message": "Estudiante restaurado correctamente (200)"}
    raise HTTPException(status_code=404, detail="Estudiante no encontrado para restaurar")

@app.get("/estudiantes/search/", response_model=List[EstudianteRead], tags=["Estudiantes"])
def buscar_estudiante(nombre: str = Query(..., min_length=1), session: Session = Depends(get_session)):
    return buscar_estudiante_por_nombre(session, nombre)

@app.get("/estudiantes/{estudiante_id}", response_model=EstudianteRead, tags=["Estudiantes"])
def obtener_estudiante_por_id(estudiante_id: int, session: Session = Depends(get_session)):
    return obtener_estudiante(session, estudiante_id)

@app.patch("/estudiantes/{estudiante_id}", response_model=EstudianteRead, tags=["Estudiantes"])
def actualizar_datos_estudiante(estudiante_id: int, obj: EstudianteUpdate, session: Session = Depends(get_session)):
    return actualizar_estudiante(session, estudiante_id, obj)

@app.delete("/estudiantes/{estudiante_id}", tags=["Estudiantes"])
def eliminar_estudiante_por_id(estudiante_id: int, session: Session = Depends(get_session)):
    if eliminar_estudiante(session, estudiante_id):
        return {"message": "Estudiante eliminado (Historial)"}
    raise HTTPException(status_code=404, detail="Estudiante no encontrado")

# CURSOS

@app.post("/cursos/", response_model=CursoRead, status_code=201, tags=["Cursos"])
def crear_nuevo_curso(obj: CursoCreate, session: Session = Depends(get_session)):
    crear_curso(session, obj)
    # Devolvemos un 201 con el recurso; para simplicidad, el operations retorna payload sin id.
    # Puedes recuperar el curso por 'codigo' si necesitas devolver con id.
    # Aquí devolvemos el último creado consultando por 'codigo' único:
    cursos = buscar_curso_por_nombre(session, obj.nombre)
    return cursos[-1] if cursos else {"message": "Curso creado (201)"}

@app.get("/cursos/", response_model=List[CursoRead], tags=["Cursos"])
def listar_todos_los_cursos(
    skip: int = 0,
    limit: int = Query(10, le=100),
    include_deleted: bool = Query(False, description="Incluir eliminados lógicamente"),
    creditos: Optional[int] = None,
    codigo: Optional[str] = None,
    nombre: Optional[str] = None,
    session: Session = Depends(get_session)
):
    return listar_cursos(session, skip, limit, include_deleted, creditos, codigo, nombre)

@app.get("/cursos/deleted", response_model=List[CursoRead], tags=["Cursos"])
def listar_cursos_borrados(session: Session = Depends(get_session)):
    return listar_cursos_eliminados(session)

@app.post("/cursos/{curso_id}/restore", tags=["Cursos"])
def restaurar_curso_por_id(curso_id: int, session: Session = Depends(get_session)):
    if restaurar_curso(session, curso_id):
        return {"message": "Curso restaurado correctamente (200)"}
    raise HTTPException(status_code=404, detail="Curso no encontrado para restaurar")

@app.get("/cursos/search/", response_model=List[CursoRead], tags=["Cursos"])
def buscar_curso(nombre: str = Query(..., min_length=1), session: Session = Depends(get_session)):
    return buscar_curso_por_nombre(session, nombre)

@app.get("/cursos/{curso_id}", response_model=CursoRead, tags=["Cursos"])
def obtener_curso_por_id(curso_id: int, session: Session = Depends(get_session)):
    return obtener_curso(session, curso_id)

@app.patch("/cursos/{curso_id}", response_model=CursoRead, tags=["Cursos"])
def actualizar_datos_curso(curso_id: int, obj: CursoUpdate, session: Session = Depends(get_session)):
    return actualizar_curso(session, curso_id, obj)

@app.delete("/cursos/{curso_id}", tags=["Cursos"])
def eliminar_curso_por_id(curso_id: int, session: Session = Depends(get_session)):
    if eliminar_curso(session, curso_id):
        return {"message": "Curso eliminado lógicamente (200)"}
    raise HTTPException(status_code=404, detail="Curso no encontrado")

# MATRÍCULAS (N:M)

@app.post("/matriculas/", tags=["Matrículas"], status_code=201)
def crear_matricula(estudiante_id: int, curso_id: int, session: Session = Depends(get_session)):
    return matricular(session, estudiante_id, curso_id)

@app.delete("/matriculas/", tags=["Matrículas"])
def eliminar_matricula(estudiante_id: int, curso_id: int, session: Session = Depends(get_session)):
    return desmatricular(session, estudiante_id, curso_id)

@app.get("/estudiantes/{estudiante_id}/cursos", response_model=List[CursoRead], tags=["Matrículas"])
def obtener_cursos_estudiante(estudiante_id: int, session: Session = Depends(get_session)):
    return cursos_de_estudiante(session, estudiante_id)

@app.get("/cursos/{curso_id}/estudiantes", response_model=List[EstudianteRead], tags=["Matrículas"])
def obtener_estudiantes_curso(curso_id: int, session: Session = Depends(get_session)):
    return estudiantes_de_curso(session, curso_id)
