const apiUrl = "http://127.0.0.1:5036/motoristas";

function preencherEndereco(){
    const cep = document.getElementById("cep").value.replace(/\D/g, '');

    if (cep.length !== 8){
        return;
    }


    const url = `https://viacep.com.br/ws/${cep}/json/`;

    fetch(url)
        .then(response => response.json())
        .then(dados => {
            if (!dados.erro){
                document.getElementById("logradouro").value = dados.logradouro;
                document.getElementById("bairro").value = dados.bairro;
                document.getElementById("cidade").value = dados.localidade;
                document.getElementById("estado").value = dados.uf;
                document.getElementById("numero").focus();
            } else {
                alert("CEP não encontrado");
                document.getElementById("logradouro").value = "";
                document.getElementById("bairro").value = "";
                document.getElementById("cidade").value = "";
                document.getElementById("estado").value = "";
            }
        })
        .catch(error => {
            console.error("Erro ao consultar ViaCEP", error)
            alert("Erro ao consultar o CEP.")
        })
}


async function handleCadastroOuEdicaoMotorista() {
    const btnSalvar = document.getElementById("btn-salvar-motorista");
    const idMotorista = btnSalvar.getAttribute('data-id');

    const motorista = {
        nome: document.getElementById("nome").value,
        cpf: document.getElementById("cpf").value,
        rg: document.getElementById("rg").value,
        salario: parseFloat(document.getElementById("salario").value) || 0,
        data_nascimento: document.getElementById("data_nascimento").value,
        numero_cnh: document.getElementById("numero_cnh").value,
        categoria_cnh: document.getElementById("categoria_cnh").value,
        validade_cnh: document.getElementById("validade_cnh").value,
        telefone: document.getElementById("telefone").value,
        email: document.getElementById("email").value,

        cep: document.getElementById("cep").value,
        logradouro: document.getElementById("logradouro").value,
        numero: document.getElementById("numero").value,
        complemento: document.getElementById("complemento").value,
        bairro: document.getElementById("bairro").value,
        cidade: document.getElementById("cidade").value,
        estado: document.getElementById("estado").value
    };

    let url = apiUrl;
    let method = 'POST';

    if (idMotorista) {
        url = `${apiUrl}/${idMotorista}`;
        method = 'PUT';
    }


    try {
        const response = await fetch(url, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(motorista)
        });

        if (!response.ok) {
            const errorData = await response.json();
            alert(`Erro ao cadastrar: ${errorData.erro || response.statusText}`);
            console.error("Erro na API:", response.status, errorData);
            return;
        }

        document.querySelector("form").reset();
        btnSalvar.textContent = "Cadastrar motorista";
        btnSalvar.setAttribute('data-id', '');
        carregarMotoristas();
    } catch (error) {
        console.error("Erro ao cadastrar motorista:", error);
        alert("Erro de conexão. Verifique o console.");
    }
}


async function carregarFormularioParaEdicaoMotorista(id) {
    try {
        const response = await fetch(`${apiUrl}/${id}`);
        if (!response.ok) {
            throw new Error('Motorista não encontrado');
        }
        const motorista = await response.json();

        document.getElementById("nome").value = motorista.nome ?? '';
        document.getElementById("cpf").value = motorista.cpf ?? '';
        document.getElementById("rg").value = motorista.rg ?? '';
        document.getElementById("salario").value = motorista.salario ?? '';
        document.getElementById("data_nascimento").value = motorista.data_nascimento ?? '';
        document.getElementById("numero_cnh").value = motorista.numero_cnh ?? '';
        document.getElementById("categoria_cnh").value = motorista.categoria_cnh ?? '';
        document.getElementById("validade_cnh").value = motorista.validade_cnh ?? '';
        document.getElementById("telefone").value = motorista.telefone ?? '';
        document.getElementById("email").value = motorista.email ?? '';
        document.getElementById("cep").value = motorista.cep ?? '';
        document.getElementById("logradouro").value = motorista.logradouro ?? '';
        document.getElementById("numero").value = motorista.numero ?? '';
        document.getElementById("complemento").value = motorista.complemento ?? '';
        document.getElementById("bairro").value = motorista.bairro ?? '';
        document.getElementById("cidade").value = motorista.cidade ?? '';
        document.getElementById("estado").value = motorista.estado ?? '';

        const btnSalvar = document.getElementById("btn-salvar-motorista");
        btnSalvar.textContent = "Salvar Alterações";
        btnSalvar.setAttribute('data-id', motorista.id);

        window.scrollTo({ top: 0, behavior: 'smooth' });

    } catch (error) {
        console.error("Erro ao carregar motorista para edição:", error);
        alert("Não foi possível carregar os dados do motorista.");
    }
}


async function carregarMotoristas() {
    try {
        const resposta = await fetch(apiUrl);
        const motoristas = await resposta.json();

        const tabela = document.getElementById("tabela-motoristas");
        tabela.innerHTML = "";

        motoristas.forEach(motorista => {
            const row = `
                <tr>
                    <td>${motorista.id ?? ""}</td>
                    <td>${motorista.nome ?? ""}</td>
                    <td>${motorista.cpf ?? ""}</td>
                    <td>${motorista.rg ?? ""}</td>
                    <td>${motorista.salario ?? ""}</td>
                    <td>${formatarData(motorista.data_nascimento)}</td>
                    <td>${motorista.numero_cnh ?? ""}</td>
                    <td>${formatarData(motorista.validade_cnh)}</td>
                    <td>${motorista.categoria_cnh ?? ""}</td>
                    <td>${motorista.email ?? ""}</td>
                    <td>${motorista.telefone ?? ""}</td>
                    <td>${motorista.cep ?? ""}</td>
                    <td>${motorista.logradouro ?? ""}</td>
                    <td>${motorista.numero ?? ""}</td>
                    <td>${motorista.complemento ?? ""}</td>
                    <td>${motorista.bairro ?? ""}</td>
                    <td>${motorista.cidade ?? ""}</td>
                    <td>${motorista.estado ?? ""}</td>
                    <td>
                        <button class="btn-editar" onclick="carregarFormularioParaEdicaoMotorista(${motorista.id})">Editar</button>
                        <button class="btn-excluir" onclick="deletarMotorista(${motorista.id})">Excluir</button>                    </td>
                </tr>
            `;
            tabela.innerHTML += row;
        });
    } catch (error) {
        console.error("Erro ao carregar motorista:", error);
    }
}

async function deletarMotorista(id) {
    if (!confirm("Tem certeza que deseja excluir esse motorista?")) {
        return;
    }

    try {
        await fetch(`${apiUrl}/${id}`, { method: "DELETE" });
        carregarMotoristas();
    } catch (error) {
        console.error("Erro ao excluir motorista:", error);
    }
}

function formatarData(dataString) {
    const data = new Date(dataString);
    const dia = String(data.getUTCDate()).padStart(2, '0');
    const mes = String(data.getUTCMonth() + 1).padStart(2, '0');
    const ano = data.getUTCFullYear();
    return `${dia}/${mes}/${ano}`;
}

window.onload = carregarMotoristas;
