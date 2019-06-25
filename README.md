# CRM_Arquitectura_Marketing

Trabajo en conjunto para el desarrollo del modulo de marketing orientado a microservicios

## Guía de proyecto

A continuación se establece una guía en base a diferentes aspectos del proyecto.

### Guia de Documentación

- Todo documento debe de estar escrito en español.
- Todo documento debe estar en la carpeta/lugar adecuado.
  - Si es un documento sobre base de datos, poner en la carpeta database.
  - Si es un documento sobre especificacion de funcionalidad/ alcance; se debe poner en la carpeta funcionalidad.
  - Si es un modelo de clases, secuencia, etc. se debe poner en la carpeta de modelos en la subcarpeta relacionada.
  - Si es una plantilla o snippet de codigo; se debe agregar a la carpeta complementarios.
  - Si es información simple, clara y necesaria para todos; se debe de poner en el readme.
- Cualquier archivo que sea subido debe de llevar el siguiente formato de nombre: TipoArchivo_NombreArchivo. Por ejemplo: ModeloDB_BaseDatosCRM.
- Todos los archivos seran subidos al branch principal del proyecto.

### Guía de Código

- El código deberá ser realizado en Ingles.
- Hacer uso de la especificación pep8 para python
- Las clases inician con mayúscula.
- Los métodos y atributos inician con minúscula.
- Los métodos inician con verbos en infinitivo,
- Las constantes son completamente en mayúscula y hace uso de snake_case (HOLA_MUNDO).
- Todo código debe estar correctamente indentado haciendo uso de TABs.

- Una línea nunca debe tener mas de 100 caracteres. Para seguir una accion se hace lo siguiente:

### Guía de GitHub

- Los commits deben seguir el siguiente formato: **Modulo_AccionRealizada**. Además de esto se debe subir una descripción más detallada de los que se hizo.

### Alcance del modulo

- Creación de campañas de marketing basadas en: Genero, Ingresos Edad (20-70 años) y Ubicación geográfica.

  - El usuario jefe de marketing tendrá la posibilidad de crear campañas consumiendo un servicio de consulta expuesto por el módulo de clientes.
  - La creación de las campañas transferirá los clientes que encajen con el perfil de la campaña hacia una base de datos relacional.
  - El jefe de marketing podrá elegir un diseño para el envío masivo de correos o subir uno propio (subir HTML).

- Gestión de campañas.
  - Monitoreo y actualización de las fases de la campaña
  - Estadísticas de las campañas
    - Resultados de llamadas en grafico
    - Clientes repetidos en más de una campaña
    - Campañas por presupuesto, por edad, por genero
    - Mapa del Ecuador pintado por campañas

- Envío de correos mensual y por demanda
  - Se generará un proceso que mensualmente enviará los correos a los clientes que estén dentro de una campaña seleccionada en la fase de ejecución
  - Se dará la posibilidad de enviar correos a demanda mediante una interfaz
  - _Intercambio de correos con usuarios específicos_

- Asignar asesores para llamadas telefónicas
  - Se asignarán a un asesor un número determinado de clientes para que este pueda realizar promoción telefónica. 
- Gestión de telemarketing
  - El asesor podrá incluir el resultado de su llamada en la base de datos
  - Revisión del estado de los clientes con el servicio de central de riesgos
  - El asesor podrá revisar el estado de riesgo de un cliente especifico mediante un servicio SOAP antes de realizar la llamada
- Servicio de central de riesgos
  - Una base de datos REDIS o DynamoDB que contenga los usuarios y su nivel de riegos.
  - Un servicio SOAP que permita consulta mediante nombre o cedula de cliente.

### Costos e infraestructura a utilizar

[AWS Infraestructure Detail](https://calculator.s3.amazonaws.com/index.html#r=IAD&key=files/calc-5ef362a0309d647b2790287620399522c3f27593&v=ver20190604sQ )
