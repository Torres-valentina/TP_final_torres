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

def guardar_ranking(nombre, puntaje):
    """
    Guarda el nombre y puntaje del jugador en un archivo de texto.

    Args:
        nombre (str): Nombre del jugador.
        puntaje (int): Puntaje obtenido.
    """
    with open(ARCHIVO_RANKING, "a", encoding="utf-8") as archivo:
        archivo.write(f"{nombre},{puntaje}\n")


def obtener_estado_ranking():
    """
    Devuelve una lista de líneas formateadas para mostrar el ranking en pantalla.
    """
    ranking = cargar_ranking()
    if not ranking:
        estado = ["El ranking está vacío. ¡Sé el primero en jugar y ganar!"]
    estado = ["Nombre         | Movimientos", "---------------|-------------"]
    for nombre, puntos in ranking:
        estado.append(f"{nombre:<14} | {puntos:<11}")
    return estado
