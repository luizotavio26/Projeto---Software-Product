const apiUrl = "http://127.0.0.1:5036/veiculos";
const usuariosApiUrl = "http://127.0.0.1:5036/clientes";

async function cadastroVeiculo() {
    const veiculo = {
        placa: document.getElementById("placa").value,
        modelo: document.getElementById("modelo_veiculo").value,
        marca: document.getElementById("marca_veiculo").value,
        renavan: document.getElementById("renavan").value,
        chassi: document.getElementById("chassi").value,
        cor: document.getElementById("cor").value,
        tipo: document.getElementById("tipo").value,
        ano_modelo: parseInt(document.getElementById("ano_modelo").value) || 0,
        ano_fabricacao: parseInt(document.getElementById("ano_fabricacao").value) || 0
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
            alert("Erro ao cadastrar veículo.");
            return;
        }

        console.log("Veículo cadastrado com sucesso!");
        document.querySelector("form").reset();
        carregarVeiculos();

    } catch (error) {
        console.error("Erro ao cadastrar veículo:", error);
    }
}


async function carregarVeiculos() {
    try {
        const resposta = await fetch(apiUrl);

        if (!resposta.ok) {
            console.error("Erro ao buscar veículos:", resposta.status);
            return;
        }

        const veiculos = await resposta.json();

        const tabela = document.getElementById("tabela-veiculos");
        tabela.innerHTML = "";

        veiculos.forEach(veiculo => {
            const row = `
                <tr>
                    <td>${veiculo.id ?? ""}</td>
                    <td>${veiculo.placa}</td>
                    <td>${veiculo.modelo}</td>
                    <td>${veiculo.marca}</td>
                    <td>${veiculo.renavan}</td>
                    <td>${veiculo.chassi}</td>
                    <td>${veiculo.cor}</td>
                    <td>${veiculo.tipo}</td>
                    <td>${veiculo.ano_modelo}</td>
                    <td>${veiculo.ano_fabricacao}</td>
                    <td>
                        <button class="btn-excluir" onclick="deletarVeiculo(${veiculo.id})">Excluir</button>
                    </td>
                </tr>
            `;
            tabela.innerHTML += row;
        });
    } catch (error) {
        console.error("Erro ao carregar veículos:", error);
    }
}


async function deletarVeiculo(id) {
    if (!confirm("Tem certeza que deseja excluir este veículo?")) {
        return;
    }
        
    try{
        const response = await fetch(`${apiUrl}/${id}`, { method: "DELETE" });

            if (!response.ok) {
                const err = await response.json();
                alert(`Erro: ${err.erro || "Falha ao excluir veículo"}`);
                return;
            }

            alert("Veículo excluído com sucesso!");
            carregarVeiculos();
        
        } catch (error) {
        console.error("Erro ao excluir veículo:", error);
    }
}

window.onload = carregarVeiculos;
