from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import pymysql.cursors

app = Flask(__name__, static_folder='static', static_url_path='/static')


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '0001',
    'database': 'estoque',
    'cursorclass': pymysql.cursors.DictCursor
}


def connect_db():
    return pymysql.connect(**db_config)


@app.route('/movimentacoes', methods=['GET'])
def mostrar_formulario_movimentacoes():
    return render_template('movimentacoes.html')


@app.route('/registrar_movimentacao', methods=['POST'])
def processar_movimentacoes():
    tipo = request.form['tipo']
    quantidade = int(request.form['quantidade'])  
    nome_produto = request.form['nome_produto']
    nome_loja = request.form['nome_loja']
    data_movimentacao = request.form['data_movimentacao']


    connection = connect_db()
    try:
        with connection.cursor() as cursor:

            sql = "INSERT INTO movimentacoes (nome_produto, nome_loja, tipo, quantidade, data_movimentacao) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (nome_produto, nome_loja, tipo, quantidade, data_movimentacao))

        connection.commit()
    finally:

        connection.close()


    return redirect(url_for('mostrar_formulario_movimentacoes'))


@app.route('/')
def index():
    return redirect(url_for('mostrar_formulario_movimentacoes'))

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
