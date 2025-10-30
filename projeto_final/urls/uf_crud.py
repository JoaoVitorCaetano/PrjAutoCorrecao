from flask import Blueprint, render_template, request
from projeto_final.dao.uf_dao import Uf, UfDAO

bp_uf = Blueprint('UF', __name__, template_folder='../templates')

@bp_uf.route('/read')
def read():
    dao = UfDAO()
    lst = dao.selecionar_tudo()

    if not lst:
        msg = 'Não há Unidades Federativas na base de dados'
    else:
        msg = f'Listados {len(lst)} Unidades Federativas na base de dados'

    return render_template('UF/read.html', msg=msg, lst=lst)


@bp_uf.route('/form_create')
def form_create():
    return render_template('/UF/form_create.html', msg="", display="none")


@bp_uf.route('/create', methods=['POST'])
def create():
    uf = Uf()
    uf.sgl_uf = request.form['sgl_uf']
    uf.nme_uf = request.form['nme_uf']


    dao = UfDAO()
    dao.inserir(uf)
    if uf.idt_uf is None:
        msg = 'Erro ao inserir UF. Procure o administrador do sistema'
    else:
        msg = f'Uf numero {uf.idt_uf} inserida com sucesso.'

    return render_template('UF/form_create.html', msg=msg, display="block")