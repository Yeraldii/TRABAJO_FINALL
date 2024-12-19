import requests
from bs4 import BeautifulSoup

def buscar_ofertas_jora(termino_busqueda, ubicacion=None):
    url_base = "https://pe.jora.com/j?"

    params = {
        "q": termino_busqueda,
        "l": ubicacion if ubicacion else ""
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    resultados = []
    for page in range(1, 3):  # Buscar en las primeras dos páginas de resultados
        params['page'] = page
        response = requests.get(url_base, params=params, headers=headers)
        
        if response.status_code != 200:
            continue
        
        soup = BeautifulSoup(response.text, "html.parser")
        ofertas = soup.find_all("div", class_="job-card result sponsored-job spon-top") + soup.find_all("div", class_="job-card result")

        for oferta in ofertas:
            try:
                titulo_element = oferta.find("h2", class_="job-title").find("a")
                titulo = titulo_element.text.strip() if titulo_element else "Sin título"
                link = "https://pe.jora.com" + titulo_element["href"] if titulo_element else ""
                
                empresa_element = oferta.find("div", class_="job-info").find("span", class_="job-company")
                empresa = empresa_element.text.strip() if empresa_element else "Sin empresa"
                
                ubicacion_element = oferta.find("a", class_="job-location")
                ubicacion = ubicacion_element.text.strip() if ubicacion_element else "Sin ubicación"

                resultados.append({
                    "titulo": titulo,
                    "empresa": empresa,
                    "ubicacion": ubicacion,
                    "link": link
                })
            except AttributeError:
                continue

        if len(resultados) >= 15:  # Limitar los resultados a los primeros 15
            break

    return resultados
