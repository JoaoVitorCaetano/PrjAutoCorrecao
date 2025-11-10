from flask import Blueprint, render_template, request
from aula03a07.dao.montadora_dao import Montadora, MontadoraDAO

bp_mt = Blueprint('mt', __name__)


@bp_mt.route('/form_create')
def form_create():
    return render_template('/mt/form_create.html', msg="", display="none")


@bp_mt.route('/create', methods=['POST'])
def create():
    # Preencher com dados de montadora vindos do formulário
    m = Montadora()
    m.sgl_montadora = request.form['sgl_montadora']
    m.nme_montadora = request.form['nme_montadora']

    # Salvando a nova montadora
    dao = MontadoraDAO()
    dao.inserir(m)
    if m.idt_montadora is None:
        msg = 'Erro ao inserir montadora. Procure o administrador do sistema'
    else:
        msg = f'Montadora número {m.idt_montadora} inserida com sucesso.'

    return render_template('/mt/form_create.html', msg=msg, display="block")


@bp_mt.route('/read')
def read():
    # Buscar as montadoras para listar em uma tabela
    dao = MontadoraDAO()
    lst = dao.selecionar_tudo()
    if not lst:
        msg = 'Não há montadoras na base de dados.'
    else:
        msg = f'Listadas {len(lst)} montadoras da base de dados.'

    return render_template('/mt/read.html', msg=msg, lst=lst)


@bp_mt.route('/edit')
def edit():
    # Buscar as montadoras para listar em uma tabela
    dao = MontadoraDAO()
    lst = dao.selecionar_tudo()
    if not lst:
        msg = 'Não há montadoras na base de dados.'
    else:
        msg = f'Listadas {len(lst)} montadoras da base de dados.'

    return render_template('/mt/compra.html', msg=msg, lst=lst)


@bp_mt.route('/delete/<int:idt>')
def delete(idt):
    dao = MontadoraDAO()
    if dao.deletar(idt):
        msg = "Montadora Excluída!"
    else:
        msg = "Erro ao tentar excluir montadora, provavelmente tem modelos associados!"

    # Carregar a nova lista sem o objeto excluído
    lst = dao.selecionar_tudo()
    if not lst:
        msg += ' | Não há montadoras na base de dados.'
    else:
        msg += f' | Listadas {len(lst)} montadoras da base de dados.'

    return render_template('/mt/compra.html', msg=msg, lst=lst)




@bp_mt.route('/form_update/<int:idt>')
def form_update(idt):
   # Buscar os dados da montadora escolhida para edição
   dao = MontadoraDAO()
   montadora = dao.selecionar_por_idt(idt)


   return render_template('/mt/form_update.html', montadora=montadora, msg='', display="none")


@bp_mt.route('/save_update', methods=['POST'])
def save_update():
   # Preencher com dados de montadora vindos do formulário de edição
   m = Montadora()
   m.idt_montadora = request.form['idt_montadora'] # Necessário porque é uma montadora existente e não uma nova montadora
   m.sgl_montadora = request.form['sgl_montadora']
   m.nme_montadora = request.form['nme_montadora']


   # Salvando a nova montadora
   dao = MontadoraDAO()
   dao.atualizar(m)
   msg = f'Montadora número {m.idt_montadora} alterada com sucesso.'


   return render_template('/mt/form_update.html', montadora=m, msg=msg, display="block")
