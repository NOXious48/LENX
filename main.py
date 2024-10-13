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
