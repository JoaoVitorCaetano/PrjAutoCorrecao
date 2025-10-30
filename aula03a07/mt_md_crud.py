from flask import Flask, render_template
from urls.mt_crud import bp_mt
from urls.md_crud import bp_md
from projeto_final.urls.uf_crud import bp_uf

app = Flask(__name__)

# Registrar os Blueprints
app.register_blueprint(bp_mt, url_prefix='/mt')
app.register_blueprint(bp_md, url_prefix='/md')

app.register_blueprint(bp_uf, url_prefix='/UF')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    # Execute a aplicação Flask
    # Em ambiente de produção, você usaria um servidor WSGI como Gunicorn ou uWSGI
    app.run(debug=True, port=80)
