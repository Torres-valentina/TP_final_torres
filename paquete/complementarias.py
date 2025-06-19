def obtener_entrada_entero(prompt, min_val, max_val):
    """
    Solicita al usuario una entrada numérica y la valida sin usar try-except.
    Asegura que la entrada sea un dígito y esté dentro de un rango específico.
    """
    while True:
        entrada = input(prompt).strip()
        if entrada.isdigit():
            num = int(entrada)
            if min_val <= num <= max_val:
                return num
            else:
                print(f"Error: El número debe estar entre {min_val} y {max_val}.")
        else:
            print("Error: Entrada no válida. Por favor, ingresa un número entero.")
