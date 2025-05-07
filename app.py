from flask import Flask, request, render_template, send_from_directory
import os
from your_script import process_image  # your image processing function
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/output'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = secure_filename(file.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], 'input_' + filename)
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output_' + filename)

    file.save(input_path)

    # Call your processing function
    process_image(input_path, output_path)

    return {'output': f'/static/output/output_{filename}'}

@app.route('/static/output/<filename>')
def output_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
