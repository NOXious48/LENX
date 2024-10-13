"""
from qr_scanner import scan_qr_code
from web_search import image_to_text, perform_web_search
import os
import cv2

def contains_qr_code(image_path):
    # Load the image
    image = cv2.imread(image_path)
    # Initialize the QR Code detector
    detector = cv2.QRCodeDetector()
    
    # Use detectAndDecode method to detect and decode the QR code
    data, bbox, _ = detector.detectAndDecode(image)
    
    # If a QR code is detected, return True
    return bbox is not None

def main():
    # Get user input for image or camera
    user_choice = int(input("Select 0: camera feed, 1: image: "))

    if user_choice == 1:
        # User selected an image
        image_path = input("Enter the path to the image: ")
        
        if not os.path.exists(image_path):
            print("Error: Image path does not exist. Please try again.")
            return
        
        if contains_qr_code(image_path):
            # QR code found, scan it
            result = scan_qr_code(image_path)
            print("QR Code scanned:", result)
        else:
            # No QR code found, prompt for text and search
            text_prompt = input("Enter a prompt: ")
            extracted_text = image_to_text(image_path)
            search_query = f"{extracted_text} {text_prompt}".strip()
            search_results = perform_web_search(search_query)
            search_results.to_csv('results.csv', index=False)
            print("Search results saved to results.csv")

    else:
        # User selected camera feed
        result = scan_qr_code(camera_index=0)
        print("QR Code scanned from camera feed:", result)

if __name__ == "__main__":
    main()
"""
"""
from flask import Flask, render_template, request
import os
from qr_scanner import scan_qr_code
from web_search import image_to_text, perform_web_search
import cv2

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
            return f"QR Code scanned: {result}"
        else:
            # No QR code found, extract text and perform search
            extracted_text = image_to_text(image_path)
            search_query = f"{extracted_text} {prompt}".strip()
            search_results = perform_web_search(search_query)
            search_results.to_csv('results.csv', index=False)
            return "Search results saved to results.csv"

    return "No image provided!"

if __name__ == '__main__':
    app.run(debug=True)

"""

from flask import Flask, render_template, request
import os
import cv2  # Importing OpenCV
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
    
    image = request.files.get('image')

    if image:
        # Save the image temporarily
        image_path = os.path.join('static', image.filename)
        image.save(image_path)

        if contains_qr_code(image_path):
            # QR code found, scan it
            result = scan_qr_code(image_path)
            message = f"QR Code scanned: {result}"
        else:
            # No QR code found, extract text and perform search
            prompt = request.form.get('prompt')
            extracted_text = image_to_text(image_path)
            search_query = f"{extracted_text} {prompt}".strip()
            search_results = perform_web_search(search_query)
            search_results.to_csv('results.csv', index=False)
            message = "Search results saved to results.csv"

        return render_template('result.html', message=message)

    return render_template('result.html', message="No image provided!")

if __name__ == '__main__':
    app.run(debug=True)
