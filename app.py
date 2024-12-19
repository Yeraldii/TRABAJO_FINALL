from flask import Flask, render_template, request
from Webscraping.Computrabajo import buscar_ofertas_computrabajo
from Webscraping.Trabajando_pe import buscar_ofertas_trabajando
from Webscraping.Jora import buscar_ofertas_jora

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/Templates/resultados", methods=["GET"])
def resultados():
    tipo_trabajo = request.args.get("tipo_trabajo")
    empresa = request.args.get("empresa")
    ubicacion = request.args.get("ubicacion")

    ofertas_computrabajo = buscar_ofertas_computrabajo(tipo_trabajo, ubicacion)
    ofertas_trabajando = buscar_ofertas_trabajando(tipo_trabajo, ubicacion)
    ofertas_jora = buscar_ofertas_jora(tipo_trabajo, ubicacion)

    return render_template("resultados.html", 
                           ofertas_computrabajo=ofertas_computrabajo,
                           ofertas_trabajando=ofertas_trabajando,
                           ofertas_jora=ofertas_jora)

if __name__ == "__main__":
    app.run(debug=True)
