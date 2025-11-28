from flask import Blueprint, render_template, request

from projeto_final.dao.cliente_dao import Cliente, ClienteDAO
from projeto_final.dao.uf_dao import UfDAO

bp_cl = Blueprint('cl', __name__)

@bp_cl.route('/form_create')
def form_create():
    dao = UfDAO()
    lst = dao.selecionar_tudo()
    return render_template('/cl/form_create.html', msg="", display="none", lst=lst)

@bp_cl.route('/create', methods=["POST"])
def create():
    cl = Cliente()
    cl.nme_cliente = request.form['nme_cliente']
    cl.dta_nasc_cliente = request.form['dta_nasc_cliente']
    cl.end_cliente = request.form['end_cliente']
    cl.cep_cliente = request.form['cep_cliente']
    cl.cod_uf = request.form['cod_uf']


    dao = ClienteDAO()
    dao.inserir(cl)
    if cl.idt_cliente is None:
        msg = 'Erro ao inserir modelo. Procure o adiministrador do sistema'
    else:
        msg = f'Cliente número {cl.idt_cliente} inserido com sucesso.'

    dao = UfDAO()
    lst = dao.selecionar_tudo()

    return render_template('/cl/form_create.html', msg=msg, display="block", lst=lst)

@bp_cl.route('/read')
def read():
    dao = ClienteDAO()
    lst = dao.selecionar_tudo()

    if not lst:
        msg = 'Não há clientes na base de dados.'
    else:
        msg = f'Listados {len(lst)} clientes na base de dados.'
    return render_template('/cl/read.html', msg=msg, lst=lst)


@bp_cl.route('/edit')
def edit():
    dao = ClienteDAO()
    lst = dao.selecionar_tudo()

    if not lst:
        msg = 'Não há Clientes na base de dados.'
    else:
        msg = f'Listados {len(lst)} clientes na base de dados.'
    return render_template('/cl/edit.html', msg=msg, lst=lst)

@bp_cl.route('/delete/<int:idt>')
def delete(idt):
    dao = ClienteDAO()
    if dao.deletar(idt):
        msg = 'Cliente excluído com sucesso!'
    else:
        msg = "Erro ao tentar excluir cliente, provavelmente tem uma compra associada!"


    lst = dao.selecionar_tudo()
    if not lst:
        msg = ' | Não há clientes na base de dados.'
    else:
        msg = f'| Listados {len(lst)} clientes na base de dados.'
    return render_template('/cl/edit.html', msg=msg, lst=lst)




@bp_cl.route('/form_update/<int:idt>')
def form_update(idt):
    dao = ClienteDAO()
    cl = dao.selecionar_por_idt(idt)
    dao = UfDAO()
    lst = dao.selecionar_tudo()


    return render_template('/cl/form_update.html', cl=cl, lst=lst, msg='', display="none")


@bp_cl.route('/save_update', methods=['POST'])
def save_update():
    cl = Cliente()
    cl.idt_cliente = request.form['idt_cliente']
    cl.nme_cliente = request.form['nme_cliente']
    cl.dta_nasc_cliente = request.form['dta_nasc_cliente']
    cl.end_cliente = request.form['end_cliente']
    cl.cep_cliente = request.form['cep_cliente']
    cl.cod_uf = request.form['cod_uf']


    dao = ClienteDAO()
    dao.atualiar(cl)
    msg = f'Cliente número {cl.idt_cliente} alterado com sucesso.'

    dao = UfDAO()
    lst = dao.selecionar_tudo()

    return render_template('/cl/form_update.html', cl=cl, msg=msg, display="block", lst=lst)