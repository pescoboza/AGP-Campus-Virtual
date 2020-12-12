from flask import Blueprint

from time import time
from datetime import date
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.lib.pagesizes import LETTER, landscape
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.ttfonts import TTFont

registerFont(TTFont("GlacialIndifference-Regular",
                    "app/static/certificate/GlacialIndifference-Regular.ttf"))
registerFont(TTFont("GlacialIndifference-Bold",
                    "app/static/certificate/GlacialIndifference-Bold.ttf"))

AUTHOR = "Agrupación George Papanicolaou de Hermosillo A. C."

SIZE = landscape(LETTER)
W = SIZE[0]
H = SIZE[1]

CERT_NAME = {
    "plmn": "Cáncer de Pulmón",
    "mama": "Cáncer de Mama",
    "crvu": "Cáncer Cervicouterino",
    "psta": "Cáncer de Próstata",
    "tstc": "Cáncer Testicular"
}

IMG_NAME = {
    "plmn": "static/certificate/cert_plmn.jpg",
    "mama": "static/certificate/cert_mama.jpg",
    "crvu": "static/certificate/cert_crvu.jpg",
    "psta": "static/certificate/cert_psta.jpg",
    "tstc": "static/certificate/cert_tstc.jpg"
}

# Returns reportlab Canvas of certificate
def generate_certificate(output_filename, name, topic, date=date.today(), ):
    if topic not in IMG_NAME:
        raise ValueError(f"Invalid topic code '{topic}'")

    canvas = Canvas(output_filename, pagesize=SIZE)
    canvas.drawImage(IMG_NAME[topic], 0, 0, width=W, height=H)

    canvas.setAuthor(AUTHOR)
    canvas.setTitle("Constancia de {} a {}".format(CERT_NAME[topic], name))

    # CONSTANCIA
    canvas.setFont("GlacialIndifference-Regular", 32)
    canvas.drawCentredString(W/2, H * 0.55, "CONSTANCIA")

    # A
    canvas.drawCentredString(W/2, H * 0.45, "A")

    # NOMBRE COMPLETO
    canvas.setFont("GlacialIndifference-Bold", 28)
    canvas.drawCentredString(W/2, H * 1/3, name.upper())

    # Por haber acreditado...
    canvas.setFont("GlacialIndifference-Regular", 20)
    canvas.drawCentredString(
        W/2, H * 0.25, "Por haber acreditado el programa preventivo de:")

    # Tipo de cancer
    canvas.setFont("GlacialIndifference-Bold", 20)
    canvas.drawCentredString(W/2, H * 0.20, CERT_NAME[topic])

    # Fecha
    canvas.setFont("GlacialIndifference-Regular", 20)

    canvas.drawCentredString(
        W/2, H * 0.15, "{}/{}/{}".format(date.day, date.month, date.year))

    return canvas


def timestamp_str():
    return str(time()).replace('.', '')



certificate = Blueprint("certificate", __name__)

from . import views
