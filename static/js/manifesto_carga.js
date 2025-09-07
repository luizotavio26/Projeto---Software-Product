const apiUrl = "http://127.0.0.1:5036/cargas"; // ajuste se necessário

async function cadastroCarga() {
    const carga = {
        tipo_carga: document.getElementById("tipo_carga").value,
        peso_carga: parseFloat(document.getElementById("peso_carga").value) || 0,
        informacoes_cliente: document.getElementById("informacoes_cliente").value,
        informacoes_motorista: document.getElementById("informacoes_motorista").value,
        origem_carga: document.getElementById("origem_carga").value,
        destino_carga: document.getElementById("destino_carga").value,
        valor_kg: parseFloat(document.getElementById("valor_kg").value) || 0,
        distancia: parseFloat(document.getElementById("distancia").value) || 0
    };

    console.log("Tentando cadastrar carga:", carga); // log para debug

    try {
        const response = await fetch(apiUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(carga)
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error("Erro na API:", response.status, errorText);
            return;
        }

        console.log("Carga cadastrada com sucesso!");
        document.querySelector("form").reset();
        carregarCargas();
    } catch (error) {
        console.error("Erro ao cadastrar carga:", error);
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
                    <td>${carga.id ?? ""}</td>
                    <td>${carga.tipo_carga}</td>
                    <td>${carga.peso_carga}</td>
                    <td>${carga.informacoes_cliente}</td>
                    <td>${carga.informacoes_motorista}</td>
                    <td>${carga.origem_carga}</td>
                    <td>${carga.destino_carga}</td>
                    <td>${carga.valor_kg}</td>
                    <td>${carga.distancia}</td>
                    <td>
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

window.onload = carregarCargas;
