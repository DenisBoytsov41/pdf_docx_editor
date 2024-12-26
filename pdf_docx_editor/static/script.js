document.getElementById('upload-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const fileInput = document.getElementById('file');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('output').textContent = data.error;
        } else {
            document.getElementById('output').innerHTML = `
                <p>Файл загружен: ${data.filename}</p>
                <button onclick="annotateFile('${data.filename}', 'pdf')">Аннотировать PDF</button>
                <button onclick="annotateFile('${data.filename}', 'docx')">Аннотировать DOCX</button>
            `;
        }
    });
});

function annotateFile(filename, type) {
    const endpoint = type === 'pdf' ? '/process_pdf' : '/process_docx';
    fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filename })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            document.getElementById('output').innerHTML += `
                <p>Файл аннотирован. <a href="/download/${data.annotated_path}" target="_blank">Скачать</a></p>`;
        }
    });
}
