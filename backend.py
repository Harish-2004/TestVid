from flask import Flask, render_template, request, jsonify
import os
from analysis import compute
import base64
from test import *
from flask_cors import CORS  # Import the CORS class
# CORS(app)  # Enable CORS for all routes
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads'
UPLOAD_FOLDER = 'uploads/'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    # Save the uploaded file to a temporary location
    filename = uploaded_file.filename
    file_path = 'temp_video.mp4'
    uploaded_file.save(file_path)

    # Call the compute function from analysis.py
    results, duration = compute(file_path)

    # Pass the results to the template
    return render_template('index.html', results=str(results), duration=duration)
@app.route('/data')
def get_data():
    # Get mobile number and country code from query parameters
    #mobile_number = request.args.get('mobile_number')
    #country_code = request.args.get('country_code')
    mobile_number='1234567890'
    country_code=1
    # Fetch data based on mobile number and country code
    data = fetch_data_by_mobile_number(mobile_number, country_code)
    print(data)

    return jsonify(data)

@app.route('/listoffiles')
def list_files():
    # Get the list of files from the UPLOAD_FOLDER
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    
    # Create a dictionary to store file names and their sizes
    file_info = {}
    for file_name in files:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        file_size = os.path.getsize(file_path)
        file_info[file_name] = file_size
    
    # Return the file information as JSON
    print(file_info)
    return jsonify(file_info)


@app.route('/sendvideo')
def send_video():
    # Specify the name of the video file to send
    video_file_name = 'video.mp4'
    video_file_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file_name)

    # Check if the file exists
    if os.path.exists(video_file_path):
        # Read the binary data of the video file
        with open(video_file_path, 'rb') as f:
            video_data = f.read()
        
        # Encode the binary data into Base64
        base64_encoded_video = base64.b64encode(video_data).decode('utf-8')

        # Create a dictionary to store the video data
        video_info = {
            'file_name': video_file_name,
            'file_size': os.path.getsize(video_file_path),
            'file_data': base64_encoded_video
        }

        # Return the video information as JSON
        return jsonify(video_info)
    else:
        return jsonify({'error': 'Video file not found'})


if __name__ == '__main__':
    app.run(debug=False)

