from flask import Flask, render_template

from projeto_final.urls.cp import bp_cp
from projeto_final.urls.mt_crud import bp_mt
from projeto_final.urls.md_crud import bp_md
from projeto_final.urls.uf_crud import bp_uf
from projeto_final.urls.cl_curd import bp_cl
from projeto_final.urls.vs_crud import bp_vs

app = Flask(__name__)


# Registrar os Blueprints
app.register_blueprint(bp_mt, url_prefix='/mt')
app.register_blueprint(bp_md, url_prefix='/md')

app.register_blueprint(bp_uf, url_prefix='/UF')

app.register_blueprint(bp_cl, url_prefix='/cl')

app.register_blueprint(bp_cp, url_prefix='/cp')

app.register_blueprint(bp_vs, url_prefix='/vs')


@app.route('/')
def index():
   return render_template('index.html')




if __name__ == '__main__':
   app.run(debug=True, port=5000)
