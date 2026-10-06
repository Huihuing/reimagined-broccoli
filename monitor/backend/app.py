from flask import Flask, jsonify, request


app = Flask(__name__)
events: list[dict] = []


@app.route("/api/events", methods=["GET", "POST"])
def api_events():
    if request.method == "POST":
        event = request.get_json(silent=True)
        if not isinstance(event, dict):
            return jsonify({"error": "JSON 객체가 필요합니다."}), 400
        events.append(event)
        return jsonify({"saved": True}), 201

    return jsonify({"events": events, "count": len(events)})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5200, debug=True)
