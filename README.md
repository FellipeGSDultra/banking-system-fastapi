# 🏦 Banking API Assíncrona

API assíncrona desenvolvida em Python com **FastAPI** que simula operações bancárias essenciais, como criação de conta, autenticação, depósitos, transferências entre contas e consulta de histórico de transações.

Este projeto foi desenvolvido como trabalho de conclusão do curso de FastAPI.

---

## 🚀 Tecnologias Utilizadas

* **Python 3.14+**
* **FastAPI**: Framework moderno e de alto desempenho para construir APIs.
* **Poetry**: Gerenciador de dependências e ambientes virtuais.
* **Uvicorn**: Servidor ASGI para rodar a aplicação.
* **PyJWT**: Geração e validação de Tokens JWT para autenticação.
* **Passlib (Bcrypt)**: Criptografia segura de senhas (hashing).
* **Pydantic**: Validação de dados e modelagem.

---

## 📦 Arquitetura e Organização do Projeto

O projeto adota uma estrutura de pastas limpa e profissional, separando as responsabilidades de cada componente:

```text
Banking_System_FastAPI/
├── src/
│   ├── database.py   # Banco de dados simulado (em memória)
│   ├── models.py     # Modelos de dados e esquemas do Pydantic
│   └── security.py   # Lógica de criptografia de senhas e JWT
├── main.py           # Arquivo principal que gerencia as rotas da API
├── pyproject.toml    # Configurações do Poetry e dependências
└── README.md         # Documentação do projeto
```

---

## 🛠️ Requisitos Técnicos Atendidos

1. **FastAPI Assíncrono**: Uso de rotas `async` para alta performance.
2. **Modelagem de Dados**: Validação rigorosa dos dados de entrada e saída com Pydantic.
3. **Validação de Operações**:
   * Proibição de valores negativos em depósitos e transferências.
   * Validação de saldo suficiente antes de transferir.
   * Bloqueio de transferências para contas de usuários que não existem no sistema.
4. **Segurança (Autenticação JWT)**: 
   * Senhas salvas com hash criptográfico (Bcrypt).
   * Rotas financeiras (`/deposit`, `/transfer`, `/history`) protegidas, exigindo Token JWT via Bearer Authentication.
5. **Documentação Automatizada**: Integração nativa com OpenAPI/Swagger.

---

## 🔧 Como Rodar o Projeto Localmente

### 1. Pré-requisitos
Certifique-se de ter o **Python** e o **Poetry** instalados na sua máquina.

### 2. Clonar o Repositório
```bash
git clone https://github.com/SEU_USUARIO/banking-system-fastapi.git
cd banking-system-fastapi
```

### 3. Instalar as Dependências
O Poetry gerenciará o ambiente virtual e baixará as versões corretas das bibliotecas:
```bash
poetry env activate
poetry add "fastapi[all]" pyjwt passlib[bcrypt]
poetry add bcrypt==3.2.2
```

### 4. Iniciar o Servidor
Com o ambiente preparado, ligue a API:
```bash
poetry run uvicorn main:app --reload
```

---

## 📖 Como Testar a API (OpenAPI / Swagger)

Após iniciar o servidor, abra o seu navegador e acesse a documentação interativa:
👉 **http://127.0.0.1:8000/docs**

### Fluxo de Teste Recomendado:
1. **Criar Usuário**: Vá na rota `POST /register`, clique em *Try it out* e crie um usuário (Ex: `{"username": "deise", "password": "123"}`).
2. **Fazer Login**: Clique no botão verde **Authorize** no topo da página. Insira as credenciais criadas para gerar e salvar o Token JWT. Os cadeados das rotas se fecharão.
3. **Adicionar Saldo**: Acesse a rota protegida `POST /deposit` e envie um valor positivo para sua conta.
4. **Registrar Segundo Usuário**: Use o `/register` novamente para criar outra conta (Ex: `"joao"`), simulando outro correntista existente.
5. **Transferir**: Acesse `POST /transfer` e envie uma quantia para o usuário criado no passo anterior.
6. **Extrato**: Acesse `GET /history` para ver a lista de todas as movimentações financeiras vinculadas à sua conta.
```