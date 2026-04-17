# 🚀 API Catraca - Backend do Sistema de Controle de Academia

API RESTful completa para gerenciamento de alunos e controle de acesso de academia. Desenvolvida com Flask, Firebase Firestore e autenticação JWT.

## 🌐 Links do Projeto

| Ambiente | URL |
| :--- | :--- |
| **Produção (Vercel)** | https://api-catraca-five.vercel.app |
| **Repositório** | https://github.com/julio-aurelio/API-catraca |
| **Documentação Swagger** | https://api-catraca-five.vercel.app/apidocs |

## ✨ Funcionalidades

- ✅ **CRUD completo** de alunos (criar, ler, atualizar, deletar)
- 🔐 **Autenticação JWT** para rotas administrativas
- 🚪 **Rota especial para catraca** - validação de acesso por CPF
- 🔍 **Busca por CPF** (com limpeza automática de formatação)
- 📝 **Atualização parcial (PATCH)** - altere apenas o que precisa
- 🗄️ **Firebase Firestore** - banco de dados em nuvem e persistente
- 📄 **Documentação Swagger/OpenAPI** interativa
- 🔄 **CORS configurado** - aceita requisições de qualquer origem

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Descrição |
| :--- | :--- | :--- |
| Python | 3.8+ | Linguagem principal |
| Flask | 2.3.3 | Framework web |
| Firebase Admin | 6.4.0 | SDK do Firestore |
| PyJWT | 2.8.0 | Autenticação via token |
| Flasgger | 0.9.7.1 | Documentação Swagger |
| Flask-CORS | 4.0.0 | Cross-origin requests |
| Vercel | - | Plataforma de deploy |

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Conta no Firebase (Firestore)
- Arquivo de credenciais do Firebase (`firebase.json`)
- Git

## 🔧 Instalação Local

### 1. Clone o repositório

```bash
git clone https://github.com/julio-aurelio/API-catraca.git
cd API-catraca
