def get_franja(numero):
    # Chequea  si no esta  etiqueto
    if numero != None:
        try:
            numero_escrito = int(numero)
            decena = numero_escrito // 10
            resto = numero_escrito % 10
            if decena > 0 and resto > 0:
                return (decena + 1) * 10
            elif decena > 0 and resto == 0:
                return (decena) * 10
            else:
                return 10
        except Exception as e:
            # En caso que se etiquete algo que no sea un numero
            print("No se etiqueto una edad, se etiqueto :", numero)
        else:
            return None
    else:
        return None