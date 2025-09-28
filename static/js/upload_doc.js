function enviarArquivo() {
    const input = document.getElementById("arquivoInput"); // ✅ pega o input
    if (input.files.length === 0) {
        alert("Selecione um arquivo!");
        return;
    }

    const file = input.files[0];
    const formData = new FormData();
    formData.append("arquivo", file);

    fetch("/upload", { method: "POST", body: formData })
    .then(res => {
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return res.json();
    })
    .then(data => console.log(data))
    .catch(err => console.error(err));

}
