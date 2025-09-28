const apiUrl = "http://127.0.0.1:5036/cadastroClientes";

async function cadastroCliente() {
    const cliente = {
        name: document.getElementById("name").value,
        idade: document.getElementById("idade").value,
        email: document.getElementById("email").value,
        senha: document.getElementById("senha").value,
        cidade: document.getElementById("cidade").value,
        uf: document.getElementById("uf").value,
        pais: document.getElementById("pais").value,
        cpf: document.getElementById("cpf").value,
        cep: document.getElementById("cep").value,
        telefone: document.getElementById("telefone").value,
        genero: document.getElementById("genero").value
    };

    console.log("Tentando cadastrar cliente:", cliente);

    try {
        const response = await fetch(apiUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(cliente)
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error("Erro na API:", response.status, errorText);
            return;
        }

        console.log("Cliente cadastrado com sucesso!");
        document.querySelector("form").reset();
        carregarClientes();
    } catch (error) {
        console.error("Erro ao cadastrar cliente:", error);
    }
}


async function carregarClientes() {
    try {
        const resposta = await fetch(apiUrl);
        const clientes = await resposta.json();

        const tabela = document.getElementById("tabela-clientes");
        tabela.innerHTML = "";

        clientes.forEach(usuario => {
            const row = `
                <tr>
                    <td>${usuario.id ?? ""}</td>
                    <td>${usuario.nome}</td>
                    <td>${usuario.email}</td>
                    <td>${usuario.cidade}</td>
                    <td>${usuario.UF}</td>
                    <td>${usuario.pais}</td>
                    <td>${usuario.Telefone}</td>
                </tr>
            `;
            tabela.innerHTML += row;
        });
    } catch (error) {
        console.error("Erro ao carregar clientes:", error);
    }
}


async function deletarCliente(id) {
    if (!confirm("Tem certeza que deseja excluir este cliente?")) {
        return;
    }

    try {
        console.log("ID do cliente a ser deletado:", id, "Tipo:", typeof id);
        console.log("URL da requisição DELETE:", `${apiUrl}/${id}`);
        const response = await fetch(`${apiUrl}/${id}`, {
            method: "DELETE"
        });

        if (!response.ok) {
            const erro = await response.json();
            alert("Erro: " + erro.erro);
            return;
        }

        carregarClientes();
    } catch (error) {
        console.error("Erro ao excluir cliente:", error);
    }
}

window.onload = carregarClientes;
