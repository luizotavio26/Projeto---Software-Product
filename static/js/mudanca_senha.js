// Duas APi, pois temos 2 rotas e bancos diferentes
const apiUrl = "http://127.0.0.1:5036/usuario/mudancaSenha";

async function handleMudancaSenha() {
    // vamos usar a variavel senha para atualizar a senha e a 
    // confirma_senha para o usuario ter certeza que digitou a senha correta
    const user = {
        email: document.getElementById("email").value,
        senha: document.getElementById("senha").value,
        confirma_senha: document.getElementById("confirma_senha").value
    }


    if (user.senha != user.confirma_senha) {
        alert("As senhas precisam ser iguais")
        console.log("Erro: as senhas diferem")
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
            console.log("Senha alterada")
            alert("Senha alterada com sucesso")

            window.location.href = "http://127.0.0.1:5036/"

            return;
        } else {
            alert(data.message || "ERRO AO REALIZAR TROCA DE SENHA");

        }








    } catch (error) {
        console.error("Erro ao realizar troca de senha:", error);

    }


}