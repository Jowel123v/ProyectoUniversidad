from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


# Base común: ID autoincremental + soft delete

class TableBase(SQLModel):
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"autoincrement": True}
    )
    # Campo interno para borrado lógico (no se expone en JSON)
    is_deleted: bool = Field(default=False, exclude=True)

    class Config:
        extra = "forbid"
        validate_assignment = True

# TABLA N:M  Estudiante - Curso (Matrícula)
# (estudiante_id, curso_id) evita duplicados

class Matricula(SQLModel, table=True):
    estudiante_id: Optional[int] = Field(
        default=None, foreign_key="estudiante.id", primary_key=True
    )
    curso_id: Optional[int] = Field(
        default=None, foreign_key="curso.id", primary_key=True
    )

# MODELO 1: ESTUDIANTE

class Estudiante(TableBase, table=True):
    __tablename__ = "estudiante"

    cedula: str = Field(
        index=True,
        unique=True,
        description="Documento único del estudiante",
        min_length=5,
        max_length=20,
    )
    nombre: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=5, max_length=120, description="Correo institucional o personal")
    semestre: int = Field(default=1, ge=1, le=10, description="Semestre (1–10)")

    # Relación N:M con Curso vía Matricula (link_model)
    cursos: List["Curso"] = Relationship(
        back_populates="estudiantes",
        link_model=Matricula
    )


# MODELO 2: CURSO

class Curso(TableBase, table=True):
    __tablename__ = "curso"

    codigo: str = Field(
        index=True,
        unique=True,
        description="Código único del curso",
        min_length=2,
        max_length=15,
    )
    nombre: str = Field(min_length=1, max_length=100)
    creditos: int = Field(default=1, ge=1, le=10)
    horario: str = Field(default="", max_length=50, description="Ej: 'Lu 08-10'")

    # Relación N:M con Estudiante vía Matricula (link_model)
    estudiantes: List[Estudiante] = Relationship(
        back_populates="cursos",
        link_model=Matricula
    )


# Exportaciones públicas
__all__ = ["Estudiante", "Curso", "Matricula", "TableBase"]
