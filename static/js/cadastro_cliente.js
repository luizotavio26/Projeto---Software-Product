const apiUrl = "http://127.0.0.1:5036/clientes";


function preencherEndereco() {
    const cep = document.getElementById("cep").value.replace(/\D/g, ''); // Limpa caracteres não numéricos

    if (cep.length !== 8) {
        // Ignora se o CEP não tiver 8 dígitos
        return;
    }

    const url = `https://viacep.com.br/ws/${cep}/json/`;

    fetch(url)
        .then(response => response.json())
        .then(dados => {
            if (!dados.erro) {
                // Preenche os campos do formulário com os dados retornados
                document.getElementById("logradouro").value = dados.logradouro;
                document.getElementById("bairro").value = dados.bairro;
                document.getElementById("cidade").value = dados.localidade;
                document.getElementById("estado").value = dados.uf;
                
                // Foca no campo 'número' para que o usuário continue o preenchimento
                document.getElementById("numero").focus(); 
            } else {
                alert("CEP não encontrado.");
                document.getElementById("logradouro").value = "";
            }
        })
        .catch(error => {
            console.error("Erro ao consultar ViaCEP:", error);
            alert("Erro ao tentar consultar o CEP.");
        });
}


// --- FUNÇÃO CENTRAL: LIDA COM CADASTRO (POST) E EDIÇÃO (PUT) ---
async function handleCadastroOuEdicao() {
    const btnSalvar = document.getElementById("btn-salvar");
    const id_cliente = btnSalvar.getAttribute('data-id');

    // 1. Coleta os dados do formulário (restante do código aqui...)
    const dadosCliente = {
        // ... (Dados de PJ, Endereço e Comuns) ...
        cnpj: document.getElementById("cnpj").value, 
        razao_social: document.getElementById("razao_social").value, 
        logradouro: document.getElementById("logradouro").value, 
        numero: document.getElementById("numero").value, 
        complemento: document.getElementById("complemento").value, 
        bairro: document.getElementById("bairro").value, 
        
        email: document.getElementById("email").value,
        senha: document.getElementById("senha").value,
        telefone: document.getElementById("telefone").value,
        cep: document.getElementById("cep").value,
        cidade: document.getElementById("cidade").value,
        estado: document.getElementById("estado").value 
    };

    // 2. Define o MÉTODO e a URL (restante do código aqui...)
    const method = id_cliente ? "PUT" : "POST"; 
    const url = id_cliente ? `${apiUrl}/${id_cliente}` : apiUrl;
    const acao = id_cliente ? "atualizar" : "cadastrar";

    try {
        const response = await fetch(url, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dadosCliente)
        });

        if (!response.ok) {
            const errorData = await response.json(); 
            const errorMessage = errorData.erro || response.statusText;
            alert(`Erro ao ${acao} (${response.status}): ${errorMessage}`);
            return;
        }

        alert(`Cliente ${acao} com sucesso!`);
        
        btnSalvar.removeAttribute('data-id');
        btnSalvar.textContent = 'Cadastrar cliente';
        document.querySelector("form").reset();
        
        carregarClientes();
    } catch (error) {
        console.error(`Erro ao ${acao} cliente:`, error);
        alert("Erro de conexão ou sistema.");
    }
}


async function carregarFormularioParaEdicao(id_cliente) {
    try {
        const response = await fetch(`${apiUrl}/${id_cliente}`);
        if (!response.ok) {
            alert("Erro ao carregar dados para edição.");
            return;
        }
        const cliente = await response.json();

        document.getElementById("cnpj").value = cliente.cnpj;
        document.getElementById("razao_social").value = cliente.razao_social;
        document.getElementById("email").value = cliente.email;
        document.getElementById("senha").value = cliente.senha;
        document.getElementById("telefone").value = cliente.telefone;
        document.getElementById("cep").value = cliente.cep;
        document.getElementById("logradouro").value = cliente.logradouro;
        document.getElementById("numero").value = cliente.numero;
        document.getElementById("complemento").value = cliente.complemento;
        document.getElementById("bairro").value = cliente.bairro;
        document.getElementById("cidade").value = cliente.cidade;
        document.getElementById("estado").value = cliente.estado;
        
        const btnSalvar = document.getElementById("btn-salvar");
        btnSalvar.setAttribute('data-id', cliente.id);
        btnSalvar.textContent = 'Salvar Alterações';
        
        window.scrollTo(0, 0);
    } catch (error) {
        console.error("Erro ao carregar dados para edição:", error);
    }
}


async function carregarClientes() {
try {
        const resposta = await fetch(apiUrl);

        if (!resposta.ok) {
            throw new Error(`Erro ao carregar lista de clientes: ${resposta.status}`);
        }

        const clientes = await resposta.json();

        const tabela = document.getElementById("tabela-clientes");
        tabela.innerHTML = "";
        
        if (!Array.isArray(clientes)) {
             console.error("A API não retornou uma lista válida de clientes.");
             return;
        }

        clientes.forEach(usuario => {
            const row = `
                <tr>
                    <td>${usuario.id ?? ""}</td>
                    <td>${usuario.cnpj ?? ""}</td>
                    <td>${usuario.razao_social ?? ""}</td>
                    <td>${usuario.email ?? ""}</td>
                    <td>${usuario.cidade ?? ""}</td>
                    <td>${usuario.estado ?? ""}</td>
                    <td>${usuario.telefone ?? ""}</td>

                    <td>${usuario.cep ?? ""}</td>
                    <td>${usuario.logradouro ?? ""}</td>
                    <td>${usuario.numero ?? ""}</td>
                    <td>${usuario.bairro ?? ""}</td>
                    <td>${usuario.cidade ?? ""}</td>
                    <td>${usuario.estado ?? ""}</td>

                    <td>
                        <button class="btn-editar" onclick="carregarFormularioParaEdicao(${usuario.id})">Editar</button>
                        <button class="btn-excluir" onclick="deletarCliente(${usuario.id})">Deletar</button>
                    </td>
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
