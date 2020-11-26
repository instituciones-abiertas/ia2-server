import requests
import urllib

# Mejora por lotes: https://datosgobar.github.io/georef-ar-api/bulk/
# Formato esperable: https://datosgobar.github.io/georef-ar-api/addresses/
API_BASE_URL = "https://apis.datos.gob.ar/georef/api/"


def get_direcciones(endpoint, direccion, provincia, **kwargs):
    kwargs["provincia"] = provincia
    kwargs["direccion"] = direccion
    kwargs["aplanar"] = True
    url = "{}{}?{}".format(API_BASE_URL, endpoint, urllib.parse.urlencode(kwargs))
    return requests.get(url).json()[endpoint]


def get_comuna_caba(direccion):
    try:
        direcciones = get_direcciones("direcciones", direccion, "caba")
        datos = {
            "nombre": direcciones[0]["departamento_nombre"],
            "lat": direcciones[0]["ubicacion_lat"],
            "lon": direcciones[0]["ubicacion_lon"],
        }
        return datos
    except Exception:
        print("No pudo encontrar una comuna valida para", direccion)
        return None


if __name__ == "__main__":
    comuna = get_comuna_caba("Av de mayo 776")
    print(comuna)
