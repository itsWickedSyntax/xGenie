from flask import Flask, render_template, request, jsonify
from backend.core.scanner import Scanner
import threading

app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend/static')

# Store scan results
scan_results = {}
scan_status = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/scan', methods=['POST'])
def start_scan():
    data = request.json
    target = data.get('target')
    deep = data.get('deep', False)
    
    if not target:
        return jsonify({'error': 'Target required'}), 400
    
    scan_id = f"scan_{len(scan_results) + 1}"
    scan_status[scan_id] = {'status': 'running', 'progress': 0}
    
    # Run scan in background thread
    def run_scan():
        scanner = Scanner(target)
        results = scanner.run_full_scan(deep=deep)
        scan_results[scan_id] = results
        scan_status[scan_id] = {'status': 'completed', 'progress': 100}
    
    thread = threading.Thread(target=run_scan)
    thread.start()
    
    return jsonify({'scan_id': scan_id, 'status': 'started'})

@app.route('/api/scan/<scan_id>/status', methods=['GET'])
def get_scan_status(scan_id):
    if scan_id not in scan_status:
        return jsonify({'error': 'Scan not found'}), 404
    
    return jsonify(scan_status[scan_id])

@app.route('/api/scan/<scan_id>/results', methods=['GET'])
def get_scan_results(scan_id):
    if scan_id not in scan_results:
        return jsonify({'error': 'Results not available'}), 404
    
    return jsonify(scan_results[scan_id])

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
