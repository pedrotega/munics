# Ejercicio 6
Creación de un contrato que puede ser usado para mantener la integridad y la inmutabilidad de exámenes. Tanto creación como realización y corrección.
## Autores:
* Luis Corbacho Flores
* Javier Español Alfonso
* Pedro Otero García

## Estructura del código
* `SmartExamBase.sol`: Contiene el contrato con los `modifiers`, declaración de variables globales, structuras y las funciones que utiliza el dueño del contrato para poder añadir los usuarios profesores.
* `SmartExam.sol`: Incluye un contrato con el resto de funciones utilizadas por estudiantes y profesores para interactuar con el contrato. 
> ⚠️ El contrato de `SmartExam.sol` hereda del contrato de `SmartExamBase.sol` por lo que solo se deberá desplegar el primero para obtener todas las funcionalidades.
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