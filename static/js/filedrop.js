
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    //following used to identify target text box/textarea
    const output = document.getElementById('qrytxt');

    // Click zone to open file dialog
    dropzone.addEventListener('click', () => fileInput.click());

    // Prevent browser defaults
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(evt => {
      dropzone.addEventListener(evt, e => {
        e.preventDefault();
        e.stopPropagation();
      });
    });

    dropzone.addEventListener('dragover', () => dropzone.classList.add('dragover'));
    dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));

    dropzone.addEventListener('drop', e => {
      dropzone.classList.remove('dragover');
      const file = e.dataTransfer.files[0];
      if (file) readFile(file);
    });

    fileInput.addEventListener('change', e => {
      const file = e.target.files[0];
      if (file) readFile(file);
    });

    function readFile(file) {
      if (!file.type.startsWith('text') && !file.name.endsWith('.json')) {
        alert('Please select a text or JSON file.');
        return;
      }
      const reader = new FileReader();
      reader.onload = () => output.value = reader.result;
      reader.readAsText(file);
    }
