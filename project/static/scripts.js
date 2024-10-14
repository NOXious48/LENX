// Global variables
let stream;

// Function to show the file name when a file is selected
function showFileName(input) {
    const label = document.getElementById('file-label');
    if (input.files.length > 0) {
        const fileName = input.files[0].name;
        label.textContent = fileName;
        label.classList.add('file-input-active');
    } else {
        label.textContent = 'Choose Image';
        label.classList.remove('file-input-active');
    }
}

// Function to open the camera
function openCamera() {
    const video = document.getElementById('video');
    const captureButton = document.getElementById('captureButton');
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(streamObj) {
                stream = streamObj;
                video.srcObject = stream;
                video.style.display = 'block';
                captureButton.style.display = 'inline-block';
                document.getElementById('cameraButton').style.display = 'none';
            })
            .catch(function(error) {
                console.error("Camera access error:", error);
            });
    }
}

// Function to capture a photo
function capturePhoto() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const photo = document.getElementById('photo');
    const retakeButton = document.getElementById('retakeButton');
    const captureButton = document.getElementById('captureButton');

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    
    const dataUrl = canvas.toDataURL('image/jpeg');
    photo.src = dataUrl;
    photo.style.display = 'block';

    video.style.display = 'none';
    captureButton.style.display = 'none';
    retakeButton.style.display = 'inline-block';

    // Stop all video streams
    stream.getTracks().forEach(track => track.stop());
}

// Function to retake a photo
function retakePhoto() {
    const video = document.getElementById('video');
    const photo = document.getElementById('photo');
    const captureButton = document.getElementById('captureButton');
    const retakeButton = document.getElementById('retakeButton');

    // Reset display
    video.style.display = 'block';
    photo.style.display = 'none';
    captureButton.style.display = 'inline-block';
    retakeButton.style.display = 'none';

    // Restart video stream
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(streamObj) {
            stream = streamObj;
            video.srcObject = stream;
        })
        .catch(function(error) {
            console.error("Camera access error:", error);
        });
}

// Function to submit the form data
function submitForm(formData) {
    fetch('/process', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())  // Changed from response.json() to response.text()
    .then(data => {
        console.log('Success:', data);
        // Replace the current page content with the response
        document.body.innerHTML = data;
    })
    .catch((error) => {
        console.error('Error:', error);
        // Handle any errors
    });
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('image').addEventListener('change', function() {
        showFileName(this);
    });

    document.getElementById('cameraButton').addEventListener('click', openCamera);
    document.getElementById('captureButton').addEventListener('click', capturePhoto);
    document.getElementById('retakeButton').addEventListener('click', retakePhoto);

    document.querySelector('form').addEventListener('submit', handleSubmit);

// Function to handle form submission
function handleSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);

    // Check if a photo was taken
    const photo = document.getElementById('photo');
    if (photo.style.display !== 'none') {
        // Convert the photo to a blob and append it to the form data
        fetch(photo.src)
            .then(res => res.blob())
            .then(blob => {
                formData.append('image', blob, 'captured_image.jpg');
                submitForm(formData);
            });
    } else {
        // Check if a file was selected
        const fileInput = document.getElementById('image');
        if (fileInput.files.length > 0) {
            submitForm(formData);
        } else {
            console.error('No image provided');
            // You might want to show an error message to the user here
        }
    }
}

});