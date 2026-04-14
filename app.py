from flask import Flask, jsonify, request
import random
import firebase_admin
from firebase_admin import credentials, firestore
from auth import token_obrigatorio, gerar_token
from flask_cors import CORS
import os
from dotenv import load_dotenv
import json
from flasgger import Swagger


load_dotenv()

app = Flask(__name__)
#versão do openapi
app.config['SWAGGER'] = {
    'openapi':'3.0.0'
}
swagger = Swagger(app, template_file='openapi.yaml')
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
CORS(app, origins="*")

ADM_USUARIO = os.getenv("ADM_USUARIO")
ADM_SENHA = os.getenv("ADM_SENHA")

if os.getenv("VERCEL"):
    #online na vercel
    cred = credentials.Certificate(json.loads(os.getenv("FIREBASE_CREDENTIALS")))
else:
    # Carregar as credenciais do Firebase
    cred = credentials.Certificate("firebase.json")

firebase_admin.initialize_app(cred)

# Conectar-se o Firestore
db = firestore.client()

# Rota principal de boas vindas
@app.route("/", methods=['GET'])
def root():
    return jsonify({
        "api":"academia-catraca",
        "version":"1.0",
        "Author": "Julio Aurelio Souza"
    }), 200

# ===========================
#       ROTA DE LOGIN
# ===========================
@app.route("/login", methods=['POST'])
def login ():
    dados = request.get_json()

    if not dados:
        return jsonify({"error": "Envie os dados para login"}), 400
    
    usuario = dados.get("usuario")
    senha = dados.get("senha")

    if not usuario or not senha:
        return jsonify({"error": "Usuário e senha são obrigatórios!"}), 400
    
    if usuario == ADM_USUARIO and senha == ADM_SENHA:
        token = gerar_token(usuario)
        return jsonify({
            "message": "Login realizado com sucesso!",
            "token": token
        }), 200
    
    return jsonify({"error": "Usuário ou senha inválidos"})

# ===========================
#   ROTAS DE ALUNOS
# ===========================

# Rota 1 - Método GET - Todos os alunos
@app.route("/alunos", methods=['GET'])
def get_alunos():
    alunos = []  # Lista vazia
    lista = db.collection('alunos').stream() # Lista todos documentos
    
    # Transforma objeto do Firestore em Dicionário Python
    for item in lista:
        alunos.append(item.to_dict())
    
    return jsonify(alunos), 200

# Rota 3 - Método GET - Retorna aluno pelo id
@app.route("/alunos/<int:id>", methods=['GET'])
def get_aluno_by_id(id):
    lista = db.collection('alunos').where('id', '==', id).stream()

    for item in lista:
        return jsonify(item.to_dict()), 200
    
    return jsonify({"error": "Aluno não encontrado"}), 404

# Rota 3.1 - Método GET - Buscar por CPF (importante pra catraca)
@app.route("/alunos/cpf/<string:cpf>", methods=['GET'])
def get_aluno_by_cpf(cpf):
    lista = db.collection('alunos').where('cpf', '==', cpf).stream()

    for item in lista:
        return jsonify(item.to_dict()), 200
    
    return jsonify({"error": "CPF não encontrado"}), 404

# =======================================
#     ROTAS PRIVADAS (precisa de token)
# =======================================

# Rota 4 - Método POST - Criar novo aluno
@app.route("/alunos", methods=['POST'])
@token_obrigatorio
def post_aluno():
    
    dados = request.get_json()

    # Validação: precisa de NOME e CPF
    if not dados or "nome" not in dados or "cpf" not in dados:
        return jsonify({"error": "Dados inválidos ou incompletos! Envie nome e cpf"}), 400
    
    # Verificar se CPF já existe
    cpf_existente = db.collection('alunos').where('cpf', '==', dados["cpf"]).stream()
    if any(True for _ in cpf_existente):
        return jsonify({"error": "CPF já cadastrado!"}), 400
    
    try:
        # 🔥 Controlador de ID automático
        contador_ref = db.collection("contador").document("controle_id")
        contador_doc = contador_ref.get()

        if not contador_doc.exists:
            contador_ref.set({"ultimo_id": 0})
            ultimo_id = 0
        else:
            ultimo_id = contador_doc.to_dict().get("ultimo_id", 0)

        novo_id = ultimo_id + 1
        contador_ref.update({"ultimo_id": novo_id})

        # Salvar no Firestore
        db.collection("alunos").add({
            "id": novo_id,
            "nome": dados["nome"],
            "cpf": dados["cpf"],
            "status": "ativo"  # ativo, suspenso, cancelado
        })

        return jsonify({
            "message": "Aluno cadastrado com sucesso!",
            "id": novo_id
        }), 201

    except Exception as e:
        print("ERRO REAL:", e)
        return jsonify({
            "error": "Falha no cadastro do aluno",
        }), 400

# Rota 5 - Método PUT - Alteração total (nome e cpf)
@app.route("/alunos/<int:id>", methods=['PUT'])
@token_obrigatorio
def aluno_put(id):
    
    dados = request.get_json()

    # PUT - É necessário enviar NOME e CPF
    if not dados or "nome" not in dados or "cpf" not in dados:
        return jsonify({"error": "Dados inválidos ou incompletos! Envie nome e cpf"}), 400
    
    try:
        docs = db.collection("alunos").where("id", "==", id).limit(1).get()
        if not docs:
            return jsonify({"error": "Aluno não encontrado"}), 404
        
        # Verificar se o novo CPF já pertence a outro aluno
        cpf_existente = db.collection('alunos').where('cpf', '==', dados["cpf"]).where('id', '!=', id).stream()
        if any(True for _ in cpf_existente):
            return jsonify({"error": "CPF já cadastrado para outro aluno!"}), 400
        
        # Pega o primeiro (e único) documento da lista
        for doc in docs:
            doc_ref = db.collection("alunos").document(doc.id)
            doc_ref.update({
                "nome": dados["nome"],
                "cpf": dados["cpf"]
            })

        return jsonify({"message": "Aluno alterado com sucesso"}), 200
    except Exception as e:
        print("ERRO:", e)
        return jsonify({"error": "Falha na alteração do aluno"}), 400

# Rota 6 - Método PATCH - Alteração parcial (pode alterar só nome ou só status)
@app.route("/alunos/<int:id>", methods=['PATCH'])
@token_obrigatorio
def aluno_patch(id):
    
    dados = request.get_json()

    # PATCH - pode alterar só nome ou só status
    if not dados or ("nome" not in dados and "status" not in dados):
        return jsonify({"error": "Dados inválidos! Envie nome ou status"}), 400
    
    try:
        docs = db.collection("alunos").where("id", "==", id).limit(1).get()
        if not docs:
            return jsonify({"error": "Aluno não encontrado"}), 404
        
        doc_ref = db.collection("alunos").document(docs[0].id)
        update_aluno = {}
        
        if "nome" in dados:
            update_aluno["nome"] = dados["nome"]
        
        if "status" in dados:
            # Valida status
            if dados["status"] not in ["ativo", "suspenso", "cancelado"]:
                return jsonify({"error": "Status inválido! Use: ativo, suspenso ou cancelado"}), 400
            update_aluno["status"] = dados["status"]

        # Atualiza o Firestore
        doc_ref.update(update_aluno)

        return jsonify({"message": "Aluno alterado com sucesso"}), 200

    except Exception as e:
        print("ERRO:", e)
        return jsonify({"error": "Falha na alteração do aluno"}), 400

# Rota 7 - DELETE - Excluir aluno
@app.route("/alunos/<int:id>", methods=['DELETE'])
@token_obrigatorio
def delete_aluno(id):
    docs = db.collection("alunos").where("id", "==", id).limit(1).get()

    if not docs:
        return jsonify({"error": "Aluno não encontrado"}), 404

    doc_ref = db.collection("alunos").document(docs[0].id)
    doc_ref.delete()
    return jsonify({"message": "Aluno excluído com sucesso!"}), 200

# ===========================
#   ROTA ESPECIAL PRA CATRACA
# ===========================
@app.route("/validar-acesso", methods=['POST'])
def validar_acesso():
    """
    Rota que a catraca vai chamar pra validar se o aluno pode entrar
    Enviar: {"cpf": "123.456.789-00"}
    """
    dados = request.get_json()
    
    if not dados or "cpf" not in dados:
        return jsonify({"error": "Envie o CPF para validação"}), 400
    
    cpf = dados["cpf"]
    
    try:
        # Busca aluno pelo CPF
        alunos = db.collection('alunos').where('cpf', '==', cpf).limit(1).stream()
        
        for aluno in alunos:
            dados_aluno = aluno.to_dict()
            
            # Verifica se está ativo
            if dados_aluno.get("status") == "ativo":
                return jsonify({
                    "acesso": True,
                    "mensagem": "Acesso liberado!",
                    "nome": dados_aluno.get("nome")
                }), 200
            else:
                return jsonify({
                    "acesso": False,
                    "mensagem": f"Acesso negado! Aluno está {dados_aluno.get('status')}",
                    "nome": dados_aluno.get("nome")
                }), 200
        
        # CPF não encontrado
        return jsonify({
            "acesso": False,
            "mensagem": "CPF não cadastrado na academia"
        }), 200
        
    except Exception as e:
        print("ERRO:", e)
        return jsonify({"error": "Erro na validação"}), 500

# ====================
#  Rotas de tratamento de erros
# ====================
@app.errorhandler(404)
def erro404(error):
    return jsonify({"error": "URL não encontrada"}), 404

@app.errorhandler(500)
def erro500(error):
    return jsonify({"error": "Servidor interno com falhas. Tente mais tarde"}), 500

if __name__ == "__main__":
    app.run(debug=True)