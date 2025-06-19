
from .constantes import *

def cargar_ranking(): 
    """
    Carga el ranking desde el archivo de texto especificado por ARCHIVO_RANKING.
    Cada línea del archivo debe ser "Nombre,Puntuacion".
    Retorna una lista de tuplas [(nombre, puntuacion)].

    """
    ranking = [] 

    with open(ARCHIVO_RANKING, "r", encoding="utf-8") as archivos:
        for linea in archivos:
            linea = linea.strip()
            valores = linea.split(",") # Divide por coma
            if len(valores) == 2: # Asegurarse de que haya nombre y puntuación
                nombre = valores[0]
                # asegurar que la puntuación sea un número
                if valores[1].isdigit():
                    puntuacion = int(valores[1])
                    ranking.append((nombre, puntuacion)) # Añadir como tupla
                else:
                    print(f" Puntuación inválida '{valores[1]}' en ranking. Se omite la entrada.")
            else:
                print(f"Línea con formato incorrecto en ranking: '{linea}'. Se omite.")
    return ranking


def guardar_ranking(ranking_a_guardar): 
    """
    Guarda el ranking completo (una lista de tuplas) en el archivo de texto
    especificado por ARCHIVO_RANKING.
    El formato de cada línea será "Nombre,Puntuacion".

    """
    
    with open(ARCHIVO_RANKING, "w", encoding="utf-8") as archivos:
        for nombre, puntuacion in ranking_a_guardar: # Iterar sobre la lista de tuplas
            linea = f"{nombre},{puntuacion}\n" # Formatea la línea
            archivos.write(linea)


def mostrar_ranking(ranking):
    """Muestra el ranking en la consola."""
    print("\n--- RANKING DE SOLITARIO ---")
    if not ranking:
        print("El ranking está vacío. ¡Sé el primero en jugar y ganar!")
        input("\nPresiona Enter para volver al menú principal...")
        return

    print("Nombre         | Movimientos")
    print("---------------|-------------")
    # Itera directamente sobre la lista 'ranking'
    for nombre, puntuacion in ranking:
        print(f"{nombre:<14} | {puntuacion:<11}")
    input("\nPresiona Enter para volver al menú principal...")
