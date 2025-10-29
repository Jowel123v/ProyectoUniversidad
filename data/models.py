from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# Base común
class TableBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    is_deleted: bool = Field(default=False, exclude=True)

    class Config:
        extra = "forbid"
        validate_assignment = True

# PERIODO
class Periodo(TableBase, table=True):
    __tablename__ = "periodo"

    anio: int = Field(ge=2000, le=2100, description="Año académico")
    numero: int = Field(ge=1, le=3, description="Número de periodo (1, 2 o 3)")
    activo: bool = Field(default=False)

    # Relación inversa
    matriculas: List["Matricula"] = Relationship(back_populates="periodo")

# MATRÍCULA tabla N:M
class Matricula(SQLModel, table=True):
    # Clave primaria compuesta: estudiante-curso-periodo
    estudiante_id: Optional[int] = Field(default=None, foreign_key="estudiante.id", primary_key=True)
    curso_id: Optional[int] = Field(default=None, foreign_key="curso.id", primary_key=True)
    periodo_id: Optional[int] = Field(default=None, foreign_key="periodo.id", primary_key=True)

    # Relaciones inversas
    estudiante: "Estudiante" = Relationship(back_populates="cursos")
    curso: "Curso" = Relationship(back_populates="estudiantes")
    periodo: "Periodo" = Relationship(back_populates="matriculas")

# ESTUDIANTE
class Estudiante(TableBase, table=True):
    __tablename__ = "estudiante"

    cedula: str = Field(index=True, unique=True, description="Documento único")
    nombre: str
    email: str
    semestre: int = Field(default=1, ge=1, le=10)

    # N:M con Curso vía Matricula (link_model)
    cursos: List["Curso"] = Relationship(back_populates="estudiantes", link_model=Matricula)

# CURSO
class Curso(TableBase, table=True):
    __tablename__ = "curso"

    codigo: str = Field(index=True, unique=True, description="Código único del curso")
    nombre: str
    creditos: int = Field(default=1, ge=1, le=10)
    horario: str = Field(default="", description="Ej: 'Lu 08-10'")

    # N:M con Estudiante vía Matricula (link_model)
    estudiantes: List[Estudiante] = Relationship(back_populates="cursos", link_model=Matricula)

__all__ = ["Estudiante", "Curso", "Matricula", "Periodo", "TableBase"]
