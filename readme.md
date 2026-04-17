# 🔌 API Catraca - Back-end para Sistema de Controle de Acesso

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python](https://img.shields.io/badge/Python-100%25-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-API-black)](https://flask.palletsprojects.com/)
[![Vercel](https://img.shields.io/badge/Deploy-Vercel-000000)](https://vercel.com)

> **API RESTful** desenvolvida em Python para gerenciar o backend do sistema Catraca Online, com rotas de autenticação e operações CRUD.

![Preview da API](https://via.placeholder.com/800x400?text=Documentação+da+API+Catraca) <!-- Substitua por um print da documentação ou diagrama -->

## 🚀 Demonstração

A API está disponível em produção:  
🔗 **[api-catraca-five.vercel.app](https://api-catraca-five.vercel.app)**

> **Nota:** Por ser uma API, acessar diretamente pode retornar um erro 404 ou JSON informativo. Utilize ferramentas como Postman ou Insomnia para testar os endpoints.

## ✨ Funcionalidades

- 🔐 **Autenticação** - Sistema de login e gerenciamento de sessão (`auth.py`)
- 📝 **Operações CRUD** - Criar, ler, atualizar e deletar registros
- 🔄 **Rota PATCH** - Atualizações parciais de recursos (melhorada no último commit)
- 📄 **Documentação OpenAPI** - Especificação da API no formato `openapi.yaml`
- ☁️ **Deploy na Vercel** - Configurado com `vercel.json` para serverless functions

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Descrição |
|------------|-------------|
| **Python 3** | Linguagem principal da API |
| **Flask** | Framework web para criação das rotas |
| **OpenAPI 3.0** | Documentação estruturada dos endpoints |
| **Vercel** | Plataforma de deploy (serverless) |
| **pip** | Gerenciador de dependências |

## 📁 Estrutura do Projeto
