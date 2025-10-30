# Sistema de Gestión de Universidad

Aplicación **FastAPI + SQLModel** para gestionar cursos, estudiantes y matrículas en una universidad.

---

## Descripción

El sistema permite registrar y administrar información de **cursos**, **estudiantes** y sus **matrículas**.  
Un curso puede tener **muchos estudiantes**, y un estudiante puede estar inscrito en **muchos cursos** (relación N:M).

### Funcionalidades principales:
- Registrar cursos (código, nombre, créditos, horario)
- Registrar estudiantes (cédula, nombre, email, semestre)
- Consultar cursos de un estudiante
- Consultar estudiantes de un curso
- Gestionar matrículas (inscripción y cancelación)

---

## Requisitos

- Python 3.10+
- FastAPI
- SQLModel
- Uvicorn

Instalar dependencias:
```bash
pip install -r requirements.txt
```
Ejecutar
```bash
python -m fastapi dev main.py
```

## Estructura de carpetas
```bash
app/
 ├── db.py              # Conexión y creación de base de datos
 ├── models.py          # Modelos SQLModel: Estudiante, Curso, Matricula
 ├── operations.py      # CRUD de estudiantes, cursos y matrículas
 ├── operations_db.py   # Lógica de base de datos y relaciones
 ├── main.py            # Inicialización de la app FastAPI y routers
 └── helpers.py         # Manejo de excepciones y validaciones personalizadas
```
## Lógica de negocio
- La cédula del estudiante es única (no se permiten duplicados).

- El código del curso es único (no se puede repetir curso).

- Un estudiante no puede estar matriculado en dos cursos al mismo tiempo.

- Si se elimina un estudiante, también se eliminan sus matrículas (en cascada).

- Validación de integridad: no se permiten matrículas duplicadas.

## Mapa de Endpoints
## Estudiantes

| Método     | Ruta                | Descripción                              | Body / Parámetros                   | Respuesta esperada         |
| :--------- | :------------------ | :--------------------------------------- | :---------------------------------- | :------------------------- |
| **POST**   | `/estudiantes/`     | Crear estudiante                         | `{cedula, nombre, email, semestre}` | `201 Created`              |
| **GET**    | `/estudiantes/`     | Listar estudiantes (filtro por semestre) | `semestre=5`                         | `200 OK`                   |
| **GET**    | `/estudiantes/{id}` | Obtener estudiante y sus cursos          | —                                   | `200 OK` o `404 Not Found` |
| **PATCH**  | `/estudiantes/{id}` | Actualizar estudiante                    | Campos parciales                    | `200 OK`                   |
| **DELETE** | `/estudiantes/{id}` | Eliminar estudiante (y sus matrículas)   | —                                   | `200 OK`                   |

## Curso

| Método     | Ruta           | Descripción                                  | Body / Parámetros                     | Respuesta esperada |
| :--------- | :------------- | :------------------------------------------- | :------------------------------------ | :----------------- |
| **POST**   | `/cursos/`     | Crear curso                                  | `{codigo, nombre, creditos, horario}` | `201 Created`      |
| **GET**    | `/cursos/`     | Listar cursos (filtro por créditos o código) | `?creditos=3`                         | `200 OK`           |
| **GET**    | `/cursos/{id}` | Obtener curso con estudiantes matriculados   | —                                     | `200 OK`           |
| **PATCH**  | `/cursos/{id}` | Actualizar datos del curso                   | Campos parciales                      | `200 OK`           |
| **DELETE** | `/cursos/{id}` | Eliminar curso                               | —                                     | `200 OK`           |

## Matriculas

| Método     | Ruta                          | Descripción                       | Body / Parámetros           | Respuesta esperada             |
| :--------- | :---------------------------- | :-------------------------------- | :-------------------------- | :----------------------------- |
| **POST**   | `/matriculas/`                | Matricular estudiante en curso    | `{estudiante_id, curso_id}` | `201 Created` o `409 Conflict` |
| **DELETE** | `/matriculas/`                | Desmatricular estudiante de curso | `{estudiante_id, curso_id}` | `200 OK`                       |
| **GET**    | `/matriculas/curso/{id}`      | Consultar estudiantes de un curso | —                           | `200 OK`                       |
| **GET**    | `/matriculas/estudiante/{id}` | Consultar cursos de un estudiante | —                           | `200 OK`                       |

## Codigos de estado usados

| Código              | Significado                            | Cuándo se usa                           |
| :------------------ | :------------------------------------- | :-------------------------------------- |
| **200 OK**          | Petición exitosa                       | Consultas o actualizaciones correctas   |
| **201 Created**     | Recurso creado correctamente           | Nuevos estudiantes, cursos o matrículas |
| **400 Bad Request** | Error de validación o regla de negocio | Datos inválidos o duplicados            |
| **404 Not Found**   | Recurso no encontrado                  | ID inexistente                          |
| **409 Conflict**    | Conflicto con los datos existentes     | Matrícula o cédula duplicada            |
