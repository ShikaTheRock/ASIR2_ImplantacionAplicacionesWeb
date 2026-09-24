import yaml

# 1. Apertura y carga segura del fichero YAML
with open("ansible.yaml", "r", encoding="utf-8") as fichero:
    doc = yaml.safe_load(fichero)

# 2. Acceso a la lista principal de libros
tareas = doc["tasks"]

# 3. Cantidad de elementos
print("Número total de Tareas:", len(tareas))
print("-" * 40)

# 4. Recorrido de la lista e impresión de títulos
print("Listado de tareas:")
countador=0
for tarea in tareas:
    countador+=1
    print(countador, "-", tarea['name'])

print("-" * 40)

# 5. Printear primera tarea del libro
print("Desglosando instalaciones de la tarea 1:")
tarea_uno = tareas[0]
print(tarea_uno["with_items"])
print("-" * 40)

# 6. Printear pass de la db
print("Contraseña de la Base de datos:", doc["vars"]['mysql_root_db_pass'])


# # 5. Tratamiento de tipos de datos variables (cadena vs lista)
# print("Autores por libro:")
# for libro in libros:
#     titulo = libro["title"]["text"]
#     autor = libro["title"]["author"]
    
#     # Comprobación de tipo: ¿Es una lista o un único string?
#     if isinstance(autor, list):
#         print(f"• '{titulo}' (Múltiples autores): {', '.join(autor)}")
#     else:
#         print(f"• '{titulo}': {autor}")