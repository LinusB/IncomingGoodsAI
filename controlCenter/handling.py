import subprocess
import os
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS  # Nur falls CORS für andere Zwecke erforderlich ist

app = Flask(__name__)
CORS(app)  # Für Cross-Origin-Anfragen, falls später benötigt
socketio = SocketIO(app)

# Definiere den Pfad zu ImageCapturing.py und imageClassification.py
script_dir = os.path.dirname(os.path.abspath(__file__))
image_capturing_path = os.path.join(script_dir, '..', 'capturing', 'imageCapturing.py')
image_classification_path = os.path.join(script_dir, '..', 'classification', 'imageClassification.py')

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
            else:
                socketio.emit('status_update', {'message': 'Fehler bei der Klassifizierung'})
        else:
            socketio.emit('status_update', {'message': 'Fehler bei der Bildaufnahme'})
    except Exception as e:
        socketio.emit('status_update', {'message': str(e)})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
