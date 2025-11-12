const apiUrl = "http://127.0.0.1:5036/usuario/mudancaSenha";

async function handleMudancaSenha() {
    const user = {
        email: document.getElementById("email").value,
        senha: document.getElementById("senha").value,
        confirma_senha: document.getElementById("confirma_senha").value
    }

    if (user.senha != user.confirma_senha) {
        alert("As senhas precisam ser iguais")
        return
    }

    try {
        const response = await fetch(apiUrl, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(user)
        });

        const data = await response.json();
        console.log(data)

        if (data.success === true) {
            console.log('teste')
            alert("Senha alterada com sucesso")

            window.location.href = "http://localhost:3000/login"
            return;

        } else {
            alert(data.message || "ERRO AO REALIZAR TROCA DE SENHA");

        }








    } catch (error) {
        console.error("Erro ao realizar troca de senha:", error);

    }


}