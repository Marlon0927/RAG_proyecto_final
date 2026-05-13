async function askQuestion() {

    const question =
        document.getElementById(
            "question"
        ).value;

    const response = await fetch(
        "http://127.0.0.1:8000/ask",
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

    const data = await response.json();

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
    ).innerHTML = fuentesHTML;
}