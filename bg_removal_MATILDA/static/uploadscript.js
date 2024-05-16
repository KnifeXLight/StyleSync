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
        alert(data.message);
        // Handle the response as needed
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle errors if any
    });
}

upload.addEventListener('dragenter', function (e) {
    upload.parentNode.className = 'area dragging';
}, false);

upload.addEventListener('dragleave', function (e) {
    upload.parentNode.className = 'area';
}, false);

upload.addEventListener('dragdrop', function (e) {
    e.preventDefault();
    upload.parentNode.className = 'area';
    var file = e.dataTransfer.files[0];
    uploadFile(file);
}, false);

upload.addEventListener('change', function (e) {
    var file = e.target.files[0];
    uploadFile(file);
}, false);
