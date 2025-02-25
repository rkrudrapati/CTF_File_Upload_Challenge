from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, send_file
import os
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'supersecretkey'  # For flashing messages

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        flash('File does not exist!')
        return redirect(url_for('index'))
    file = request.files['image']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        exec_path = app.config['UPLOAD_FOLDER']+ filename
        os.chmod(exec_path,mode=0o775)
        flash('File uploaded successfully!')
        return redirect(url_for('gallery'))
    else:
        flash('Only JPG, JPEG, PNG & GIF files are allowed.')
        return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    file_path = f"{app.config['UPLOAD_FOLDER']}{filename}"
    print(f"file path: {file_path}")
    command = f"{file_path}"
    print(f"the command is {command}")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Get the output and error (if any)
    stdout, stderr = process.communicate()
    # Decode the stdout bytes to string
    captured_output = stdout.decode('utf-8')
    if not captured_output:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    elif captured_output:
        return f'<img src="{file_path}" alt={filename}/> \n {captured_output}'


@app.route('/gallery')
def gallery():
   files = os.listdir(app.config['UPLOAD_FOLDER'])
   return render_template('gallery.html', files=files)

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
