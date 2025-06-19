from paquete.complementarias import *
from paquete.funciones import *
import sys
def main():
    """
    Muestra el menú principal y maneja las opciones.
    """

    while True:
        print("--- MENÚ PRINCIPAL ---")
        print("1. Jugar")
        print("2. Ver Ranking")
        print("3. Silenciar Juego")
        print("4. Salir")

        opcion = obtener_entrada_entero("Elige una opción: ", 1, 4)

        if opcion == 1:
            #registro jugador
            # Dentro de la funcion juego_solitario, cuando alguien gana:
            movimientos = 10 #harcodeado 
            nombre_jugador = input("Ingresa tu nombre para el ranking: ").strip()
            ranking_actual = cargar_ranking() # Carga la lista de tuplas
            ranking_actual.append((nombre_jugador, movimientos)) # Añade la nueva tupla
            guardar_ranking(ranking_actual) # Guarda la lista de tuplas completa

        elif opcion == 2:
            ranking_actual = cargar_ranking() 
            mostrar_ranking(ranking_actual)
        elif opcion == 3:
            pass
        elif opcion == 4:
            print("¡Hasta pronto!")
            break

if __name__ == "__main__":
    sys.exit(main())