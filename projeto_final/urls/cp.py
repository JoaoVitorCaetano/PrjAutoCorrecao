from flask import Blueprint, render_template, request
from projeto_final.dao.compra_dao import Compra, CompraDAO
from projeto_final.dao.versao_dao import Versao, VersaoDAO
from projeto_final.dao.cliente_dao import Cliente, ClienteDAO
from datetime import date
import random

def gerar_nf():
    nf = random.choices("0123456789", k=9)
    return "".join(nf)

bp_cp = Blueprint('cp', __name__)

@bp_cp.route('/compra')
def form_create():
    dao = VersaoDAO()
    lst = dao.selecionar_tudo()

    dao_cliente = ClienteDAO()
    lst_clientes = dao_cliente.selecionar_tudo()

    return render_template('/cp/compra.html', msg="", display="none", lst=lst, lst_clientes=lst_clientes)


@bp_cp.route('/comprar/', methods=['POST'])
def comprar():
    data_atual = date.today()
    cp = Compra()
    cp.dta_compra = data_atual
    cp.num_nf_compra = gerar_nf()
    cp.cod_versao = request.form['cod_versao']
    cp.cod_cliente = request.form['cod_cliente']
    cp.vlr_final_compra = request.form['vlr_final_compra']


    dao = CompraDAO()
    dao.inserir(cp)
    if cp.idt_compra is None:
        msg = 'Erro ao registrar compra. Tente Novamente.'
    else:
        msg = f'Compra número {cp.idt_compra} registrada com sucesso.'

    dao_versoes = VersaoDAO()
    lst = dao_versoes.selecionar_tudo()

    return render_template('/cp/compra.html', msg=msg, display="block", lst=lst)

@bp_cp.route('/read')
def read():
    dao = ClienteDAO()
    lst = dao.selecionar_tudo()

    if not lst:
        msg = 'Não há clientes na base de dados.'
    else:
        msg = f'Listados {len(lst)} clientes na base de dados.'
    return render_template('/cl/read.html', msg=msg, lst=lst)


@bp_cp.route('/delete/<int:idt>')
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
    return render_template('/cl/compra.html', msg=msg, lst=lst)

