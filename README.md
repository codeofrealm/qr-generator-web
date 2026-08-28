# Zeronex QR Code Generator

A minimal web app that generates high-quality QR codes from any link or text, with an automatic **Zeronex** watermark baked into every image.

## Features

- Generate QR codes instantly from any URL or text
- Zeronex watermark embedded directly into the image
- Download QR codes as PNG files
- No images stored on the server — everything is generated in memory
- Clean dark UI, fully responsive

## Project Structure

```
qr-code/
├── app.py               # Flask app — routes and QR generation logic
├── templates/
│   └── index.html       # Frontend UI with inline JS
└── static/
    └── style.css        # Styles
```

## Requirements

- Python 3.8+
- Flask
- qrcode
- Pillow

Install dependencies:

```bash
pip install flask qrcode[pil] pillow
```

## Running the App

```bash
python app.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## How It Works

1. User enters a URL or text and clicks **Generate QR Code**
2. The form submits to `/generate` via `fetch`
3. Flask generates the QR code in memory using `qrcode` + `Pillow`, applies the Zeronex watermark, and returns it as a base64 PNG
4. The image is displayed in the browser
5. Clicking **Download QR Code** posts to `/download`, which streams the PNG as a file attachment

## Notes

- QR codes use `ERROR_CORRECT_H` (30% error correction) for maximum scannability even with the watermark
- No files are written to disk at any point
