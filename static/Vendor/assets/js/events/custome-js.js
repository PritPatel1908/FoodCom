// Add dynamic product more img file
const addFileBtn = document.getElementById('add-file-btn');
const fileInputContainer = document.getElementById('file-input-container');
    
addFileBtn.addEventListener('click', () => {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.className = 'form-control mt-2';
    fileInput.name = 'files[]';
    fileInput.multiple = true;
    
    fileInputContainer.appendChild(fileInput);
});

// Select default text
// $('input').focus(function() {
//     $(this).select();
// });