from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, send_file
import os
import subprocess

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}
app.config['SECRET_KEY'] = 'supersecretkey'  # For flashing messages

def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
   if 'image' not in request.files:
       flash('No file part')
       return redirect(url_for('index'))
   file = request.files['image']
   if file.filename == '':
       flash('No selected file')
       return redirect(url_for('index'))
   if file and allowed_file(file.filename):
       filename = file.filename
       file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
       flash('File uploaded successfully!')
       return redirect(url_for('gallery'))
   else:
       flash('Only JPG, JPEG, PNG & GIF files are allowed.')
       return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
   return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/gallery')
def gallery():
   files = os.listdir(app.config['UPLOAD_FOLDER'])
   return render_template('gallery.html', files=files)


# Home page route
@app.route('/ip')
def ipindex():
    return render_template('ipindex.html')

# Route to handle the ping request
@app.route('/ping', methods=['POST'])
def ping():
    ip_address = request.form['ip_address']  # Get the IP address from the form
    
    try:
        # Ping the IP address
        result = subprocess.run(['ping', '-c', '4', ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE)#, shell=True)
        
        # If ping command failed
        if result.returncode != 0:
            response = f"Failed to ping {ip_address}. Error: {result.stderr.decode('utf-8')}"
        else:
            # Decode and return the output
            response = result.stdout.decode('utf-8')
        
    except Exception as e:
        response = f"Error: {str(e)}"
    
    return render_template('result.html', ip_address=ip_address, response=response)


if __name__ == "__main__":
   app.run(debug=True)

