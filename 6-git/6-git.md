# Informe de Práctica: Gestión de Ramas, Conflictos y Trabajo Colaborativo en Git
**Autor:** Héctor  
**Módulo:** Implantación de Aplicaciones Web ($2^{\circ}$ ASIR - IES La Senia)  

---

## Introducción

En esta tarea de la UD01 hemos puesto en práctica el flujo de trabajo avanzado con Git, abarcando tanto la gestión individual de ramas y conflictos locales como el trabajo en equipo en parejas para simular la resolución de conflictos concurrentes en un repositorio remoto compartido con César.

---

## Parte 1: Práctica Individual y Configuración Inicial

Para empezar a trabajar en el repositorio de la tarea, lo primero que hice en mi equipo fue inicializar Git y enlazarlo con el repositorio remoto que creamos en GitHub (`Tarea-Conflictos-IAW`).

![Inicialización del repositorio y primer commit](6-git/screenshot_2026-10-15_11-40-04.png)

Aquí creé el archivo `README.md`, hice el primer commit, renombré la rama a `main` y configuré el origen remoto para subir los cambios iniciales con `git push -u origin main`.

---

## Parte 2: Trabajo en Equipo y Simulación de Conflictos

En esta fase colaborativa, tanto César como yo trabajamos de forma paralela sobre el repositorio. César se encargó de la rama `caracteristica-a` y yo de la rama `caracteristica-b`, modificando el mismo fichero (`fichero_inicial`) para provocar y analizar los conflictos de fusión.

### 1. El punto de vista de César (`caracteristica-a`)
César creó su rama de característica, editó el archivo añadiendo un estado y la subió a GitHub:

![César creando la rama caracteristica-a y editando con nano](6-git/1.png)

Posteriormente, modificó el fichero usando `nano` para dejar el texto *"Estado: Eso es pepino"* y configuró el upstream para publicarlo:

![César editando el fichero_inicial](6-git/2.png)

Tras esto, César volvió a la rama `main` y fusionó su rama mediante un avance rápido (*Fast-forward*), haciendo el commit correspondiente y subiendo los cambios limpios al servidor:

![César realizando el merge fast-forward en main](6-git/3.png)

### 2. Mi punto de vista y desarrollo (`caracteristica-b`)
Por mi parte, operé de forma simultánea en mi máquina dentro del directorio de trabajo. Primero preparé mi rama de característica utilizando el comando de cambio y renombrado:

![Renombrado a caracteristica-b](6-git/screenshot_2026-10-26_09-56-01.png)

A continuación, comprobé el contenido del fichero para ver qué texto contenía tras nuestras modificaciones cruzadas:

![Comprobación del contenido con cat](6-git/screenshot_2026-10-26_09-56-16.png)

Como se puede ver, en mi rama introduje el texto *"Estado: Eso es mortadela"*. Acto seguido, preparé los cambios, hice el commit con el mensaje `"mortadela"` y subí la rama al servidor remoto:

![Commit y push de la caracteristica-b](6-git/screenshot_2026-10-26_09-57-04.png)

### 3. Sincronización y gestión de ramas divergentes
Cuando intenté actualizar mi repositorio local utilizando `git pull` para traer los cambios que había subido César, Git me advirtió que las ramas habían divergido y me pidió definir una estrategia de reconciliación:

![Aviso de divergencia al hacer git pull](6-git/screenshot_2026-10-26_10-08-13.png)

Finalmente, al intentar unificar los cambios con `git merge origin/caracteristica-b`, la terminal me devolvió el aviso de que ya se encontraba actualizado en ese puntero, reflejando el estado de sincronización de nuestras ramas de trabajo:

![Intento de fusión y estado actualizado](6-git/screenshot_2026-10-26_10-08-29.png)

---

## Conclusión

Esta práctica me ha servido para comprender de forma muy visual cómo funciona el control de versiones en entornos reales de desarrollo. Hemos comprobado cómo Git gestiona las fusiones limpias de tipo *Fast-forward* cuando no hay interferencias, y cómo detecta las divergencias y posibles conflictos cuando varios colaboradores editamos las mismas líneas de código de manera simultánea.
