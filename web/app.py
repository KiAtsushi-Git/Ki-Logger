from flask import Flask, render_template, jsonify
import os
from collections import defaultdict

app = Flask(__name__, static_url_path='/static', static_folder='static')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_DIR = os.path.join(BASE_DIR, "logs")

def parse_logs_raw():
    entries = []
    for name in os.listdir(LOG_DIR):
        name_dir = os.path.join(LOG_DIR, name)
        if not os.path.isdir(name_dir):
            continue
        for log_file in sorted(os.listdir(name_dir)):
            full_path = os.path.join(name_dir, log_file)
            with open(full_path, encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("]")
                    if len(parts) >= 4:
                        level = parts[0][1:]
                        time = parts[1][1:]
                        group = parts[2][1:]
                        location = parts[3][1:]
                        msg = "]".join(parts[4:]).strip()
                        entries.append({
                            "name": group,
                            "file": location,
                            "time": time,
                            "level": level,
                            "message": msg
                        })
    entries.sort(key=lambda e: e["time"])
    return entries

@app.route('/')
def index():
    entries = parse_logs_raw()
    grouped = {"ERROR": [], "WARNING": [], "INFO": []}
    for e in entries:
        lvl = e["level"].upper()
        if lvl in grouped:
            grouped[lvl].append(e)
    return render_template("index.html", grouped=grouped)

@app.route("/by-name")
def by_name():
    return render_template("by_name.html")

@app.route("/by-file")
def by_file():
    return render_template("by_file.html")

@app.route("/api/logs/by-name")
def api_logs_by_name():
    entries = parse_logs_raw()
    result = defaultdict(list)
    for e in entries:
        if e["name"]:
            result[e["name"]].append(e)
    print("Имена из логов:", list(result.keys()))
    return jsonify(result)



@app.route("/api/logs/by-file")
def api_logs_by_file():
    entries = parse_logs_raw()

    result = defaultdict(lambda: defaultdict(list))
    for e in entries:
        loc = e["file"]
        if ":" in loc:
            filepath, lineno = loc.rsplit(":", 1)
        else:
            filepath, lineno = loc, "0"
        result[filepath][lineno].append(e)

    result_dict = {}
    for filepath, lines in result.items():
        lines_sorted = dict(sorted(lines.items(), key=lambda x: int(x[0])))
        result_dict[filepath] = lines_sorted

    return jsonify(result_dict)

if __name__ == "__main__":
    app.run(debug=True)
