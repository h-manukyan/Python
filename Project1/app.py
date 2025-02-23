from flask import Flask, request, send_from_directory, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///files.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, nullable=False)

@app.before_request
def create_tables():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")  # Serve the HTML form

@app.route("/files/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    new_file = File(filename=file.filename)
    db.session.add(new_file)
    db.session.commit()

    return jsonify({'message': 'File uploaded', 'file_id': new_file.id}), 201

@app.route("/files/download/<int:file_id>", methods=["GET"])
def download(file_id):
    file_entry = File.query.get(file_id)
    if not file_entry:
        return jsonify({'error': 'File not found'}), 404
    
    return send_from_directory(app.config['UPLOAD_FOLDER'], file_entry.filename, as_attachment=True)   

@app.route('/files/allFiles', methods=['GET'])
def list_files():
    files = File.query.all()
    file_list = [{"filename": file.filename, "file_id": file.id} for file in files]
    return jsonify({"files": file_list})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
