from flask import Flask, request, redirect, jsonify, render_template
import os
from werkzeug.utils import secure_filename
from predictCatOrCheese import catOrCheese

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sendfile', methods=['POST'])
def send_file():
    fileob = request.files["file2upload"]
    filename = secure_filename(fileob.filename)
    save_path = "{}/{}".format(app.config["UPLOAD_FOLDER"], filename)
    fileob.save(save_path)

    # open and close to update the access time.
    with open(save_path, "r") as f:
        pass
    print(fileob)
    return catOrCheese(fileob)

if __name__ == '__main__':
    app.run(debug=False)
