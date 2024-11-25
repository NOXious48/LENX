import cv2

def scan_qr_code(image_path=None, camera_index=0):
    # Initialize the QRCode detector
    qr_code_detector = cv2.QRCodeDetector()
    last_data = None  # To store the last detected QR code data

    if image_path:
        img = cv2.imread(image_path)

        # Resize the image to make detection faster
        img = cv2.resize(img, (640, 480))

        # Detect and decode the QR code
        data, bbox, _ = qr_code_detector.detectAndDecode(img)

        if data and data != last_data:
            print("QR Code detected, data:", data)
            last_data = data  # Update last detected data

            # Draw bounding box around the QR code
            if bbox is not None:
                bbox = bbox.astype(int)
                for i in range(len(bbox)):
                    pt1 = tuple(bbox[i][0])
                    pt2 = tuple(bbox[(i + 1) % len(bbox)][0])
                    cv2.line(img, pt1, pt2, color=(0, 255, 0), thickness=2)

            # Show the image with the detected QR code
            cv2.imshow("QR Code Scanner", img)
            #cv2.waitKey(0)  # Wait for any key press
            cv2.destroyAllWindows()
            return data
        else:
            print("No QR Code found")
            return None

    else:
        # Open webcam with the specified camera index
        cap = cv2.VideoCapture(camera_index)

        if not cap.isOpened():
            print(f"Error: Cannot open camera with index {camera_index}")
            return

        while True:
            ret, img = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            # Resize the frame for faster detection
            img = cv2.resize(img, (640, 480))

            # Detect and decode the QR code
            data, bbox, _ = qr_code_detector.detectAndDecode(img)

            if data and data != last_data:
                print("QR Code detected, data:", data)
                last_data = data  # Update last detected data

                # Draw bounding box around the QR code
                if bbox is not None:
                    bbox = bbox.astype(int)
                    for i in range(len(bbox)):
                        pt1 = tuple(bbox[i][0])
                        pt2 = tuple(bbox[(i + 1) % len(bbox)][0])
                        cv2.line(img, pt1, pt2, color=(0, 255, 0), thickness=2)

            # Display the video frame
            cv2.imshow("QR Code Scanner", img)

            # Press any key to quit the loop
            if cv2.waitKey(1) != -1:
                break

        cap.release()
        cv2.destroyAllWindows()

# Example usage:
# For scanning from an image
# scan_qr_code('path_to_your_image.png')

# For scanning from the first camera (default)
#scan_qr_code(camera_index=0)

# For scanning from the second camera (external)
# scan_qr_code(camera_index=1)

