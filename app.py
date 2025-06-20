from flask import Flask, render_template, request, send_file
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    images = request.files.getlist('images')
    image_list = []

    for image in images:
        img = Image.open(image.stream).convert('RGB')
        image_list.append(img)

    if not image_list:
        return "Nenhuma imagem válida enviada."

    output_path = os.path.join(UPLOAD_FOLDER, 'output.pdf')
    print(f"Salvando PDF em: {output_path}")
    image_list[0].save(output_path, save_all=True, append_images=image_list[1:])

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

