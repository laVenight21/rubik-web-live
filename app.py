from flask import Flask, Response, jsonify, render_template, request

import bridge

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/api/start")
def api_start():
    s = bridge.create_session()
    if s is None:
        return jsonify(error="Server sedang penuh, coba lagi beberapa saat lagi."), 503
    return jsonify(sid=s.id)


@app.post("/api/frame/<sid>")
def api_frame(sid):
    s = bridge.get_session(sid)
    if s is None:
        return jsonify(error="Sesi tidak ditemukan atau sudah berakhir"), 404
    jpeg = s.submit(request.get_data())
    resp = Response(jpeg, mimetype="image/jpeg")
    resp.headers["X-Done"] = "1" if s.done else "0"
    if s.error:
        resp.headers["X-Error"] = s.error.encode("ascii", "replace").decode()[:200]
    return resp


@app.post("/api/key/<sid>")
def api_key(sid):
    s = bridge.get_session(sid)
    if s is None:
        return jsonify(error="Sesi tidak ditemukan"), 404
    s.push_key((request.get_json(silent=True) or {}).get("key", ""))
    return jsonify(ok=True)


@app.post("/api/stop/<sid>")
def api_stop(sid):
    bridge.close_session(sid)
    return jsonify(ok=True)


if __name__ == "__main__":
    app.run(debug=False, threaded=True)
