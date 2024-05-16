from flask import Flask, request, render_template, jsonify
from rembg import remove
from PIL import Image
import os
from io import BytesIO
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Define the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# defines only allowed extension as png
ALLOWED_EXTENSIONS = {'png'}

#limits file size to 16 MB
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# checks that a period is in filename (signifies extentsion), splits the filename into the part before the period and after, selects the second item which is the extension, makes it lower case, then checks to see if its in allowed extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('uploadtest.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'})
    
    #message if file is too large
    if file.content_length > MAX_CONTENT_LENGTH:
        return jsonify({'error': 'File size exceeds limit'})
    
    filename = secure_filename(file.filename)
    
    if file:
        # Save the uploaded image to the upload folder
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        try:
            # Open the input image
            input_image = Image.open(filename)
            
            # Remove the background
            output_image = remove(input_image)
            
            # Save the processed image
            output_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_' + file.filename)
            output_image.save(output_filename)
            
            # Remove the uploaded image
            os.remove(filename)
            
            return jsonify({'filename': 'processed_' + file.filename})
        except Exception as e:
            return jsonify({'error': str(e)})
    return jsonify({'error': 'Unknown error'})
    
if __name__ == '__main__':
    app.run(debug=True)
