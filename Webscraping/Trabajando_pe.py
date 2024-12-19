import requests
from bs4 import BeautifulSoup

def buscar_ofertas_trabajando(termino_busqueda, empresa=None, ubicacion=None):
    url_base = "https://trabajando.pe/trabajos"
    
    # Parámetros de búsqueda
    params = {
        "search_keywords": termino_busqueda,
        "search_location": ubicacion if ubicacion else ""
    }
    
    # Si se proporciona una empresa, agregarla a los parámetros de búsqueda
    if empresa:
        params["search_keywords"] += f" {empresa}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    # Realizar la solicitud HTTP a la página de resultados
    response = requests.get(url_base, params=params, headers=headers)

    if response.status_code != 200:
        return [{"titulo": "No se encontró trabajo con los términos que usted especificó", "empresa": "N/A", "ubicacion": "N/A", "link": ""}]
    
    # Analizar el contenido HTML con BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    ofertas = soup.find_all("article", class_="job_listing")

    resultados = []

    for oferta in ofertas[:10]:  # Limitar los resultados a los primeros 10
        try:
            # Título del trabajo y enlace
            titulo_element = oferta.find("h2", class_="entry-title")
            titulo = titulo_element.text.strip() if titulo_element else "Sin título"
            link = titulo_element.find("a")["href"] if titulo_element else ""
            
            # Empresa
            empresa_element = oferta.find("div", class_="company-name")
            empresa = empresa_element.text.strip() if empresa_element else "Sin empresa"
            
            # Ubicación
            ubicacion_element = oferta.find("div", class_="company-address")
            ubicacion = ubicacion_element.text.strip() if ubicacion_element else "Sin ubicación"

            # Salario (si está presente)
            salario_element = oferta.find("div", class_="salary-amt")
            salario = salario_element.text.strip() if salario_element else "No especificado"

            resultados.append({
                "titulo": titulo,
                "empresa": empresa,
                "ubicacion": ubicacion,
                "salario": salario,
                "link": link
            })
        except AttributeError:
            continue

    return resultados
