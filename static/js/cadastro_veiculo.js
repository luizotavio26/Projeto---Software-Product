const apiUrl = "http://127.0.0.1:5036/veiculos";
const usuariosApiUrl = "http://127.0.0.1:5036/clientes";

async function cadastroVeiculo() {
    const veiculo = {
        placa: document.getElementById("placa").value,
        modelo: parseFloat(document.getElementById("modelo_veiculo").value) || 0,
        marca: document.getElementById("marca_veiculo").value,
        renavan: document.getElementById("renavan").value,
        chassi: document.getElementById("chassi").value,
        cor: document.getElementById("cor").value,
        tipo: parseFloat(document.getElementById("tipo").value) || 0,
        ano_veiculo_modelo: parseFloat(document.getElementById("ano_modelo").value) || 0,
        ano_veiculo_fabricacao: parseFloat(document.getElementById("ano_fabricacao").value) || 0
    };

    console.log("Tentando cadastrar veículo:", veiculo);

    try {
        const response = await fetch(apiUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(veiculo)
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error("Erro na API:", response.status, errorText);
            return;
        }

        console.log("Veículo cadastradp com sucesso!");
        document.querySelector("form").reset();
        carregarCargas();
    } catch (error) {
        console.error("Erro ao cadastrar veículo:", error);
    }
}


async function carregarVeiculos() {
    try {
        const resposta = await fetch(apiUrl);
        const veiculos = await resposta.json();

        const tabela = document.getElementById("tabela-veiculos");
        tabela.innerHTML = "";

        cargas.forEach(veiculos => {
            const row = `
                <tr>
                    <td>${veiculos.id ?? ""}</td>
                    <td>${veiculos.placa}</td>
                    <td>${veiculos.modelo_veiculo}</td>
                    <td>${veiculos.marca_veiculo}</td>
                    <td>${veiculos.renavan}</td>
                    <td>${veiculos.chassi}</td>
                    <td>${veiculos.cor}</td>
                    <td>${veiculos.tipo}</td>
                    <td>${veiculos.ano_veiculo_modelo}</td>
                    <td>${veiculos.ano_veiculo_fabricacao}</td>
                    <td>
                        <button class="btn-excluir" onclick="deletarveiculo(${carga.id})">Excluir</button>
                    </td>
                </tr>
            `;
            tabela.innerHTML += row;
        });
    } catch (error) {
        console.error("Erro ao carregar veículos:", error);
    }
}

// async function carregarClientes() {
//     try {
//         const response = await fetch(usuariosApiUrl);
//         const data = await response.json();
//         const clientes = data.ListaUsuarios;

//         const select = document.getElementById("informacoes_cliente");
//         select.innerHTML = '<option value="">Selecione um cliente</option>';
        
//         clientes.forEach(cliente => {
//             const option = document.createElement("option");
//             option.value = cliente.nome;
//             option.textContent = `${cliente.nome} (ID: ${cliente.id})`;
//             select.appendChild(option);
//         });
//     } catch (error) {
//         console.error("Erro ao carregar clientes:", error);
//     }
// }

async function deletarVeiculo(id) {
    if (!confirm("Tem certeza que deseja excluir este veículo?")) {
        return;
    }

    try {
        await fetch(`${apiUrl}/${id}`, { method: "DELETE" });
        carregarVeiculos();
    } catch (error) {
        console.error("Erro ao excluir veículo:", error);
    }
}

window.onload = function() {
    carregarVeiculos();
    // carregarClientes();
};