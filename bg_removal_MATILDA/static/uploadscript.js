var upload = document.getElementById('upload');

function onFile() {
    var me = this,
        file = upload.files[0],
        name = file.name.replace(/\.[^/.]+$/, '');

    if (file.type === '' ||
        file.type === 'audio/mp3' ||       
        file.type === 'file/text' ||
        file.type === 'audio/mpeg' ||
        file.type === 'audio/wav' ||
        file.type === 'audio/x-wav' ||
        file.type === 'audio/wave' ||
        file.type === 'audio/x-pn-wav') {
        if (file.size < (3000 * 1024)) {
            upload.parentNode.className = 'area uploading';
        } else {
            window.alert('File size is too large, please ensure you are uploading a file of less than 3MB');
        }
    } else {
        window.alert('File type ' + file.type + ' not supported');
    }
}

upload.addEventListener('dragenter', function (e) {
    upload.parentNode.className = 'area dragging';
}, false);

upload.addEventListener('dragleave', function (e) {
    upload.parentNode.className = 'area';
}, false);

upload.addEventListener('dragdrop', function (e) {
    onFile();
}, false);

upload.addEventListener('change', function (e) {
    onFile();
}, false);
