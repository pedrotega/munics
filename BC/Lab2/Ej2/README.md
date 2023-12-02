# Ejercicio 2

## Autores:
* Luis Corbacho Flores
* Javier Español Alfonso
* Pedro Otero García

###
- [Análisis y definición del escenario](#id1) :bar_chart:
- [Diseño](#id2) :pencil:
    - [Caso de uso](#id2_1) :wrench:
    - [Estructura del contrato](#id2_2) :bookmark_tabs:
- [Demo](#id3) ⚙️
###

<div id="id1" />

## Análisis y definición del escenario :bar_chart:

Para este ejercicio se ha partido del caso de uso del [ejercicio 6 de la práctica 1](https://github.com/pedrotega/munics/tree/main/BC/Lab1/Ej6) que e resume a continuación.

Los exámenes oficiales como la [EBAU](https://ciug.gal/gal/abau) (Evaluación de Bachillerato para el Acceso a la Universidad) enfrentan desafíos como el pago de tasas, corrección justa y revisión de respuestas. El uso de una blockchain pública como *[Ethereum](https://ethereum.org/en/)* podría resolver estas problemáticas. Al almacenar la información de los exámenes en contratos inteligentes, se garantiza la integridad de la información y las correciones, además de permitir a los profesores facilitar los exámenes de manera simultánea para todos los alumnos. Esto asegura un inicio justo, evita la manipulación del contenido del examen y ofrece a los estudiantes acceso transparente a sus evaluaciones corregidas.

En esta práctica se pretende aprovechar el almacenamiento descentralizado en [IPFS](https://ipfs.tech/) (Inter-Planetary File System) para completar el servicio de los exámenes inteligentes. Uno de los principales inconvenientes de usar contratos inteligentes es que resulta muy costoso (en cuanto al computo y por tanto al precio en gas) guardar archivos en el contrato. La solución más común es almanecar los archivos que van a estar relacionados con un contrato en IPFS y guardar la referencia al archivo, que es su hash conocido como CID (*Content IDentifier*), en el contrato inteligente.

De esta manera los alumnos podrán entregar su examen en un nodo IPFS (en este caso un nodo local) y subir el hash de su examen en el contrato inteligente, así como ver la corrección de su examen una vez este disponible. En el caso del profesor el podrá obtener la información de todos los exámenes recividos, descargar los archivos de los exámenes desde IPFS y subir las correcciones.


<div id="id2" />

## Diseño :pencil:

<div id="id2_1" />

### Caso de uso :wrench:


**Gestión de Exámenes de Certificación**

**Descripción:**
Un contrato inteligente, llamado *SmartExam*, se utiliza para administrar el proceso de inscripción, pagos y entrega de las pruebas. Así como, la evaluación y la corrección de los exámenes por profesores autorizados por las entidades de certificación.

 como los certificados de nivel de inglés de Cambridge o la EBAU.

**Actores Involucrados:**
- **Estudiantes:** Personas que desean realizar el examen.
- **Profesores:** Personas autorizadas que corrijirán las pruebas.
- **Entidades de Certificación:** Instituciones privadas (por ejemplo, [Cambridge](https://www.cambridgeenglish.org/exams-and-tests/)) o públicas (como la [CiUG](https://ciug.gal/gal/abau) no casod da EBAU) que ofrecen pruebas oficiales.

**Flujo del Proceso:**
>ℹ️ Todas las interactuaciones de los actores involucrados con el contrato se hacen a través de un interfaz web.

1. **Inscripción y pago del examen:**
   - Los estudiantes acceden a un contrato inteligente y se registran al examen pagando un importe determinado especificado en el contrato.

2. **Entrega y visualización del examen:**
   - Los alumnos inscritos entregan sus examenes que son subidos a IPFS y cuyos CIDs serán almacenados en el contrato asociado a la dirección de cada alumno en la blockchain.
   - Una vez entregado, los alumnos podrán descargar sus exámenes si así lo desean.

3. **Asignación de los profesores:**
   - La entidad de certificación (propietario del contrato) especifica los profesores que podrán corregir los exámenes añadiendo sus direcciones al contrato.

4. **Corrección de los exámenes:**
   - Los profesores autorizados ven la información de los exámens y añaden sus correcciones a IPFS asociando los CIDs resultado con los CID de los exámenes correspondientes.

5. **Ver correcciones:**
   - Los alumnos ven y descargan los ficheros de las correcciones.

**Beneficios:**
- **Facilidad de Inscripción:** Simplifica el proceso de inscripción para los estudiantes, ofreciendo un método transparente y eficiente.
- **Transparencia y Seguridad:** Garantiza la integridad de los datos y transacciones financieras mediante el uso de la blockchain.


<div id="id2_2" />

### Estructura del contrato :bookmark_tabs:

## Contrato SmartExam

Este contrato, basado en la librería `Ownable`, gestiona exámenes, profesores y estudiantes.

### Constantes

- `_ENROLLING_PRICE`: Costo de inscripción en el examen.

### Arrays

- `_professors`: Direcciones de todos los profesores.
- `_studentsEnrolled`: Direcciones de estudiantes inscritos en un examen.

### Mappings

- `_submissions`: Asocia hash de exámenes con direcciones de estudiantes.
- `_exams`: Asocia direcciones de estudiantes con hash de exámenes.
- `_corrections`: Asocia hash de exámenes con hash de correcciones.

### Modificadores

- `checkSubmission`: Verifica si una dirección coincide con la del estudiante que envió el examen.
- `checkAddress`: Comprueba si una dirección está presente (o no) en `_professors` o `_studentsEnrolled`.

### Funciones Principales

- `registerProfessor`: Permite al propietario del contrato agregar direcciones de profesores.
- `enroll`: Permite a una dirección inscribirse en un examen pagando el monto requerido (`_ENROLLING_PRICE`).
- `setExam`: Permite a un estudiante registrar su examen.
- `setCorrection`: Permite a un profesor registrar una corrección para un examen.
- `getStudent`: Permite a un profesor obtener la dirección de un estudiante a partir del hash de su examen.
- `getCorrections`: Permite a un profesor obtener todas las correcciones.
- `getCorrection`: Permite a un estudiante obtener la corrección de su examen.
- `getExams`: Permite a un profesor obtener todos los exámenes.
- `getExam`: Permite a un estudiante obtener su propio examen.
- `getEnrollingPrice`: Devuelve el costo de inscripción.
- `isOwner`: Verifica si el remitente de la llamada es el propietario.
- `isProfessor`: Verifica si el remitente de la llamada es un profesor.
- `isStudentEnrolled`: Verifica si el remitente de la llamada es un estudiante inscrito.

> ℹ️ Para limitar el acceso a las funciones que solo se puede acceder el _owner_ se ha importado el modificador `onlyOwner` del repositorio de [openzeppelin](https://www.openzeppelin.com/).
         

<div id="id3" />

## Demo ⚙️

Para un mejor entendimiento de la aplicación de contrato `SmartExam` se han creado unos videos en los que se aprecia su funcionamiento:

* En el primer vídeo podemos ver como un estudiante puede inscribirse en un examen, subirlo a la blockchain y posteriormente visualizarlo y descargarlo. 

[student_ui.webm](https://github.com/pedrotega/munics/assets/115726518/961714ef-ced4-4717-bb6f-7a2775e483d8)

> ℹ️ En el primer formulario de `login` lo que se hace es comprobar la dirección (en la blockchain de sepolia) del usario. Una vez obtenido se llama al contrato para diferenciar si el usuario es el propietario, un profesor, un estudiante inscrito o todavía no está inscrito.

> ℹ️ Como _tesnet_ se ha utilizado la blockchain de [Sepolia](https://www.alchemy.com/overviews/sepolia-testnet).

* En el segundo vído se puede ver como el propietario añade a un profesor y este puede ver la información del examen y subir la corrección del examen.

[owner_professor_ui.webm](https://github.com/pedrotega/munics/assets/115726518/4f667888-7d1e-41a7-a499-8402c2f5be9e)

> ℹ️ A veces la red de Sepolia tarda unos segundos en confirmar las modificaciones en el contrato. Es importante tenerlo en cuenta porque, por ejemplo, cuando se sube un archivo a IPFS hasta que no se confirme los cambios en el contrato el usuario no podrán recuperar el archivo (ya que primero se lee el CID del archivo en el contrato).

* Y finalmente, en el último vídeo se muestra como un alumno puede recuperar la corrección del examen.

[student_correction_ui.webm](https://github.com/pedrotega/munics/assets/115726518/c50044bf-26f6-4453-b9f3-2457711e0e61)
