def get_franja(numero):
    # Diferencia si no se etiqueto
    if numero != None:
        try:
            numero_escrito = int(numero)
            decena = numero_escrito // 10
            if decena > 0:
                return (decena + 1) * 10
            else:
                return 10
        except Exception as e:
            # En caso que se etiquete algo que no sea un numero
            print("No se etiqueto un numero, se etiqueto :", numero)
        else:
            return None
    else:
        return None