const apiUrl = "http://127.0.0.1:5036/cargas";
const usuariosApiUrl = "http://127.0.0.1:5036/clientes";
const apiUrlMotoristas = "http://127.0.0.1:5036/motoristas";
const apiUrlVeiculos = "http://127.0.0.1:5036/veiculos";


function setSelectValue(selectId, id, label) {
    const select = document.getElementById(selectId);
    if (!id) return;

    select.value = String(id);

    if (select.value !== String(id) && label) {
        const option = document.createElement("option");
        option.value = String(id);
        option.textContent = `${label} (ID: ${id})`;
        select.appendChild(option);
        select.value = String(id);
    }
}


async function handleCadastroOuEdicaoCarga() {
    const btnSalvar = document.getElementById("btn-salvar-carga");
    const idCarga = btnSalvar.getAttribute('data-id');

    const selectCliente = document.getElementById("informacoes_cliente");
    const selectMotorista = document.getElementById("informacoes_motorista");
    const selectVeiculo = document.getElementById("informacoes_veiculo");

    const carga = {
        tipo_carga: document.getElementById("tipo_carga").value,
        peso_carga: parseFloat(document.getElementById("peso_carga").value) || 0,
        cliente_id: parseInt(selectCliente.value),
        motorista_id: parseInt(selectMotorista.value),
        veiculo_id: parseInt(selectVeiculo.value),
        origem_carga: document.getElementById("origem_carga").value,
        destino_carga: document.getElementById("destino_carga").value
    };

    if (!carga.cliente_id || !carga.motorista_id || !carga.veiculo_id || !carga.tipo_carga || !carga.origem_carga || !carga.destino_carga) {
        alert("Por favor, preencha todos os campos obrigatórios.");
        return;
    }

    let url = apiUrl;
    let method = 'POST';

    if (idCarga) {
        url = `${apiUrl}/${idCarga}`;
        method = 'PUT';
    }

    try {
        const response = await fetch(url, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(carga)
        });

        if (!response.ok) {
            const errorData = await response.json();
            alert(`Erro ao salvar: ${errorData.erro || response.statusText}`);
            return;
        }

        document.querySelector("form").reset();
        btnSalvar.textContent = "Cadastrar carga";
        btnSalvar.setAttribute('data-id', '');
        
        carregarCargas();

    } catch (error) {
        console.error("Erro ao salvar carga:", error);
        alert("Erro de conexão. Verifique o console.");
    }
}

async function carregarFormularioParaEdicaoCarga(id) {
    try {
        const response = await fetch(`${apiUrl}/${id}`);
        if (!response.ok) {
            throw new Error('Carga não encontrada');
        }
        const carga = await response.json();
        console.log("Carga recebida:", carga); 

        document.getElementById("tipo_carga").value = carga.tipo_carga;
        document.getElementById("peso_carga").value = carga.peso_carga;
        document.getElementById("origem_carga").value = carga.origem_carga;
        document.getElementById("destino_carga").value = carga.destino_carga;
        
        document.getElementById("informacoes_cliente").value = String(carga.cliente_id);
        document.getElementById("informacoes_motorista").value = String(carga.motorista_id);
        document.getElementById("informacoes_veiculo").value = String(carga.veiculo_id);

        const btnSalvar = document.getElementById("btn-salvar-carga");
        btnSalvar.textContent = "Salvar Alterações";
        btnSalvar.setAttribute('data-id', carga.id);

        window.scrollTo({ top: 0, behavior: 'smooth' });

    } catch (error) {
        console.error("Erro ao carregar carga para edição:", error);
        alert("Não foi possível carregar os dados da carga.");
    }
}


async function carregarCargas() {
    try {
        const resposta = await fetch(apiUrl);
        const cargas = await resposta.json();

        const tabela = document.getElementById("tabela-cargas");
        tabela.innerHTML = "";

        cargas.forEach(carga => {
            const row = `
                <tr>
                    <td>${carga.id}</td>
                    <td>${carga.tipo_carga}</td>
                    <td>${carga.peso_carga}</td>
                    <td>${carga.cliente ?? 'N/A'}</td> 
                    <td>${carga.motorista ?? 'N/A'}</td>
                    <td>${carga.veiculo ?? 'N/A'}</td>
                    <td>${carga.origem_carga}</td>
                    <td>${carga.destino_carga}</td>
                    <td>${carga.valor_km ?? '...'}</td>
                    <td>${carga.distancia ?? '...'}</td>
                    <td>${carga.valor_frete ?? '...'}</td>
                    <td>
                        <button class="btn-editar" onclick="carregarFormularioParaEdicaoCarga(${carga.id})">Editar</button>
                        <button class="btn-excluir" onclick="deletarCarga(${carga.id})">Excluir</button>
                    </td>
                </tr>
            `;
            tabela.innerHTML += row;
        });
    } catch (error) {
        console.error("Erro ao carregar cargas:", error);
    }
}


async function carregarClientes() {
try {
        const resposta = await fetch(usuariosApiUrl);
        const usuarios = await resposta.json();
        
        const usuarios_lista = usuarios; 

        const select = document.getElementById("informacoes_cliente");
        select.innerHTML = '<option value="">Selecione um cliente</option>';

        if (Array.isArray(usuarios_lista)) {
            usuarios_lista.forEach(cliente => {
                const option = document.createElement("option");
                option.value = String(cliente.id);
                option.textContent = `${cliente.razao_social} (ID: ${cliente.id})`;
                select.append(option);
            });
        } else {
             console.error("Resposta da API de clientes não é uma lista:", usuarios);
        }
    } catch (error) {
        console.error("Erro ao carregar clientes:", error);
    }
}

async function carregarMotoristas() {
    try {
        const resposta = await fetch(apiUrlMotoristas);
        const motoristas = await resposta.json();

        const motoristas_lista = motoristas;

        const select = document.getElementById("informacoes_motorista");
        select.innerHTML = '<option value="">Selecione um Motorista</option>';

        if (Array.isArray(motoristas_lista)) {
            motoristas_lista.forEach(motorista => {
                const option = document.createElement("option");
                option.value = String(motorista.id);
                option.textContent = `${motorista.nome} (ID: ${motorista.id})`;
                select.append(option);
            });
        } else {
            console.error("Resposta da API de motoristas não é uma lista:", motoristas);
        }
    } catch (error) {
        console.error("Erro ao carregar motorista:", error);
    }
}



async function carregarVeiculos() {
    try {
        const resposta = await fetch(apiUrlVeiculos);
        const veiculos = await resposta.json();
        
        const veiculos_lista = veiculos;

        const select = document.getElementById("informacoes_veiculo");
        select.innerHTML = '<option value="">Selecione um veículo</option>';

        if (Array.isArray(veiculos_lista)) {
            veiculos_lista.forEach(veiculo => {
                const option = document.createElement("option");
                option.value = String(veiculo.id);
                option.textContent = `${veiculo.tipo} (ID: ${veiculo.id})`;
                select.append(option);
            });
        } else {
            console.error("Resposta da API de veículos não é uma lista:", veiculos);
        }
    } catch (error) {
        console.error("Erro ao carregar veículos:", error);
    }
}


async function carregarCidadesSP() {
    const apiIbgeUrl = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/35/municipios";
    const selectOrigem = document.getElementById("origem_carga");
    const selectDestino = document.getElementById("destino_carga");

    try {
        const response = await fetch(apiIbgeUrl);
        const cidades = await response.json();

        cidades.sort((a, b) => a.nome.localeCompare(b.nome));

        cidades.forEach(cidade => {
            const optionOrigem = document.createElement("option");
            optionOrigem.value = cidade.nome;
            optionOrigem.textContent = cidade.nome;
            selectOrigem.appendChild(optionOrigem);

            const optionDestino = document.createElement("option");
            optionDestino.value = cidade.nome;
            optionDestino.textContent = cidade.nome;
            selectDestino.appendChild(optionDestino);
        });

    } catch (error) {
        console.error("Erro ao carregar cidades:", error);
    }
}


async function deletarCarga(id) {
    if (!confirm("Tem certeza que deseja excluir esta carga?")) {
        return;
    }

    try {
        await fetch(`${apiUrl}/${id}`, { method: "DELETE" });
        carregarCargas();
    } catch (error) {
        console.error("Erro ao excluir carga:", error);
    }
}

window.onload = async function () {
    await carregarClientes();
    await carregarMotoristas();
    await carregarVeiculos();
    await carregarCidadesSP();
    carregarCargas();

};
