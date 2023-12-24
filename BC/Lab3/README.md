# Smart Exam
## Aplicacicón descentralizada parala gestión de exámenes

## Autores:
* Luis Corbacho Flores
* Javier Español Alfonso
* Pedro Otero García

###
- [Contenidos](#id0) 📚
- [Contratos](#id1) 📜
    - [Contrato SmartExamBase](#id1_1)
    - [Contrato SmartExam](#id1_2)
- [Demostración](#id2) 📺
###

<div id="id0" />

## Contenidos 📚
- **smartexam_dapp**: Contiene toda la lógica de la aplicación descentralizada.
- **contracts**: Contiene los contratos inteligentes implementados escritos en Solidity.
- **testing**: Son los ficheros utilizados para hacer los test unitarios con [https://spin.atomicobject.com/tests-solidity-foundry/](foundry).

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

> ℹ️ _SmartExamBase_ hereda del contrato de [openzeppelin](https://www.openzeppelin.com/) `Ownable.sol` que implementa funcionalidades para gestionar el propietario del contrato. Se puede, entre otras funcionalidades, obtener el propietario (`owner()`) o transferir la propiedad (`transferProperty()`)

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

<div id="id2" />

## Demostración

En el primer vídeo se puede ver como:

1. Se comprueba que en el nodo de IPFS no existe ningún archivo subido.
2. Se entra con la cuenta de propietario.
3. Como propietario se añade un profesor al examen.
4. Como propietario se editan los parámetros del examen.
5. Se cambia a la cuenta estudiante.
6. Como estudiante no registrado se registra al examen. Se tiene que actualizar la página porque los parámetros no se habían editado en la _blockchain_ (si los datos no se han editado al menos una vez no dejará inscribirse al examen).

https://github.com/pedrotega/munics/assets/115726518/e81eb334-615b-4367-a2af-3f0e10bb480b

En este segundo vídeo se ha realizado:

1. El propietario empieza el examen añadiendo el enunciado a la DApp.
2. Se comprueba como el archivo se ha añadido al nodo de IPFS.
3. Se cambia a la cuenta de estudiante.
4. El estudiante descarga y visualiza el examen.
5. El estudiante añade sus respuestas a la DApp.

https://github.com/pedrotega/munics/assets/115726518/bf790aa6-1c21-4ec6-b0da-933924e7f751

En el tercer vídeo se muestra el proceso de corrección por parte del profesor:

1. El profesor obtiene los estudiantes inscritos en un examen.
2. El profesor obtiene las respuestas de un estudiante a partir de su dirección.
3. El profesor añade la corrección a la DApp.
4. Se comprueba como la corrección se ha añadido a IPFS.
5. El profesor comprueba las correcciones obtenidas. Se puede observar que hasta que la transacción de la corrección no se comfirme en la _blockchain_ de Sepolia, no se podrá acceder a sus datos (hacia el final del vídeo).

https://github.com/pedrotega/munics/assets/115726518/73c7b79e-5885-451e-9690-1e0549b8a58c

Finalmente, en el último vídeo se puede ver como:

1. El estudiante recupera se examen.
2. Obtiene el fichero con las correcciones de su entrega.
3. Visualiza la nota que ha obtenido.

https://github.com/pedrotega/munics/assets/115726518/5b2e5de7-6fad-454a-89f7-1d52cabb568b

