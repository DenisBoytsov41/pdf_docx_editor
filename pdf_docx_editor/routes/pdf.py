from flask import Blueprint, request, jsonify
from utils.annotator import annotate_pdf
import os

bp_pdf = Blueprint('pdf', __name__)

@bp_pdf.route('/process_pdf', methods=['POST'])
def process_pdf():
    filename = request.json.get('filename')
    filepath = os.path.join('uploads', filename)

    if not os.path.exists(filepath):
        return jsonify({'error': 'Файл не найден'}), 404

    if not filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Файл не является PDF'}), 400

    try:
        annotated_filepath = annotate_pdf(filepath)
        return jsonify({'annotated_path': annotated_filepath})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
