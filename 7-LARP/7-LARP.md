---
title: "7-LAMP"
author: "Hector V."
date: "5.11.2026"
subject: "IAW"
titlepage: true
titlepage-rule-height: 0
titlepage-background: 0-Template/portada.jpg
toc-own-page: true
titlepage-text-color: ffffff
---


# Memoria UD02 - Tarea 1: Despliegue de la pila LAMP en Ubuntu sobre Proxmox VE

**Módulo:** Implantación de Aplicaciones Web (IAW) — 2º ASIR · IES La Senia
**Alumno:** Héctor Villanueva
**Servidor:** Ubuntu (resolute) · hostname `hector` · IP `192.168.3.243`
**Pila:** Apache2 · MariaDB 11.8.6 · PHP · Adminer 6.3.0 · GoAccess 1.9.4

---

## Paso Previo: Aprovisionamiento en Proxmox VE

La máquina Ubuntu se ha desplegado en el clúster Proxmox VE del aula y se administra de forma remota por SSH. La IP asignada en la red del aula es **192.168.3.243**, que se usa en todas las pruebas desde el navegador (`http://192.168.3.243`). La conexión SSH puede verse en el título de la terminal Konsole de la captura 16 (`(shika) 192.168.3.243 — Konsole`).
---

## Paso 1: Servidor web Apache

### 1.1 Actualización de repositorios e instalación

```bash
sudo apt update
sudo apt install apache2
```

![Captura 1 — apt update y apt install apache2](7-LARP/0.png)

### 1.2 Comprobación del servicio

```bash
sudo systemctl status apache2
sudo systemctl is-enabled apache2
```

### 1.3 Página de bienvenida de Apache

Acceso desde el navegador a `http://192.168.3.243`: carga la página por defecto "Apache2 Default Page – It works!".

![Captura 2 — Página por defecto de Apache2](7-LARP/1.png)

### 1.4 Página personalizada

Se sustituye el contenido de `/var/www/html/index.html` para mostrar el nombre y el módulo.

![Captura 3 — Página personalizada en el navegador](7-LARP/2.png)

---

## Paso 2: Servidor de bases de datos (MariaDB)

Se instala `mariadb-server` y se prepara un script SQL (`alumnos.sql`) con todas las sentencias.

### 2.1 Creación del script

```bash
nano alumnos.sql
```

![Captura 4 — Edición del script con nano](7-LARP/3.png)

### 2.2 Sentencias SQL ejecutadas

```sql
-- 1. Crear la base de datos
CREATE DATABASE IF NOT EXISTS alumnos_db;

-- 2. Crear un usuario específico
CREATE USER IF NOT EXISTS 'alumno_iaw'@'localhost'
IDENTIFIED BY 'Alumno123!';

-- 3. Conceder permisos completos sobre la BD
GRANT ALL PRIVILEGES ON alumnos_db.*
TO 'alumno_iaw'@'localhost';

-- 4. Seleccionar la base de datos
USE alumnos_db;

-- 5. Crear la tabla alumnos
CREATE TABLE IF NOT EXISTS alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    edad INT NOT NULL
);

-- 6. Insertar tres registros ficticios
INSERT INTO alumnos (nombre, edad) VALUES
('Carlos García', 20),
('Lucía Martínez', 22),
('Pablo Sánchez', 19);

-- 7. Consultar los registros
SELECT * FROM alumnos;

-- 8. Comprobar los permisos del usuario
SHOW GRANTS FOR 'alumno_iaw'@'localhost';
```

![Captura 5 — Contenido de alumnos.sql](7-LARP/4.png)

### 2.3 Ejecución del script

```bash
sudo mariadb < alumnos.sql
```

La salida muestra los 3 registros insertados y los permisos del usuario: `GRANT ALL PRIVILEGES ON alumnos_db.*` para `alumno_iaw@localhost`.

![Captura 6 — Ejecución del script y resultado](7-LARP/5.png)

### 2.4 Consulta SELECT con el usuario de aplicación

Se comprueba la persistencia conectando con el usuario `alumno_iaw` (sin usar root):

```bash
mariadb -u alumno_iaw -p alumnos_db
```
```sql
SELECT * FROM alumnos;
```

![Captura 7 — SELECT * FROM alumnos; con alumno](7-LARP/6.png)

---

## Paso 3: PHP y conectividad con la base de datos

### 3.1 Instalación de PHP

```bash
sudo apt install php libapache2-mod-php php-mysql -y
sudo systemctl restart apache2
```

![Captura 8 — Instalación de PHP, módulo de Apache y conector MySQL](7-LARP/7.png)

### 3.2 Archivo `info.php`

Se crea `/var/www/html/info.php` con `phpinfo();`.

```php
<?php
phpinfo();
?>
```

![Captura 9 — Edición de /var/www/html/info.php](7-LARP/8.png)

### 3.3 Script dinámico `consulta.php`

Se crea `/var/www/html/consulta.php` a partir de la plantilla del anexo, con las credenciales del usuario `alumno_iaw`.

![Captura 10 — Contenido de /var/www/html/consulta php](7-LARP/9.png)

Resultado en el navegador (`http://192.168.3.243/consulta.php`): la tabla HTML se genera dinámicamente con los datos de la base de datos.

![Captura 11 — Tabla generada por consulta.php](7-LARP/10.png)

---

## Paso 4: Gestor web de base de datos (Adminer)

Se ha elegido la **Opción A: Adminer**, descargando el script PHP oficial en `/var/www/html/adminer.php`.

### 4.1 Autenticación

Acceso a `http://192.168.3.243/adminer.php` con motor MySQL / MariaDB, usuario `alumno_iaw` y base de datos `alumnos_db`.

![Captura 12 — Pantalla de login de Adminer](7-LARP/11.png)

### 4.2 Sesión activa

Sesión iniciada como `alumno_iaw`, mostrando la base de datos `alumnos_db` y la tabla `alumnos`.

![Captura 13 — Sesión activa en Adminer](7-LARP/12.png)

### 4.3 Inserción de un registro desde la interfaz web

Desde "Comando SQL" se inserta un nuevo registro:

```sql
INSERT INTO alumnos(id, nombre, edad) VALUES ("4","b","55")
```

Adminer confirma: *Consulta ejecutada, 1 registro afectado*.

![Captura 14 — INSERT ejecutado desde Adminer](7-LARP/13.png)
---

## Paso 5: Análisis de logs de Apache con GoAccess

### 5.1 Instalación

```bash
sudo apt install goaccess
```

![Captura 15 — Instalación de GoAccess 1.9.4](7-LARP/14.png)

### 5.2 Panel interactivo en terminal

```bash
sudo goaccess /var/log/apache2/access.log --log-format=COMBINED
```

El dashboard muestra 100 peticiones totales, 2 visitantes únicos, 26 ficheros solicitados y 1 URL no encontrada (`/favicon.ico`, 404). Entre las URLs más solicitadas aparecen `/adminer.php`, `/info.php` y `/consulta.php`.

![Captura 16 — GoAccess en terminal (Konsole)](7-LARP/15.png)

### 5.3 Generación del informe HTML

```bash
goaccess /var/log/apache2/access.log -o /var/www/html/informe.html --log-format=COMBINED
```

![Captura 17 — Comando para generar el informe H7-LARP](7-LARP/16.png)

### 5.4 Informe en el navegador

Acceso a `http://192.168.3.243/informe.html`: resumen de peticiones, visitantes únicos por día y gráficas.

![Captura 18 — Informe HTML de GoAccess en el navegador](7-LARP/17.png)
