# app.py
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
from analysis import perform_analysis

# Annahme: Du hast bereits eine Funktion, die die Analyse durchführt.
# from analysis import perform_analysis

app = Flask(__name__)
CORS(app)  # Erlaubt Cross-Origin Requests für alle Domains

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'ppt', 'pptx'}

# Sicherstellen, dass der Upload-Ordner existiert
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def your_analysis_function(filepath):
    # Hier käme deine Logik zur Analyse der PowerPoint-Datei
    # Für die Demonstration geben wir einfach statische Werte zurück
    print(f"------------Analyzing file {filepath}------------")
    analysis_result = perform_analysis(filepath)
    print(f"----------------Analysis result: {analysis_result}----------------")
    return analysis_result

@app.route('/api/upload', methods=['POST'])
def file_upload():
    # Prüfen, ob im Request überhaupt eine Datei mitgeschickt wurde
    if 'file' not in request.files:
        return jsonify({'error': 'Keine Datei im Request'}), 400
    file = request.files['file']

    # Prüfen, ob der Dateiname nicht leer ist und ob die Datei erlaubt ist
    if file.filename == '':
        return jsonify({'error': 'Keine Datei ausgewählt'}), 400
    if file and allowed_file(file.filename):
        # Sichere Speicherung der Datei
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Analyse der Datei
        result = your_analysis_function(filepath)
        
        # Antwort mit dem Analyseergebnis
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Ungültiger Dateityp'}), 400

if __name__ == '__main__':
    app.run(debug=True)  # Startet den Server im Debug-Modus
