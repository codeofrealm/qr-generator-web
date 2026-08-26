from flask import Flask, render_template, request, send_file
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)


def create_qr(data):
    # Create QR code in memory
    qr = qrcode.QRCode(
        version=1,
        error_correction=ERROR_CORRECT_H,
        box_size=12,
        border=4
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color="black",
        back_color="white"
    ).convert("RGBA")

    # -----------------------------
    # Zeronex watermark
    # -----------------------------

    overlay = Image.new(
        "RGBA",
        img.size,
        (255, 255, 255, 0)
    )

    draw = ImageDraw.Draw(overlay)

    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            45
        )
    except OSError:
        font = ImageFont.load_default()

    watermark = "Zeronex"

    bbox = draw.textbbox(
        (0, 0),
        watermark,
        font=font
    )

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (img.width - text_width) // 2
    y = (img.height - text_height) // 2

    # Subtle watermark
    draw.text(
        (x, y),
        watermark,
        font=font,
        fill=(100, 100, 100, 35)
    )

    img = Image.alpha_composite(
        img,
        overlay
    )

    # Convert image to memory
    image_buffer = io.BytesIO()

    img.convert("RGB").save(
        image_buffer,
        format="PNG"
    )

    image_buffer.seek(0)

    return image_buffer


@app.route("/", methods=["GET", "POST"])
def home():

    qr_data = None

    if request.method == "POST":

        data = request.form.get(
            "data",
            ""
        ).strip()

        if data:

            image_buffer = create_qr(data)

            # Convert image to Base64 for browser
            import base64

            qr_data = base64.b64encode(
                image_buffer.getvalue()
            ).decode("utf-8")

    return render_template(
        "index.html",
        qr_data=qr_data
    )


@app.route("/download", methods=["POST"])
def download():

    data = request.form.get(
        "data",
        ""
    ).strip()

    if not data:
        return "No QR data provided.", 400

    image_buffer = create_qr(data)

    return send_file(
        image_buffer,
        mimetype="image/png",
        as_attachment=True,
        download_name="Zeronex_QR.png"
    )


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )