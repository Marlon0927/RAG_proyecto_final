async function uploadPDF() {

    const fileInput =
        document.getElementById(
            "pdfFile"
        );

    const file =
        fileInput.files[0];

    if (!file) {

        alert(
            "Selecciona un PDF"
        );

        return;
    }

    const formData =
        new FormData();

    formData.append(
        "file",
        file
    );

    const response =
        await fetch(
            "/upload-pdf",
            {
                method: "POST",
                body: formData
            }
        );

    const data =
        await response.json();

    document.getElementById(
        "uploadStatus"
    ).innerText =
        data.message;
}



async function askQuestion() {

    const question =
        document.getElementById(
            "question"
        ).value;

    const response =
        await fetch(
            "/ask",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );

    const data =
        await response.json();

    document.getElementById(
        "response"
    ).innerHTML = `
        <h3>Respuesta:</h3>
        <p>${data.respuesta}</p>
    `;

    let fuentesHTML =
        "<h3>Fuentes:</h3>";

    data.fuentes.forEach(f => {

        fuentesHTML += `
            <div class="source">
                ${f}
            </div>
        `;
    });

    document.getElementById(
        "sources"
    ).innerHTML =
        fuentesHTML;
}