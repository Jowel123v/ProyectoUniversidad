from typing import List, Optional, Dict, Any
from sqlmodel import Session, select
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from data.models import (
    Estudiante,
    Curso,
    Matricula,
    Periodo,
)

# HELPERS

def _apply_active_filter(model, include_deleted: bool = False):
    """Condición para incluir/excluir eliminados lógicamente."""
    if include_deleted:
        return True
    return model.is_deleted == False  # noqa: E712

def _handle_exception(session: Session, exc: Exception, message: str):
    """Rollback y excepción HTTP unificada."""
    session.rollback()
    raise HTTPException(status_code=500, detail=f"{message}. Error: {str(exc)}")

def _created_payload(obj) -> Dict[str, Any]:
    """
    Respuesta para CREATE:
    - oculta 'id' y 'is_deleted' (aunque is_deleted ya está oculto por el modelo)
    """
    return obj.dict(exclude={"id", "is_deleted"})


# ESTUDIANTES (CREAR + BUSQUEDA)

def crear_estudiante(session: Session, obj: Estudiante) -> Dict[str, Any]:
    try:
        obj.id = None
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return _created_payload(obj)
    except SQLAlchemyError as e:
        _handle_exception(session, e, "Error al crear el estudiante")

def listar_estudiantes(
    session: Session,
    skip: int = 0,
    limit: int = 10,
    include_deleted: bool = False,
    semestre: Optional[int] = None,
    nombre: Optional[str] = None,
) -> List[Estudiante]:
    try:
        q = select(Estudiante).where(_apply_active_filter(Estudiante, include_deleted))
        if semestre is not None:
            q = q.where(Estudiante.semestre == semestre)
        if nombre:
            q = q.where(Estudiante.nombre.ilike(f"%{nombre}%"))
        q = q.offset(skip).limit(limit)
        return session.exec(q).all()
    except SQLAlchemyError as e:
        _handle_exception(session, e, "Error al listar estudiantes")

def obtener_estudiante(session: Session, estudiante_id: int) -> Estudiante:
    try:
        obj = session.get(Estudiante, estudiante_id)
        if not obj or obj.is_deleted:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado o eliminado")
        return obj
    except SQLAlchemyError as e:
        _handle_exception(session, e, "Error al obtener estudiante")

def buscar_estudiante_por_nombre(session: Session, nombre: str) -> List[Estudiante]:
    try:
        q = select(Estudiante).where(
            Estudiante.nombre.ilike(f"%{nombre}%"),
            Estudiante.is_deleted == False,  # noqa: E712
        )
        resultados = session.exec(q).all()
        if not resultados:
            raise HTTPException(status_code=404, detail=f"No se encontraron estudiantes con '{nombre}'")
        return resultados
    except SQLAlchemyError as e:
        _handle_exception(session, e, "Error al buscar estudiantes por nombre")

def actualizar_estudiante(session: Session, estudiante_id: int, obj_update: Estudiante) -> Estudiante:
    try:
        obj = session.get(Estudiante, estudiante_id)
        if not obj or obj.is_deleted:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado o eliminado")

        data = obj_update.dict(exclude_unset=True)
        data.pop("id", None)
        data.pop("is_deleted", None)

        for k, v in data.items():
            setattr(obj, k, v)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj
    except SQLAlchemyError as e:
        _handle_exception(session, e, "Error al actualizar estudiante")
