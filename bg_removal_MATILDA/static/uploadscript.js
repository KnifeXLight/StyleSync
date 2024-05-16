var upload = document.getElementById('upload');

function uploadFile(file) {
    var formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Uploaded:', data);
        // Handle the response as needed
        // Convert the response object to a string
        var responseString = JSON.stringify(data);
        // Display the response in the designated element
        document.getElementById('uploadmessage').innerText = responseString;
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle errors if any
    });
}
// event listener to help us change opacity or other options when mouse enters
upload.addEventListener('dragenter', function (e) {
    upload.parentNode.className = 'area dragging';
}, false);

// event listener to help us change opacity or other options when mouse leaves
upload.addEventListener('dragleave', function (e) {
    upload.parentNode.className = 'area';
}, false);

// event listener for file upload by dropping
upload.addEventListener('dragdrop', function (e) {
    e.preventDefault();
    upload.parentNode.className = 'area';
    var file = e.dataTransfer.files[0];
    uploadFile(file);
}, false);

// event listener for file upload by clicking
upload.addEventListener('change', function (e) {
    var file = e.target.files[0];
    uploadFile(file);
}, false);
