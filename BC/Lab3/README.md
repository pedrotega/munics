# Smart Exam
## Aplicacicón descentralizada parala gestión de exámenes

## Autores:
* Luis Corbacho Flores
* Javier Español Alfonso
* Pedro Otero García

###
- [Contratos](#id1) 📜
    - [Contrato SmartExamBase](#id1_1)
    - [Contrato SmartExam](#id1_2)
- [Demostración](#id2) 📺
###

<div id="id1" />

## Contratos 📜

<div id="id1_1" />

### Contrato SmartExamBase

#### Parámetros

El contrato se inicializa con varios parámetros que definen la estructura del examen:
- **Statement**: Representa el hash del archivo real del examen para evitar manipulaciones.
- **Fechas**: `dateLastUpload`, `dateExam` y `dateStartExam` definen marcas de tiempo para la última carga, fecha del examen y fecha real de inicio del examen, respectivamente.
- **Duración**: Indica la duración del examen en minutos.
- **Precio de Inscripción**: Denota el precio para inscribirse en el examen, almacenado en `wei`.

#### Estructuras y Mapas

- **Struct de Estudiante**: Contiene información relacionada con las entregas de los estudiantes, correcciones y puntuaciones.
- **Mapass**: `_professors` almacena las direcciones de los profesores; `_students` mapea las direcciones de los estudiantes con sus datos respectivos; `_studAdds` es un vector de direcciones de estudiantes; `_correctionCIDs` es otro vecotr que almacena CIDs para las correcciones.

#### Modificadores

- `onlyProfessor`: Restringe el acceso a funciones solo para profesores.
- `checkStudent`: Asegura que un estudiante exista dentro del contrato.
- `checkSubmission`: Requiere que exista una entrega por parte de un estudiante.
- `checkNOTSubmission`: Requiere que NO exista una entrega por parte de un estudiante.

#### Control de Acceso

- **Funciones del Propietario**: Permiten al propietario gestionar profesores (`addProfessor` y `deleteProfessor`), editar parámetros de exámenes (`editExamParameters`), iniciar exámenes (`startExam`) y retirar fondos (`widthdraw`).
- **Funciones de Visualización**: `isOwner`, `isProfessor` e `isStudentEnrolled` permiten verificar la propiedad, ser profesor y el estado de inscripción de un estudiante, respectivamente.
- **Obtener Enunciado** (`getStatement()`): Permite al propietario, profesores y estudiantes inscritos acceder al CID del enunciado.

> [!NOTE]
>

<div id="id1_2" />

### Contrato SmartExam


#### Funciones para Profesores

- **Obtener Estudiantes**: `getStudents` permite a un profesor obtener las direcciones de los estudiantes inscritos.
- **Obtener Entrega de un Estudiante**: `getStudentSubmission` permite a un profesor obtener el CID de la entrega de un estudiante a partir de su dirección.
- **Añadir Corrección**: `setCorrection` permite a un profesor agregar una corrección para un examen, junto con una puntuación.
- **Obtener Correcciones**: `getCorrections` permite a un profesor obtener todos los CIDs de correcciones realizadas.

#### Funciones para Estudiantes

- **Inscripción en el Examen**: `enroll` permite a un estudiante inscribirse en un examen pagando la tarifa correspondiente.
- **Establecer Entrega**: `setSubmission` permite a un estudiante almacenar el CID de su entrega.
- **Obtener Entrega Propia**: `getMyExam` devuelve el CID de la entrega de un estudiante.
- **Obtener Corrección Propia**: `getMyCorrection` devuelve el CID de la corrección de un estudiante.
- **Obtener Puntuación Propia**: `getMyScore` devuelve la puntuación de un estudiante.
- **Certificado de Estudiante**: `certificateStudent` confirma si un estudiante ha aprobado o no.


