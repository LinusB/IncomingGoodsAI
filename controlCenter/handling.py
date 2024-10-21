import subprocess
import os
from flask import Flask, render_template, send_from_directory, make_response
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from openpyxl import Workbook, load_workbook
from datetime import datetime

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

# Definiere den Pfad zu ImageCapturing.py und imageClassification.py
script_dir = os.path.dirname(os.path.abspath(__file__))
image_capturing_path = os.path.join(script_dir, '..', 'capturing', 'imageCapturing.py')
image_classification_path = os.path.join(script_dir, '..', 'classification', 'imageClassification.py')
generate_excel_monthly_report_path = os.path.join(script_dir, '..', 'creation', 'generate_excel_monthly_report.py')
generate_excel_yearly_report_path = os.path.join(script_dir, '..', 'creation', 'generate_excel_yearly_report.py')

# Route für den Zugriff auf Dateien im currentProcess-Ordner
@app.route('/currentProcess/<path:filename>')
def serve_current_process_file(filename):
    current_process_dir = os.path.join(script_dir, './currentProcess')  # Ordnerpfad für currentProcess
    return send_from_directory(current_process_dir, filename)

def run_script(script_path):
    process = subprocess.Popen(['python', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for stdout_line in iter(process.stdout.readline, ""):
        socketio.emit('status_update', {'message': stdout_line})
    process.stdout.close()
    process.wait()
    for stderr_line in iter(process.stderr.readline, ""):
        socketio.emit('status_update', {'message': stderr_line})
    process.stderr.close()
    return process.returncode

@app.route('/start_capture', methods=['GET'])
def start_capture():
    try:
        # Führe ImageCapturing.py aus
        returncode_capture = run_script(image_capturing_path)
        
        if returncode_capture == 0:
            # Führe imageClassification.py aus
            returncode_classification = run_script(image_classification_path)
            
            if returncode_classification == 0:
                socketio.emit('status_update', {'message': 'Bildaufnahme und Klassifizierung erfolgreich'})
                returncode_report = run_script(generate_excel_monthly_report_path)
                if returncode_report == 0:
                    socketio.emit('status_update', {'message': 'Monatlicher Excel-Bericht erfolgreich generiert'})
                else:
                    socketio.emit('status_update', {'message': 'Fehler beim Generieren des monatlichen Excel-Berichts'})
            else:
                socketio.emit('status_update', {'message': 'Fehler bei der Klassifizierung'})
        else:
            socketio.emit('status_update', {'message': 'Fehler bei der Bildaufnahme'})
    except Exception as e:
        socketio.emit('status_update', {'message': str(e)})

# Funktion, um nur die gewünschten Spalten der letzten 5 Einträge zu extrahieren
def get_last_five_entries(file_path):
    if not os.path.exists(file_path):
        return []

    workbook = load_workbook(file_path)
    sheet = workbook.active
    
    # Wir interessieren uns nur für die Spalten:
    # - Warennummer (Spalte 1)
    # - Abschnittsbeschreibung (Spalte 7)
    # - Infrastat-Beschreibung (Spalte 8)
    rows = list(sheet.iter_rows(min_row=2, values_only=True))
    recent_entries = rows[-5:]  # Die letzten 5 Zeilen auswählen
    
    # Nur die gewünschten Spalten extrahieren
    filtered_entries = [(row[0], row[6], row[7]) for row in recent_entries]
    
    return filtered_entries

# Route für die Hauptseite
@app.route('/')
def index():
    response = make_response(render_template('index.html'))
    
    # Setze die Header, um das Caching zu deaktivieren
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response

# Route für die Report-Seite
@app.route('/report')
def report():
    excel_file_path = os.path.join(script_dir, '..', 'results', f"Wareneingang_{datetime.now().strftime('%m%Y')}.xlsx")
    recent_entries = get_last_five_entries(excel_file_path)
    
    response = make_response(render_template('report.html', entries=recent_entries))
    
    # Setze die Header, um das Caching zu deaktivieren
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response

# Route für den Monatsreport (Excel-Datei des aktuellen Monats)
@app.route('/download_monthly_report')
def download_monthly_report():
    # Generiere den Dateinamen basierend auf dem aktuellen Monat
    month_file_name = f"Wareneingang_{datetime.now().strftime('%m%Y')}.xlsx"
    file_path = os.path.join(script_dir, '..', 'results')  # Verzeichnis, in dem sich die Datei befindet
    return send_from_directory(directory=file_path, path=month_file_name, as_attachment=True)

# Route für den Jahresreport (Excel-Datei des aktuellen Jahres)
@app.route('/download_yearly_report')
def download_yearly_report():
    returncode_report = run_script(generate_excel_yearly_report_path)
    if returncode_report == 0:
        socketio.emit('status_update', {'message': 'Monatlicher Excel-Bericht erfolgreich generiert'})
    else:
        socketio.emit('status_update', {'message': 'Fehler beim Generieren des monatlichen Excel-Berichts'})
    # Generiere den Dateinamen basierend auf dem aktuellen Jahr
    year_file_name = f"Jahreswareneingang_{datetime.now().strftime('%Y')}.xlsx"
    file_path = os.path.join(script_dir, '..', 'results')  # Verzeichnis, in dem sich die Datei befindet
    return send_from_directory(directory=file_path, path=year_file_name, as_attachment=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)