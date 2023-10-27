# Ejercicio 6

## Autores:
* Luis Corbacho Flores
* Javier Español Alfonso
* Pedro Otero García

=============================

###
- [Análisis y definición del escenario](#id1) :bar_chart:
- [Diseño](#id2) :pencil:
    - [Caso de uso](#id2_1) :wrench:
    - [Estructura del contrato](#id2_2) :bookmark_tabs:
- [Utilidades](#id3) ⚙️

###

<div id="id1" />

## Análisis y definición del escenario :bar_chart:

A la hora de hacer un examen oficial pueden surgir todo tipo de problemáticas en cuanto a los tiempos y corrección de los mismos. Poniendo como ejemplo el examen de la [EBAU](https://ciug.gal/gal/abau), es difícil coordinal que en todas las partes de la misma región empiecen al mismo tiempo. Además una vez que los exámenes son corregidos, los alumnos no tienen ninguna oportunidad de revisar sus respuestas y tan solo se pueden limitar a hacer reclamaciones en las que se corregirán (o no) su examen.

Viendo desde el punto de vista de los profesores resulta complicado dar acceso a los exámenes para evitar que estos puedan ser modificados durante el proceso (especialmente cuando se hace físicamente). 

Estos problemas pueden ser resueltos usando una _blockchain_ pública como *[Ethereum](https://ethereum.org/en/)*. Los profesores podrán poner disponible el examen en un contrato inteligente de tal modo que los alumnos puedan acceder a él al mismo tiempo. Al hacer que toda la información de un examen este en un contrato inteligente, permite que el enunciado del examen, las respuestas, correciones, alumnos y profesores queden registrados en la blockchain. Esto evita falsificaciones y manipulaciones a la vez que garantiza la integridad y autoridad de toda la información en el contrato.

<div id="id2" />

## Diseño :pencil:

<div id="id2_1" />

### Caso de uso :wrench:

Nuestro caso de uso está orientado a exámenes oficiales de entidades privadas. Por mencionar un caso de la vida real, los certificados de nivel de inglés de [Cambridge](https://www.cambridgeenglish.org/exams-and-tests/) tienen un cierto precio de inscripción que se podría pagar a la hora de inscribirte en el contrato inteligente. Además las certificaciones de Cambridge se pueden hacer en ordenador lo que facilitaría la interactuación con el contrato.

En un principio cuando se crea un examen, este no va a estar almacenado en la blockchain pero sí un hash de este. Cuando el profesor inicie el examen se añadirá un link al fichero online (almacenado en un drive, dropbox...) para que los alumnos que estén inscritos puedan acceder al examen solo a partir de ese momento.

<div id="id2_2" />

### Estructura del contrato :bookmark_tabs:
* `SmartExamBase.sol`: Contiene el contrato con los `modifiers`, declaración de variables globales, structuras y las funciones que utiliza el dueño del contrato para poder añadir los usuarios profesores.

    * **Estructuras**:
        * `Exam`: Contiene la información perteneciente a un examen creado por un profesor. Variables:
            * `course`: Nombre del curso al que pertenece el examen.
            * `id`: Identificador para distinguir a los examenes entre ellos.
            * `hash`: Hash del archivo real donde se guarda el examen para evitar manipulaciones.
            * `dateLastUpload` : Fecha de la última actualización de los parámetros del examen.
            * `dateExam` : Fecha exacta de cuando el examen debería llevarse a cabo.
            * `dateStartExam` : Fecha real de cuando ha empezado el examen.
            * `duration` : Duración del examen en minutos.
            * `enrollingPrice` : Precio de inscripción del examen.
        * `ExamStudent`: Contiene la información de examen concreto de un estudiante. Variables:
            * ``studentAdd``: Dirección del alumno que ha hecho el examen.
            * ``exam``: _Struct_ del examen que se ha hecho.
            * ``hash_submision``: Hash del archivo con las respuestas del examen (creado por el alumno).
            * ``url_exam_submited``: URL para acceder al archivo con las respuestas del examen (creado por el profesor).
            * ``hash_correction``: Hash del archivo con las correcciones del examen (creado por el profesor que ha corregido el examen).
            * ``url_exam_correction``: URL para acceder al archivo con las correcciones del examen.
            * ``score``: Nota del examen.
        * `Student`: Contiene la información relacionada con un resultante. Variables:
            * add: Dirección del estudiante.
            * exams_enrolled: Mapa para saber en que examenes está inscrito el estudiante. Relaciona el ID de un examen (_key_) con un buleano (_value_, falso si no está inscrito).
            * exams_done: Mapa para obterner el `ExamStudent` (_value_) con la información de un examen hecho por el alumno a partir del ID del examen (_key_).
    * **Mapas**: 
        * `profToId`: Usado para conocer los profesores registrado. A partir de su dirección (_key_) se puede conocer su identificador (_value_) único generado a partir la misma dirección. Si su identificador (número entero) es 0, podemos concluir que no está registrado.
        * `students`: Relaciona la dirección de un estudiante (_key_) con su estructura `Student` (_value_).
        * `examsSubmited`: Permite relacionar el ID de un examen (_key_) con un vector de las direcciones de los alumnos que han hecho el examen (_value_).
    * **Otros**:
        * `exams`: Es un array que contiene todas las estructuras correspondientes a los contratos creados.
        * `countExam`: Es un contador de los examenes que se han creado. También sirve para asignar el ID a los contratos cuando se crean.
    * **Modificadores**:
        * `onlyProfessor`: Solo deja ejecutar la función si la dirección que llama al contrato es la de un profesor (para ello se ayuda del mapa `profToId`).
        * `onlyStudent`: Solo deja acceder a la función si la dirección que llama al contrato es la de un estudiante (para ello usa el mapa `students`). 
    * **Funciones**:
        * `_generarId`: Es una función privada que genera un número, que se usará como identificador, a partir de una dirección
        * `addProfessor`: Permite al owner añadir profesores al contrato.

> ℹ️ `_generarId` es la única función privada del contrato, el resto son externas. Se ha decidido así ya que el contrato se ha creado para poder ser utilizado por una DApp (solo se harán llamadas desde fuera del contrato).  


> ℹ️ Para limitar el acceso a las funciones que solo se puede acceder el owner se ha importado el modificador `onlyOwner` del repositorio de [openzeppelin](https://www.openzeppelin.com/)
         
            

* `SmartExam.sol`: Incluye un contrato con el resto de funciones utilizadas por estudiantes y profesores para interactuar con el contrato. 
    * **Funciones**:
        * Relacionadas con los usuarios *Profesor*:
            * `createExam`: Permite a los usuarios *Profesor* crear nuevos examenes con las características de la estructura _exam_. 
            * `modifyExam`: Permite a los usuarios *Profesor* modificar los parámetros de un examen existenete.
            * `startExam`: Permite a los usuarios *Profesor* empezar un examen. Es en esta función en la que se añade a la estructura _exam_ el parámetro _url_ que por defecto está a _"null"_. Una vez iniciado el examen, este ya no se puede modificar.
            * `getSubmissions`: Permite a los usuario *Profesor* obtener las direcciones de los alumnos que han entregado un examen particular (utilizando el ID del examen para ello).
            * `getExamSubmited`: Permite al usuario *Profesor* obtener la información del examen de un alumno en particular indicando la direcctión de dicho alumno.
            * `addCorrection`: Añade el enlace al archivo con la corrección del examen y el hash correspondiente a la estructura _ExamStudent_ asociada al examen entregado por un estudiante.
        * Relacionadas con los usuarios *Estudiante*:
            * `enrollIntoExam`: Permite inscribirse a un examen en concreto abonando para ello el precio correspondiente al examen. A partir de ese momento, la dirección que ha hecho la llamada a esta función pasa a ser de usuario tipo *Estudiante*.
            * `submitExam`: Permite a un usuario *Estudiante* entregar un enlace con el archivo correspondiente a sus respuestas y el hash correspondiente a dicho archivo. Siempre y cuando la entrega se haya realizado entre la hora de inicio del examen y antes de que se acabase el plazo de entrega.
        * Otro:
            * `getExam`: Permite obtener la información de una estructura _exam_ en concreto. No se limita el acceso a esta función ya que sus parámetros son de caracter informativo.


> ⚠️ El contrato de `SmartExam.sol` hereda del contrato de `SmartExamBase.sol` por lo que solo se deberá desplegar el primero para obtener todas las funcionalidades.

<div id="id3" />

## Utilidades ⚙️
* `computeTime.js` es un pequeño código que se puede utilizar para obtener una hora en formato UNIX. La hora en este formato se utliza para especificar la última actualización de un examen, cuándo se prevé que empezará dicho examen y la hora en la que realmente ha empezado.
* Enlace con los recursos de ejemplo que se pueden utilizar: [exams](https://drive.google.com/drive/folders/1wMeLc6moeWmUkCd34y71oaKUWkX0-THC?usp=share_link)
* Para obtener el SHA256 por terminal:
    * En Linux:
    ```shell
        > sha256sum Examen\ historia.docx
    ```
    * En Windows:
    ```shell
        > Get-FileHash '.\Examen historia.docx' | Format-list
    ```