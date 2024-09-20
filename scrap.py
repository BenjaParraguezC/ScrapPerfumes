import requests
from bs4 import BeautifulSoup
import re

def limpiar_nombre_perfume(nombre):
    nombre_limpio = re.sub(r"['\"]", "", nombre)
    nombre_limpio = nombre_limpio.replace(" ", "+")
    return nombre_limpio

def obtener_info_producto(url, selector_precio):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        respuesta = requests.get(url, headers=headers)
        respuesta.raise_for_status()
        sopa = BeautifulSoup(respuesta.text, 'html.parser')
        
        elemento_precio = sopa.select_one(selector_precio)
        if elemento_precio:
            return elemento_precio.text.strip()
        
        return "Precio no encontrado"
    except Exception as e:
        return f"Error: {str(e)}"

def buscar_perfume(marca, nombre, sitios):
    perfume_buscado = f"{marca} {nombre}"
    nombre_busqueda = limpiar_nombre_perfume(perfume_buscado)
    nombre_solo = limpiar_nombre_perfume(nombre)
    resultados = []
    for sitio in sitios:
        if sitio["nombre"] == "Cosmetic":
            url_busqueda = f"{sitio['url_base']}{nombre_solo}{sitio['parametro_busqueda']}"
        else:
            url_busqueda = sitio["url_base"] + nombre_busqueda + sitio["parametro_busqueda"]
        precio = obtener_info_producto(url_busqueda, sitio["selector_precio"])
        resultados.append({
            "sitio": sitio["nombre"],
            "url": url_busqueda,
            "precio": precio
        })
    return resultados

# Configuración de los sitios
sitios = [
    {
        "nombre": "Sairam",
        "url_base": "https://sairam.cl/search?q=",
        "parametro_busqueda": "",
        "selector_precio": "div.product-block__price.product-block__price--discount span:first-child"
    },
    {
        "nombre": "ElitePerfumes",
        "url_base": "https://www.eliteperfumes.cl/search?q=",
        "parametro_busqueda": "",
        "selector_precio": ".price__default .price__current"
    },
    {
        "nombre": "Cosmetic",
        "url_base": "https://cosmetic.cl/search?q=",
        "parametro_busqueda": "&type=product",
        "selector_precio": ".money"
    }
]

# Nombre y marca del perfume a buscar
marca_perfume = "MontBlanc"
nombre_perfume = "Legend Spirit edt"

# Realizar la búsqueda
resultados = buscar_perfume(marca_perfume, nombre_perfume, sitios)

# Imprimir resultados
print(f"Resultados para: {marca_perfume} {nombre_perfume}")
for resultado in resultados:
    print(f"Sitio: {resultado['sitio']}")
    print(f"URL: {resultado['url']}")
    print(f"Precio: {resultado['precio']}")
    print("---")