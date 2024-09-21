import requests
from bs4 import BeautifulSoup
import re

def limpiar_nombre_perfume(nombre):
    nombre_limpio = re.sub(r"['\"]", "", nombre)
    nombre_limpio = nombre_limpio.replace(" ", "+")
    return nombre_limpio

def obtener_info_producto(url, selector_precio, sitio_nombre):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        respuesta = requests.get(url, headers=headers)
        respuesta.raise_for_status()
        
        sopa = BeautifulSoup(respuesta.text, 'html.parser')
        
        if sitio_nombre == "SilkPerfumes":
            elemento_script = sopa.select_one("script#web-pixels-manager-setup")
            if elemento_script:
                contenido_script = elemento_script.string
                match = re.search(r'"amount":(\d+)', contenido_script)
                if match:
                    precio = int(match.group(1))
                    return f"${precio:,.0f}".replace(",", ".")
        elif sitio_nombre == "Dperfumes":
            elemento_precio = sopa.select_one(selector_precio)
            if elemento_precio:
                texto_precio = elemento_precio.text.strip()
                match = re.search(r'\$\d+(?:\.\d+)?', texto_precio)
                if match:
                    return match.group(0)
        else:
            elemento_precio = sopa.select_one(selector_precio)
            if elemento_precio:
                return elemento_precio.text.strip()
        
        return "Precio no encontrado"
    except Exception as e:
        return f"Error: {str(e)}"

def buscar_perfume(marca, nombre, sitios):
    resultados = []
    for sitio in sitios:
        perfume_buscado = f"{marca} {nombre}"
        nombre_busqueda = limpiar_nombre_perfume(perfume_buscado)
        
        url_busqueda = sitio["url_base"] + nombre_busqueda + sitio["parametro_busqueda"]
        precio = obtener_info_producto(url_busqueda, sitio["selector_precio"], sitio["nombre"])
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
        "nombre": "Dperfumes",
        "url_base": "https://dperfumes.cl/?s=",
        "parametro_busqueda": "&post_type=product",
        "selector_precio": "span.screen-reader-text:nth-of-type(2)"
    },
    {
        "nombre": "SilkPerfumes",
        "url_base": "https://silkperfumes.cl/search?type=product%2C&options%5Bprefix%5D=last&q=",
        "parametro_busqueda": "&filter.p.product_type=",
        "selector_precio": "strong.price_current" 
    }
]

# Nombre y marca del perfume a buscar
marca_perfume = "MontBlanc"
nombre_perfume = "Legend Spirit"

# Realizar la búsqueda
resultados = buscar_perfume(marca_perfume, nombre_perfume, sitios)

# Imprimir resultados
print(f"Resultados para: {marca_perfume} {nombre_perfume}")
for resultado in resultados:
    print(f"Sitio: {resultado['sitio']}")
    print(f"URL: {resultado['url']}")
    print(f"Precio: {resultado['precio']}")
    print("---")