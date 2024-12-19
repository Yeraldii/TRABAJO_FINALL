import requests
from bs4 import BeautifulSoup

def buscar_ofertas_computrabajo(termino_busqueda, empresa=None):
    url_base = "https://pe.computrabajo.com/ofertas-de-trabajo/?q="

    termino_busqueda = termino_busqueda.replace(" ", "+")

    if empresa:
        empresa = empresa.replace(" ", "+")
        url = f"{url_base}{termino_busqueda}+{empresa}"
    else:
        url = f"{url_base}{termino_busqueda}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Referer": "https://pe.computrabajo.com",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return [{"titulo": "No se encontró trabajo con los términos que usted especificó", "empresa": "N/A", "ubicacion": "N/A", "link": ""}]

    soup = BeautifulSoup(response.text, "html.parser")
    ofertas = soup.find_all("article", class_="box_offer")

    resultados = []

    for oferta in ofertas[:10]:
        try:
            titulo = oferta.find("a", class_="js-o-link").text.strip()

            empresa = oferta.find("a", class_="fc_base t_ellipsis").text.strip() if oferta.find("a", class_="fc_base t_ellipsis") else "Sin especificar"

            ubicacion_element = oferta.find("p", class_="fs16 fc_base mt5")
            if ubicacion_element:
                ubicacion = ubicacion_element.find("span", class_="mr10").text.strip()
            else:
                ubicacion = "Sin ubicación"

            link = oferta.find("a", class_="js-o-link")["href"]
            link = f"https://pe.computrabajo.com{link.split('?')[0]}"

            resultados.append({
                "titulo": titulo,
                "empresa": empresa,
                "ubicacion": ubicacion,
                "link": link
            })
        except AttributeError:
            continue

    return resultados
