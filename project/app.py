from flask import Flask, render_template, request, jsonify
import os
import cv2  # Importing OpenCV
import pandas as pd  # Importing pandas to handle CSV files
from qr_scanner import scan_qr_code
from web_search import image_to_text, perform_web_search,call_llm

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
    prompt = request.form.get('prompt')
    
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

                result = call_llm(prompt + extracted_text+"Provide url too if you can")
                print(result)

                # Write the LLM result to a text file
                with open("Output.txt", "w", encoding="utf-8") as text_file:
                    text_file.write(result)

                # Read the contents of the Output.txt file
                with open("Output.txt", "r", encoding="utf-8") as file:
                   llm_result_content = file.read()
                    
                #search_results = perform_web_search(extracted_text, max=20)
                #search_results.to_csv('results.csv', index=False)

                # Read the CSV file and prepare data for rendering
                #csv_data = pd.read_csv('results.csv').values.tolist()
                return render_template('result.html', llm_result_content=result)

            else:
                return render_template('result.html', csv_data=None, error="No text extracted.")  # No text found

    return render_template('result.html', csv_data=None, error="No image provided.")  # No image provided case

if __name__ == '__main__':
    app.run(debug=True)
