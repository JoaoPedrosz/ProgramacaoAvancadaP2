from flask import json, request, jsonify
import flask
from bson import json_util
from app import app
from app import db
from bson.objectid import ObjectId

@app.route('/')
@app.route('/index')
def index():
	return flask.jsonify(json.loads(json_util.dumps(db.candidato.find({}).sort("_id", 1))))

@app.route("/create")
def create():
	return flask.render_template('create.html')

@app.route('/createAction', methods=['POST'])
def createAction():
	json_data = request.form.to_dict()
	if json_data is not None:
		if db.candidato.insert_one(json_data).inserted_id is not None:
			return jsonify(mensagem='Inserido')
		else:
			return jsonify(mensagem='Não inserido')
	else:
		return jsonify(mensagem='Nada a inserir')

@app.route("/update/<string:login>")
def update(login):
	candidato = db.candidato.find_one({"login": login})
	if candidato is not None:
		return flask.render_template('update.html', candidato=candidato)
	else:
		return jsonify(mensagem='Login não existe')

@app.route('/updateAction', methods=['POST'])
def updateAction():
	json_data = request.form.to_dict()
	if json_data is not None:
		if db.candidato.update_one({'_id': ObjectId(json_data["_id"])}, {"$set": {'nome': json_data["nome"], 'login': json_data["login"],'senha': json_data["senha"],'descricao': json_data["descricao"]}}).modified_count > 0:
			return jsonify(mensagem='Alterado')
		else:
			return jsonify(mensagem='Não alterado')
	else:
		return jsonify(mensagem='Nada a alterar')

@app.route("/delete/<string:login>")
def delete(login):
    result = db.candidato.delete_one({"login": login})
    if(result.deleted_count > 0):
        return jsonify(mensagem='Removido')
    else:
        return jsonify(mensagem='Não removido')
