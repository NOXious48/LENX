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
            message = f"QR Code scanned: {result}"
            csv_data = None  # No CSV data to show for QR code scans
        else:
            # No QR code found, extract text and perform search
            extracted_text = image_to_text(image_path)
            search_query = f"{extracted_text} {prompt}".strip()
            search_results = perform_web_search(search_query)
            search_results.to_csv('results.csv', index=False)
            message = "Search results saved to results.csv"

            # Read the CSV file and prepare data for rendering
            csv_data = pd.read_csv('results.csv').values.tolist()

        return render_template('result.html', message=message, csv_data=csv_data)

    return render_template('result.html', message="No image provided!", csv_data=None)

if __name__ == '__main__':
    app.run(debug=True)
