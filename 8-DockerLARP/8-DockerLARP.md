---
title: "8-DockerLARP"
author: "Hector V."
date: "16.11.2026"
subject: "IAW"
titlepage: true
titlepage-rule-height: 0
titlepage-background: 0-Template/portada.jpg
toc-own-page: true
titlepage-text-color: ffffff
---

# Práctica: despliegue de una pila LAMP con Docker Compose

## ¿Qué hemos montado?

En esta práctica he montado un pequeño entorno LAMP usando Docker Compose. La idea era tener Apache y PHP para servir la página web, MariaDB para guardar los datos y phpMyAdmin para poder consultar la base de datos desde el navegador. Como parte extra, también he añadido GoAccess para ver estadísticas de las visitas al servidor.

He ido montando y comprobando cada parte por separado, y después he probado que todo funcionase junto.

## 1. Preparar la carpeta del proyecto

Primero preparé la carpeta `lamp-docker-practica` y organicé los archivos para que no estuviera todo mezclado:

- `compose.yml`: configuración de los servicios y de cómo se comunican.
- `database/init.sql`: script SQL para crear la tabla `alumnos` e insertar un primer registro.
- `src/index.php`: página inicial para comprobar que Apache y PHP funcionan.
- `src/conexion.php`: página que conecta PHP con MariaDB, inserta un alumno y muestra los registros.
- Los archivos de configuración de Apache y GoAccess, además del informe generado.
- `.env`: variables con los datos de acceso a MariaDB.

![Estructura inicial del proyecto](8-DockerLARP/capturas/01_estructura.png)

El archivo `.env` guarda las contraseñas y los datos de la base de datos separados del resto de la configuración. Por seguridad no incluyo aquí sus valores ni una captura donde se puedan leer.

## 2. Configurar los contenedores con Docker Compose

En `compose.yml` definí los servicios principales:

- **web**: utiliza la imagen `php:8.3-apache` y publica la web en el puerto `8080` del equipo.
- **db**: utiliza MariaDB 11.4 y guarda sus datos en un volumen persistente.
- **phpmyadmin**: permite administrar la base de datos desde el navegador, en el puerto `8081`.
- **goaccess**: lo añadí después como extra para analizar los registros de Apache y publicar el informe en tiempo real.

También configuré una red interna llamada `lamp_network`, para que los contenedores puedan comunicarse entre ellos usando el nombre del servicio. Por ejemplo, PHP se conecta al servidor de base de datos usando `db`, no `localhost`.

La carpeta `src` se monta dentro del contenedor web, así que los archivos PHP del proyecto están disponibles directamente para Apache. El script `init.sql` se monta en la carpeta especial `/docker-entrypoint-initdb.d/` de MariaDB. Además, MariaDB usa el volumen `db_data` para conservar la información aunque se eliminen y creen de nuevo los contenedores.

En el contenedor web activé las extensiones `mysqli` y `pdo_mysql`, necesarias para que PHP pueda trabajar con MySQL/MariaDB.

![Configuración inicial de Compose](8-DockerLARP/capturas/02_compose_base.png)

Una vez preparada la configuración, levanté los servicios y comprobé que los contenedores principales aparecían en ejecución.

![Contenedores principales en ejecución](8-DockerLARP/capturas/03_contenedores_iniciales.png)

## 3. Comprobar Apache y PHP

Después preparé `index.php` con un mensaje sencillo y la versión de PHP. Así podía comprobar rápidamente que Apache servía la página y que PHP se estaba ejecutando, y no se estaba mostrando el archivo como texto.

![Código de index.php](8-DockerLARP/capturas/04_index_php.png)

Al entrar en `http://localhost:8080` apareció el mensaje de que el servidor LAMP estaba funcionando correctamente y también se mostró la versión de PHP.

![Página inicial funcionando en el navegador](8-DockerLARP/capturas/05_web_funcionando.png)

## 4. Preparar MariaDB y phpMyAdmin

Para la base de datos dejé configuradas las credenciales mediante las variables de `.env`. El nombre de la base de datos, el usuario y las contraseñas se pasan a los contenedores desde Compose, evitando escribir esos datos directamente en el código PHP.

En `database/init.sql` preparé la tabla `alumnos`, con los campos `id`, `nombre` y `email`, y añadí un registro inicial de prueba. Este archivo se ejecuta automáticamente cuando MariaDB inicializa por primera vez una base de datos nueva. Es importante recordar que estos scripts de inicialización no se vuelven a ejecutar cada vez que reiniciamos un contenedor si el volumen de datos ya existe.

También configuré phpMyAdmin para que se conecte al servicio `db`. Se puede abrir desde `http://localhost:8081`. Desde ahí comprobé que aparecía la base de datos y que estaba creada la tabla `alumnos`.

![Tabla alumnos visible en phpMyAdmin](8-DockerLARP/capturas/06_phpmyadmin_alumnos.png)

## 5. Conectar PHP con MariaDB

La siguiente parte fue crear `src/conexion.php`. El archivo recoge las variables de conexión del entorno y utiliza el nombre del servicio `db` como servidor. Después establece la conexión con `mysqli`, inserta un alumno de prueba mediante una consulta preparada y muestra los alumnos registrados en una tabla HTML.

![Código de conexion.php](8-DockerLARP/capturas/07_codigo_conexion.png)

Al abrir `http://localhost:8080/conexion.php` apareció el mensaje de conexión correcta y pude ver los registros de la tabla `alumnos`. Cada vez que se carga la página se inserta otro registro de prueba, por eso el número de filas va aumentando.

![Conexión PHP-MariaDB y registros mostrados](8-DockerLARP/capturas/08_conexion_php_correcta.png)

## 6. Comprobar que los datos persisten

También comprobé que los datos no desaparecen al recrear los contenedores. Para ello paré el entorno con `docker compose down` y lo volví a levantar, **sin utilizar `-v`**. De esta forma se eliminan los contenedores, pero se conserva el volumen `db_data` donde MariaDB guarda la información.

Después volví a consultar la tabla desde phpMyAdmin y seguían apareciendo los registros que se habían insertado. Esto confirma que los datos están guardados en el volumen y no dependen de que el contenedor siga siendo el mismo.

![Prueba de parada y arranque de los servicios](8-DockerLARP/capturas/09_reinicio_servicios.png)

![Registros conservados en MariaDB](8-DockerLARP/capturas/10_datos_mariadb.png)

## 7. Extra: monitorización con GoAccess

Como ampliación elegí GoAccess para analizar las visitas que recibe Apache. Añadí un cuarto servicio a Compose y compartí un volumen llamado `apache_logs` entre Apache y GoAccess. Apache escribe un registro específico en `goaccess.log` y GoAccess lee ese archivo para generar `src/report.html`. El informe se puede abrir desde `http://localhost:8080/report.html`, y el servicio de GoAccess utiliza el puerto `7890` para las actualizaciones en tiempo real.

Esta parte dio algo más de guerra que las anteriores. Al principio GoAccess arrancaba, pero no recibía líneas de registro y el informe no se actualizaba. El problema era que el archivo de acceso habitual de Apache no estaba disponible como un archivo normal compartido para GoAccess. Para solucionarlo añadí un registro específico (`goaccess.log`) en la configuración del VirtualHost activo de Apache y lo dejé dentro del volumen compartido. También hubo que ajustar el bloque de comandos multilínea y la colocación del servicio GoAccess en el YAML de Compose para que arrancase correctamente.

Después de esos cambios, GoAccess pudo leer las peticiones y generar el panel con estadísticas: número de solicitudes, visitantes, archivos solicitados y otros datos.

![Contenedores de GoAccess y el resto del entorno arrancados](8-DockerLARP/capturas/11_goaccess_arrancado.png)

![Informe de GoAccess en el navegador](8-DockerLARP/capturas/12_informe_goaccess.png)

## 8. Problemas que fueron apareciendo y cómo los resolví

Durante el montaje aparecieron algunos detalles que tuve que revisar:

- **La tabla de MariaDB no aparecía como esperaba al principio.** Revisé el script SQL y la inicialización de la base de datos. También tuve en cuenta que, si el volumen de MariaDB ya está creado, cambiar `init.sql` no provoca que el script se ejecute otra vez automáticamente.
- **La conexión desde PHP tenía que usar el nombre del servicio.** La dejé apuntando a `db`, que es como se resuelve el contenedor dentro de la red de Compose, en lugar de usar `localhost`.
- **GoAccess arrancaba, pero no tenía datos que procesar.** Añadí un archivo de log específico de Apache dentro del volumen compartido y configuré el VirtualHost para escribir también en él.
- **El comando de GoAccess daba problemas con el formato multilínea del YAML.** Ajusté la estructura del bloque y la indentación del servicio para que Compose lo interpretase correctamente.

## 9. Resultado final

Al terminar, el entorno queda con estos servicios y direcciones:

| Servicio | Para qué sirve | Acceso desde el equipo |
|---|---|---|
| Apache + PHP (`web`) | Sirve la web y ejecuta los archivos PHP | `http://localhost:8080` |
| MariaDB (`db`) | Guarda la base de datos | Solo dentro de la red de Docker, en el puerto `3306` |
| phpMyAdmin | Permite consultar y administrar MariaDB | `http://localhost:8081` |
| GoAccess | Analiza los registros de Apache | Informe: `http://localhost:8080/report.html` · WebSocket: puerto `7890` |

En general, he conseguido desplegar la pila LAMP con Docker Compose, comprobar que PHP se conecta a MariaDB, visualizar los datos desde phpMyAdmin y verificar que se conservan al recrear los contenedores. Como extra, he añadido GoAccess para tener un panel de estadísticas de las visitas al servidor.
