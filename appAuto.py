from flask import Flask, jsonify
from aula01.montadora import MontadoraDAO

app = Flask(__name__)


@app.route('/montadoras_json', methods=['GET'])
def montadoras_json():
    dao = MontadoraDAO()
    """
    Rota para listar todas as montadoras do banco de dados.
    Retorna uma resposta JSON.
    """
    if not dao.connection or not dao.connection.is_connected():
        return jsonify({'erro': 'Não foi possível conectar ao banco de dados.'}), 500

    montadoras = dao.get_montadoras()

    if montadoras:
        # Flask automaticamente serializa uma lista de dicionários para JSON
        return jsonify(montadoras), 200
    else:
        # Se não houver montadoras ou ocorrer um erro na busca
        return jsonify({'mensagem': 'Nenhuma montadora encontrada ou erro ao buscar dados.'}), 404


if __name__ == '__main__':
    # Execute a aplicação Flask
    # Em um ambiente de produção, você usaria um servidor WSGI como Gunicorn ou uWSGI
    app.run(debug=True, port=80)
