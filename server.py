import sys
import os
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

# Ensure workspace root is in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.database import init_db
from backend.agents.vision_agent import VisionAgent
from backend.agents.analytics_agent import AnalyticsAgent
from backend.agents.procurement_agent import ProcurementAgent
from backend.esg_exporter import generate_esg_report

# Initialize SQLite database schema & seed data
init_db()

vision_agent = VisionAgent()
analytics_agent = AnalyticsAgent()
procurement_agent = ProcurementAgent()

class EcoPlateRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Clean custom request logging
        sys.stdout.write(f"[{self.log_date_time_string()}] {self.command} {self.path} -> {args[0]}\n")

    def _send_json(self, data, status=200):
        body = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, filepath, content_type):
        if not os.path.exists(filepath):
            self.send_error(404, "File Not Found")
            return
        with open(filepath, 'rb') as f:
            content = f.read()
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        # REST API Routes
        if path == '/api/health':
            self._send_json({"status": "healthy", "service": "EcoPlate AI Agent Backend", "version": "1.0.0"})
        elif path == '/api/dashboard/stats':
            data = analytics_agent.analyze_waste_trends()
            self._send_json(data)
        elif path == '/api/agents/analytics':
            data = analytics_agent.analyze_waste_trends()
            self._send_json(data)
        elif path == '/api/esg/report':
            data = generate_esg_report()
            self._send_json(data)
        elif path == '/api/deliverables':
            # Load project deliverables text
            deliverables = {}
            for filename, key in [('1_Lean_Canvas.md', 'lean_canvas'), ('2_Concept_Note.md', 'concept_note'), ('3_Pitch_Deck_Outline.md', 'pitch_deck')]:
                fpath = os.path.join(os.path.dirname(__file__), filename)
                if os.path.exists(fpath):
                    with open(fpath, 'r', encoding='utf-8') as f:
                        deliverables[key] = f.read()
            self._send_json(deliverables)

        # Static File Serving
        elif path == '/' or path == '/index.html':
            self._send_file(os.path.join(os.path.dirname(__file__), 'index.html'), 'text/html; charset=utf-8')
        elif path.startswith('/static/css/'):
            fpath = os.path.join(os.path.dirname(__file__), path.lstrip('/'))
            self._send_file(fpath, 'text/css')
        elif path.startswith('/static/js/'):
            fpath = os.path.join(os.path.dirname(__file__), path.lstrip('/'))
            self._send_file(fpath, 'application/javascript')
        else:
            self.send_error(404, "Route Not Found")

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        content_length = int(self.headers.get('Content-Length', 0))
        body_bytes = self.rfile.read(content_length) if content_length > 0 else b'{}'
        try:
            body = json.loads(body_bytes.decode('utf-8'))
        except Exception:
            body = {}

        if path == '/api/waste/scan':
            dish_name = body.get('dish_name')
            weight = body.get('weight_grams')
            res = vision_agent.scan_disposal_frame(selected_dish=dish_name, custom_weight=weight)
            self._send_json(res)
        elif path == '/api/agents/procurement':
            res = procurement_agent.run_procurement_optimization()
            self._send_json(res)
        else:
            self.send_error(404, "API Endpoint Not Found")

def run_server(port=8000):
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, EcoPlateRequestHandler)
    print(f"============================================================", flush=True)
    print(f"  EcoPlate AI Backend & Web App Server Running!", flush=True)
    print(f"  Access UI at: http://127.0.0.1:{port}", flush=True)
    print(f"  API Health:    http://127.0.0.1:{port}/api/health", flush=True)
    print(f"============================================================", flush=True)
    httpd.serve_forever()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    run_server(port)
