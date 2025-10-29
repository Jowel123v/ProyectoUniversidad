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


# ESTUDIANTES (CREAR)


def crear_estudiante(session: Session, obj: Estudiante) -> Dict[str, Any]:
    try:
        obj.id = None
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return _created_payload(obj)
    except SQLAlchemyError as e:
        _handle_exception(session, e, "Error al crear el estudiante")