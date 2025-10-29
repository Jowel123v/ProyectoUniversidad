from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class TableBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    is_deleted: bool = Field(default=False, exclude=True)

    class Config:
        extra = "forbid"
        validate_assignment = True

class Matricula(SQLModel, table=True):
    estudiante_id: Optional[int] = Field(default=None, foreign_key="estudiante.id", primary_key=True)
    curso_id: Optional[int] = Field(default=None, foreign_key="curso.id", primary_key=True)

class Estudiante(TableBase, table=True):
    __tablename__ = "estudiante"
    cedula: str = Field(index=True, unique=True, min_length=5, max_length=20, description="Documento único")
    nombre: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=5, max_length=120)
    semestre: int = Field(default=1, ge=1, le=10, description="Semestre (1–10)")
    cursos: List["Curso"] = Relationship(back_populates="estudiantes", link_model=Matricula)

class Curso(TableBase, table=True):
    __tablename__ = "curso"
    codigo: str = Field(index=True, unique=True, min_length=2, max_length=15, description="Código único")
    nombre: str = Field(min_length=1, max_length=100)
    creditos: int = Field(default=1, ge=1, le=10)
    horario: str = Field(default="", max_length=50, description="Ej: 'Lu 08-10'")
    estudiantes: List[Estudiante] = Relationship(back_populates="cursos", link_model=Matricula)

__all__ = ["Estudiante", "Curso", "Matricula", "TableBase"]
