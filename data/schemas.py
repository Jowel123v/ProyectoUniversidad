from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

# ESTUDIANTE
class EstudianteBase(BaseModel):
    cedula: str = Field(min_length=5, max_length=20)
    nombre: str = Field(min_length=1, max_length=100)
    email: EmailStr
    semestre: int = Field(ge=1, le=10)

class EstudianteCreate(EstudianteBase):
    pass

class EstudianteUpdate(BaseModel):
    cedula: Optional[str] = Field(default=None, min_length=5, max_length=20)
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    semestre: Optional[int] = Field(default=None, ge=1, le=10)

class EstudianteRead(EstudianteBase):
    id: int

# CURSO
class CursoBase(BaseModel):
    codigo: str = Field(min_length=2, max_length=15)
    nombre: str = Field(min_length=1, max_length=100)
    creditos: int = Field(ge=1, le=10)
    horario: Optional[str] = Field(default="", max_length=50)

class CursoCreate(CursoBase):
    pass

class CursoUpdate(BaseModel):
    codigo: Optional[str] = Field(default=None, min_length=2, max_length=15)
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=100)
    creditos: Optional[int] = Field(default=None, ge=1, le=10)
    horario: Optional[str] = Field(default=None, max_length=50)

class CursoRead(CursoBase):
    id: int

# MATRÍCULA
class MatriculaIn(BaseModel):
    estudiante_id: int
    curso_id: int
