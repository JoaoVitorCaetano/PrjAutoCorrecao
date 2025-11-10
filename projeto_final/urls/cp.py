from flask import Blueprint, render_template, redirect, request
from projeto_final.dao.compra_dao import Compra, CompraDAO
from projeto_final.dao.versao_dao import Versao, VersaoDAO
from projeto_final.dao.cliente_dao import Cliente, ClienteDAO
from datetime import date
import random

bp_cp = Blueprint('cp', __name__)

@bp_cp.route('/form_create')
def form_create():
    dao = VersaoDAO()
    lst = dao.selecionar_tudo()
    return render_template('/cp/compra.html', msg="", display="none", lst=lst)

@bp_cp.route('/create', methods=["POST"])
def create():
    def gerar_nf():
        nf = random.choices("0123456789", k=44)
        return "".join(nf)

    data_atual = date.today()
    cp = Compra()
    cp.dta_compra = data_atual
    cp.num_nf_compra = gerar_nf()
    cp.cod_versao =
    cp.cod_cliente = request.form['cep_cliente']
    cp.vlr_final_compra = request.form['cod_uf']


    dao = ClienteDAO()
    dao.inserir(cl)
    if cl.idt_cliente is None:
        msg = 'Erro ao inserir modelo. Procure o adiministrador do sistema'
    else:
        msg = f'Cliente número {cl.idt_cliente} inserido com sucesso.'

    dao = UfDAO()
    lst = dao.selecionar_tudo()

    return render_template('/cl/form_create.html', msg=msg, display="block", lst=lst)

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

