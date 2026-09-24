import yaml

# 1. Apertura y carga segura del fichero YAML
with open("books.yaml", "r", encoding="utf-8") as fichero:
    doc = yaml.safe_load(fichero)

# 2. Acceso a la lista principal de libros
libros = doc["bookstore"]["book"]

# 3. Cantidad de elementos
print("Número total de libros:", len(libros))
print("-" * 40)

# 4. Recorrido de la lista e impresión de títulos
print("Lista de títulos:")
for libro in libros:
    print(f"- {libro['title']['text']}")

print("-" * 40)

# 5. Tratamiento de tipos de datos variables (cadena vs lista)
print("Autores por libro:")
for libro in libros:
    titulo = libro["title"]["text"]
    autor = libro["title"]["author"]
    
    # Comprobación de tipo: ¿Es una lista o un único string?
    if isinstance(autor, list):
        print(f"• '{titulo}' (Múltiples autores): {', '.join(autor)}")
    else:
        print(f"• '{titulo}': {autor}")