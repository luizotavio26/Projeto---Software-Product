const apiUrl = "http://127.0.0.1:5036/usuario";

async function handleConta() {
   /* const btnSalvar = document.getElementById("btn-salvar");
    const id_cliente = btnSalvar.getAttribute('data-id'); */

    const dadosUser = {
        nome_usuario: document.getElementById("nome_usuario").value, 
        email: document.getElementById("email").value, 
        senha: document.getElementById("senha").value, 
    
    };

    try {
        const response = await fetch(url, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dadosCliente)
        });
        const data = response.json()

        if (response.ok) {
            alert("Login deu certo");
            window.location("/")
        } else {
            console.log(data.message)
            alert("Erro ao realizar cadastro")
        }

    
    } catch (error) {
        console.error(`Erro ao ${acao} cliente:`, error);
        alert("Erro de conexão ou sistema.");
    }
}
