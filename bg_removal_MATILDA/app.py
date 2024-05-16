from flask import Flask, request, render_template, jsonify
from rembg import remove
from PIL import Image
import os

app = Flask(__name__)

# Define the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

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


@app.route('/uploadtest', methods=['GET', 'POST'])
def upload_test():
    if request.method == 'GET':
        return render_template('uploadtest.html')
    elif request.method == 'POST':
        # This block is for handling the test upload
        if 'file' not in request.files:
            return jsonify({'error': 'No file part for upload test'})

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file for upload test'})

        # Handle the test upload as needed
        return jsonify({'message': 'Test upload successful'})  

if __name__ == '__main__':
    app.run(debug=True)
