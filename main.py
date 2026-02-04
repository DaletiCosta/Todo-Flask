from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

tarefas = []
proximo_id = 1


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tarefas", methods=["GET"])
def listar_tarefas():
    return jsonify(tarefas)


@app.route("/tarefas", methods=["POST"])
def criar_tarefa():
    global proximo_id

    dados = request.get_json(silent=True) or {}
    titulo = (dados.get("titulo") or "").strip()

    if not titulo:
        return jsonify({"erro": "titulo é obrigatório"}), 400

    tarefa = {"id": proximo_id, "titulo": titulo, "concluida": False}
    proximo_id += 1
    tarefas.append(tarefa)

    return jsonify(tarefa), 201


@app.route("/tarefas/<int:id>", methods=["DELETE"])
def deletar_tarefa(id):
    global tarefas

    antes = len(tarefas)
    tarefas = [t for t in tarefas if t["id"] != id]

    if len(tarefas) == antes:
        return jsonify({"erro": "tarefa não encontrada"}), 404

    return jsonify({"mensagem": "tarefa removida"}), 200

@app.route("/tarefas/<int:id>", methods=["PUT"])
def atualizar_tarefa(id):
    dados = request.get_json(silent=True) or {}
    concl = dados.get("concluida", None)

    # valida se veio True/False
    if not isinstance(concl, bool):
        return jsonify({"erro": "concluida deve ser true/false"}), 400

    for tarefa in tarefas:
        if tarefa["id"] == id:
            tarefa["concluida"] = concl
            return jsonify(tarefa), 200

    return jsonify({"erro": "tarefa não encontrada"}), 404



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

