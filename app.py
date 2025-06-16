import os
from flask import Flask, render_template, send_from_directory, request, redirect, url_for

app = Flask(__name__)
UPLOAD_DIR = os.path.join(app.root_path, 'uploads')
KEY_DIR    = os.path.join(UPLOAD_DIR, 'pgp')

@app.route("/")
def home():
    files = os.listdir(os.path.join(UPLOAD_DIR, 'files')) if os.path.isdir(os.path.join(UPLOAD_DIR, 'files')) else []
    return render_template("index.html", files=files)

@app.route("/files/<path:fname>")
def download(fname):
    return send_from_directory(os.path.join(UPLOAD_DIR,'files'), fname, as_attachment=True)

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("file")
    if f:
        dest = os.path.join(UPLOAD_DIR, 'files')
        os.makedirs(dest, exist_ok=True)
        f.save(os.path.join(dest, f.filename))
    return redirect(url_for("home"))

@app.route("/pgp-key")
def pgp_key():
    return send_from_directory(KEY_DIR, "public_key.asc", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)
