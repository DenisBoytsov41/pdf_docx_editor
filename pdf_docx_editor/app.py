from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from routes.docx import bp_docx
from routes.pdf import bp_pdf
from PyPDF2 import PdfReader
from docx import Document
from flask import send_from_directory

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.register_blueprint(bp_pdf)
app.register_blueprint(bp_docx)

def allowed_file(filename):
    """Проверяет, разрешён ли тип файла."""
    allowed_extensions = {'pdf', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route('/')
def index():
    """Главная страница."""
    return render_template('index.html')

@app.route('/download/uploads/<filename>')
def download_file(filename):
    """Маршрут для скачивания файла."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Обработка загрузки файлов и возвращение содержимого."""
    if 'file' not in request.files:
        return jsonify({'error': 'Файл не был загружен'}), 400

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        file_content = ""
        if filename.lower().endswith('.pdf'):
            file_content = read_pdf(filepath)
        elif filename.lower().endswith('.docx'):
            file_content = read_docx(filepath)

        return jsonify({'filename': filename, 'content': file_content})
    return jsonify({'error': 'Недопустимый тип файла'}), 400


def read_pdf(filepath):
    """Чтение содержимого PDF файла."""
    reader = PdfReader(filepath)
    content = ""
    for page in reader.pages:
        content += page.extract_text() + "\n"
    return content


def read_docx(filepath):
    """Чтение содержимого DOCX файла."""
    doc = Document(filepath)
    content = ""
    for paragraph in doc.paragraphs:
        content += paragraph.text + "\n"
    return content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
