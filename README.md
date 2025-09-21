🚚 **Sistema de Gerenciamento Logístico**


📌 **Visão Geral do Projeto**

Nosso projeto consiste no desenvolvimento de um Sistema de Gerenciamento Logístico, que permitirá otimizar processos, organizar dados e melhorar a eficiência de operações logísticas.

Durante toda a construção, utilizaremos Docker para criar, implantar e executar aplicações em containers, garantindo isolamento, portabilidade e eficiência no ambiente de desenvolvimento.


```
👥 Equipe

Ana Beatriz

João Pedro

Luiz Otávio

Murillo Rodrigues

Uatila Santos
```


🎯 **Objetivo**

Criar um sistema completo, com front-end, back-end e banco de dados, garantindo integração eficiente entre as camadas.

--------------------------------------------------------------

📌 **Diagrama de Deployment**

![Imagem não reenderizada](./images/Diagrama%20de%20Deployment.jpg)

-----------------------------------------------------------

🖥 **Front-End**

O site será desenvolvido com as três tecnologias base da Web:

HTML → Estrutura das páginas
CSS → Estilo e identidade visual
JavaScript → Dinamismo e interatividade


⚙️ **Back-End**

A API será construída com:

Python → Linguagem principal pela simplicidade e flexibilidade
Flask → Microframework que oferece rapidez, escalabilidade e facilidade para construção de APIs REST


🗄 **Banco de Dados**

O banco será implementado com:

MySQL → Armazenamento seguro e eficiente
Suporte a APIs MySQL para melhor desempenho, segurança e integração padronizada


🐳 **Containerização**

Todo o projeto será conteinerizado com Docker, garantindo:
Isolamento do ambiente
Portabilidade
Facilidade de implantação

-----------------------------------------------------------

📌 **Board do Projeto**

[Board do Projeto no Miro](https://miro.com/app/board/uXjVJQ4lUns=/)

-----------------------------------------------------------

✅ **Lista de Funcionalidades - em ordem por prioridade**

1. Manifesto de carga
2. Cadastro de clientes
3. Cadastro de veículos
4. Cadastros de motoristas
5. Cálculo do valor de frete
6. Emissão de relatórios e documentos
7. Faturamento da empresa

------------------------------------------------------------

🚀 **Como rodar o projeto**

▶️ **Como Executar a API localmente**

1.  Clone o repositório

    ```bash
    git clone https://github.com/luizotavio26/projeto---software-product.git
    cd projeto---software-product
    ```

2.  Crie um ambiente virtual (opcional, mas recomendado)

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows
    ```

3.  Instale as dependências

    ```bash
    pip install -r requirements.txt
    ```

4.  Execute a API

    ```bash
    python app.py
    ```

    A aplicação estará disponível em: 📍 http://localhost:5036
    📝 **Observação:** O banco de dados é criado automaticamente na primeira execução.

---

🐳 **Como Executar a API com Docker**

1.  Clone o repositório

    ```bash
    git clone https://github.com/luizotavio26/projeto---software-product.git
    cd projeto---software-product
    ```

2.  Construa a imagem Docker
    ```bash
    docker build -t manifesto-carga-api .
    ```

3.  Execute o container
    ```bash
    docker run -d -p 5036:5036 manifesto-carga-api
    ```

    **Ou, utilizando Docker Compose (Recomendado):**
    ```bash
    docker-compose up --build
    ```
