from flask import Blueprint, request, jsonify
from utils.annotator import annotate_docx
import os

bp_docx = Blueprint('docx', __name__)

@bp_docx.route('/process_docx', methods=['POST'])
def process_docx():
    filename = request.json.get('filename')
    filepath = os.path.join('uploads', filename)

    if not os.path.exists(filepath):
        return jsonify({'error': 'Файл не найден'}), 404

    if not filename.lower().endswith('.docx'):
        return jsonify({'error': 'Файл не является DOCX'}), 400

    try:
        annotated_filepath = annotate_docx(filepath)
        return jsonify({'annotated_path': annotated_filepath})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
