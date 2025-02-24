from flask import Flask, jsonify, Response
import subprocess
import os
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


#CORS(app, origins=["http://localhost:3000", "https://tableau-looker-ui-new-design-1057220697534.us-central1.run.app"])

CORS(app, resources={r"/run-selenium": {"origins": ["http://localhost:3000", "https://tableau-looker-ui-new-design-1057220697534.us-central1.run.app"]}})


LOG_FILE = os.path.join(os.path.dirname(__file__), "../logs/selenium_log.log")
os.environ["DISPLAY"] = ":0"
os.environ["XDG_RUNTIME_DIR"] = "/run/user/1000"


@app.route('/run-script', methods=['POST'])
def run_script():
    """API to run the Selenium script and clear previous logs."""
    try:
        # Run Selenium script as a subprocess
        process = subprocess.Popen(["python", "selenium_runner.py"])
        return jsonify({"message": "Script started", "status": "running"}), 200
    except Exception as e:
        return jsonify({"message": "Script failed to start", "error": str(e)}), 500

@app.route('/get-latest-logs', methods=['GET'])
def get_latest_logs():
    """API to stream the latest logs in real-time."""
    def stream_logs():
        with open(LOG_FILE, "r") as log_file:
            while True:
                line = log_file.readline()
                if line:
                    yield f"data: {line}\n\n"
                else:
                    time.sleep(1)  # Wait before checking for new logs

    return Response(stream_logs(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
