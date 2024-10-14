"""
from flask import Flask, render_template, request
import os
import cv2  # Importing OpenCV
import pandas as pd  # Importing pandas to handle CSV files
from qr_scanner import scan_qr_code
from web_search import image_to_text, perform_web_search

app = Flask(__name__)

def contains_qr_code(image_path):
    # Load the image and check for QR code
    detector = cv2.QRCodeDetector()
    image = cv2.imread(image_path)
    data, bbox, _ = detector.detectAndDecode(image)
    return bbox is not None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    prompt = request.form.get('prompt')
    image = request.files.get('image')

    if image:
        # Save the image temporarily
        image_path = os.path.join('static', image.filename)
        image.save(image_path)

        if contains_qr_code(image_path):
            # QR code found, scan it
            result = scan_qr_code(image_path)
            search_query=result
            search_results = perform_web_search(search_query)
            # Return result without message, if desired
            # return render_template('result.html', csv_data=None)  # Show no CSV results
        else:
            # No QR code found, extract text and perform search
            extracted_text = image_to_text(image_path)
            search_query = f"{extracted_text} {prompt}".strip()
            search_results = perform_web_search(search_query)
            search_results.to_csv('results.csv', index=False)

            # Read the CSV file and prepare data for rendering
            csv_data = pd.read_csv('results.csv').values.tolist()
            return render_template('result.html', csv_data=csv_data)  # Show search results

    return render_template('result.html', csv_data=None)  # No image provided case

if __name__ == '__main__':
    app.run(debug=True)
"""
"""from flask import Flask, render_template, request, jsonify
import os
import cv2  # Importing OpenCV
import pandas as pd  # Importing pandas to handle CSV files
from qr_scanner import scan_qr_code
from web_search import image_to_text, perform_web_search

app = Flask(__name__)

def contains_qr_code(image_path):
    # Load the image and check for QR code
    detector = cv2.QRCodeDetector()
    image = cv2.imread(image_path)
    data, bbox, _ = detector.detectAndDecode(image)
    return True if bbox is not None else False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    image = request.files.get('image')
    

    if image:
        # Save the image temporarily
        image_path = os.path.join('static', image.filename)
        image.save(image_path)

        # Check for QR code
        qr_code_data = contains_qr_code(image_path)

        if qr_code_data==True:
            # QR code found, return the URL to the frontend
            qr_data=scan_qr_code(image_path)
            search_results = perform_web_search(qr_data,max=1)
            search_results.to_csv('results.csv', index=False)

            # Read the CSV file and prepare data for rendering
            csv_data = pd.read_csv('results.csv').values.tolist()
            return render_template('result.html', csv_data=csv_data)  # Show search results
            #return jsonify({'qr_code_data': qr_data})  # Send QR data back to frontend
        else:
            # No QR code found, extract text and perform search
            prompt = request.form.get('prompt')
            extracted_text = image_to_text(image_path)
            search_query = f"{extracted_text} {prompt}".strip()
            search_results = perform_web_search(search_query,max=20)
            search_results.to_csv('results.csv', index=False)

            # Read the CSV file and prepare data for rendering
            csv_data = pd.read_csv('results.csv').values.tolist()
            return render_template('result.html', csv_data=csv_data)  # Show search results

    return render_template('result.html', csv_data=None)  # No image provided case

if __name__ == '__main__':
    app.run(debug=True)

"""
"""
from flask import Flask, render_template, request, jsonify
import os
import cv2  # Importing OpenCV
import pandas as pd  # Importing pandas to handle CSV files
from qr_scanner import scan_qr_code
from web_search import image_to_text, perform_web_search

app = Flask(__name__)

def contains_qr_code(image_path):
    # Load the image and check for QR code
    detector = cv2.QRCodeDetector()
    image = cv2.imread(image_path)
    data, bbox, _ = detector.detectAndDecode(image)
    return bbox is not None, data  # Return whether QR code exists and its data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    image = request.files.get('image')
    
    if image:
        # Save the image temporarily
        image_path = os.path.join('static', image.filename)
        image.save(image_path)

        # Check for QR code
        qr_code_found, qr_data = contains_qr_code(image_path)

        if qr_code_found:
            # QR code found, perform web search with QR data
            search_results = perform_web_search(qr_data, max=1)
            search_results.to_csv('results.csv', index=False)

            # Read the CSV file and prepare data for rendering
            csv_data = pd.read_csv('results.csv').values.tolist()
            return render_template('result.html', csv_data=csv_data)  # Show search results
        else:
            # No QR code found, extract text and perform search
            extracted_text = image_to_text(image_path)
            if extracted_text.strip():  # Only search if there's text extracted
                search_results = perform_web_search(extracted_text, max=20)
                search_results.to_csv('results.csv', index=False)

                # Read the CSV file and prepare data for rendering
                csv_data = pd.read_csv('results.csv').values.tolist()
                return render_template('result.html', csv_data=csv_data)  # Show search results
            else:
                return render_template('result.html', csv_data=None, error="No text extracted.")  # No text found

    return render_template('result.html', csv_data=None, error="No image provided.")  # No image provided case

if __name__ == '__main__':
    app.run(debug=True)
"""

from flask import Flask, render_template, request, jsonify
import os
import cv2
import pandas as pd
from qr_scanner import scan_qr_code
from web_search import image_to_text, perform_web_search

app = Flask(__name__)

def contains_qr_code(image_path):
    detector = cv2.QRCodeDetector()
    image = cv2.imread(image_path)
    data, bbox, _ = detector.detectAndDecode(image)
    return bbox is not None, data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    image = request.files.get('image')
    prompt = request.form.get('prompt', '')

    if image:
        # Save the image temporarily
        image_path = os.path.join('static', 'temp_image.jpg')
        image.save(image_path)

        # Check for QR code
        qr_code_found, qr_data = contains_qr_code(image_path)

        if qr_code_found:
            # QR code found, perform web search with QR data
            search_query = qr_data
            search_results = perform_web_search(search_query, max=1)
        else:
            # No QR code found, extract text and perform search
            extracted_text = image_to_text(image_path)
            if extracted_text.strip():
                search_query = f"{extracted_text} {prompt}".strip()
                search_results = perform_web_search(search_query, max=20)
            else:
                return render_template('result.html', csv_data=None, error="No text extracted from image.")

        # Save search results to CSV
        search_results.to_csv('results.csv', index=False)

        # Read the CSV file and prepare data for rendering
        csv_data = pd.read_csv('results.csv').values.tolist()
        return render_template('result.html', csv_data=csv_data)

    return render_template('result.html', csv_data=None, error="No image provided.")

if __name__ == '__main__':
    app.run(debug=True)