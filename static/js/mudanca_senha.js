// Duas APi, pois temos 2 rotas e bancos diferentes
const apiUrl = "http://127.0.0.1:5036/usuario/mudancaSenha";

async function handleMudancaSenha() {
    // vamos usar a variavel senha para atualizar a senha e a 
    // confirma_senha para o usuario ter certeza que digitou a senha correta
    const senha =  document.getElementById("senha").value;
    const confirma_senha = document.getElementById("confirma_senha").value;
    
    // se as senhas forem diferentes, vamos exibir o erro e encerrar a função
    if (senha != confirma_senha){
        alert("As senhas precisam ser iguais")
        console.log("Erro: as senhas diferem")
        return // vamos encerrar a função aqui se as senhas não forem iguais

    } 

    //NOTA: seria interessante ter mais um get para ver se o usuario realmente está no BD???? Essa página será acessada por email
    // se ocorrer tudo bem com as senhas vamos fazer o put
    /*
    const user = {
        email: document.getElementById("email").value,
        senha: document.getElementById("senha").value
    };
    */
    
    // tentando fazer a requisição
    try {
        console.log("teste")
        const response = await fetch(apiUrl, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(senha)
        });
        const data = await response.json();

        console.log(data)

        if (data.success === true) {
            console.log("Senha alterada")
            alert("Senha alterada com sucesso")

            window.location.href = "http://127.0.0.1:5036/"
            
            return;
        }

        

        // Se o login não foi bem-sucedido, exibe a mensagem de erro apropriada
        alert(data.message || "ERRO AO REALIZAR LOGIN");



    } catch (error) {
        console.error("Erro ao realizer login:", error);

    }


}