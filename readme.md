# 🔌 API Catraca - Back-end para Sistema de Controle de Acesso

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-black)](https://flask.palletsprojects.com/)
[![Vercel](https://img.shields.io/badge/Deploy-Vercel-000000)](https://vercel.com)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0-green)](https://swagger.io/)

> **API RESTful** desenvolvida em Python para gerenciar o backend do sistema Catraca Online, com rotas de autenticação, operações CRUD e suporte a atualizações parciais (PATCH).

## 🚀 Demonstração

A API está disponível em produção:  
🔗 **[api-catraca-five.vercel.app](https://api-catraca-five.vercel.app)**

> **Nota:** Por ser uma API, acessar diretamente pode retornar um erro 404 ou JSON informativo. Utilize ferramentas como Postman, Insomnia ou cURL para testar os endpoints.

## ✨ Funcionalidades

- 🔐 **Autenticação segura** - Sistema de login e gerenciamento de sessão via `auth.py`
- 📝 **CRUD completo** - Criar, ler, atualizar e deletar registros de acesso
- 🔄 **Rota PATCH** - Atualizações parciais de recursos (otimizada no último commit)
- 📄 **Documentação OpenAPI** - Especificação completa no formato `openapi.yaml`
- ☁️ **Deploy na Vercel** - Configurado com `vercel.json` para serverless functions
- 🐍 **100% Python** - Código limpo e de fácil manutenção

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Descrição |
|------------|--------|-------------|
| **Python** | 3.8+ | Linguagem principal da API |
| **Flask** | 2.0+ | Framework web para criação das rotas |
| **Flask-CORS** | 4.0+ | Suporte a requisições cross-origin |
| **OpenAPI** | 3.0 | Documentação estruturada dos endpoints |
| **Vercel** | - | Plataforma de deploy (serverless) |
| **pip** | latest | Gerenciador de dependências |

## 📁 Estrutura do Projeto
API-catraca/
│
├── app.py # Aplicação principal e rotas da API
├── auth.py # Módulo de autenticação e segurança
├── openapi.yaml # Documentação OpenAPI (Swagger)
├── requirements.txt # Dependências do projeto
├── vercel.json # Configuração de deploy na Vercel
├── .gitignore # Arquivos ignorados pelo Git
└── pycache/ # Cache do Python (gerado automaticamente)

text

## 🔧 Como Executar Localmente

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)
- Git (para clonar o repositório)

### Passos detalhados

1. **Clone o repositório**
   ```bash
   git clone https://github.com/julio-aurelio/API-catraca.git
   cd API-catraca
Crie um ambiente virtual (recomendado para isolar dependências)

bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
Instale as dependências

bash
pip install -r requirements.txt
Configure variáveis de ambiente (se necessário)

bash
# Linux/Mac
export FLASK_APP=app.py
export FLASK_ENV=development

# Windows (cmd)
set FLASK_APP=app.py
set FLASK_ENV=development

# Windows (PowerShell)
$env:FLASK_APP="app.py"
$env:FLASK_ENV="development"
Execute a aplicação

bash
python app.py
# ou
flask run
Acesse a API
Disponível em: http://localhost:5000

📡 Endpoints da API
Autenticação
Método	Endpoint	Descrição	Corpo da Requisição
POST	/auth/login	Autentica um usuário	{"usuario": "string", "senha": "string"}
POST	/auth/logout	Encerra a sessão	{"token": "string"}
GET	/auth/status	Verifica status da autenticação	-
Registros de Acesso
Método	Endpoint	Descrição	Parâmetros
GET	/api/registros	Lista todos os registros	?page=1&limit=10
POST	/api/registros	Cria um novo registro	Corpo JSON com dados
GET	/api/registros/{id}	Busca registro específico	id (path)
PUT	/api/registros/{id}	Atualiza registro completamente	Corpo JSON completo
PATCH	/api/registros/{id}	Atualiza parcialmente	Corpo JSON parcial
DELETE	/api/registros/{id}	Remove um registro	id (path)
Health Check
Método	Endpoint	Descrição
GET	/health	Verifica se a API está online
GET	/	Informações básicas da API
📖 Documentação completa: Consulte o arquivo openapi.yaml ou importe-o no Swagger Editor para ver todos os detalhes dos schemas e respostas.

🔄 Fluxo de Funcionamento
graph LR
    A[Cliente] --> B[Requisição HTTP]
    B --> C{app.py}
    C --> D[Rotas públicas]
    C --> E[Rotas protegidas]
    E --> F[auth.py valida token]
    F -->|Válido| G[Processa requisição]
    F -->|Inválido| H[Retorna 401]
    G --> I[Operações CRUD/PATCH]
    I --> J[Resposta JSON]
    D --> J
    H --> J
    J --> A
🧪 Testando a API
Com cURL (linha de comando)
bash
# 1. Health check
curl -X GET https://api-catraca-five.vercel.app/health

# 2. Login (obter token)
curl -X POST https://api-catraca-five.vercel.app/auth/login \
  -H "Content-Type: application/json" \
  -d '{"usuario":"admin", "senha":"123456"}'

# 3. Listar registros (com autenticação)
curl -X GET https://api-catraca-five.vercel.app/api/registros \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"

# 4. Criar novo registro
curl -X POST https://api-catraca-five.vercel.app/api/registros \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{"usuario_id": 1, "status": "liberado"}'

# 5. Atualização parcial (PATCH)
curl -X PATCH https://api-catraca-five.vercel.app/api/registros/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{"status": "bloqueado"}'

# 6. Deletar registro
curl -X DELETE https://api-catraca-five.vercel.app/api/registros/1 \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
Com Postman
Importe a documentação

Abra o Postman

Clique em "Import" → "Upload Files"

Selecione o arquivo openapi.yaml

A coleção será criada automaticamente

Configure variáveis

text
base_url: https://api-catraca-five.vercel.app
token: {{token_obtido_no_login}}
Teste os endpoints na ordem:

POST /auth/login (salvar token)

GET /api/registros (usar token)

POST /api/registros (criar)

PATCH /api/registros/{id} (atualizar parcial)

Com Python (requests)
python
import requests

BASE_URL = "https://api-catraca-five.vercel.app"

# Login
response = requests.post(f"{BASE_URL}/auth/login", 
                        json={"usuario": "admin", "senha": "123456"})
token = response.json()["token"]

# Buscar registros
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{BASE_URL}/api/registros", headers=headers)

# Atualização parcial
response = requests.patch(f"{BASE_URL}/api/registros/1",
                         headers=headers,
                         json={"status": "liberado"})
📦 Dependências
As dependências estão listadas no requirements.txt:

txt
Flask==2.3.3
Flask-CORS==4.0.0
python-dotenv==1.0.0
PyJWT==2.8.0  # Para autenticação com JWT
werkzeug==2.3.7
Para instalar todas:

bash
pip install -r requirements.txt
🚢 Deploy na Vercel
O projeto está configurado para deploy automático na Vercel através do vercel.json:

json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
Fazer seu próprio deploy:
bash
# Instalar Vercel CLI
npm install -g vercel

# Fazer login
vercel login

# Deploy (será gerada uma URL temporária)
vercel

# Deploy para produção
vercel --prod
📊 Códigos de Resposta
Código	Significado	Quando ocorre
200	OK	Requisição bem-sucedida
201	Created	Recurso criado com sucesso
204	No Content	Deleção bem-sucedida
400	Bad Request	Dados inválidos ou faltando
401	Unauthorized	Token ausente ou inválido
403	Forbidden	Sem permissão para acessar
404	Not Found	Endpoint ou recurso não existe
422	Unprocessable Entity	Validação de dados falhou
500	Internal Server Error	Erro no servidor
📝 Melhorias Recentes (Changelog)
[2026-04-14] - Melhoria na Rota PATCH
✨ Otimização da rota de atualização parcial

🐛 Correção de bugs na validação de dados

📄 Documentação atualizada no openapi.yaml

⚡ Performance melhorada nas requisições

[2026-04-14] - Versão Inicial
🎉 Lançamento da API com rotas básicas

🔐 Implementação do sistema de autenticação

📝 Suporte a CRUD completo

🔐 Segurança
✅ Tokens JWT para autenticação stateless

✅ Validação de dados em todas as rotas

✅ CORS configurado para origens específicas

✅ Senhas hasheadas (se usando banco de dados)

⚠️ HTTPS habilitado no deploy da Vercel

🤝 Contribuição
Contribuições são muito bem-vindas! Siga os passos:

Fork o projeto

Crie uma branch (git checkout -b feature/nova-feature)

Commit as mudanças (git commit -m 'Adiciona nova feature X')

Push para a branch (git push origin feature/nova-feature)

Abra um Pull Request

Diretrizes para contribuição:
Mantenha o código limpo e documentado

Atualize o openapi.yaml ao modificar endpoints

Teste localmente antes de enviar

Descreva claramente as mudanças no PR

🐛 Reportar Bugs
Encontrou um bug? Por favor, abra uma Issue com:

Descrição detalhada do problema

Passos para reproduzir

Comportamento esperado vs atual

Screenshots (se aplicável)

📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

🔗 Integração com Outros Projetos
Esta API foi desenvolvida para servir o front-end do:

🚪 Catraca Online - Interface de validação de acesso com animações

🏢 Admin Academia - Área administrativa para gestão

📞 Suporte
Dúvidas ou sugestões? Entre em contato:

📧 Email: [julio.aurelio@exemplo.com]

💬 GitHub Issues: Abrir issue

📈 Roadmap
Futuras melhorias planejadas:

Integração com banco de dados (PostgreSQL/MongoDB)

Rate limiting para proteção contra abusos

Logs detalhados de requisições

Webhooks para eventos importantes

Dashboard administrativo

Testes unitários e de integração

CI/CD com GitHub Actions

📚 Recursos Adicionais
Documentação do Flask

OpenAPI Specification

Vercel Python Documentation

JWT.io

👨‍💻 Autor
Julio Aurelio Souza
https://img.shields.io/badge/GitHub-julio--aurelio-181717?style=flat&logo=github
https://img.shields.io/badge/LinkedIn-Julio%2520Aurelio-blue?style=flat&logo=linkedin

⭐ Mostre seu apoio
Se esta API foi útil para seu projeto, considere dar uma estrela no GitHub! ⭐

Isso ajuda o projeto a crescer e incentiva novas funcionalidades.

