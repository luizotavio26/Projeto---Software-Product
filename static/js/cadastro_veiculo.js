const apiUrl = "http://127.0.0.1:5036/veiculos";


async function handleCadastroOuEdicaoVeiculo() {

    const btnSalvar = document.getElementById("btn-salvar");
    const id_veiculo = btnSalvar.getAttribute('data-id');

    const veiculo = {
        placa: document.getElementById("placa").value,
        modelo: document.getElementById("modelo_veiculo").value,
        marca: document.getElementById("marca_veiculo").value,
        renavan: document.getElementById("renavan").value,
        chassi: document.getElementById("chassi").value,
        cor: document.getElementById("cor").value,
        tipo: document.getElementById("tipo").value,
        peso_maximo_kg: parseInt(document.getElementById("peso_maximo_kg").value) || 0,
        ano_modelo: parseInt(document.getElementById("ano_modelo").value) || 0,
        ano_fabricacao: parseInt(document.getElementById("ano_fabricacao").value) || 0
    };

    let method = 'POST';
        let url = apiUrl;

        if (id_veiculo) {
            method = 'PUT';
            url = `${apiUrl}/${id_veiculo}`;
            console.log("Tentando ATUALIZAR veículo:", veiculo);
        } else {
            console.log("Tentando CADASTRAR veículo:", veiculo);
        }

    try {
        const response = await fetch(url, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(veiculo)
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error("Erro na API:", response.status, errorText);
            alert("Erro ao salvar veículo.");
            return;
        }

        console.log("Veículo salvo com sucesso!");
        limparFormularioVeiculo();
        carregarVeiculos();

    } catch (error) {
        console.error("Erro ao salvar veículo:", error);
    }

}

function limparFormularioVeiculo() {
    document.querySelector(".form-veiculo").reset();

    const btnSalvar = document.getElementById("btn-salvar");
    btnSalvar.textContent = 'Cadastrar veículo';
    btnSalvar.setAttribute('data-id', '');
}


async function carregarFormularioParaEdicaoVeiculo(id) {
    try {
        const response = await fetch(`${apiUrl}/${id}`);
        if (!response.ok) {
            alert("Erro ao carregar dados do veículo para edição.");
            return;
        }
        const veiculo = await response.json();

        document.getElementById("placa").value = veiculo.placa;
        document.getElementById("modelo_veiculo").value = veiculo.modelo;
        document.getElementById("marca_veiculo").value = veiculo.marca;
        document.getElementById("renavan").value = veiculo.renavan;
        document.getElementById("chassi").value = veiculo.chassi;
        document.getElementById("cor").value = veiculo.cor;
        document.getElementById("tipo").value = veiculo.tipo;
        document.getElementById("peso_maximo_kg").value = veiculo.peso_maximo_kg;
        document.getElementById("ano_modelo").value = veiculo.ano_modelo;
        document.getElementById("ano_fabricacao").value = veiculo.ano_fabricacao;

        const btnSalvar = document.getElementById("btn-salvar");
        btnSalvar.textContent = 'Salvar Alterações';
        btnSalvar.setAttribute('data-id', id);
        
        window.scrollTo(0, 0);

    } catch (error) {
        console.error("Erro ao carregar veículo para edição:", error);
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
                    <td>${veiculo.peso_maximo_kg} kg</td>
                    <td>${veiculo.ano_modelo}</td>
                    <td>${veiculo.ano_fabricacao}</td>
                    <td>
                        <button class="btn-editar" onclick="carregarFormularioParaEdicaoVeiculo(${veiculo.id})">Editar</button>
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
