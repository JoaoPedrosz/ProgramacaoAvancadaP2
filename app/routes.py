from flask import Flask, request, jsonify, render_template
from bson import json_util, ObjectId
from app import app, db

# rota padrão: lista as notas em HTML
@app.route('/')
def index():
    notas = list(db.notafiscal.find({}).sort("numero", 1))
    return render_template('listNotas.html', notas=notas)

# rota JSON: lista todas as notas
@app.route('/notas')
def listar_notas():
    notas = list(db.notafiscal.find({}, {"_id": 0}))
    return jsonify(status="OK", notas=notas)

# exibe o formulário de criação
@app.route('/create')
def create():
    return render_template('create.html')

# processa criação
@app.route('/createAction', methods=['POST'])
def createAction():
    data = request.form.to_dict()
    if data:
        result = db.notafiscal.insert_one(data)
        if result.inserted_id:
            return jsonify(mensagem='Inserido')
    return jsonify(mensagem='Não inserido')

# exibe o formulário de edição
@app.route('/update/<string:numero>')
def update(numero):
    nota = db.notafiscal.find_one({"numero": numero})
    if nota:
        return render_template('update.html', nota=nota)
    return jsonify(mensagem='Nota não existe')

# processa edição
@app.route('/updateAction', methods=['POST'])
def updateAction():
    data = request.form.to_dict()
    numero = data.pop('numero', None)
    if numero:
        update_fields = {
            'comprador': data.get('comprador'),
            'cnpj':       data.get('cnpj'),
            'endereco':   data.get('endereco'),
            'telefone':   data.get('telefone'),
            'data':       data.get('data'),
            'valor':      data.get('valor'),
            'itens':      data.get('itens')
        }
        res = db.notafiscal.update_one({"numero": numero}, {"$set": update_fields})
        if res.modified_count > 0:
            return jsonify(mensagem='Alterado')
    return jsonify(mensagem='Não alterado')

# exclui nota
@app.route('/delete/<string:numero>')
def delete(numero):
    res = db.notafiscal.delete_one({"numero": numero})
    if res.deleted_count > 0:
        return jsonify(mensagem='Removido')
    return jsonify(mensagem='Não removido')
