const apiUrl = "http://127.0.0.1:5036/motoristas";

async function cadastroMotorista() {
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
        endereco: document.getElementById("endereco").value,
        cidade: document.getElementById("cidade").value,
        cep: document.getElementById("cep").value,
        uf: document.getElementById("uf").value};

    console.log("Tentando cadastrar motorista:", motorista);

    try {
        const response = await fetch(apiUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(motorista)
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error("Erro na API:", response.status, errorText);
            return;
        }

        console.log("motorista cadastradO com sucesso!");
        document.querySelector("form").reset();
        carregarMotoristas();
    } catch (error) {
        console.error("Erro ao cadastrar motorista:", error);
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
                    <td>${motorista.nome}</td>
                    <td>${motorista.numero_cnh}</td>
                    <td>${formatarData(motorista.validade_cnh)}</td>
                    <td>${motorista.categoria_cnh}</td>
                    <td>${motorista.email}</td>
                    <td>${motorista.telefone}</td>
                    <td>
                        <button class="btn-excluir" onclick="deletarMotorista(${motorista.id})">Excluir</button>
                    </td>
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
